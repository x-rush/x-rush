"""Generate the in-body pixel art used by the X-RUSH profile README.

Two families are produced:
  * assets/sprites/*.svg   15x15 pixel class sprites (one per party member)
  * assets/divider.svg     a pixel rule that replaces the generic Markdown hr

Every shape is drawn on an integer grid and merged into horizontal runs so the
output stays small and every edge lands on a whole pixel.
"""

from pathlib import Path
import math

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
GRID = 15
SCALE = 2
PAD = 5
CANVAS = 40

INK = {
    "main": "#5DEFFF",
    "accent": "#9D7CFF",
    "signal": "#B8F35A",
    "hi": "#D7E1EA",
    "line": "#31445A",
}


def runs(pixels):
    """Merge a set of (x, y) pixels into horizontal runs per row."""
    rows = {}
    for x, y in pixels:
        rows.setdefault(y, []).append(x)
    for y in sorted(rows):
        xs = sorted(rows[y])
        start = xs[0]
        previous = xs[0]
        for x in xs[1:]:
            if x == previous + 1:
                previous = x
                continue
            yield start, y, previous - start + 1
            start = previous = x
        yield start, y, previous - start + 1


def render(groups):
    """Render colour groups of 15x15 pixels into the 40x40 icon canvas."""
    body = [
        f'  <path d="M4 1H36L39 4V36L36 39H4L1 36V4Z" fill="#0D1321" stroke="#294154"/>',
        '  <g shape-rendering="crispEdges">',
    ]
    for key, pixels in groups:
        for x, y, width in runs(pixels):
            body.append(
                f'    <rect x="{PAD + x * SCALE}" y="{PAD + y * SCALE}" '
                f'width="{width * SCALE}" height="{SCALE}" fill="{INK[key]}"/>'
            )
    body.append("  </g>")
    return body


def engineer():
    """A gear: solid disc, eight square teeth, punched-out hub."""
    disc, teeth, hub = set(), set(), set()
    for y in range(GRID):
        for x in range(GRID):
            dx, dy = x - 7, y - 7
            radius = math.hypot(dx, dy)
            if radius <= 4.3:
                disc.add((x, y))
            if radius <= 1.7:
                hub.add((x, y))
    for y in range(GRID):
        for x in range(GRID):
            dx, dy = x - 7, y - 7
            radius = math.hypot(dx, dy)
            angle = math.degrees(math.atan2(dy, dx)) % 45
            if 4.4 <= radius <= 6.2 and min(angle, 45 - angle) <= 10:
                teeth.add((x, y))
    inner = {(x, y) for y in range(GRID) for x in range(GRID) if math.hypot(x - 7, y - 7) <= 2.9}
    return [
        ("signal", teeth),
        ("main", disc - hub),
        ("line", inner - hub),
        ("hi", {(7, 7)}),
    ]


def architect():
    """A blueprint sheet: frame, continuous guide grid, marked corner."""
    frame, grid, hi = set(), set(), set()
    for y in range(GRID):
        for x in range(GRID):
            if (x in (1, 13) and 1 <= y <= 13) or (y in (1, 13) and 1 <= x <= 13):
                frame.add((x, y))
            elif x in (5, 9) and 2 <= y <= 12:
                grid.add((x, y))
            elif y in (5, 9) and 2 <= x <= 12:
                grid.add((x, y))
    hi.update({(2, 2), (3, 2), (2, 3), (3, 3)})
    return [("accent", frame), ("main", grid), ("hi", hi)]


def builder():
    """A staggered brick wall: three courses of 3x3 bricks."""
    bricks = set()
    courses = (((2, 4), (2, 6), (8, 12)), ((6, 8), (2, 4), (6, 10)), ((10, 12), (2, 6), (8, 12)))
    for (top, bottom), *spans in courses:
        for left, right in spans:
            for y in range(top, bottom + 1):
                for x in range(left, right + 1):
                    bricks.add((x, y))
    return [("signal", bricks)]


def scout():
    """A magnifier: ring, diagonal handle, and a bright focus point."""
    ring, handle, focus = set(), set(), set()
    for y in range(GRID):
        for x in range(GRID):
            radius = math.hypot(x - 6, y - 6)
            if 3.4 <= radius <= 5.2:
                ring.add((x, y))
    for step in range(4):
        handle.add((10 + step, 10 + step))
        handle.add((11 + step, 10 + step))
    focus.update({(5, 5), (7, 5), (5, 7), (7, 7)})
    return [("main", ring), ("accent", handle), ("signal", focus)]


SPRITES = {
    "engineer": (engineer, "Engineer pixel sprite — a cyan gear"),
    "architect": (architect, "Architect pixel sprite — a violet blueprint sheet"),
    "builder": (builder, "Builder pixel sprite — a green brick stack"),
    "scout": (scout, "Scout pixel sprite — a cyan radar sweep"),
}


def write_sprite(name):
    builder_fn, label = SPRITES[name]
    groups = builder_fn()
    lines = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40" viewBox="0 0 40 40" '
        f'role="img" aria-label="{label}">',
        f"  <title>{label}</title>",
        *render(groups),
        "</svg>",
        "",
    ]
    path = ASSETS / "sprites" / f"{name}.svg"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


def divider():
    """880x20 pixel rule: stair brackets, dashed rail, cyan core."""
    width, height = 880, 20
    rail, core, bracket = set(), set(), set()
    for x in range(0, width, 24):
        for dx in range(14):
            rail.add((x + dx, 9))
            rail.add((x + dx, 10))
    for x in range(width // 2 - 36, width // 2 + 36):
        rail.discard((x, 9))
        rail.discard((x, 10))
    for x in range(width // 2 - 36, width // 2 + 36, 6):
        for dx in (0, 1, 2, 3):
            core.add((x + dx, 9))
            core.add((x + dx, 10))
    stairs = ((0, 8), (2, 8), (4, 8), (0, 6), (2, 6), (4, 6), (6, 6), (2, 4), (4, 4), (6, 4), (8, 4), (4, 2), (6, 2), (8, 2), (10, 2))
    for x, y in stairs:
        bracket.add((x, y))
        bracket.add((width - 1 - x, y))
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" role="img" '
        'aria-label="X-RUSH pixel divider">',
        "  <title>X-RUSH pixel divider</title>",
        '  <g shape-rendering="crispEdges">',
    ]
    layers = ((rail, INK["line"], "0.45"), (core, INK["main"], None), (bracket, INK["main"], "0.6"))
    for pixels, ink, opacity in layers:
        alpha = f' opacity="{opacity}"' if opacity else ""
        for x, y, run in runs(pixels):
            lines.append(
                f'    <rect x="{x}" y="{y}" width="{run}" height="2" '
                f'fill="{ink}"{alpha}/>'
            )
    lines += ["  </g>", "</svg>", ""]
    path = ASSETS / "divider.svg"
    path.write_text("\n".join(lines), encoding="utf-8")
    return path


if __name__ == "__main__":
    for name in SPRITES:
        print(write_sprite(name))
    print(divider())
