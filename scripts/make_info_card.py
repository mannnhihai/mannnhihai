from pathlib import Path

OUTPUT = Path("info-card.svg")

WIDTH = 520
HEIGHT = 430

BACKGROUND = "#0d1117"
BORDER = "#30363d"
TEXT = "#c9d1d9"
MUTED = "#8b949e"
GREEN = "#39d353"
BLUE = "#58a6ff"
PURPLE = "#bc8cff"
YELLOW = "#f2cc60"


def main():

    svg = []

    svg.append('<?xml version="1.0" encoding="UTF-8"?>')

    svg.append(f'''
<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{WIDTH}"
    height="{HEIGHT}"
    viewBox="0 0 {WIDTH} {HEIGHT}"
>
''')

    # Background
    svg.append(f'''
<rect
    x="1"
    y="1"
    width="{WIDTH - 2}"
    height="{HEIGHT - 2}"
    rx="12"
    fill="{BACKGROUND}"
    stroke="{BORDER}"
    stroke-width="2"
/>
''')

    # Terminal buttons
    svg.append('''
<circle cx="25" cy="25" r="6" fill="#ff5f56"/>
<circle cx="45" cy="25" r="6" fill="#ffbd2e"/>
<circle cx="65" cy="25" r="6" fill="#27c93f"/>
''')

    # Terminal title
    svg.append('''
<text
    x="90"
    y="30"
    font-family="monospace"
    font-size="13"
    fill="#8b949e"
>
madhusudan@github: ~
</text>
''')

    # Separator
    svg.append(f'''
<line
    x1="20"
    y1="50"
    x2="{WIDTH - 20}"
    y2="50"
    stroke="{BORDER}"
/>
''')

    # Name
    svg.append('''
<text
    x="25"
    y="82"
    font-family="monospace"
    font-size="22"
    font-weight="bold"
    fill="#ffffff"
>
Madhusudan Thakur
</text>
''')

    # Profile
    svg.append('''
<text
    x="25"
    y="106"
    font-family="monospace"
    font-size="12"
    fill="#8b949e"
>
B.Tech CSE • Amity University
</text>
''')

    rows = [
        ("ROLE", "DevOps / Cloud Enthusiast", GREEN),
        ("EDU", "B.Tech CSE • 2023–2027", BLUE),
        ("EXP", "DevOps Intern @ NIC", PURPLE),
        ("CLOUD", "AWS EC2 • NetBox • Linux", YELLOW),
        ("CODE", "C • C++ • Java • Python • SQL", GREEN),
        ("WEB", "HTML • CSS • JS • React • Node", BLUE),
        ("CORE", "DSA • OOP • DBMS • OS", PURPLE),
    ]

    start_y = 145

    for i, (key, value, color) in enumerate(rows):

        y = start_y + i * 34
        delay = 0.35 + i * 0.18

        svg.append(f'''
<g opacity="0">

<animate
    attributeName="opacity"
    from="0"
    to="1"
    dur="0.45s"
    begin="{delay}s"
    fill="freeze"
/>

<text
    x="25"
    y="{y}"
    font-family="monospace"
    font-size="11"
    font-weight="bold"
    fill="{color}"
>
{key}
</text>

<text
    x="100"
    y="{y}"
    font-family="monospace"
    font-size="11"
    fill="{TEXT}"
>
{value}
</text>

</g>
''')

    # NIC section
    svg.append('''
<g opacity="0">

<animate
    attributeName="opacity"
    from="0"
    to="1"
    dur="0.5s"
    begin="1.8s"
    fill="freeze"
/>

<text
    x="25"
    y="390"
    font-family="monospace"
    font-size="11"
    fill="#39d353"
>
$ cat experience.txt
</text>

<text
    x="25"
    y="410"
    font-family="monospace"
    font-size="11"
    fill="#8b949e"
>
NIC • NetBox IPAM • AWS EC2
</text>

</g>
''')

    svg.append("</svg>")

    OUTPUT.write_text(
        "\n".join(svg),
        encoding="utf-8"
    )

    print("SUCCESS!")
    print(f"Created: {OUTPUT}")


if __name__ == "__main__":
    main()
