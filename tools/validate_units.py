"""Validate canonical OD Unit structure and local runtime references."""

import re
import sys
from pathlib import Path
from urllib.parse import unquote


ROOT = Path(__file__).resolve().parents[1]
UNITS_ROOT = ROOT / "public" / "units"
EXPECTED_HEADINGS = [
    "1 Key Vocabulary",
    "2 Knowledge List Guide",
    "3 Mind Map Workshop",
    "4 Grammar and Expression",
    "5 Challenge Practice",
    "6 Writing Task",
    "7 Wrap-Up",
]
CANONICAL_PAGE = re.compile(
    r"public/units/od[1-4]/unit-\d{2}/index\.html$"
)
CANONICAL_UNIT_FILE = re.compile(
    r"public/units/od[1-4]/unit-\d{2}/"
)
SOURCE_ARTIFACT = re.compile(
    r"(\.docx?$|\.pdf$|_extracted|source-pages|/source/)", re.IGNORECASE
)
REFERENCE = re.compile(
    r"""(?:src|href)=["']([^"'#]+)|url\(["']?([^"')]+)["']?\)""",
    re.IGNORECASE,
)
EXTERNAL_REFERENCE = re.compile(
    r"^(?:https?:|data:|mailto:|tel:|javascript:)", re.IGNORECASE
)


def relative(path):
    return path.relative_to(ROOT).as_posix()


def local_target(page, reference):
    clean = reference.split("?", 1)[0].split("#", 1)[0]
    if not clean:
        return None
    decoded = unquote(clean)
    if decoded.startswith("/"):
        return ROOT / "public" / decoded.lstrip("/")
    return (page.parent / decoded).resolve()


def main():
    errors = []
    all_files = [path for path in UNITS_ROOT.rglob("*") if path.is_file()]
    canonical_pages = [
        path for path in all_files if CANONICAL_PAGE.search(relative(path))
    ]

    for file_path in all_files:
        file_name = relative(file_path)
        if (
            CANONICAL_UNIT_FILE.search(file_name)
            and SOURCE_ARTIFACT.search(file_name)
        ):
            errors.append(
                f"{file_name}: source artifact must live under content/"
            )

    for page in canonical_pages:
        page_name = relative(page)
        source = page.read_text(encoding="utf-8")

        if "viewport-fit=cover" not in source:
            errors.append(f"{page_name}: missing viewport-fit=cover")
        if re.search(r"<(?:canvas|textarea)\b", source, re.IGNORECASE):
            errors.append(
                f"{page_name}: web handwriting controls are not allowed"
            )

        headings = [
            re.sub(r"<[^>]+>", "", match).strip()
            for match in re.findall(
                r"<h2[^>]*>([\s\S]*?)</h2>", source, re.IGNORECASE
            )
        ]
        if headings != EXPECTED_HEADINGS:
            errors.append(
                f"{page_name}: expected the standard seven section headings "
                "in order"
            )

        references = {
            first or second
            for first, second in REFERENCE.findall(source)
            if not EXTERNAL_REFERENCE.match(first or second)
        }
        for reference in references:
            try:
                target = local_target(page, reference)
            except (ValueError, UnicodeError):
                errors.append(
                    f"{page_name}: malformed local reference {reference}"
                )
                continue
            if target is not None and not target.exists():
                errors.append(
                    f"{page_name}: missing local reference {reference}"
                )

    if not canonical_pages:
        errors.append("No canonical Unit pages found.")

    if errors:
        print(f"Unit validation failed ({len(errors)}):", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        raise SystemExit(1)

    print(
        f"Validated {len(canonical_pages)} canonical Unit pages "
        "with no errors."
    )


if __name__ == "__main__":
    main()

