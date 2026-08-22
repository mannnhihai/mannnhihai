from pathlib import Path
import html

import numpy as np
from PIL import Image


INPUT = Path("source-prepped.png")
OUTPUT = Path("madhusudan-ascii.svg")

# Bright -> dark
RAMP = " .`:-=+*cs#%@"

# Number of ASCII characters across
WIDTH = 100

# Terminal characters are taller than they are wide
CHAR_ASPECT = 0.48

# SVG appearance
FONT_SIZE = 8
LINE_HEIGHT = 10
TEXT_COLOR = "#b7bcc5"
BACKGROUND = "#0d1117"

MARGIN_X = 12
MARGIN_Y = 12


def brightness_to_char(brightness):
    """
    Convert pixel brightness to an ASCII character.

    White -> space
    Black -> dense character
    """

    index = int(
        (255 - brightness) / 256 * len(RAMP)
    )

    index = min(
        len(RAMP) - 1,
        index
    )

    return RAMP[index]


def main():

    if not INPUT.exists():
        raise FileNotFoundError(
            "source-prepped.png was not found."
        )

    print("Loading prepared image...")

    image = Image.open(INPUT).convert("L")

    original_width, original_height = image.size

    # Calculate proportional ASCII height
    new_height = max(
        1,
        int(
            original_height
            / original_width
            * WIDTH
            * CHAR_ASPECT
        )
    )

    print(
        f"Original image: "
        f"{original_width} x {original_height}"
    )

    print(
        f"ASCII grid: "
        f"{WIDTH} x {new_height}"
    )

    # Resize image to ASCII grid
    image = image.resize(
        (WIDTH, new_height),
        Image.Resampling.LANCZOS
    )

    pixels = np.array(image)

    lines = []

    for row in pixels:

        line = ""

        for brightness in row:

            char = brightness_to_char(
                int(brightness)
            )

            line += char

        lines.append(line)

    # SVG dimensions
    svg_width = (
        MARGIN_X * 2
        + WIDTH * 5
    )

    svg_height = (
        MARGIN_Y * 2
        + new_height * LINE_HEIGHT
    )

    print("Generating SVG...")

    svg = []

    svg.append(
        '<?xml version="1.0" encoding="UTF-8"?>'
    )

    svg.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {svg_width} {svg_height}" '
        f'width="{svg_width}" '
        f'height="{svg_height}" '
        f'xml:space="preserve">'
    )

    # Background
    svg.append(
        f'<rect width="100%" height="100%" '
        f'fill="{BACKGROUND}"/>'
    )

    svg.append("""
<style>
    text {
        font-family:
            "SFMono-Regular",
            Menlo,
            Monaco,
            Consolas,
            "Liberation Mono",
            monospace;
        font-weight: 500;
    }
</style>
""")

    # Generate each row
    for row_index, line in enumerate(lines):

        y = (
            MARGIN_Y
            + (row_index + 1) * LINE_HEIGHT
        )

        # Each row starts slightly later
        begin = row_index * 0.045

        # Escape XML special characters
        safe_line = html.escape(line)

        # Unique clip path
        clip_id = f"rowClip{row_index}"

        svg.append(
            f'<clipPath id="{clip_id}">'
        )

        svg.append(
            f'<rect x="{MARGIN_X}" '
            f'y="{y - LINE_HEIGHT + 1}" '
            f'width="0" '
            f'height="{LINE_HEIGHT + 3}">'
        )

        # Animate clip from left to right
        svg.append(
            f'<animate '
            f'attributeName="width" '
            f'from="0" '
            f'to="{WIDTH * 5}" '
            f'dur="0.65s" '
            f'begin="{begin:.3f}s" '
            f'fill="freeze"/>'
        )

        svg.append(
            '</rect>'
        )

        svg.append(
            '</clipPath>'
        )

        # Text row
        svg.append(
            f'<text '
            f'x="{MARGIN_X}" '
            f'y="{y}" '
            f'font-size="{FONT_SIZE}px" '
            f'fill="{TEXT_COLOR}" '
            f'clip-path="url(#{clip_id})" '
            f'xml:space="preserve">'
            f'{safe_line}'
            f'</text>'
        )

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print()
    print("SUCCESS!")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()

