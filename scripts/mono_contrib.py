"""Recolours the generated contribution graphics to match the black / silver theme.

github-profile-3d-contrib takes language colours straight from GitHub
(Python blue, JavaScript yellow, ...) and has no setting for them, so this
runs after it in the workflow and maps every coloured value to a grey ramp,
in order of first appearance. Greys are left alone.

    python scripts/mono_contrib.py profile-3d-contrib/profile-mono.svg ...
"""
import re
import sys

RAMP = ["#f2f2f2", "#b8b8b8", "#8c8c8c", "#666666", "#4d4d4d", "#3a3a3a", "#2e2e2e"]
OTHER = {"#444444": "#262626"}  # the action's fixed colour for "other" languages
HEX = re.compile(r"#([0-9a-fA-F]{6})\b")


def coloured(h):
    r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return max(r, g, b) - min(r, g, b) > 12


def recolour(svg):
    mapping = dict(OTHER)
    for m in HEX.finditer(svg):
        h = "#" + m.group(1).lower()
        if h not in mapping and coloured(m.group(1)):
            mapping[h] = RAMP[min(len([k for k in mapping if k not in OTHER]), len(RAMP) - 1)]
    return HEX.sub(lambda m: mapping.get("#" + m.group(1).lower(), m.group(0)), svg)


if __name__ == "__main__":
    for path in sys.argv[1:]:
        with open(path, encoding="utf-8") as fh:
            svg = fh.read()
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(recolour(svg))
        print("recoloured", path)
