"""2.5D icons drawn inside figures (no floor shadow). Symbols are emitted once per page as #nt-<obj>-<hue>-E."""
import re
import toss_icons as _ti

NS = set()


def _id(obj, hue):
    return f"nt-{obj}-{hue or 'x'}-E"


def use3(obj, hue, x, y, s):
    NS.add((obj, hue))
    return f"<use href='#{_id(obj, hue)}' x='{x}' y='{y}' width='{s}' height='{s}'/>"


def html3(obj, hue, cls="ic3"):
    NS.add((obj, hue))
    return f'<svg class="{cls}" viewBox="0 0 64 64" aria-hidden="true"><use href="#{_id(obj, hue)}"/></svg>'


def ns_defs():
    if not NS:
        return ""
    d = _ti.defs_svg({(o, h, "E") for o, h in NS})
    syms = "".join(re.findall(r"<symbol.*?</symbol>", d, flags=re.S)).replace(_ti.SH, "").replace('id="t-', 'id="nt-')
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{syms}</defs></svg>'
