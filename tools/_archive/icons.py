"""Icon set: one glyph on a rounded plate. 2.5D = extruded plate + glyph shadow; flat = same without the extrusion."""
import math

HUES = {  # light, base, dark
    "blue": ("#7CC4FF", "#2F8CFF", "#1B5FC4"),
    "indigo": ("#9AA6FF", "#5B6CF5", "#3A47C2"),
    "violet": ("#C09BFF", "#8B5CF6", "#5E36BE"),
    "pink": ("#FF9DBF", "#F2547F", "#B82F58"),
    "orange": ("#FFBB7A", "#FF8A2B", "#C25E10"),
    "amber": ("#FFDB7A", "#F5B100", "#B07C00"),
    "green": ("#7BE5AB", "#22C16B", "#12874A"),
    "teal": ("#6DE6E0", "#14B8B0", "#0B857F"),
    "red": ("#FF9A90", "#F0473A", "#B02A20"),
    "slate": ("#B4BED0", "#6B7A90", "#44526A"),
}

S = 'fill="none" stroke="@W" stroke-width="3.4" stroke-linecap="round" stroke-linejoin="round"'


def _gear():
    out = [f'<circle cx="32" cy="28" r="8" {S}/>', '<circle cx="32" cy="28" r="2.6" fill="@W"/>']
    for k in range(8):
        a = math.radians(k * 45)
        x1, y1 = 32 + 12.5 * math.cos(a), 28 + 12.5 * math.sin(a)
        x2, y2 = 32 + 15.5 * math.cos(a), 28 + 15.5 * math.sin(a)
        out.append(f'<path d="M{x1:.1f} {y1:.1f}L{x2:.1f} {y2:.1f}" stroke="@W" stroke-width="4.6" stroke-linecap="round"/>')
    return "".join(out)


def _bug():
    return ('<ellipse cx="32" cy="31" rx="8" ry="11" fill="@W"/><circle cx="32" cy="17.5" r="4.4" fill="@W"/>'
            f'<path d="M24 25l-7-3M24 32h-8M25 39l-6 4M40 25l7-3M40 32h8M39 39l6 4M29 14l-3-3M35 14l3-3" {S} stroke-width="2.8"/>'
            '<path d="M32 22v19" stroke="@D" stroke-width="2.4" stroke-linecap="round"/>')


GLYPHS = {
    "js": f'<path d="M26 14c-5 0-6 2-6 6v4c0 3-2 4-4 4 2 0 4 1 4 4v4c0 4 1 6 6 6M38 14c5 0 6 2 6 6v4c0 3 2 4 4 4-2 0-4 1-4 4v4c0 4-1 6-6 6" {S}/>',
    "json": f'<path d="M26 14c-5 0-6 2-6 6v4c0 3-2 4-4 4 2 0 4 1 4 4v4c0 4 1 6 6 6M38 14c5 0 6 2 6 6v4c0 3 2 4 4 4-2 0-4 1-4 4v4c0 4-1 6-6 6" {S}/>'
            '<circle cx="29" cy="28" r="1.9" fill="@W"/><circle cx="35" cy="28" r="1.9" fill="@W"/>',
    "expr": f'<path d="M24 15c-4 0-5 2-5 5v3.5c0 2.5-2 3.5-3.5 3.5 1.5 0 3.5 1 3.5 3.5V34c0 3 1 5 5 5M40 15c4 0 5 2 5 5v3.5c0 2.5 2 3.5 3.5 3.5-1.5 0-3.5 1-3.5 3.5V34c0 3-1 5-5 5" {S} stroke-width="3"/>'
            f'<path d="M28 25h8M28 31h8" {S} stroke-width="3"/>',
    "console": f'<rect x="14" y="14" width="36" height="28" rx="5" {S}/><path d="M21 23l6 5-6 5M31 34h10" {S}/>',
    "warn": '<path d="M32 13l17 29H15z" fill="@W" stroke="@W" stroke-width="4" stroke-linejoin="round"/>'
            '<rect x="30.4" y="23" width="3.2" height="9.5" rx="1.6" fill="@D"/><circle cx="32" cy="37" r="2" fill="@D"/>',
    "tag": '<path d="M16 15h14l18 18-14 14L16 29z" fill="@W" stroke="@W" stroke-width="3" stroke-linejoin="round" transform="translate(0,-3)"/>'
           '<circle cx="24" cy="21" r="3" fill="@D"/>',
    "shapes": '<circle cx="22" cy="34" r="7" fill="@W"/><rect x="31" y="27" width="15" height="15" rx="3" fill="@W"/>'
              '<path d="M34 24l-7-12-7 12z" fill="@W" stroke="@W" stroke-width="2" stroke-linejoin="round"/>',
    "quote": '<path d="M15 36V27c0-6 3-9 9-10v4c-2.500.5-4 2-4 5h4v10zM33 36V27c0-6 3-9 9-10v4c-2.500.5-4 2-4 5h4v10z" fill="@W" transform="translate(2,3)"/>',
    "equal": '<rect x="14" y="15" width="36" height="4.4" rx="2.2" fill="@W"/><rect x="14" y="26" width="36" height="4.4" rx="2.2" fill="@W"/><rect x="14" y="37" width="36" height="4.4" rx="2.2" fill="@W"/>',
    "swap": f'<path d="M16 21h26M36 14l8 7-8 7M48 36H22M28 29l-8 7 8 7" {S}/>',
    "updown": f'<path d="M24 42V16M17 23l7-8 7 8M40 14v26M33 33l7 8 7-8" {S}/>',
    "box": '<path d="M32 12l16 8.500-16 8.500-16-8.500z" fill="@W"/><path d="M16 22.500l15 8v14l-15-8z" fill="@W" opacity=".78"/>'
           '<path d="M48 22.500l-15 8v14l15-8z" fill="@W" opacity=".58"/>',
    "array": '<rect x="13" y="25" width="11" height="15" rx="3" fill="@W"/><rect x="26.500" y="25" width="11" height="15" rx="3" fill="@W"/><rect x="40" y="25" width="11" height="15" rx="3" fill="@W"/>'
             '<circle cx="18.500" cy="17" r="2.200" fill="@W"/><circle cx="32" cy="17" r="2.200" fill="@W"/><circle cx="45.500" cy="17" r="2.200" fill="@W"/>',
    "layers": '<rect x="14" y="28" width="28" height="15" rx="3.500" fill="@W" opacity=".5"/><rect x="19" y="21" width="28" height="15" rx="3.500" fill="@W" opacity=".78"/>'
              '<rect x="24" y="13" width="26" height="15" rx="3.500" fill="@W"/>',
    "branch": f'<circle cx="32" cy="16" r="4.600" fill="@W"/><circle cx="19" cy="41" r="4.600" fill="@W"/><circle cx="45" cy="41" r="4.600" fill="@W"/>'
              f'<path d="M32 20v5c0 6-13 6-13 12M32 25c0 6 13 6 13 12" {S}/>',
    "falsy": f'<circle cx="32" cy="28" r="13" {S}/><path d="M23 37l18-18" {S}/>',
    "question": f'<path d="M24 22c0-6 4-9 9-8s7 6 3 10c-3 2.500-4 4-4 7" {S} stroke-width="4"/><circle cx="32" cy="41" r="2.800" fill="@W"/>',
    "loop": f'<path d="M46 25a14 14 0 0 0-24-6M18 31a14 14 0 0 0 24 6" {S}/><path d="M47 14v11H36M17 42V31h11" {S}/>',
    "checklist": f'<path d="M15 19l3.500 3.500 6-7M15 30l3.500 3.500 6-7M15 41l3.500 3.500 6-7" {S} stroke-width="3" transform="translate(0,-3)"/><path d="M31 19h18M31 30h18M31 41h18" {S} stroke-width="3.400" transform="translate(0,-3)"/>',
    "fn": f'<rect x="22" y="17" width="20" height="22" rx="4.500" fill="@W"/><path d="M11 28h8M15 24l4 4-4 4M45 28h8M49 24l4 4-4 4" {S} stroke-width="3"/>',
    "exit": f'<path d="M25 14h-9v28h9" {S}/><path d="M26 28h21M40 21l7 7-7 7" {S}/>',
    "callback": f'<path d="M17 21h17a10 10 0 0 1 0 20h-6" {S}/><path d="M33 35l-7 6 7 6" {S} transform="translate(0,-2)"/>',
    "arrowfn": f'<path d="M15 23h14M15 33h14" {S}/><path d="M36 19l12 9-12 9" {S}/>',
    "find": f'<path d="M15 19h20M15 29h11M15 39h13" {S}/><circle cx="38" cy="31" r="7.500" {S}/><path d="M44 37l6 6" {S}/>',
    "balance": '<path d="M32 13v28M21 42h22M17 20h30" fill="none" stroke="@W" stroke-width="3.400" stroke-linecap="round"/>'
               '<path d="M17 21l-6 12h12zM47 21l-6 12h12z" fill="@W" stroke="@W" stroke-width="2" stroke-linejoin="round"/>',
    "target": f'<circle cx="32" cy="28" r="13" {S}/><circle cx="32" cy="28" r="4.500" fill="@W"/><path d="M32 11v6M32 39v6M15 28h6M43 28h6" {S} stroke-width="3"/>',
    "scope": f'<rect x="13" y="13" width="38" height="30" rx="5" {S}/><rect x="21" y="20" width="22" height="16" rx="3" {S} stroke-width="3"/><rect x="28" y="25" width="8" height="6" rx="1.500" fill="@W"/>',
    "chain": f'<g transform="rotate(-35 32 28)"><rect x="12" y="22" width="23" height="13" rx="6.500" {S}/><rect x="29" y="22" width="23" height="13" rx="6.500" {S}/></g>',
    "hourglass": f'<path d="M20 14h24M20 42h24M23 14c0 8 6 10 9 14-3 4-9 6-9 14M41 14c0 8-6 10-9 14 3 4 9 6 9 14" {S}/>',
    "clock": f'<circle cx="32" cy="28" r="14" {S}/><path d="M32 19v10l7 4" {S}/>',
    "flow": '<circle cx="17" cy="28" r="5" fill="@W"/><circle cx="47" cy="28" r="5" fill="@W"/>' + f'<path d="M25 28h14M34 22l6 6-6 6" {S}/>',
    "folder": '<path d="M14 19a3 3 0 0 1 3-3h9l4 5h17a3 3 0 0 1 3 3v16a3 3 0 0 1-3 3H17a3 3 0 0 1-3-3z" fill="@W" transform="translate(0,-1)"/>',
    "tree": f'<path d="M19 15v24M19 23h9M19 39h9" {S} stroke-width="3"/><rect x="28" y="17" width="19" height="10" rx="3" fill="@W"/><rect x="28" y="34" width="19" height="10" rx="3" fill="@W"/>',
    "code": f'<path d="M24 20l-9 8 9 8M40 20l9 8-9 8M35 15l-6 26" {S}/>',
    "key": f'<circle cx="23" cy="28" r="7" {S}/><path d="M30 28h19M43 28v7M48.500 28v5" {S}/>',
    "gear": _gear(),
    "click": '<rect x="13" y="19" width="30" height="17" rx="8.500" fill="@W" opacity=".75"/><path d="M36 28l12 9-5.500 1.200 3.500 6-3.500 2-3.500-6-4 3.800z" fill="@W" stroke="@D" stroke-width="1.600" stroke-linejoin="round"/>',
    "envelope": f'<rect x="13" y="16" width="38" height="26" rx="4.500" fill="@W"/><path d="M14 20l18 13 18-13" fill="none" stroke="@D" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    "layout": '<rect x="13" y="13" width="38" height="9" rx="2.500" fill="@W"/><rect x="13" y="26" width="17" height="17" rx="2.500" fill="@W" opacity=".8"/><rect x="34" y="26" width="17" height="17" rx="2.500" fill="@W" opacity=".8"/>',
    "pieces": '<rect x="13" y="24" width="22" height="20" rx="4" fill="@W" opacity=".7"/><rect x="29" y="12" width="22" height="20" rx="4" fill="@W"/>',
    "dialog": '<rect x="13" y="13" width="28" height="22" rx="3.500" fill="@W" opacity=".5"/><rect x="22" y="22" width="29" height="22" rx="4" fill="@W"/>'
              '<path d="M22 29h29" stroke="@D" stroke-width="2.600"/><circle cx="27" cy="25.500" r="1.400" fill="@D"/><circle cx="31.500" cy="25.500" r="1.400" fill="@D"/>',
    "bind": '<rect x="12" y="20" width="15" height="15" rx="4" fill="@W"/><rect x="37" y="20" width="15" height="15" rx="4" fill="@W"/>' + f'<path d="M27 27.500h10" {S} stroke-width="4"/><circle cx="32" cy="27.500" r="2.600" fill="@W"/>',
    "path": f'<circle cx="17" cy="41" r="4" fill="@W"/><circle cx="47" cy="15" r="4" fill="@W"/><path d="M17 37c0-12 15-6 15-15s9-5 15-3" {S} stroke-dasharray="1 7" stroke-width="4.400"/>',
    "db": '<path d="M19 18v20c0 3.500 5.800 6 13 6s13-2.500 13-6V18z" fill="@W"/><ellipse cx="32" cy="18" rx="13" ry="5.500" fill="@W"/>'
          '<path d="M19 18c0 3.500 5.800 6 13 6s13-2.500 13-6M19 28c0 3.500 5.800 6 13 6s13-2.500 13-6" fill="none" stroke="@D" stroke-width="2.400" opacity=".75"/><ellipse cx="32" cy="17" rx="13" ry="5.500" fill="@W" opacity=".0"/>',
    "copy": '<rect x="13" y="21" width="25" height="22" rx="4" fill="@W" opacity=".55"/><rect x="25" y="13" width="26" height="23" rx="4" fill="@W"/>',
    "pin": '<path d="M32 12a11 11 0 0 1 11 11c0 9-11 21-11 21S21 32 21 23a11 11 0 0 1 11-11z" fill="@W"/><circle cx="32" cy="23" r="4.200" fill="@D"/>',
    "dropdown": '<rect x="13" y="13" width="38" height="13" rx="4.500" fill="@W"/><path d="M39 17.500l4 4 4-4" fill="none" stroke="@D" stroke-width="2.600" stroke-linecap="round" stroke-linejoin="round"/>'
                '<rect x="13" y="30" width="38" height="6" rx="3" fill="@W" opacity=".6"/><rect x="13" y="39" width="38" height="6" rx="3" fill="@W" opacity=".4"/>',
    "masterdetail": '<rect x="13" y="13" width="16" height="31" rx="3.500" fill="@W" opacity=".65"/><path d="M17 20h8M17 27h8M17 34h8" stroke="@D" stroke-width="2.400" stroke-linecap="round"/>'
                    '<rect x="33" y="13" width="18" height="31" rx="3.500" fill="@W"/><path d="M37 20h10M37 27h10M37 34h6" stroke="@D" stroke-width="2.400" stroke-linecap="round"/>',
    "check": '<circle cx="32" cy="28" r="15" fill="@W"/><path d="M24 28.500l6 6 10-12" fill="none" stroke="@D" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>',
    "table": '<rect x="13" y="13" width="38" height="31" rx="4.500" fill="@W"/><path d="M13 24h38M26 24v20M39 24v20" stroke="@D" stroke-width="2.400" opacity=".8"/><path d="M13 24h38" stroke="@D" stroke-width="2.400"/>',
    "funnel": '<path d="M13 15h38L37 30v11l-10 4V30z" fill="@W" stroke="@W" stroke-width="3" stroke-linejoin="round"/>',
    "sort": f'<path d="M21 14v28M14 35l7 8 7-8" {S}/><path d="M36 17h13M36 27h9M36 37h5" {S}/>',
    "wand": f'<path d="M16 43l20-20" {S} stroke-width="5"/><path d="M43 10l2.600 6.400L52 19l-6.400 2.600L43 28l-2.600-6.400L34 19l6.400-2.600z" fill="@W" transform="translate(-2,0)"/>',
    "pager": f'<path d="M25 17L14 28l11 11M39 17l11 11-11 11" {S}/><rect x="29.500" y="22" width="5" height="12" rx="2.500" fill="@W"/>',
    "coin": '<circle cx="32" cy="28" r="15" fill="@W"/><circle cx="32" cy="28" r="11" fill="none" stroke="@D" stroke-width="1.800" opacity=".6"/>'
            '<path d="M23.500 21l4 14 4.500-10 4.500 10 4-14M22 27h20M22 31h20" fill="none" stroke="@D" stroke-width="2.400" stroke-linecap="round" stroke-linejoin="round"/>',
    "steps": '<rect x="13" y="33" width="11" height="11" rx="2.500" fill="@W" opacity=".6"/><rect x="26.500" y="24" width="11" height="20" rx="2.500" fill="@W" opacity=".8"/><rect x="40" y="14" width="11" height="30" rx="2.500" fill="@W"/>',
    "bug": _bug(),
    "server": '<rect x="13" y="13" width="38" height="13" rx="4" fill="@W"/><rect x="13" y="30" width="38" height="13" rx="4" fill="@W"/>'
              '<circle cx="21" cy="19.500" r="2.200" fill="@D"/><circle cx="21" cy="36.500" r="2.200" fill="@D"/><path d="M29 19.500h14M29 36.500h14" stroke="@D" stroke-width="2.400" stroke-linecap="round"/>',
    "book": '<path d="M13 15h14c3 0 5 2 5 5v24c0-3-2-5-5-5H13z" fill="@W"/><path d="M51 15H37c-3 0-5 2-5 5v24c0-3 2-5 5-5h14z" fill="@W" opacity=".78"/>',
    "shrink": f'<path d="M14 28h13M21 21l7 7-7 7M50 28H37M43 21l-7 7 7 7" {S}/>',
    "flag": f'<path d="M19 13v32" {S}/><path d="M21 15h25l-6 9 6 9H21z" fill="@W" stroke="@W" stroke-width="2.600" stroke-linejoin="round"/>',
    "toolbox": f'<rect x="13" y="24" width="38" height="20" rx="4.500" fill="@W"/><path d="M25 24v-4a3 3 0 0 1 3-3h8a3 3 0 0 1 3 3v4" {S}/><rect x="28" y="31" width="8" height="6" rx="2" fill="@D"/>',
}


def _sym(gid, glyph, hue):
    light, base, dark = HUES[hue]
    body = GLYPHS[glyph]
    front = body.replace("@W", "#fff").replace("@D", dark)
    shadow = body.replace("@W", dark).replace("@D", dark)
    return (f'<symbol id="{gid}" viewBox="0 0 64 64">'
            f'<ellipse class="ex" style="opacity:calc(var(--ex,1)*.14)" cx="32" cy="59.500" rx="21" ry="3.200" fill="#1b2a4a"/>'
            f'<rect class="ex" style="opacity:var(--ex,1)" x="6" y="10" width="52" height="48" rx="15" fill="{dark}"/>'
            f'<rect x="6" y="4" width="52" height="48" rx="15" fill="url(#g-{hue})"/>'
            f'<path d="M6 18A14 14 0 0 1 20 4h24a14 14 0 0 1 14 14v1C46 15 18 15 6 19z" fill="#fff" opacity=".2"/>'
            f'<g class="ex" style="opacity:calc(var(--ex,1)*.32)" transform="translate(0,2.400)">{shadow}</g>'
            f'<g>{front}</g></symbol>')


def defs(used):
    """used: set of (glyph, hue). Returns a hidden <svg> with gradients and symbols."""
    grads = "".join(f'<linearGradient id="g-{h}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c[0]}"/>'
                    f'<stop offset="1" stop-color="{c[1]}"/></linearGradient>' for h, c in HUES.items())
    syms = "".join(_sym(f"ic-{g}-{h}", g, h) for g, h in sorted(used))
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{grads}{syms}</defs></svg>'


def icon(glyph, hue, cls="", flat=False):
    vb = "6 4 52 48" if flat else "0 0 64 64"
    c = ("ic flat " if flat else "ic ") + cls
    return (f'<svg class="{c.strip()}" viewBox="{vb}" aria-hidden="true" focusable="false">'
            f'<use href="#ic-{glyph}-{hue}"/></svg>')
