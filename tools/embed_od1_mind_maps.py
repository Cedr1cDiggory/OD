"""Embed approved OD1 mind-map WebP assets in the Mind Map Workshop section."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

MIND_MAPS = {
    11: (
        "The Farmer and the Hat story mind map showing the characters and story events in sequence.",
        "Follow the branches and story order to retell The Farmer and the Hat.",
    ),
    13: (
        "Where's Your Home mind map comparing homes in towns, cities, and the country.",
        "Use the complete map to compare places to live and explain an address.",
    ),
    14: (
        "City Mouse and Country Mouse story mind map showing the visits and story events in sequence.",
        "Follow the numbered arrows to retell the two mice visiting each other's homes.",
    ),
    15: (
        "Percussion Instruments mind map showing instrument types, actions, and important details.",
        "Use the branches to explain how different percussion instruments make sounds.",
    ),
    16: (
        "Let's Make Music mind map showing the class problem, idea, concert, and solution.",
        "Follow the story from the class problem to the concert solution.",
    ),
    17: (
        "Living and Nonliving Things mind map comparing their needs, actions, growth, and changes.",
        "Compare the branches to explain how living and nonliving things are different.",
    ),
    18: (
        "The Gingerbread Man story mind map showing the characters, chase, river problem, and ending.",
        "Follow the numbered sequence to retell The Gingerbread Man.",
    ),
}


def main() -> None:
    for unit, (alt, caption) in MIND_MAPS.items():
        page = ROOT / "public" / "units" / "od1" / f"unit-{unit:02d}" / "index.html"
        source = page.read_text(encoding="utf-8")
        section_start = source.index('<section class="section" id="mind-map">')
        section_end = source.index("</section>", section_start)
        section = source[section_start:section_end]
        if 'src="assets/images/mind-map.webp"' in section:
            print(f"Unit {unit:02d}: already embedded")
            continue

        purpose_end = source.index('</div>', source.index('<div class="purpose">', section_start)) + len('</div>')
        figure = (
            '<figure class="image-card">'
            f'<img src="assets/images/mind-map.webp" alt="{alt}">'
            f'<figcaption class="caption">{caption}</figcaption>'
            '</figure>'
        )
        updated = source[:purpose_end] + figure + source[purpose_end:]
        page.write_text(updated, encoding="utf-8")
        print(f"Unit {unit:02d}: embedded")


if __name__ == "__main__":
    main()
