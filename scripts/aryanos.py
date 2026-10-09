"""Shared look for every ARYAN.OS asset: palette, embedded fonts, text measuring.

The palette and type are lifted from the portfolio (neverthesameagain.github.io/aryanmathur.github.io).
GitHub serves README images through a proxy that blocks web fonts, so each SVG carries
its own subset of Bricolage Grotesque, Geist and Geist Mono as base64 woff2.
"""
import base64
import functools
import pathlib
from xml.sax.saxutils import escape

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"

BG = "#06070a"
RAISED = "#0b0d11"
INSET = "#101318"
INK = "#f3f1ec"
DIM = "#9a9da4"
FAINT = "#83868d"
LINE = "rgba(245,244,238,0.09)"
LINE_STRONG = "rgba(245,244,238,0.18)"
SIGNAL = "#ff5a36"
LAB = "#49e0c8"
BUILD = "#7691ff"

# Light-theme twins, only used by the transparent section headers.
L_INK = "#0b0d11"
L_DIM = "#565a62"
L_LINE = "rgba(11,13,17,0.14)"
L_SIGNAL = "#e2401c"
L_LAB = "#0f9d88"
L_BUILD = "#3f5fe0"

FACES = {
    "display": ("bric-800.woff2", "AOS Display"),
    "title": ("bric-600.woff2", "AOS Title"),
    "mono": ("gmono-400.woff2", "AOS Mono"),
    "mono-med": ("gmono-500.woff2", "AOS Mono Med"),
    "body": ("geist-400.woff2", "AOS Body"),
}
STACKS = {
    "display": "'AOS Display', 'Bricolage Grotesque', ui-sans-serif, sans-serif",
    "title": "'AOS Title', 'Bricolage Grotesque', ui-sans-serif, sans-serif",
    "mono": "'AOS Mono', ui-monospace, SFMono-Regular, Menlo, monospace",
    "mono-med": "'AOS Mono Med', ui-monospace, SFMono-Regular, Menlo, monospace",
    "body": "'AOS Body', -apple-system, 'Segoe UI', Helvetica, Arial, sans-serif",
}


@functools.cache
def _b64(file):
    return base64.b64encode((FONTS / file).read_bytes()).decode()


def font_css(*faces):
    out = []
    for face in faces:
        file, family = FACES[face]
        out.append(
            f"@font-face{{font-family:'{family}';src:url(data:font/woff2;base64,{_b64(file)}) format('woff2');}}"
        )
    for face in faces:
        out.append(f".{face}{{font-family:{STACKS[face]};}}")
    return "\n".join(out)


@functools.cache
def _metrics(file):
    from fontTools.ttLib import TTFont

    font = TTFont(FONTS / file)
    return font.getBestCmap(), font["hmtx"].metrics, font["head"].unitsPerEm


def measure(text, face, size, spacing=0.0):
    """Advance width of `text` in px, so layouts can sit things right after a word."""
    cmap, hmtx, upm = _metrics(FACES[face][0])
    units = 0
    for ch in text:
        glyph = cmap.get(ord(ch))
        units += hmtx[glyph][0] if glyph else upm * 0.6
    return units * size / upm + spacing * max(len(text) - 1, 0)


def t(s):
    return escape(s)


def svg(width, height, body, faces, style="", title=""):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{t(title)}">
<title>{t(title)}</title>
<style>
{font_css(*faces)}
{style}
</style>
{body}
</svg>
"""


def scanlines(id_="scan", opacity=0.05):
    return f"""<pattern id="{id_}" width="4" height="4" patternUnits="userSpaceOnUse">
<rect width="4" height="1" fill="#ffffff" opacity="{opacity}"/></pattern>"""


def grid(id_="grid", step=40, opacity=0.035):
    return f"""<pattern id="{id_}" width="{step}" height="{step}" patternUnits="userSpaceOnUse">
<path d="M{step} 0H0V{step}" fill="none" stroke="#ffffff" stroke-opacity="{opacity}"/></pattern>"""


def frame(w, h, r=18, glow=None, glow_at=(0.15, 1.0)):
    """A dark 'screen': background, grid, optional colour bloom, scanlines, hairline border."""
    defs = [scanlines(), grid()]
    layers = [f'<rect width="{w}" height="{h}" rx="{r}" fill="{BG}"/>',
              f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#grid)"/>']
    if glow:
        defs.append(f"""<radialGradient id="bloom" cx="{glow_at[0]}" cy="{glow_at[1]}" r="0.75">
<stop offset="0" stop-color="{glow}" stop-opacity="0.16"/><stop offset="1" stop-color="{glow}" stop-opacity="0"/></radialGradient>""")
        layers.append(f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#bloom)"/>')
    back = f"<defs>{''.join(defs)}</defs>" + "".join(layers)
    front = (f'<rect width="{w}" height="{h}" rx="{r}" fill="url(#scan)" pointer-events="none"/>'
             f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{LINE_STRONG}"/>')
    return back, front


def chip(x, y, label, color=DIM, fill=INSET, stroke=LINE_STRONG, size=14, pad=12, h=30, cls="mono"):
    w = measure(label, "mono", size) + pad * 2
    return (f'<g><rect x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="{h/2}" fill="{fill}" stroke="{stroke}"/>'
            f'<text x="{x + pad:.1f}" y="{y + h/2 + size*0.36:.1f}" class="{cls}" font-size="{size}" fill="{color}">{t(label)}</text></g>'), w


def chips(x, y, labels, gap=8, max_x=None, **kw):
    out, cx, cy = [], x, y
    for label in labels:
        w = measure(label, "mono", kw.get("size", 14)) + kw.get("pad", 12) * 2
        if max_x and cx + w > max_x and cx > x:
            cx, cy = x, cy + kw.get("h", 30) + gap
        s, w = chip(cx, cy, label, **kw)
        out.append(s)
        cx += w + gap
    return "".join(out), cy


def write(name, content):
    path = ASSETS / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    print(f"{name:34s} {len(content)/1024:6.1f} KB")
