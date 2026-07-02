"""Create a canonical OD Unit page from the shared template."""

import argparse
import html
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "unit-page.html"


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create an OD1-OD4 Unit without overwriting existing work."
    )
    parser.add_argument("level", choices=("od1", "od2", "od3", "od4"))
    parser.add_argument("unit", type=int, choices=range(1, 19), metavar="{1..18}")
    parser.add_argument("title")
    return parser.parse_args()


def main():
    args = parse_args()
    unit_number = f"{args.unit:02d}"
    page_dir = ROOT / "public" / "units" / args.level / f"unit-{unit_number}"
    page_path = page_dir / "index.html"
    source_dir = ROOT / "content" / args.level / f"unit-{unit_number}"

    if page_path.exists():
        raise SystemExit(
            f"Refusing to overwrite existing page: {page_path.relative_to(ROOT)}"
        )

    (page_dir / "assets" / "images").mkdir(parents=True, exist_ok=True)
    source_dir.mkdir(parents=True, exist_ok=True)

    page = (
        TEMPLATE.read_text(encoding="utf-8")
        .replace("{{LEVEL_LABEL}}", args.level.upper())
        .replace("{{UNIT_NUMBER}}", str(args.unit))
        .replace("{{UNIT_TITLE}}", html.escape(args.title, quote=True))
    )
    page_path.write_text(page, encoding="utf-8")
    (source_dir / "README.md").write_text(
        f"# {args.level.upper()} Unit {args.unit} sources\n\n"
        "Place source documents and extraction artifacts here.\n",
        encoding="utf-8",
    )

    print(f"Created {page_path.relative_to(ROOT)}")
    print(f"Created {source_dir.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

