"""Convert public runtime PNG assets to verified WebP siblings."""

import argparse
import re
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
TEXT_SUFFIXES = {".html", ".css", ".js", ".json", ".xml", ".md"}
PNG_REFERENCE = re.compile(r"[A-Za-z0-9_./@+-]+\.png")


def has_alpha(image: Image.Image) -> bool:
    return image.mode in {"RGBA", "LA"} or (
        image.mode == "P" and "transparency" in image.info
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--finalize",
        action="store_true",
        help="Update local references to WebP and delete replaced public PNG files.",
    )
    return parser.parse_args()


def update_references() -> int:
    changed = 0
    for path in PUBLIC.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        source = path.read_text(encoding="utf-8")

        def replace(match):
            raw = match.group(0)
            if raw.startswith("/"):
                candidate = PUBLIC / raw.lstrip("/")
            else:
                candidate = path.parent / raw
            candidate = candidate.resolve()
            if (
                candidate.is_file()
                and candidate.suffix.lower() == ".png"
                and candidate.with_suffix(".webp").is_file()
            ):
                return raw[:-4] + ".webp"
            return raw

        updated = PNG_REFERENCE.sub(replace, source)
        if updated != source:
            path.write_text(updated, encoding="utf-8")
            changed += 1
    return changed


def main() -> None:
    args = parse_args()
    png_files = sorted(PUBLIC.rglob("*.png"))
    converted = 0
    reused = 0
    before = sum(path.stat().st_size for path in png_files)

    for source in png_files:
        target = source.with_suffix(".webp")
        with Image.open(source) as image:
            expected_size = image.size
            alpha = has_alpha(image)
            if not target.exists():
                output = image.convert("RGBA" if alpha else "RGB")
                save_args = {"format": "WEBP", "method": 6}
                if alpha:
                    save_args.update(lossless=True, exact=True)
                else:
                    save_args.update(quality=88)
                icc_profile = image.info.get("icc_profile")
                if icc_profile:
                    save_args["icc_profile"] = icc_profile
                output.save(target, **save_args)
                converted += 1
            else:
                reused += 1

        with Image.open(target) as check:
            check.verify()
        with Image.open(target) as check:
            if check.size != expected_size:
                raise RuntimeError(
                    f"Dimension mismatch: {source.relative_to(ROOT)} -> "
                    f"{target.relative_to(ROOT)}"
                )

        print(
            f"{source.relative_to(ROOT)} -> {target.relative_to(ROOT)} "
            f"({source.stat().st_size} -> {target.stat().st_size} bytes)"
        )

    after = sum(path.with_suffix(".webp").stat().st_size for path in png_files)
    print(f"PNG files: {len(png_files)}")
    print(f"Converted: {converted}; reused existing WebP: {reused}")
    print(f"Total bytes: {before} -> {after}")

    if args.finalize:
        changed = update_references()
        residual = []
        for path in PUBLIC.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                text = path.read_text(encoding="utf-8")
                if ".png" in text:
                    residual.append(path)
        if residual:
            names = ", ".join(str(path.relative_to(ROOT)) for path in residual)
            raise RuntimeError(f"PNG references remain in: {names}")

        for source in png_files:
            source.unlink()
        print(f"Updated reference files: {changed}")
        print(f"Deleted replaced PNG files: {len(png_files)}")


if __name__ == "__main__":
    main()
