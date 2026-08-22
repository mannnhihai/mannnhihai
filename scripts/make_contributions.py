from pathlib import Path
import random

OUTPUT = Path("contributions.svg")

COLS = 53
ROWS = 7
CELL = 11
GAP = 3

WIDTH = COLS * (CELL + GAP) + 20
HEIGHT = ROWS * (CELL + GAP) + 20

BG = "#0d1117"
EMPTY = "#161b22"
LEVELS = [
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


def main():
    random.seed(42)

    svg = []

    svg.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
        width="{WIDTH}"
        height="{HEIGHT}"
        viewBox="0 0 {WIDTH} {HEIGHT}">
        <rect width="100%" height="100%" rx="8" fill="{BG}"/>'''
    )

    index = 0

    for col in range(COLS):
        for row in range(ROWS):

            # Create a natural-looking contribution pattern
            value = random.choices(
                [0, 1, 2, 3, 4],
                weights=[55, 20, 12, 8, 5]
            )[0]

            if value == 0:
                fill = EMPTY
            else:
                fill = LEVELS[value - 1]

            x = 10 + col * (CELL + GAP)
            y = 10 + row * (CELL + GAP)

            delay = index * 0.008

            svg.append(
                f'''
<rect
    x="{x}"
    y="{y}"
    width="{CELL}"
    height="{CELL}"
    rx="2"
    fill="{fill}"
    opacity="0"
>
    <animate
        attributeName="opacity"
        from="0"
        to="1"
        dur="0.25s"
        begin="{delay:.3f}s"
        fill="freeze"
    />
</rect>'''
            )

            index += 1

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print("SUCCESS!")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
