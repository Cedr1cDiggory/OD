#!/usr/bin/env python3
"""Extract DOCX text as Markdown and save embedded images.

By default, all DOCX files below ``public/units/3`` are extracted. Each
document is written to a sibling directory named ``<document>_extracted``.
"""

from __future__ import annotations

import argparse
import posixpath
import shutil
import sys
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET
from zipfile import BadZipFile, ZipFile


NS = {
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
}
W = f"{{{NS['w']}}}"
R_EMBED = f"{{{NS['r']}}}embed"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
IMAGE_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/image"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract DOCX text to Markdown and save embedded images."
    )
    parser.add_argument(
        "source",
        nargs="?",
        type=Path,
        default=Path("public/units/3"),
        help="A DOCX file or a directory containing DOCX files (default: public/units/3)",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        type=Path,
        help="Output root. Without this option, output is placed beside each DOCX.",
    )
    parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Do not search subdirectories when source is a directory.",
    )
    return parser.parse_args()


def find_docx_files(source: Path, recursive: bool) -> list[Path]:
    if source.is_file():
        if source.suffix.lower() != ".docx":
            raise ValueError(f"Not a DOCX file: {source}")
        return [source]
    if not source.is_dir():
        raise FileNotFoundError(f"Source does not exist: {source}")
    pattern = "**/*.docx" if recursive else "*.docx"
    return sorted(path for path in source.glob(pattern) if not path.name.startswith("~$"))


def output_path(docx: Path, source: Path, output_root: Path | None) -> Path:
    dirname = f"{docx.stem}_extracted"
    if output_root is None:
        return docx.parent / dirname
    if source.is_dir():
        return output_root / docx.relative_to(source).parent / dirname
    return output_root / dirname


def read_relationships(archive: ZipFile) -> dict[str, str]:
    rels_path = "word/_rels/document.xml.rels"
    if rels_path not in archive.namelist():
        return {}
    root = ET.fromstring(archive.read(rels_path))
    relationships: dict[str, str] = {}
    for rel in root.findall(f"{{{REL_NS}}}Relationship"):
        if rel.get("Type") != IMAGE_REL or rel.get("TargetMode") == "External":
            continue
        rel_id = rel.get("Id")
        target = rel.get("Target")
        if rel_id and target:
            relationships[rel_id] = posixpath.normpath(posixpath.join("word", target))
    return relationships


class MarkdownExtractor:
    def __init__(self, archive: ZipFile, output_dir: Path) -> None:
        self.archive = archive
        self.output_dir = output_dir
        self.image_dir = output_dir / "images"
        self.relationships = read_relationships(archive)
        self.image_names: dict[str, str] = {}
        self.used_names: set[str] = set()

    def save_image(self, rel_id: str) -> str | None:
        target = self.relationships.get(rel_id)
        if not target or target not in self.archive.namelist():
            return None
        if rel_id in self.image_names:
            return self.image_names[rel_id]

        source_name = PurePosixPath(target).name or f"image-{len(self.image_names) + 1}"
        candidate = source_name
        counter = 2
        while candidate.casefold() in self.used_names:
            stem, suffix = Path(source_name).stem, Path(source_name).suffix
            candidate = f"{stem}-{counter}{suffix}"
            counter += 1
        self.used_names.add(candidate.casefold())
        self.image_names[rel_id] = candidate
        self.image_dir.mkdir(parents=True, exist_ok=True)
        (self.image_dir / candidate).write_bytes(self.archive.read(target))
        return candidate

    def inline_content(self, element: ET.Element) -> str:
        parts: list[str] = []
        for node in element.iter():
            if node.tag == f"{W}t":
                parts.append(node.text or "")
            elif node.tag == f"{W}tab":
                parts.append("\t")
            elif node.tag in {f"{W}br", f"{W}cr"}:
                parts.append("<br>")
            elif node.tag == f"{{{NS['a']}}}blip":
                rel_id = node.get(R_EMBED)
                image_name = self.save_image(rel_id) if rel_id else None
                if image_name:
                    parts.append(f"![{Path(image_name).stem}](images/{image_name})")
        return "".join(parts).strip()

    @staticmethod
    def paragraph_style(paragraph: ET.Element) -> str:
        style = paragraph.find(f"{W}pPr/{W}pStyle")
        return style.get(f"{W}val", "") if style is not None else ""

    def paragraph(self, element: ET.Element, first_content: bool = False) -> str:
        content = self.inline_content(element)
        if not content:
            return ""
        style = self.paragraph_style(element).lower().replace(" ", "")
        if style in {"title", "标题"} or first_content:
            return f"# {content}"
        heading_levels = {
            "heading1": 2,
            "heading2": 3,
            "heading3": 4,
            "标题1": 2,
            "标题2": 3,
            "标题3": 4,
        }
        if style in heading_levels:
            return f"{'#' * heading_levels[style]} {content}"
        if element.find(f"{W}pPr/{W}numPr") is not None:
            return f"- {content}"
        return content

    def cell(self, cell: ET.Element) -> str:
        blocks: list[str] = []
        for child in cell:
            if child.tag == f"{W}p":
                content = self.paragraph(child)
                if content:
                    blocks.append(content)
            elif child.tag == f"{W}tbl":
                # Markdown cannot represent a table inside another table cell.
                # Flatten nested cells while preserving their document order.
                nested = [
                    self.cell(nested_cell)
                    for row in child.findall(f"{W}tr")
                    for nested_cell in row.findall(f"{W}tc")
                ]
                blocks.extend(content for content in nested if content)
        value = "<br>".join(blocks)
        return value.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")

    def table(self, table: ET.Element) -> str:
        rows = [
            [self.cell(cell) for cell in row.findall(f"{W}tc")]
            for row in table.findall(f"{W}tr")
        ]
        if not rows:
            return ""
        width = max(len(row) for row in rows)
        rows = [row + [""] * (width - len(row)) for row in rows]
        lines = [
            "| " + " | ".join(rows[0]) + " |",
            "| " + " | ".join(["---"] * width) + " |",
        ]
        lines.extend("| " + " | ".join(row) + " |" for row in rows[1:])
        return "\n".join(lines)

    def extract(self) -> str:
        document = ET.fromstring(self.archive.read("word/document.xml"))
        body = document.find(f"{W}body")
        if body is None:
            return ""
        blocks: list[str] = []
        has_content = False
        for child in body:
            block = ""
            if child.tag == f"{W}p":
                block = self.paragraph(child, first_content=not has_content)
            elif child.tag == f"{W}tbl":
                block = self.table(child)
            if block:
                blocks.append(block)
                has_content = True
        return "\n\n".join(blocks).rstrip() + "\n"


def extract_docx(docx: Path, destination: Path) -> tuple[Path, int]:
    destination.mkdir(parents=True, exist_ok=True)
    image_dir = destination / "images"
    if image_dir.exists():
        shutil.rmtree(image_dir)
    with ZipFile(docx) as archive:
        if "word/document.xml" not in archive.namelist():
            raise ValueError("DOCX has no word/document.xml")
        extractor = MarkdownExtractor(archive, destination)
        markdown = extractor.extract()
    markdown_path = destination / "content.md"
    markdown_path.write_text(markdown, encoding="utf-8")
    return markdown_path, len(extractor.image_names)


def main() -> int:
    args = parse_args()
    source = args.source.expanduser().resolve()
    output_root = args.output_dir.expanduser().resolve() if args.output_dir else None
    try:
        files = find_docx_files(source, recursive=not args.no_recursive)
        if not files:
            print(f"No DOCX files found in: {source}", file=sys.stderr)
            return 1
        for docx in files:
            destination = output_path(docx, source, output_root)
            markdown_path, image_count = extract_docx(docx, destination)
            print(f"Extracted: {docx}")
            print(f"  Markdown: {markdown_path}")
            print(f"  Images: {image_count} -> {destination / 'images'}")
    except (BadZipFile, ET.ParseError, OSError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
