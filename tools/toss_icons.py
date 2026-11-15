"""Toss-style object icons. Each object fn(mode, hue=None) -> inner SVG for a 64x64 box.
mode 'D' = flat colour + lower shade (emoji-like), 'E' = gradient + gloss (jelly 3D)."""
import math

PAL = {  # light, base, dark
    'blue': ('#8FD0FF', '#3D9BFF', '#1F68D6'), 'orange': ('#FFC37A', '#FF9A3C', '#D96A12'),
    'indigo': ('#A9B1FF', '#6572F7', '#3F48C8'), 'amber': ('#FFE08A', '#FFC12E', '#D99200'),
    'violet': ('#CDA9FF', '#9A68F8', '#6B3FCB'), 'red': ('#FF9F95', '#F5513F', '#C42F22'),
    'slate': ('#C3CBDA', '#7F8CA3', '#55627A'), 'glass': ('#EAF6FF', '#CBE6FF', '#9CCBF2'),
    'ink': ('#5b667a', '#3a4458', '#262d3d'), 'green': ('#8CEAB4', '#2FCB74', '#179553'),
    'teal': ('#7BE8E2', '#18C0B8', '#0D8C86'), 'pink': ('#FFA9C7', '#F6628F', '#BF3A66'),
    'paper': ('#FFFFFF', '#F7F9FC', '#C9D3E3'),
}


def fills(m, c):
    l, b, d = PAL[c]
    if m == 'E':
        return f'url(#gl-{c})', f'url(#gd-{c})'
    return b, d


def defs():
    out = ''
    for c, (l, b, d) in PAL.items():
        out += (f'<linearGradient id="gl-{c}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{l}"/><stop offset="1" stop-color="{b}"/></linearGradient>'
                f'<linearGradient id="gd-{c}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{b}"/><stop offset="1" stop-color="{d}"/></linearGradient>')
    return out


SH = '<ellipse cx="32" cy="60.500" rx="18" ry="2.600" fill="#1b2a4a" opacity=".13"/>'


def R(m, c, x, y, w, h, r=4, dy=3):
    f, d = fills(m, c)
    return (f'<rect x="{x}" y="{y + dy}" width="{w}" height="{h}" rx="{r}" fill="{d}"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{f}"/>')


def C(m, c, cx, cy, r, dy=3):
    f, d = fills(m, c)
    return (f'<circle cx="{cx}" cy="{cy + dy}" r="{r}" fill="{d}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{f}"/>')


def P(m, c, d_, dy=3, sw=3, tr=''):
    f, d = fills(m, c)
    t = f' transform="{tr}"' if tr else ''
    return (f'<g{t}><path d="{d_}" fill="{d}" stroke="{d}" stroke-width="{sw}" stroke-linejoin="round" transform="translate(0,{dy})"/>'
            f'<path d="{d_}" fill="{f}" stroke="{f}" stroke-width="{sw}" stroke-linejoin="round"/></g>')


def S(m, c, d_, w=7, dy=3):
    f, d = fills(m, c)
    a = f'fill="none" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"'
    return (f'<path d="{d_}" {a} stroke="{d}" transform="translate(0,{dy})"/><path d="{d_}" {a} stroke="{f}"/>')


def W(d_, w=3.5, op=1):  # white detail stroke
    return f'<path d="{d_}" fill="none" stroke="#fff" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'


def K(d_, c='ink', w=3.5, op=1):  # dark detail stroke
    return f'<path d="{d_}" fill="none" stroke="{PAL[c][2]}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" opacity="{op}"/>'


def WR(x, y, w, h, r=2, op=.92):  # white detail rect
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="#fff" opacity="{op}"/>'


def G(m, x, y, w, h, op=.55):  # gloss (jelly only)
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{min(w, h) / 2}" fill="#fff" opacity="{op}"/>' if m == 'E' else ''


def dot(x, y, r, c='#fff', op=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" opacity="{op}"/>'


# ---------------------------------------------------------------- objects
def tag(m, h='blue'):
    body = 'M32 7L47 18V50a4 4 0 0 1-4 4H21a4 4 0 0 1-4-4V18Z'
    return (SH + f'<g transform="rotate(-12 32 32)">' + P(m, h, body, 3, 4) + dot(32, 20, 3.6, '#fff', .95)
            + WR(24, 33, 16, 3.6, 1.8) + WR(24, 41, 10, 3.6, 1.8) + G(m, 21, 22, 4, 22, .5) + '</g>')


def box(m, h='orange'):
    lt, bs, dk = PAL[h]
    top = lt if m == 'D' else f'url(#gl-{h})'
    left = bs if m == 'D' else f'url(#gd-{h})'
    return (SH + '<g stroke-linejoin="round" stroke-width="3">'
            f'<path d="M10 19L32 30V56L10 45Z" fill="{left}" stroke="{left}"/><path d="M54 19L32 30V56L54 45Z" fill="{dk}" stroke="{dk}"/>'
            f'<path d="M32 8L54 19L32 30L10 19Z" fill="{top}" stroke="{top}"/></g>'
            '<path d="M26 11.500L48 22.500" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".55"/>'
            '<path d="M15 33L27 39V46L15 40Z" fill="#fff" opacity=".9"/>')


def sign(m, h=None):
    return (SH + R(m, 'slate', 29.5, 8, 5, 48, 2.5, 0)
            + P(m, 'indigo', 'M13 12H43L51 20L43 28H13Z', 2.5, 3) + P(m, 'amber', 'M51 33H21L13 41L21 49H51Z', 2.5, 3)
            + WR(19, 18, 18, 3.6, 1.8) + WR(27, 39, 18, 3.6, 1.8) + G(m, 17, 14, 22, 2.6, .45))


def vend(m, h='blue'):
    items = ''.join(f'<rect x="{x}" y="{y}" width="5" height="7" rx="1.8" fill="{c}"/>' for x, y, c in
                    [(22, 17, '#FF9A3C'), (29, 17, '#F5513F'), (22, 28, '#FFC12E'), (29, 28, '#3D9BFF')])
    return (SH + R(m, h, 12, 6, 40, 49, 7, 2) + f'<rect x="17" y="11" width="23" height="30" rx="3.5" fill="#CBE6FF"/>' + items
            + G(m, 19, 12.5, 2.4, 24, .8) + dot(46, 16, 2.4) + dot(46, 23, 2.4, '#fff', .75) + dot(46, 30, 2.4, '#fff', .5)
            + f'<rect x="17" y="45" width="30" height="6" rx="3" fill="{PAL["ink"][2]}"/>')


def hourglass(m, h='violet'):
    glass = 'M20 14H44C44 25 36 28 36 32C36 36 44 39 44 50H20C20 39 28 36 28 32C28 28 20 25 20 14Z'
    af, ad = fills(m, 'amber')
    return (SH + f'<path d="{glass}" fill="#CBE6FF" opacity=".95" stroke="#9CCBF2" stroke-width="1.5"/>'
            f'<path d="M24 17H40C39 22 35 25 32 27C29 25 25 22 24 17Z" fill="{af}"/><path d="M22.5 50C23.5 44 28 41.5 32 41.5C36 41.5 40.5 44 41.5 50Z" fill="{af}"/>'
            f'<rect x="31" y="28" width="2" height="12" rx="1" fill="{ad}"/>' + G(m, 22, 17, 2.4, 12, .7)
            + R(m, h, 14, 7, 36, 7, 3.5, 2) + R(m, h, 14, 49, 36, 7, 3.5, 2))


def bug(m, h='red'):
    rf, rd = fills(m, h)
    return (SH + '<g stroke="#262d3d" stroke-width="3" stroke-linecap="round"><path d="M16 30L8 26M15 40L7 42M48 30L56 26M49 40L57 42M26 11L22 5M38 11L42 5"/></g>'
            f'<circle cx="32" cy="38" r="19" fill="{rd}"/><circle cx="32" cy="36" r="19" fill="{rf}"/>'
            '<path d="M32 18V55" stroke="#262d3d" stroke-width="2.6" stroke-linecap="round"/>'
            + ''.join(dot(x, y, r, '#262d3d') for x, y, r in [(24, 32, 3.4), (41, 34, 3.4), (25, 44, 3), (40, 45, 3)])
            + f'<path d="M20 18A13 12 0 0 1 44 18Z" fill="{PAL["ink"][2]}"/>' + dot(27, 16, 1.8) + dot(37, 16, 1.8) + G(m, 17, 29, 3.4, 12, .6))


def laptop(m, h='blue'):
    return (SH + R(m, 'slate', 9, 10, 46, 32, 5, 3) + '<rect x="13" y="14" width="38" height="24" rx="2.5" fill="#CBE6FF"/>'
            + K('M22 22l-4 4 4 4M42 22l4 4-4 4M35 20l-6 12', h, 3) + G(m, 15, 15, 2.4, 20, .7)
            + P(m, 'blue' if h != 'slate' else 'slate', 'M7 46H57L53 53H11Z', 2, 3))


def console(m, h='ink'):
    return (SH + R(m, 'ink', 8, 10, 48, 42, 7, 3) + dot(16, 17, 2.3, '#FF6B5E') + dot(23, 17, 2.3, '#FFC12E') + dot(30, 17, 2.3, '#35D07F')
            + W('M16 28l8 6-8 6', 4, 1).replace('#fff', '#35D07F') + '<rect x="29" y="38" width="14" height="3.6" rx="1.8" fill="#8CEAB4"/>' + G(m, 11, 22, 2, 24, .18))


def toolbox(m, h='red'):
    return (SH + f'<path d="M24 23v-5a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v5" fill="none" stroke="{PAL["ink"][2]}" stroke-width="4.5" stroke-linecap="round"/>'
            + R(m, h, 7, 22, 50, 32, 7, 3) + f'<rect x="7" y="35" width="50" height="4" fill="{PAL[h][2]}" opacity=".55"/>'
            + R(m, 'amber', 26, 31, 12, 11, 3, 2) + G(m, 11, 25, 30, 4, .5))


def blocks(m, h=None):
    return (SH + R(m, 'green', 7, 34, 22, 21, 5, 3) + C(m, 'orange', 46, 44, 11, 3)
            + P(m, 'amber', 'M31 10L43 29H19Z', 3, 5) + G(m, 11, 38, 4, 10, .5))


def bubble(m, h='pink'):
    return (SH + P(m, h, 'M12 12H52A6 6 0 0 1 58 18V36A6 6 0 0 1 52 42H34L22 54V42H12A6 6 0 0 1 6 36V18A6 6 0 0 1 12 12Z', 3, 3)
            + '<path d="M19 33v-6c0-3 2-5 5-5v3c-1.3.2-2 1-2 2h2v6zM33 33v-6c0-3 2-5 5-5v3c-1.3.2-2 1-2 2h2v6z" fill="#fff" transform="translate(0,-2)"/>'
            + G(m, 11, 16, 14, 3, .5))


def scale(m, h='amber'):
    return (SH + R(m, 'slate', 22, 52, 20, 5, 2.5, 2) + R(m, 'slate', 30, 14, 4, 40, 2, 0)
            + K('M12 22L8 36M12 22L26 36M52 22L38 36M52 22L56 36', 'ink', 1.8, .6)
            + R(m, h, 8, 14, 48, 6, 3, 2)
            + P(m, 'blue', 'M5 36H27A11 11 0 0 1 5 36Z', 2, 2) + P(m, 'pink', 'M37 36H59A11 11 0 0 1 37 36Z', 2, 2))


def equals(m, h='indigo'):
    return SH + R(m, h, 9, 11, 46, 11, 5.5, 3) + R(m, h, 9, 26, 46, 11, 5.5, 3) + R(m, h, 9, 41, 46, 11, 5.5, 3) + G(m, 14, 13, 18, 2.6, .55)


def swap(m, h='blue'):
    return (SH + P(m, h, 'M8 17H38V10L56 24L38 38V31H8Z', 3, 3) + P(m, 'pink', 'M56 38H26V31L8 45L26 59V52H56Z', 3, 3).replace('translate(0,3)', 'translate(0,2)'))


def array(m, h='green'):
    out = SH
    for x in (5, 23.5, 42):
        out += R(m, h, x, 24, 17, 26, 5, 3) + dot(x + 8.5, 31, 2.6, '#fff', .9) + WR(x + 4, 39, 9, 3, 1.5, .8)
    return out + G(m, 8, 27, 3, 14, .45)


def layers(m, h=None):
    return SH + R(m, 'violet', 8, 38, 48, 13, 5, 3) + R(m, 'blue', 8, 25, 48, 13, 5, 3) + R(m, 'teal', 8, 12, 48, 13, 5, 3) + G(m, 12, 14, 18, 3, .5)


def doc(m, h='slate'):
    return (SH + R(m, 'paper', 14, 6, 36, 50, 6, 3) + f'<rect x="14" y="6" width="36" height="50" rx="6" fill="none" stroke="{PAL["glass"][2]}" stroke-width="1.5"/>'
            + K('M26 22c-3 0-4 1-4 4v3c0 2-1 3-3 3 2 0 3 1 3 3v3c0 3 1 4 4 4M38 22c3 0 4 1 4 4v3c0 2 1 3 3 3-2 0-3 1-3 3v3c0 3-1 4-4 4', 'blue', 3.4))


def no(m, h='red'):
    return (SH + C(m, h, 32, 30, 24, 3) + f'<circle cx="32" cy="30" r="14.5" fill="none" stroke="#fff" stroke-width="6"/>'
            + W('M22 40L42 20', 6) + G(m, 14, 20, 4, 14, .5))


def qblock(m, h='amber'):
    return SH + R(m, h, 9, 8, 46, 46, 11, 3) + W('M25 25c0-5 4-8 8-7s7 5 4 9c-2 2-4 3-4 6', 5) + dot(33, 43, 3) + G(m, 13, 13, 3, 14, .55)


def loop(m, h='green'):
    return (SH + S(m, h, 'M49 29A18 18 0 0 0 17 21', 7) + P(m, h, 'M55 11V32H35Z', 2, 4)
            + S(m, h, 'M15 35A18 18 0 0 0 47 43', 7) + P(m, h, 'M9 53V32H29Z', 2, 4))


def clipboard(m, h='amber'):
    return (SH + R(m, h, 11, 8, 42, 48, 7, 3) + '<rect x="16" y="15" width="32" height="36" rx="3.500" fill="#fff"/>'
            + R(m, 'slate', 23, 4, 18, 10, 4, 2) + W('M22 33l6 6 13-14', 5).replace('#fff', PAL['green'][1])
            + '<rect x="21" y="44" width="22" height="3" rx="1.5" fill="#D6DEEA"/>')


def door(m, h='teal'):
    return (SH + R(m, h, 8, 8, 28, 47, 5, 3) + dot(30, 33, 2.6, '#fff') + G(m, 11, 12, 3, 16, .5)
            + P(m, 'orange', 'M38 30H48V23L60 34L48 45V38H38Z', 2, 3))


def phone(m, h='green'):
    return SH + P(m, h, 'M13 17C13 12 17 10 21 11L26 12L28 21L23 24C26 31 30 35 37 39L41 34L50 36L51 41C51 46 48 50 43 50C26 49 13 34 13 17Z', 3, 3) + G(m, 19, 14, 3, 10, .5)


def arrowobj(m, h='indigo'):
    return SH + P(m, h, 'M8 24H36V13L56 32L36 51V40H8Z', 3, 3) + G(m, 12, 27, 14, 3, .55)


def magnifier(m, h='amber'):
    f, d = fills(m, h)
    return (SH + S('D' if m == 'D' else 'E', 'ink', 'M42 42L54 54', 9, 2)
            + f'<circle cx="28" cy="29" r="17" fill="{d}" transform="translate(0,2)"/><circle cx="28" cy="28" r="17" fill="{f}"/>'
            + '<circle cx="28" cy="28" r="11" fill="#E4F3FF"/>' + G(m, 20, 20, 3, 9, .85))


def wrench(m, h='slate'):
    f, d = fills(m, h)
    return (SH + S(m, h, 'M16 50L38 28', 10, 3) + f'<circle cx="44" cy="20" r="13" fill="{d}" transform="translate(0,3)"/><circle cx="44" cy="20" r="13" fill="{f}"/>'
            + '<circle cx="48" cy="16" r="5.5" fill="#fff"/>' + G(m, 36, 13, 3, 9, .5))


def gear(m, h='slate'):
    f, d = fills(m, h)
    teeth = ''.join(f'<rect x="28.500" y="6" width="7" height="12" rx="2.500" fill="{{c}}" transform="rotate({k * 45} 32 31)"/>' for k in range(8))
    return (SH + f'<g transform="translate(0,3)">{teeth.replace("{c}", d)}<circle cx="32" cy="31" r="17" fill="{d}"/></g>'
            + teeth.replace('{c}', f) + f'<circle cx="32" cy="31" r="17" fill="{f}"/><circle cx="32" cy="31" r="7" fill="#fff"/>' + G(m, 22, 22, 3, 9, .55))


def target(m, h='red'):
    return (SH + C(m, h, 32, 31, 25, 3) + '<circle cx="32" cy="31" r="18" fill="#fff"/>' + f'<circle cx="32" cy="31" r="12" fill="{PAL[h][1]}"/>'
            + '<circle cx="32" cy="31" r="6.5" fill="#fff"/>' + f'<circle cx="32" cy="31" r="3" fill="{PAL["amber"][1]}"/>')


def nested(m, h='blue'):
    return SH + R(m, h, 6, 8, 52, 46, 11, 3) + '<rect x="14" y="16" width="36" height="30" rx="6" fill="#E4F3FF"/>' + R(m, 'indigo', 22, 24, 20, 14, 4, 2) + G(m, 10, 12, 3, 16, .5)


def chain(m, h='blue'):
    f, d = fills(m, h)
    a = 'fill="none" stroke-width="8" stroke-linecap="round"'
    link = lambda x, st: f'<rect x="{x}" y="22" width="26" height="15" rx="7.500" {a} stroke="{st}"/>'
    return (SH + f'<g transform="rotate(-35 32 31)"><g transform="translate(0,3)">{link(8, d)}{link(30, d)}</g>{link(8, f)}{link(30, f)}</g>')


def alarm(m, h='red'):
    f, d = fills(m, h)
    return (SH + C(m, 'amber', 15, 14, 7, 2) + C(m, 'amber', 49, 14, 7, 2) + R(m, 'slate', 13, 50, 6, 8, 2, 0)
            + C(m, h, 32, 34, 22, 3) + '<circle cx="32" cy="34" r="16" fill="#fff"/>' + K('M32 24V35L39 39', 'ink', 3.6) + dot(32, 34, 2, PAL['ink'][2]))


def ticket(m, h='violet'):
    return (SH + P(m, h, 'M8 16H56V26A6 6 0 0 0 56 38V48H8V38A6 6 0 0 0 8 26Z', 3, 3) + W('M43 21V43', 2.6, .9).replace('stroke-linecap="round"', 'stroke-linecap="round" stroke-dasharray="3 4"')
            + WR(16, 25, 18, 4, 2) + WR(16, 33, 12, 4, 2) + G(m, 12, 19, 22, 3, .45))


def play(m, h='blue'):
    return SH + C(m, h, 32, 31, 24, 3) + '<path d="M27 20L45 31L27 42Z" fill="#fff" stroke="#fff" stroke-width="4" stroke-linejoin="round"/>' + G(m, 15, 20, 3, 12, .5)


def folder(m, h='amber'):
    return (SH + P(m, h, 'M6 17A4 4 0 0 1 10 13H23L28 19H54A4 4 0 0 1 58 23V49A4 4 0 0 1 54 53H10A4 4 0 0 1 6 49Z', 3, 3)
            + f'<path d="M6 29H58V49A4 4 0 0 1 54 53H10A4 4 0 0 1 6 49Z" fill="#fff" opacity=".28"/>' + G(m, 10, 32, 28, 3, .5))


def folders(m, h='amber'):
    return (SH + P(m, h, 'M4 13A3 3 0 0 1 7 10H18L22 15H40A3 3 0 0 1 43 18V40A3 3 0 0 1 40 43H7A3 3 0 0 1 4 40Z', 3, 3)
            + P(m, 'orange', 'M26 30A3 3 0 0 1 29 27H38L41 31H57A3 3 0 0 1 60 34V52A3 3 0 0 1 57 55H29A3 3 0 0 1 26 52Z', 3, 3) + G(m, 30, 36, 20, 3, .5))


def window(m, h='indigo'):
    return (SH + R(m, h, 6, 9, 52, 44, 8, 3) + '<rect x="6" y="19" width="52" height="34" rx="0" fill="#fff"/>'
            + f'<path d="M6 19H58V45A8 8 0 0 1 50 53H14A8 8 0 0 1 6 45Z" fill="#fff"/>' + dot(14, 14, 2, '#fff', .9) + dot(21, 14, 2, '#fff', .9)
            + K('M25 29l-6 6 6 6M39 29l6 6-6 6M35 27l-6 16', h, 3.4))


def key(m, h='amber'):
    f, d = fills(m, h)
    return (SH + R(m, h, 28, 27, 28, 8, 4, 3) + R(m, h, 44, 34, 6, 9, 2, 2) + R(m, h, 52, 34, 5, 7, 2, 2)
            + f'<circle cx="20" cy="33" r="13" fill="{d}"/><circle cx="20" cy="31" r="13" fill="{f}"/><circle cx="20" cy="31" r="5" fill="#fff"/>' + G(m, 11, 24, 3, 8, .6))


def button(m, h='red'):
    f, d = fills(m, h)
    return (SH + f'<ellipse cx="32" cy="46" rx="25" ry="10" fill="{PAL["slate"][2]}"/><ellipse cx="32" cy="42" rx="25" ry="10" fill="{PAL["slate"][1]}"/>'
            + f'<ellipse cx="32" cy="36" rx="19" ry="14" fill="{d}"/><ellipse cx="32" cy="31" rx="19" ry="14" fill="{f}"/>' + G(m, 20, 23, 12, 3.5, .6))


def envelope(m, h='amber'):
    return (SH + R(m, h, 7, 14, 50, 36, 7, 3) + '<path d="M9 20A5 5 0 0 1 14 16H50A5 5 0 0 1 55 20L32 36Z" fill="#fff" opacity=".42"/>' + G(m, 11, 19, 3, 12, .45))


def layout(m, h=None):
    return (SH + R(m, 'teal', 6, 8, 52, 13, 5, 3) + R(m, 'blue', 6, 25, 24, 28, 5, 3) + R(m, 'indigo', 34, 25, 24, 12, 5, 3) + R(m, 'amber', 34, 41, 24, 12, 5, 3) + G(m, 10, 11, 18, 3, .5))


def puzzle(m, h='violet'):
    return SH + P(m, h, 'M10 18H22A6 6 0 1 1 34 18H46V30A6 6 0 1 0 46 42V54H34A6 6 0 1 0 22 54H10Z', 3, 2) + G(m, 14, 22, 3, 12, .5)


def dialog(m, h='indigo'):
    return (SH + R(m, 'slate', 5, 8, 38, 30, 6, 3) + R(m, h, 19, 21, 40, 32, 7, 3) + '<rect x="24" y="31" width="30" height="17" rx="3.5" fill="#fff"/>'
            + dot(26, 26.5, 1.8) + dot(32, 26.5, 1.8, '#fff', .8) + K('M29 38h20M29 43h12', 'glass', 2.6))


def plug(m, h='green'):
    return (SH + S(m, 'ink', 'M32 40V50C32 56 40 56 40 52', 5, 2) + R(m, 'slate', 24, 6, 5, 15, 2, 0) + R(m, 'slate', 35, 6, 5, 15, 2, 0)
            + R(m, h, 15, 18, 34, 24, 9, 3) + G(m, 20, 22, 4, 11, .55))


def pin(m, h='red'):
    return SH + P(m, h, 'M32 6A16 16 0 0 1 48 22C48 34 32 56 32 56S16 34 16 22A16 16 0 0 1 32 6Z', 3, 3) + dot(32, 22, 6.5) + G(m, 22, 14, 3, 10, .5)


def db(m, h='indigo'):
    f, d = fills(m, h)
    return (SH + f'<path d="M12 16V48C12 53 21 57 32 57S52 53 52 48V16Z" fill="{d}"/><path d="M12 14V44C12 49 21 53 32 53S52 49 52 44V14Z" fill="{f}"/>'
            + f'<ellipse cx="32" cy="14" rx="20" ry="8" fill="{PAL[h][0]}"/>' + W('M12 27C12 32 21 35 32 35S52 32 52 27M12 40C12 45 21 48 32 48S52 45 52 40', 2.6, .55) + G(m, 16, 22, 3, 22, .45))


def pencil(m, h='amber'):
    return (SH + '<g transform="rotate(40 32 32)">' + R(m, 'pink', 24, 3, 16, 8, 3, 2) + R(m, 'slate', 24, 11, 16, 6, 0, 0)
            + R(m, h, 24, 17, 16, 28, 2, 3) + f'<path d="M24 45H40L32 59Z" fill="#FFE2BD"/><path d="M29 54L32 59L35 54Z" fill="#3a4458"/>' + G(m, 27, 20, 3, 20, .5) + '</g>')


def warn(m, h='amber'):
    return SH + P(m, h, 'M32 9L57 52H7Z', 3, 6) + '<rect x="29.500" y="23" width="5" height="16" rx="2.500" fill="#fff"/>' + dot(32, 45, 3)


def copy(m, h='blue'):
    return (SH + R(m, h, 7, 14, 30, 40, 6, 3) + R(m, 'paper', 24, 8, 32, 44, 6, 3)
            + K('M30 20h20M30 28h20M30 36h12', h, 3.2) + G(m, 11, 18, 3, 14, .5))


def dropdown(m, h='blue'):
    return (SH + R(m, h, 7, 9, 50, 17, 7, 3) + W('M41 15l4 4 4-4', 3.2) + WR(13, 15, 16, 4, 2)
            + R(m, 'paper', 7, 31, 50, 10, 5, 2) + R(m, 'paper', 7, 44, 50, 10, 5, 2) + dot(14, 36, 2.2, PAL[h][1]) + dot(14, 49, 2.2, PAL['amber'][1]))


def masterdetail(m, h=None):
    return (SH + R(m, 'teal', 5, 9, 21, 44, 6, 3) + K('M10 18H21M10 26H21M10 34H21', 'teal', 2.8, .55).replace(PAL['teal'][2], '#fff')
            + R(m, 'blue', 30, 9, 29, 44, 6, 3) + WR(35, 16, 19, 4, 2) + WR(35, 24, 19, 4, 2, .75) + WR(35, 32, 12, 4, 2, .55))


def check(m, h='green'):
    return SH + C(m, h, 32, 31, 24, 3) + W('M21 31l8 8 15-17', 6.5) + G(m, 15, 20, 3, 13, .5)


def table(m, h='blue'):
    return (SH + R(m, 'paper', 6, 9, 52, 44, 8, 3) + f'<path d="M6 17A8 8 0 0 1 14 9H50A8 8 0 0 1 58 17V25H6Z" fill="{fills(m, h)[0]}"/>'
            + K('M6 25H58M24 25V53M41 25V53M6 36H58M6 46H58', 'glass', 1.8) + G(m, 12, 12, 16, 3, .5))


def funnel(m, h='teal'):
    return SH + P(m, h, 'M7 10H57L38 31V50L26 56V31Z', 3, 4) + G(m, 12, 13, 20, 3, .55)


def sortobj(m, h='violet'):
    return SH + R(m, 'violet', 8, 10, 48, 11, 5.5, 3) + R(m, 'indigo', 8, 26, 34, 11, 5.5, 3) + R(m, 'blue', 8, 42, 20, 11, 5.5, 3) + G(m, 12, 12, 18, 2.6, .55)


def wand(m, h='amber'):
    return (SH + S(m, 'ink', 'M13 54L37 30', 8, 3)
            + P(m, h, 'M46 5L50 15L60 19L50 23L46 33L42 23L32 19L42 15Z', 2, 3) + dot(20, 17, 3, PAL['pink'][1]) + dot(53, 40, 2.6, PAL['violet'][1]))


def pages(m, h='blue'):
    return (SH + R(m, 'blue', 19, 5, 33, 45, 5, 3) + R(m, 'indigo', 16, 9, 33, 45, 5, 3) + R(m, 'paper', 12, 13, 33, 44, 5, 3)
            + K('M19 25h19M19 33h19M19 41h11', 'blue', 3))


def calculator(m, h='blue'):
    out = SH + R(m, h, 11, 5, 42, 53, 8, 3) + '<rect x="16" y="11" width="32" height="13" rx="3.500" fill="#E4F3FF"/>'
    for r in range(3):
        for c in range(3):
            col = '#FFC12E' if c == 2 else '#fff'
            out += f'<rect x="{16 + c * 11}" y="{29 + r * 9.5}" width="9" height="7" rx="2.5" fill="{col}"/>'
    return out + K('M42 18h-6', 'blue', 2.6, .6)


def coin(m, h='amber'):
    return (SH + C(m, h, 32, 31, 24, 3) + f'<circle cx="32" cy="31" r="17" fill="none" stroke="{PAL[h][2]}" stroke-width="2.4" opacity=".55"/>'
            + K('M23 23l4 16 5-11 5 11 4-16M21 30h22M21 35h22', h, 3.2) + G(m, 15, 20, 3, 13, .55))


def steps(m, h='green'):
    return (SH + R(m, h, 6, 38, 17, 17, 5, 3) + R(m, 'teal', 24, 27, 17, 28, 5, 3) + R(m, 'blue', 42, 14, 17, 41, 5, 3) + G(m, 9, 41, 3, 8, .55))


def bulb(m, h='amber'):
    f, d = fills(m, h)
    return (SH + K('M32 3V7M12 10L15 13M52 10L49 13M5 28H9M59 28H55', h, 3) + f'<circle cx="32" cy="27" r="17" fill="{d}" transform="translate(0,2)"/><circle cx="32" cy="27" r="17" fill="{f}"/>'
            + R(m, 'slate', 24, 42, 16, 12, 4, 2) + G(m, 22, 17, 3.4, 11, .65))


def server(m, h='blue'):
    out = SH
    for i, y in enumerate((8, 26, 44)):
        out += R(m, h, 7, y, 50, 14, 6, 3) + dot(16, y + 7, 2.4, '#fff') + dot(23, y + 7, 2.4, PAL['green'][0] if i != 1 else PAL['amber'][0]) + WR(34, y + 5.5, 16, 3.2, 1.6, .8)
    return out


def book(m, h='indigo'):
    return (SH + R(m, h, 12, 6, 40, 50, 6, 3) + '<rect x="16" y="9" width="3" height="44" rx="1.5" fill="#fff" opacity=".35"/>' + WR(24, 17, 22, 4, 2) + WR(24, 25, 16, 4, 2, .75) + G(m, 22, 44, 22, 3, .0))


def note(m, h='amber'):
    return (SH + P(m, h, 'M9 9H55V43L43 55H9Z', 3, 3) + '<path d="M55 43L43 55V47a4 4 0 0 1 4-4Z" fill="#fff" opacity=".5"/>' + K('M17 21H47M17 29H47M17 37H34', h, 3, .55) + G(m, 12, 12, 16, 3, .5))


def rocket(m, h='red'):
    return (SH + P(m, 'red', 'M20 33L9 46L23 43Z', 2, 2) + P(m, 'red', 'M44 33L55 46L41 43Z', 2, 2) + P(m, 'amber', 'M25 44H39L32 60Z', 0, 2)
            + R(m, 'paper', 20, 6, 24, 42, 12, 3) + '<circle cx="32" cy="24" r="6" fill="#3D9BFF"/>' + G(m, 23, 14, 3, 20, .6)
            + f'<path d="M20 16C23 10 27 7 32 6C37 7 41 10 44 16Z" fill="{PAL["red"][1]}"/>')



def same(m, h='blue'):
    return (SH + R(m, h, 3, 14, 20, 32, 6, 3) + R(m, h, 41, 14, 20, 32, 6, 3) + WR(7.500, 22, 11, 3.4, 1.7, .85) + WR(45.500, 22, 11, 3.4, 1.7, .85) + WR(7.500, 30, 8, 3.4, 1.7, .6) + WR(45.500, 30, 8, 3.4, 1.7, .6)
            + C(m, 'pink', 32, 30, 11, 2) + WR(26, 25.500, 12, 3.4, 1.7, 1) + WR(26, 31.500, 12, 3.4, 1.7, 1))


def buzzer(m, h='violet'):
    return (SH + K('M9 26A26 26 0 0 1 15 15M55 26A26 26 0 0 0 49 15M4 34A30 30 0 0 1 8 22M60 34A30 30 0 0 0 56 22', h, 3, .75)
            + C(m, h, 32, 34, 20, 3) + '<circle cx="32" cy="34" r="12.500" fill="#fff" opacity=".92"/>' + C(m, 'green', 32, 34, 5, 1) + G(m, 17, 26, 3.4, 12, .55))


def bell(m, h='amber'):
    return (SH + C(m, 'orange', 32, 50, 5.5, 2) + P(m, h, 'M32 9C23 9 18 16 18 25V35L13 42H51L46 35V25C46 16 41 9 32 9Z', 3, 3)
            + R(m, 'orange', 29.500, 4, 5, 6, 2.500, 0) + G(m, 22, 18, 3.4, 14, .6))


def conveyor(m, h='ink'):
    return (SH + R(m, 'blue', 11, 18, 13, 13, 3.5, 3) + R(m, 'pink', 28, 18, 13, 13, 3.5, 3) + R(m, 'green', 45, 18, 13, 13, 3.5, 3)
            + R(m, 'ink', 4, 37, 56, 13, 6.5, 3) + ''.join(dot(x, 43.5, 2.2, '#fff', .55) for x in (14, 24, 34, 44, 54)) + dot(10, 43.500, 3.4, '#8793a8') + dot(54, 43.500, 3.4, '#8793a8'))


def stamp(m, h='indigo'):
    return (SH + R(m, 'red', 22, 4, 20, 20, 10, 3) + R(m, 'slate', 28, 20, 8, 14, 2, 0) + R(m, h, 12, 32, 40, 11, 5, 3)
            + '<rect x="10" y="50" width="44" height="5" rx="2.500" fill="#1f68d6" opacity=".25"/>' + G(m, 26, 8, 3, 8, .6))


def stopwatch(m, h='blue'):
    return (SH + R(m, 'slate', 26, 4, 12, 8, 2.500, 0) + R(m, 'slate', 44, 11, 7, 5, 2, 0).replace('<rect', '<rect transform="rotate(40 47 13)"', 2)
            + C(m, h, 32, 36, 21, 3) + '<circle cx="32" cy="36" r="15.500" fill="#fff"/>' + K('M32 36V24M32 36L40 41', 'ink', 3.4)
            + dot(32, 36, 2.200, PAL['ink'][2]) + G(m, 15, 28, 3, 12, .55))


def house(m, h='amber'):
    return (SH + R(m, h, 12, 28, 40, 26, 4, 3) + P(m, 'red', 'M7 30L32 9L57 30Z', 3, 4) + R(m, 'teal', 27, 38, 10, 16, 2, 0)
            + R(m, 'glass', 16, 35, 8, 8, 2, 0) + R(m, 'glass', 40, 35, 8, 8, 2, 0))


def palette(m, h='orange'):
    return (SH + P(m, h, 'M32 6C17 6 6 16 6 30C6 42 15 52 26 52C31 52 32 49 30 46C28 43 30 40 34 40H42C50 40 58 35 58 28C58 16 47 6 32 6Z', 3, 3)
            + dot(18, 28, 4.500, PAL['red'][1]) + dot(26, 16, 4.500, PAL['amber'][1]) + dot(40, 15, 4.500, PAL['blue'][1]) + dot(49, 27, 4.500, PAL['green'][1]) + G(m, 14, 16, 3, 8, .5))


def cabinet(m, h='teal'):
    out = SH + R(m, h, 9, 5, 46, 52, 7, 3)
    for y in (10, 25, 40):
        out += f'<rect x="14" y="{y}" width="36" height="12" rx="3.500" fill="#fff" opacity=".92"/>' + K(f'M27 {y + 6}H37', h, 3.2, .8)
    return out


def traffic(m, h='ink'):
    return (SH + R(m, 'ink', 17, 4, 30, 53, 11, 3) + dot(32, 16, 6.500, PAL['red'][1]) + dot(32, 30.500, 6.500, PAL['amber'][1]) + dot(32, 45, 6.500, PAL['green'][1])
            + dot(30, 14, 1.800, '#fff', .7) + dot(30, 28.5, 1.800, '#fff', .7) + dot(30, 43, 1.800, '#fff', .7))


def keyboard(m, h='slate'):
    keys = ''
    for i in range(4):
        keys += WR(14 + i * 9.5, 24, 7, 6, 1.8)
    for i in range(4):
        keys += WR(14 + i * 9.5, 33, 7, 6, 1.8)
    keys += WR(40.5, 24, 9.5, 6, 1.8, .55) + WR(40.5, 33, 9.5, 6, 1.8, .55)
    return (SH + R(m, h, 6, 16, 52, 34, 7, 3) + keys + WR(19, 42, 26, 4.6, 2.3) + G(m, 10, 19, 3, 22, .45))


def erd(m, h='teal'):
    f, d = fills(m, h)
    def card(x, y, w, hh, c):
        cf = fills(m, c)[0]
        return (R(m, 'paper', x, y, w, hh, 5, 3)
                + f'<path d="M{x} {y + 5}a5 5 0 0 1 5-5H{x + w - 5}a5 5 0 0 1 5 5V{y + 8}H{x}Z" fill="{cf}"/>'
                + K(f'M{x + 5} {y + 13.5}H{x + w - 7}M{x + 5} {y + 19}H{x + w - 11}', 'glass', 2.2))
    return (S(m, 'slate', 'M30 17H41a6 6 0 0 1 6 6V33', 3.6, 2)
            + K('M42 33l5 -5 5 5M42 35.5H52', 'slate', 2.4)
            + card(4, 6, 28, 24, h) + card(32, 36, 28, 20, 'indigo') + G(m, 8, 9, 12, 2.4, .5))


def trash(m, h='red'):
    return (SH + R(m, h, 24, 5, 16, 8, 3, 0) + '<rect x="28" y="8.5" width="8" height="3" rx="1.5" fill="#fff" opacity=".9"/>'
            + P(m, h, 'M15 21H49L46 53a4 4 0 0 1-4 4H22a4 4 0 0 1-4-4Z', 3, 3)
            + R(m, 'slate', 9, 13, 46, 8, 4, 2) + W('M26 29V48M38 29V48', 4, .9) + G(m, 21, 25, 3, 18, .45))

def sparkle(m, h='amber'):
    star = lambda cx, cy, r: f'M{cx} {cy - r}Q{cx + r * .18} {cy - r * .18} {cx + r} {cy}Q{cx + r * .18} {cy + r * .18} {cx} {cy + r}Q{cx - r * .18} {cy + r * .18} {cx - r} {cy}Q{cx - r * .18} {cy - r * .18} {cx} {cy - r}Z'
    return SH + P(m, h, star(27, 32, 21), 3, 2) + P(m, 'violet', star(49, 15, 9), 2, 2) + P(m, 'teal', star(50, 46, 6), 2, 2) + G(m, 22, 22, 3, 9, .55)

OBJ = {k: v for k, v in dict(
    tag=tag, box=box, sign=sign, vend=vend, hourglass=hourglass, bug=bug, laptop=laptop, console=console, toolbox=toolbox, blocks=blocks,
    bubble=bubble, scale=scale, equals=equals, swap=swap, array=array, layers=layers, doc=doc, no=no, qblock=qblock, loop=loop,
    clipboard=clipboard, door=door, phone=phone, arrow=arrowobj, magnifier=magnifier, wrench=wrench, gear=gear, target=target,
    nested=nested, chain=chain, alarm=alarm, ticket=ticket, play=play, folder=folder, folders=folders, window=window, key=key,
    button=button, envelope=envelope, layout=layout, puzzle=puzzle, dialog=dialog, plug=plug, pin=pin, db=db, pencil=pencil,
    warn=warn, copy=copy, dropdown=dropdown, masterdetail=masterdetail, check=check, table=table, funnel=funnel, sort=sortobj,
    wand=wand, pages=pages, same=same, buzzer=buzzer, bell=bell, conveyor=conveyor, stamp=stamp, stopwatch=stopwatch, house=house, palette=palette, cabinet=cabinet, traffic=traffic, calculator=calculator, coin=coin, steps=steps, bulb=bulb, server=server, book=book, note=note, rocket=rocket, keyboard=keyboard, erd=erd, trash=trash, sparkle=sparkle,
).items()}


def symbol(obj, hue, mode):
    fn = OBJ[obj]
    body = fn(mode, hue) if hue else fn(mode)
    return f'<symbol id="t-{obj}-{hue or "x"}-{mode}" viewBox="0 0 64 64">{body}</symbol>'


def defs_svg(used):
    syms = ''.join(symbol(o, h, m) for o, h, m in sorted(used, key=lambda t: (t[0], t[1] or '', t[2])))
    return f'<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>{defs()}{syms}</defs></svg>'


def use(obj, hue, mode, cls=''):
    return (f'<svg class="ti {cls}".strip() viewBox="0 0 64 64" aria-hidden="true" focusable="false"><use href="#t-{obj}-{hue or "x"}-{mode}"/></svg>'
            .replace('.strip()', ''))
