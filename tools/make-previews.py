#!/usr/bin/env python3
"""Generate 1200x630 Open Graph preview cards into assets/img/previews/.

One card per post in _posts/ that has `title` and `chapter` in its front matter
(chapter-NN.png), plus default.png built from the site title and tagline in
_config.yml. Re-run after adding a chapter: python tools/make-previews.py
"""
import re
from itertools import combinations
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

SITE = Path(__file__).resolve().parent.parent
OUT = SITE / "assets" / "img" / "previews"
FONTS = Path("C:/Windows/Fonts")

W, H, S = 1200, 630, 2  # final size, supersample factor
BG_TOP, BG_BOTTOM = (0x1B, 0x15, 0x10), (0x10, 0x0C, 0x08)
GOLD, MUTED, PARCHMENT = "#ffd100", "#c09a3e", "#d8c69b"
LEFT, RIGHT = 80, 1120
TITLE_MAX_W = 700  # keeps the title clear of the orbit motif
TITLE_MID, TITLE_MAX_H = 300, 290  # title block (cap top to last baseline) centred on the orbit
RULE_Y, FOOTER_BASE = 528, 578
ORBIT_C, ORBIT_K = (985, 300), 2.3  # centre and scale of the avatar.svg motif


def font(bold, size, italic=False):
    name = "georgiaz.ttf" if bold and italic else "georgiab.ttf" if bold else "georgiai.ttf" if italic else "georgia.ttf"
    return ImageFont.truetype(str(FONTS / name), round(size * S))


def unquote(v):
    v = v.strip()
    if v[:1] == '"' and v.endswith('"'):
        return v[1:-1].replace('\\"', '"').replace("\\\\", "\\")
    if v[:1] == "'" and v.endswith("'"):
        return v[1:-1].replace("''", "'")
    return re.sub(r"\s+#.*$", "", v)  # drop a trailing YAML comment


def front_matter(path):
    text = path.read_text(encoding="utf-8")
    m = re.match(r"---\s*\n(.*?)\n---", text, re.S)
    fm = {}
    for line in (m.group(1).splitlines() if m else []):
        k = re.match(r"([A-Za-z_]+):\s*(.*)$", line)
        if k:
            fm[k.group(1)] = unquote(k.group(2))
    return fm


def tokens(title):
    """Words, with an extra break opportunity after '/'. Each token is (text, space_before)."""
    out = []
    for word in title.split():
        parts = re.findall(r"[^/]+/?|/", word)
        out += [(p, i == 0 and bool(out)) for i, p in enumerate(parts)]
    return out


def join(toks):
    return "".join((" " if sp and i else "") + t for i, (t, sp) in enumerate(toks))


def best_split(toks, n, f):
    """Split tokens into n lines minimising the widest line."""
    best = None
    for cuts in combinations(range(1, len(toks)), n - 1):
        bounds = (0, *cuts, len(toks))
        lines = [join(toks[a:b]) for a, b in zip(bounds, bounds[1:])]
        widest = max(f.getlength(l) for l in lines)
        if best is None or widest < best[0]:
            best = (widest, lines)
    return best


def fit_title(title, max_size=104, min_size=40, two_line_floor=72):
    """Largest size that fits in one or two lines; a third line only when two would go below the floor."""
    toks = tokens(title)
    for max_lines, floor in ((2, two_line_floor), (3, min_size)):
        for size in range(max_size, floor - 1, -2):
            f = font(True, size)
            for n in range(1, min(max_lines, len(toks)) + 1):
                widest, lines = best_split(toks, n, f)
                if widest <= TITLE_MAX_W * S and (n - 1) * size * 1.14 + cap_height(f) / S <= TITLE_MAX_H:
                    return f, size, lines
    raise SystemExit(f"title does not fit in three lines: {title!r}")


def cap_height(f):
    return -f.getbbox("H", anchor="ls")[1]


def tracked(d, xy, text, f, fill, spacing):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill, anchor="ls")
        x += f.getlength(ch) + spacing * S


def fit_line(text, size, bold, italic, max_w):
    while size > 14 and font(bold, size, italic).getlength(text) > max_w * S:
        size -= 1
    return font(bold, size, italic)


def orbit(img):
    """The avatar.svg motif: a faint disc, three rings, four waypoints, a half-orbit arc, a hub."""
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy = (v * S for v in ORBIT_C)
    k = ORBIT_K * S

    def circle(r, **kw):
        d.ellipse((cx - r * k, cy - r * k, cx + r * k, cy + r * k), **kw)

    circle(80, fill=(0x24, 0x1C, 0x13, 255))
    for r, c in ((58, "#3a2e20"), (44, "#4a3b28"), (30, "#5c4a31")):
        circle(r, outline=c, width=round(1.5 * k))
    d.arc((cx - 58 * k, cy - 58 * k, cx + 58 * k, cy + 58 * k), -90, 90,
          fill=(0xC0, 0x9A, 0x3E, 215), width=round(2 * k))
    for dx, dy in ((0, -58), (41, 0), (0, 58), (-41, 0)):
        d.ellipse((cx + (dx - 4) * k, cy + (dy - 4) * k, cx + (dx + 4) * k, cy + (dy + 4) * k), fill=MUTED)
    circle(9, fill=MUTED)
    circle(4, fill=BG_TOP)
    img.alpha_composite(layer)


def card(kicker, title, footer, footer_italic=False):
    img = Image.new("RGBA", (W * S, H * S))
    d = ImageDraw.Draw(img)
    for y in range(H * S):
        t = y / (H * S - 1)
        d.line([(0, y), (W * S, y)], fill=tuple(round(a + (b - a) * t) for a, b in zip(BG_TOP, BG_BOTTOM)))
    orbit(img)

    tracked(d, (LEFT * S, 92 * S), kicker, font(False, 22), MUTED, 3.2)

    f, size, lines = fit_title(title)
    lead, cap = size * 1.14, cap_height(f) / S
    first_base = TITLE_MID - ((len(lines) - 1) * lead + cap) / 2 + cap
    for i, line in enumerate(lines):
        d.text((LEFT * S, (first_base + i * lead) * S), line, font=f, fill=GOLD, anchor="ls")

    d.line([(LEFT * S, RULE_Y * S), (RIGHT * S, RULE_Y * S)], fill=MUTED, width=S)
    ff = fit_line(footer, 30, False, footer_italic, RIGHT - LEFT)
    d.text((LEFT * S, FOOTER_BASE * S), footer, font=ff, fill=PARCHMENT, anchor="ls")
    return img.resize((W, H), Image.LANCZOS).convert("RGB")


def save(img, name):
    path = OUT / name
    img.save(path, optimize=True)
    print(f"{path.relative_to(SITE).as_posix()}  {path.stat().st_size // 1024} KB")


def site_config():
    cfg = {}
    for line in (SITE / "_config.yml").read_text(encoding="utf-8").splitlines():
        m = re.match(r"(title|tagline):\s*(.*)$", line)
        if m and m.group(1) not in cfg:
            cfg[m.group(1)] = unquote(m.group(2))
    return cfg


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = site_config()  # top-level title and tagline
    save(card("THE BUILD LOG", cfg["title"], cfg["tagline"], footer_italic=True), "default.png")
    for post in sorted((SITE / "_posts").glob("*.md")):
        fm = front_matter(post)
        if not fm.get("title") or not fm.get("chapter", "").isdigit():
            continue
        n = int(fm["chapter"])
        save(card(f"THE BUILD LOG  \u00b7  CHAPTER {n}", fm["title"], cfg["title"]), f"chapter-{n:02d}.png")


if __name__ == "__main__":
    main()
