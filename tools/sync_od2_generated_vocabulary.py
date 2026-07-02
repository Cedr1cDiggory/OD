"""Build OD2 Unit 1-18 runtime vocabulary WebPs from generated source PNGs."""

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
ASSETS = {
    "content/od2/unit-01/animal-groups-vocabulary-generated.png":
        "public/units/od2/unit-01/assets/images/animal-groups-vocabulary.webp",
    "content/od2/unit-01/animal-body-parts-vocabulary-generated.png":
        "public/units/od2/unit-01/assets/images/animal-body-parts-vocabulary.webp",
    "content/od2/unit-02/vocabulary-generated.png":
        "public/units/od2/unit-02/assets/images/vocabulary.webp",
    "content/od2/unit-03/vocabulary-generated.png":
        "public/units/od2/unit-03/assets/images/vocabulary.webp",
    "content/od2/unit-04/vocabulary-generated.png":
        "public/units/od2/unit-04/assets/images/vocabulary.webp",
    "content/od2/unit-05/vocabulary-generated.png":
        "public/units/od2/unit-05/assets/images/vocabulary.webp",
    "content/od2/unit-06/vocabulary-generated.png":
        "public/units/od2/unit-06/assets/images/vocabulary.webp",
    "content/od2/unit-07/vocabulary-generated.png":
        "public/units/od2/unit-07/assets/images/vocabulary.webp",
    "content/od2/unit-08/vocabulary-generated.png":
        "public/units/od2/unit-08/assets/images/vocabulary.webp",
    "content/od2/unit-09/vocabulary-generated.png":
        "public/units/od2/unit-09/assets/images/vocabulary.webp",
    "content/od2/unit-10/vocabulary-generated.png":
        "public/units/od2/unit-10/assets/images/vocabulary.webp",
    "content/od2/unit-11/vocabulary-generated.png":
        "public/units/od2/unit-11/assets/images/vocabulary.webp",
    "content/od2/unit-12/vocabulary-generated.png":
        "public/units/od2/unit-12/assets/images/vocabulary.webp",
    "content/od2/unit-13/vocabulary-generated.png":
        "public/units/od2/unit-13/assets/images/vocabulary.webp",
    "content/od2/unit-14/vocabulary-generated.png":
        "public/units/od2/unit-14/assets/images/vocabulary.webp",
    "content/od2/unit-15/vocabulary-generated.png":
        "public/units/od2/unit-15/assets/images/vocabulary.webp",
    "content/od2/unit-16/vocabulary-generated.png":
        "public/units/od2/unit-16/assets/images/vocabulary.webp",
    "content/od2/unit-17/vocabulary-generated.png":
        "public/units/od2/unit-17/assets/images/vocabulary.webp",
    "content/od2/unit-18/vocabulary-generated.png":
        "public/units/od2/unit-18/assets/images/vocabulary.webp",
}


def main() -> None:
    for source_name, destination_name in ASSETS.items():
        source = ROOT / source_name
        destination = ROOT / destination_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(source) as image:
            size = image.size
            image.convert("RGB").save(destination, "WEBP", quality=90, method=6)
        with Image.open(destination) as check:
            check.verify()
        print(f"{destination.relative_to(ROOT)} ({size[0]}x{size[1]})")


if __name__ == "__main__":
    main()
