"""Figures added in the back-end review: static SVGs and scroll-driven SVG steppers."""
import html
from dbdiagrams import svg, rect, table
from diagrams import _box, _t
from demos2 import PLAY, PAUSE


def S(steps, body):
    """Body visible only on the given steps."""
    return f"<g class='st-item' data-steps='{','.join(str(x) for x in steps)}'>{body}</g>"


def arrow(d, cls="d-line", p="x", m="a"):
    return f"<path d='{d}' class='{cls}' marker-end='url(#{p}-{m})'/>"


def stepper(caption, svg_body, notes, cls=""):
    n = len(notes)
    nt = "".join(f'<div class="st-note st-item" data-steps="{i}"><b><i>{i + 1}</i>{html.escape(t)}</b> <span>{html.escape(d)}</span></div>'
                 for i, (t, d) in enumerate(notes))
    dots = "".join(f'<i class="st-dot" data-steps="{",".join(str(k) for k in range(i, n))}"></i>' for i in range(n))
    return (f'<figure class="diagram demo stepper svgst {cls}" data-step="0" data-max="{n - 1}">'
            f'<figcaption>{html.escape(caption)}</figcaption><div class="diagram-scroll">{svg_body}</div>'
            f'<div class="st-notes" aria-live="polite">{nt}</div>'
            '<div class="st-foot"><div class="st-btns">'
            f'<button type="button" class="dm-btn st-run">{PLAY}실행</button>'
            f'<button type="button" class="dm-btn st-pause">{PAUSE}<span class="t-pause">정지</span><span class="t-resume">이어서</span></button>'
            f'</div><div class="st-dots" aria-hidden="true">{dots}</div></div></figure>')


# ------------------------------------------------------------------ Client (static)
def client():
    b = [_t(24, 28, "DB 안에 실제로 들어 있는 ZCLASS", "d-ink", 13, 700)]
    b.append(table(24, 40, ["MANDT", "CID", "CNAME"],
                   [["100", "CL301", "ABAP반"], ["100", "CL303", "UI5반"], ["200", "CL301", "시험용 반"], ["200", "CL900", "점검 반"]],
                   [74, 90, 110], rh=30, hl_rows=(0, 1)))
    b.append(_t(24, 212, "MANDT가 100인 줄과 200인 줄이 한 테이블에 같이 있어요", "d-quiet", 12))
    b.append(rect(330, 92, 110, 40, "d-hl2", 20))
    b.append(_t(385, 117, "Client 100 로그인", "d-amber", 11.5, 700, "middle"))
    b.append(arrow("M312 112H326", "d-line-amber", "cl", "c"))
    b.append(arrow("M442 112H478", "d-line-amber", "cl", "c"))
    b.append(_t(484, 28, "SE16에서 보이는 ZCLASS", "d-ink", 13, 700))
    b.append(table(484, 40, ["MANDT", "CID", "CNAME"], [["100", "CL301", "ABAP반"], ["100", "CL303", "UI5반"]], [66, 80, 104], rh=30, hl_rows=(0, 1)))
    b.append(_t(484, 152, "MANDT가 100인 레코드만 나와요", "d-quiet", 12))
    b.append(_t(484, 172, "200번 Client로 로그인하면 아래 두 줄만 보여요", "d-quiet", 12))
    b.append(rect(24, 40 + 30 * 3, 274, 60, "d-zone-b", 0))
    return svg("cl", 232, "같은 테이블 안의 레코드가 MANDT 값으로 나뉘고, 로그인한 Client의 레코드만 보여요", "".join(b))


# ------------------------------------------------------------------ Transport (stepper)
def transport():
    sysx = [(40, "DEV", "개발"), (290, "QAS", "테스트"), (540, "PRD", "운영")]
    b = []
    for x, k, ko in sysx:
        b.append(_box(x, 40, 180, 150))
        b.append(_t(x + 16, 66, k, "d-ink d-mono", 14, 700))
        b.append(_t(x + 60, 66, f"{ko} 시스템", "d-quiet", 12))
    b.append(arrow("M224 115H286", "d-line", "tp"))
    b.append(arrow("M474 115H536", "d-line", "tp"))

    def parcel(x, y, hl=True):
        return (rect(x, y, 148, 76, "d-hl" if hl else "d-cell", 8)
                + _t(x + 10, y + 20, "Transport Request", "d-accent", 11.5, 700)
                + _t(x + 10, y + 38, "DEVK900123", "d-ink d-mono", 11.5)
                + _t(x + 10, y + 56, "ZCID · ZCLASS", "d-ink d-mono", 11.5)
                + _t(x + 10, y + 70, "", "d-quiet", 10))
    for i, (x, _, _) in enumerate(sysx):
        b.append(S([i], parcel(x + 16, 92)))
    # objects that arrived earlier stay as "도착" labels
    b.append(S([1, 2], _t(56, 182, "원본은 여기 남아요", "d-quiet", 11.5)))
    b.append(S([2], _t(306, 182, "확인 끝", "d-quiet", 11.5)))
    b.append(S([1], arrow("M224 115H286", "d-line-accent", "tp", "b")))
    b.append(S([2], arrow("M474 115H536", "d-line-accent", "tp", "b")))
    # $TMP
    tmp = (rect(56, 214, 148, 52, "d-hl2", 8) + _t(66, 234, "$TMP (Local Object)", "d-amber", 11.5, 700)
           + _t(66, 254, "ZTEST_TABLE", "d-ink d-mono", 11.5)
           + "<path d='M214 240H300' class='d-line-amber' stroke-dasharray='5 4'/>"
           + "<path d='M306 230l16 20M322 230l-16 20' class='d-line-amber'/>"
           + _t(334, 245, "Transport Request가 없어서 다른 시스템으로 못 가요", "d-amber", 12, 700))
    b.append(S([3], tmp))
    return stepper("Transport 이동 · 개발에서 운영까지",
                   svg("tp", 286, "Transport Request가 개발에서 테스트, 운영 시스템으로 객체를 옮겨요", "".join(b)), [
                       ("개발(DEV)에서 만들고 저장해요", "Package를 정해 저장하면 바꾼 객체(ZCID, ZCLASS)가 Transport Request 하나에 담겨요. 택배 상자에 물건을 넣는 단계예요."),
                       ("요청을 풀어서 테스트(QAS)로 보내요", "요청을 Release(내보내기)하면 같은 객체가 테스트 시스템에 들어가요. 개발 시스템의 원본은 그대로 남아요."),
                       ("확인이 끝나면 운영(PRD)으로 보내요", "테스트에서 문제가 없으면 같은 요청을 운영 시스템에 넣어요. 실제 업무는 운영 시스템에서 해요."),
                       ("$TMP로 저장한 객체는 떠나지 못해요", "Local Object($TMP)는 요청 번호가 없어서 개발 시스템에만 머물러요. 혼자 연습할 때만 써요."),
                   ])


# ------------------------------------------------------------------ Save vs activate (stepper)
def activate():
    b = []
    b.append(_t(40, 30, "Domain ZCNAME (반 이름)", "d-ink d-mono", 13, 700))
    b.append(_box(40, 44, 300, 120))
    b.append(_t(56, 68, "저장한 버전 (Inactive)", "d-amber", 12.5, 700))
    b.append(_box(420, 44, 300, 120, True))
    b.append(_t(436, 68, "실제로 쓰는 버전 (Active)", "d-accent", 12.5, 700))
    b.append(S([0, 2, 3], _t(56, 112, "고친 내용이 없어요", "d-quiet", 12)))
    b.append(S([1], rect(56, 86, 268, 56, "d-hl2", 8) + _t(70, 110, "CHAR, 길이 40", "d-ink d-mono", 13, 650)
               + _t(70, 130, "Ctrl+S로 저장만 했어요", "d-quiet", 11.5)))
    b.append(S([0, 1], rect(436, 86, 268, 56, "d-cell", 8) + _t(450, 110, "CHAR, 길이 20", "d-ink d-mono", 13, 650)
               + _t(450, 130, "예전 버전 그대로예요", "d-quiet", 11.5)))
    b.append(S([2, 3], rect(436, 86, 268, 56, "d-hl", 8) + _t(450, 110, "CHAR, 길이 40", "d-ink d-mono", 13, 650)
               + _t(450, 130, "Ctrl+F3으로 확정했어요", "d-quiet", 11.5)))
    b.append(S([2], arrow("M344 114H414", "d-line-accent", "ac", "b") + _t(379, 104, "활성화", "d-accent", 11.5, 700, "middle")))
    # users
    users = [("Data Element ZCNAME", 250), ("테이블 ZCLASS", 420), ("ABAP 프로그램", 590)]
    for nm, x in users:
        b.append(rect(x - 75, 214, 150, 34, "d-cell", 17))
        b.append(_t(x, 236, nm, "d-ink", 12, 600, "middle"))
        b.append(arrow(f"M{x} 210L{min(max(x, 470), 670)} 170", "d-line", "ac"))
    b.append(S([1], _t(380, 278, "다른 객체들은 아직 길이 20을 보고 있어요", "d-amber", 12, 700, "middle")))
    b.append(S([3], _t(380, 278, "이제 모두 길이 40을 써요. 고쳤는데 그대로라면 활성화를 빠뜨린 거예요", "d-accent", 12, 700, "middle")))
    return stepper("저장과 활성화 · 두 가지 버전",
                   svg("ac", 292, "저장하면 Inactive 버전만 바뀌고, 활성화해야 다른 객체가 쓰는 Active 버전이 바뀌어요", "".join(b)), [
                       ("처음 상태", "Domain ZCNAME은 길이 20으로 활성화돼 있어요. Data Element, 테이블, 프로그램이 모두 이 Active 버전을 가져다 써요."),
                       ("길이를 40으로 고치고 저장만 해요", "저장(Ctrl+S)하면 Inactive 버전에만 들어가요. 다른 객체는 여전히 길이 20을 봐요."),
                       ("활성화해요", "활성화(Ctrl+F3)하면 Inactive 버전이 Active 버전이 되고, 저장한 버전 칸은 비어요."),
                       ("이제 모두 새 버전을 써요", "Domain을 쓰는 Data Element와 테이블, 프로그램이 길이 40을 보게 돼요. 그래서 Domain → Data Element → 테이블 순서로 하나씩 활성화해요."),
                   ])


# ------------------------------------------------------------------ Reference fields (static)
def reffield():
    b = [_t(24, 26, "SFLIGHT · 금액", "d-ink d-mono", 13, 700)]
    b.append(table(24, 38, ["CARRID", "PRICE", "CURRENCY"], [["LH", "666.00", "EUR"], ["AA", "422.94", "USD"], ["KE", "370000", "KRW"]],
                   [80, 100, 100], rh=30, hl_col=1))
    b.append(rect(204, 38, 100, 120, "d-hl", 0))
    for c, v in enumerate(["CURRENCY", "EUR", "USD", "KRW"]):
        b.append(_t(254, 38 + 30 * c + 19.5, v, "d-ink d-mono", 11.5, 650 if c == 0 else None, "middle"))
    b.append("<path d='M154 172C154 198 254 198 254 172' class='d-line-accent' marker-end='url(#rf-b)'/>")
    b.append(_t(204, 214, "PRICE(CURR) → Ref. field CURRENCY(CUKY)", "d-accent", 12, 700, "middle"))
    b.append(_t(420, 26, "SPFLI · 수량", "d-ink d-mono", 13, 700))
    b.append(table(420, 38, ["CONNID", "DISTANCE", "DISTID"], [["0400", "6162", "KM"], ["0017", "2572", "MI"]],
                   [90, 110, 100], rh=30, hl_col=1))
    b.append(rect(620, 38, 100, 90, "d-hl", 0))
    for c, v in enumerate(["DISTID", "KM", "MI"]):
        b.append(_t(670, 38 + 30 * c + 19.5, v, "d-ink d-mono", 11.5, 650 if c == 0 else None, "middle"))
    b.append("<path d='M565 142C565 168 670 168 670 142' class='d-line-accent' marker-end='url(#rf-b)'/>")
    b.append(_t(618, 184, "DISTANCE(QUAN) → Ref. field DISTID(UNIT)", "d-accent", 12, 700, "middle"))
    b.append(_t(380, 250, "숫자만 보면 666인지 370000인지 크기를 비교할 수 없어요. 옆의 단위 필드를 같이 봐야 뜻이 정해져요", "d-quiet", 12, None, "middle"))
    return svg("rf", 266, "금액 필드는 통화 필드를, 수량 필드는 단위 필드를 참조 필드로 연결해요", "".join(b))


# ------------------------------------------------------------------ Structure family (static)
def ddic_objs():
    b = []
    W, G = 170, 16
    xs = [24 + i * (W + G) for i in range(4)]
    titles = [("Structure", "모양만 정해요"), ("Table Type", "그 모양의 목록"), ("Include", "공통 필드 끼워 넣기"), ("Append Structure", "표준 테이블에 덧붙이기")]
    for x, (t, sub) in zip(xs, titles):
        b.append(_t(x, 26, t, "d-ink", 13, 700))
        b.append(_t(x, 44, sub, "d-quiet", 11.5))

    def row(x, y, fields, cls="d-cell", w=W, h=26):
        cw = w / len(fields)
        o = []
        for i, f in enumerate(fields):
            o.append(rect(x + i * cw, y, cw, h, cls))
            o.append(_t(x + i * cw + cw / 2, y + h / 2 + 4, f, "d-ink d-mono", 10.5, None, "middle"))
        return "".join(o)
    x = xs[0]
    b.append(row(x, 60, ["SID", "SNAME", "CID"], "d-head"))
    b.append(f"<rect x='{x}' y='92' width='{W}' height='26' rx='4' class='d-cell' stroke-dasharray='4 3'/>")
    b.append(_t(x + W / 2, 109, "데이터 칸 없음", "d-quiet", 11, None, "middle"))
    b.append(_t(x, 146, "DB에 저장 안 돼요", "d-amber", 11.5, 700))
    b.append(_t(x, 164, "ABAP 변수 1건의 타입", "d-quiet", 11.5))
    x = xs[1]
    b.append(row(x, 60, ["SID", "SNAME", "CID"], "d-head"))
    for k in range(3):
        b.append(f"<rect x='{x}' y='{92 + k * 28}' width='{W}' height='24' rx='4' class='d-cell' stroke-dasharray='4 3'/>")
        b.append(_t(x + W / 2, 108 + k * 28, f"{k + 1}건째 자리", "d-quiet", 11, None, "middle"))
    b.append(_t(x, 196, "DB에 저장 안 돼요", "d-amber", 11.5, 700))
    b.append(_t(x, 214, "Internal Table의 타입", "d-quiet", 11.5))
    x = xs[2]
    b.append(_t(x, 70, "ZSTUDENT", "d-ink d-mono", 11.5, 700))
    b.append(row(x, 78, ["MANDT", "SID", "SNAME"], "d-head"))
    b.append(rect(x, 108, W, 54, "d-hl", 6))
    b.append(_t(x + 8, 126, ".INCLUDE ZS_AUDIT", "d-accent d-mono", 11, 700))
    b.append(_t(x + 8, 146, "ERNAM · ERDAT", "d-ink d-mono", 11))
    b.append(_t(x, 186, "여러 테이블에 같은 묶음", "d-quiet", 11.5))
    b.append(_t(x, 204, "(만든 사람, 만든 날짜)", "d-quiet", 11.5))
    x = xs[3]
    b.append(_t(x, 70, "MARA (SAP 표준)", "d-ink d-mono", 11.5, 700))
    b.append(row(x, 78, ["MANDT", "MATNR", "…"], "d-head"))
    b.append(rect(x, 108, W, 54, "d-hl2", 6))
    b.append(_t(x + 8, 126, "Append ZAMARA", "d-amber d-mono", 11, 700))
    b.append(_t(x + 8, 146, "ZZCOLOR · ZZSIZE", "d-ink d-mono", 11))
    b.append(_t(x, 186, "표준은 직접 못 고쳐서", "d-quiet", 11.5))
    b.append(_t(x, 204, "뒤에 내 필드를 붙여요", "d-quiet", 11.5))
    b.append("<path d='M%d 248H%d' class='d-line'/>" % (24, 24 + 2 * W + G))
    b.append(_t(24 + W + G / 2, 268, "타입만 정의 (저장 X)", "d-quiet", 12, 700, "middle"))
    b.append("<path d='M%d 248H%d' class='d-line'/>" % (xs[2], xs[3] + W))
    b.append(_t(xs[2] + W + G / 2, 268, "테이블에 필드를 더해요 (그 테이블에 저장)", "d-quiet", 12, 700, "middle"))
    return svg("dd", 284, "Structure와 Table Type은 모양만 정하고, Include와 Append는 테이블에 필드를 더해요", "".join(b))


# ------------------------------------------------------------------ ZCOUNTRY (static)
def zcountry():
    b = []
    b.append(_box(24, 24, 180, 50))
    b.append(_t(40, 46, "Domain LAND1", "d-ink d-mono", 12.5, 700))
    b.append(_t(40, 64, "Value Table: T005", "d-quiet", 11.5))

    def tbl(x, y, name, sub, vals, hl=False, w=170):
        o = [_t(x, y - 10, name, "d-ink d-mono", 12.5, 700), _t(x + w, y - 10, sub, "d-quiet", 11, None, "end")]
        o.append(table(x, y, ["LAND1"], [[v] for v in vals], [w], rh=26, hl_rows=tuple(range(len(vals))) if hl else ()))
        return "".join(o)
    b.append(tbl(24, 128, "T005", "전 세계", ["KR", "US", "JP", "DE", "…"]))
    b.append(tbl(294, 128, "ZCOUNTRY", "운영 국가만", ["KR", "US", "JP"], True))
    b.append(_t(564, 118, "강사 테이블", "d-ink", 12.5, 700))
    b.append(table(564, 128, ["TID", "NATIO"], [["T01", "KR"], ["T02", "US"], ["T03", "DE"]], [70, 100], rh=26, hl2_cells=((2, 1),)))
    b.append("<path d='M114 76V114' class='d-line-amber' stroke-dasharray='5 4' marker-end='url(#zc-c)'/>")
    b.append(_t(124, 100, "제안만 해요", "d-amber", 11.5, 700))
    b.append(arrow("M560 168H470", "d-line-accent", "zc", "b"))
    b.append(_t(515, 160, "검사", "d-accent", 11.5, 700, "middle"))
    b.append(_t(515, 184, "Check Table", "d-quiet", 10.5, None, "middle"))
    b.append(arrow("M290 168H200", "d-line-accent", "zc", "b"))
    b.append(_t(245, 160, "검사", "d-accent", 11.5, 700, "middle"))
    b.append(_t(245, 184, "Check Table", "d-quiet", 10.5, None, "middle"))
    b.append(_t(649, 250, "DE는 ZCOUNTRY에 없어서 오류", "d-amber", 11.5, 700, "middle"))
    b.append(_t(380, 318, "강사-NATIO는 직접 고른 ZCOUNTRY로 검사하고, ZCOUNTRY-LAND1은 다시 T005로 검사해요", "d-quiet", 12, None, "middle"))
    return svg("zc", 334, "Domain은 T005를 제안하지만 강사 NATIO의 Check Table은 직접 고른 ZCOUNTRY예요", "".join(b))


# ------------------------------------------------------------------ Text table (stepper)
def texttable():
    b = []
    b.append(_t(24, 26, "T005 (코드)", "d-ink d-mono", 12.5, 700))
    b.append(table(24, 36, ["LAND1"], [["KR"], ["US"]], [110], rh=28, hl_col=0))
    b.append(_t(214, 26, "T005T (Text Table)", "d-ink d-mono", 12.5, 700))
    rows = [["3", "KR", "대한민국"], ["E", "KR", "South Korea"], ["3", "US", "미국"], ["E", "US", "United States"]]
    W = [70, 70, 140]
    b.append(S([0], table(214, 36, ["SPRAS", "LAND1", "LANDX"], rows, W, rh=28)))
    b.append(S([1], table(214, 36, ["SPRAS", "LAND1", "LANDX"], rows, W, rh=28, hl_rows=(0, 2))))
    b.append(S([2], table(214, 36, ["SPRAS", "LAND1", "LANDX"], rows, W, rh=28, hl_rows=(1, 3))))
    b.append(arrow("M136 80C170 80 176 94 210 94", "d-line", "tt"))
    b.append(S([0], _t(214, 194, "키: MANDT + SPRAS + LAND1 · 언어마다 1건씩", "d-quiet", 12)))
    # login badge + F4 popup
    for st, lang, items in [(1, "한국어(KO)로 로그인", ["KR  대한민국", "US  미국"]), (2, "영어(EN)로 로그인", ["KR  South Korea", "US  United States"])]:
        body = rect(540, 30, 196, 34, "d-hl2", 17) + _t(638, 52, lang, "d-amber", 12, 700, "middle")
        body += _box(540, 86, 196, 104, True) + _t(556, 108, "F4 목록", "d-accent", 12, 700)
        for k, it in enumerate(items):
            body += rect(552, 120 + k * 30, 172, 26, "d-cell", 5) + _t(562, 137 + k * 30, it, "d-ink d-mono", 11.5)
        body += arrow("M500 120H534", "d-line-accent", "tt", "b")
        b.append(S([st], body))
    return stepper("로그인 언어와 Text Table · 언어별 이름",
                   svg("tt", 210, "로그인 언어에 맞는 T005T 레코드를 골라 F4 목록에 이름을 보여 줘요", "".join(b)), [
                       ("코드와 이름을 나눠 담아요", "T005에는 나라 코드만, T005T에는 언어별 이름이 들어 있어요. 같은 KR이 한국어 1건, 영어 1건으로 두 번 나와요."),
                       ("한국어로 로그인하면", "SPRAS가 3(한국어)인 줄만 골라서, F4 목록에 \"KR 대한민국\"처럼 보여 줘요."),
                       ("영어로 로그인하면", "같은 화면인데 SPRAS가 E인 줄을 골라서 \"KR South Korea\"로 보여 줘요. 코드는 그대로이고 이름만 바뀌어요."),
                   ])


# ------------------------------------------------------------------ F4 priority (static)
def f4order():
    steps = [("필드에 직접 붙인 Search Help", "Explicit search help attachment"),
             ("Check Table (과 그 Search Help)", "Input help implemented with check table"),
             ("Data Element의 Search Help", "Input help with search help of data element"),
             ("Domain의 Fixed Value", "Input help with fixed values"),
             ("데이터 타입 기본 도움 (달력, 시계)", "Input help based on data type")]
    b = [_t(24, 24, "F4를 누르면 위에서부터 차례로 찾아서, 처음 찾은 것을 보여 줘요", "d-ink", 13, 700)]
    for i, (k, en) in enumerate(steps):
        y = 40 + i * 46
        hl = i == 1
        b.append(rect(24 + i * 18, y, 440, 38, "d-hl" if hl else "d-cell", 8))
        b.append(_t(44 + i * 18, y + 24, f"{i + 1}", "d-accent d-mono" if hl else "d-quiet d-mono", 13, 700))
        b.append(_t(66 + i * 18, y + 17, k, "d-ink", 12.5, 650))
        b.append(_t(66 + i * 18, y + 32, en, "d-quiet", 10.5))
    # example
    b.append(_t(560, 60, "예: ZSTUDENT-CID", "d-ink d-mono", 12.5, 700))
    b.append(_t(560, 84, "① 붙인 Search Help 없음", "d-quiet", 12))
    b.append(_t(560, 106, "② Check Table ZCLASS 있음", "d-accent", 12, 700))
    b.append(_t(560, 128, "→ 여기서 멈추고", "d-accent", 12, 700))
    b.append(_t(560, 148, "ZCLASS의 반 목록이 떠요", "d-accent", 12, 700))
    b.append(arrow("M554 102H522", "d-line-accent", "f4", "b"))
    return svg("f4", 276, "F4 목록은 필드 Search Help, Check Table, Data Element Search Help, Fixed Value, 데이터 타입 순서로 찾아요", "".join(b))


# ------------------------------------------------------------------ Key inheritance (static)
def keyinherit():
    C = {"CARRID": ("d-hl2", "d-amber"), "CONNID": ("d-hl", "d-accent"), "FLDATE": ("d-cell", "d-ink")}
    rows = [("SCARR", "항공사", ["CARRID"]), ("SPFLI", "운항 노선", ["CARRID", "CONNID"]), ("SFLIGHT", "날짜별 운항편", ["CARRID", "CONNID", "FLDATE"])]
    b = []
    BW, X0 = 112, 170
    for i, (t, ko, ks) in enumerate(rows):
        y = 30 + i * 84
        b.append(_t(24, y + 20, t, "d-ink d-mono", 13, 700))
        b.append(_t(24, y + 38, ko, "d-quiet", 11.5))
        for j, k in enumerate(ks):
            fill, tc = C[k]
            new = j == len(ks) - 1
            b.append(rect(X0 + j * BW, y, BW - 8, 40, fill, 8))
            b.append(_t(X0 + j * BW + (BW - 8) / 2, y + 25, k, "d-ink d-mono", 12, 700 if new else None, "middle"))
        if i:
            for j in range(len(ks) - 1):
                cx = X0 + j * BW + (BW - 8) / 2
                b.append(f"<path d='M{cx} {y - 42}V{y - 4}' class='d-line' stroke-dasharray='4 3' marker-end='url(#ki-a)'/>")
            b.append(_t(X0 + (len(ks) - 1) * BW + BW - 2, y + 25, "← 새 키", "d-quiet", 11.5))
    # right: relation labels
    b.append(_box(586, 30, 166, 208))
    b.append(_t(600, 54, "읽는 법", "d-ink", 12.5, 700))
    tx = ["위 테이블의 키 전체가", "아래 테이블 키의 앞부분에", "그대로 있으면 부모와 자식", "", "SCARR 1 : CN SPFLI", "SPFLI 1 : CN SFLIGHT", "둘 다 식별 관계 (실선)"]
    for k, t in enumerate(tx):
        b.append(_t(600, 78 + k * 21, t, "d-accent d-mono" if k >= 4 else "d-quiet", 11.5, 650 if k >= 4 else None))
    b.append(_t(24, 280, "MANDT는 모든 테이블 맨 앞에 붙어서 빼고 그렸어요. 아래로 내려갈수록 키가 하나씩 늘어나요", "d-quiet", 12))
    return svg("ki", 294, "SCARR의 키가 SPFLI로, SPFLI의 키가 SFLIGHT로 그대로 내려가고 키가 하나씩 늘어나요", "".join(b))


# ------------------------------------------------------------------ JOIN (stepper)
def joins():
    st = [["0001", "민수", "CL301"], ["0002", "지아", "CL303"], ["0007", "가온", ""]]
    cl = [["CL301", "ABAP반"], ["CL303", "UI5반"]]
    b = []
    b.append(_t(24, 26, "ZSTUDENT (왼쪽, FROM 쪽)", "d-ink d-mono", 12.5, 700))
    b.append(table(24, 36, ["SID", "SNAME", "CID"], st, [64, 64, 80], rh=28, hl_col=None))
    b.append(_t(330, 26, "ZCLASS (오른쪽)", "d-ink d-mono", 12.5, 700))
    b.append(table(330, 36, ["CID", "CNAME"], cl, [80, 90], rh=28))
    b.append(S([0], _t(24, 172, "가온은 반이 아직 정해지지 않아서 CID가 비어 있어요", "d-quiet", 12)))
    link = ("<path d='M232 78H326' class='d-line-accent'/><path d='M232 106H326' class='d-line-accent'/>"
            + "<path d='M232 134H262' class='d-line-amber' stroke-dasharray='4 3'/>"
            + _t(270, 138, "짝 없음", "d-amber", 11, 700))
    b.append(S([1, 2, 3], link))
    b.append(S([1], _t(24, 172, "ON s.cid = c.cid: CID가 같은 줄끼리 짝을 지어요", "d-accent", 12, 700)))
    res_in = [["0001", "민수", "ABAP반"], ["0002", "지아", "UI5반"]]
    res_lf = res_in + [["0007", "가온", "(비어 있음)"]]
    b.append(S([2], _t(24, 206, "INNER JOIN 결과 · 2건", "d-accent", 12.5, 700)
               + table(24, 216, ["SID", "SNAME", "CNAME"], res_in, [70, 70, 110], rh=28)
               + _t(300, 250, "짝이 없는 가온은 빠져요", "d-amber", 12, 700)))
    b.append(S([3], _t(24, 206, "LEFT OUTER JOIN 결과 · 3건", "d-accent", 12.5, 700)
               + table(24, 216, ["SID", "SNAME", "CNAME"], res_lf, [70, 70, 110], rh=28, hl2_cells=((2, 2),))
               + _t(300, 250, "왼쪽 학생은 모두 남고,", "d-amber", 12, 700)
               + _t(300, 270, "짝이 없으면 CNAME이 비어요", "d-amber", 12, 700)))
    return stepper("INNER JOIN과 LEFT OUTER JOIN · 짝 맞추기",
                   svg("jn", 340, "INNER JOIN은 짝이 있는 줄만, LEFT OUTER JOIN은 왼쪽 줄을 모두 남겨요", "".join(b)), [
                       ("두 테이블을 준비해요", "학생 세 명 중 가온(0007)은 아직 반이 없어서 CID가 비어 있어요."),
                       ("CID가 같은 줄끼리 짝을 지어요", "민수는 CL301, 지아는 CL303과 짝이 돼요. 가온은 짝이 없어요."),
                       ("INNER JOIN: 짝이 있는 줄만", "양쪽에 짝이 있는 2건만 결과에 남아요. 반이 없는 학생은 목록에서 사라져요."),
                       ("LEFT OUTER JOIN: 왼쪽은 모두", "왼쪽(FROM 쪽) 학생 3건이 모두 남고, 짝이 없는 가온의 CNAME은 비어요. \"반이 없는 학생도 보여 줘\"일 때 써요."),
                   ])


STATIC = {
    "Client 칸막이": ("같은 테이블이어도 Client(MANDT)마다 데이터가 따로예요", client),
    "참조 필드 연결": ("금액은 통화 필드를, 수량은 단위 필드를 가리켜요", reffield),
    "테이블이 아닌 DDIC 객체": ("Structure, Table Type, Include, Append Structure 비교", ddic_objs),
    "Check Table 직접 고르기": ("Value Table은 제안, 실제 검사는 직접 고른 Check Table로 해요", zcountry),
    "F4 목록 우선순위": ("F4 목록은 위에서부터 차례로 찾아요", f4order),
    "키 물려받기": ("부모 키가 자식 키 앞부분으로 그대로 내려가요", keyinherit),
}
STEPPERS = {
    "Transport 이동": transport,
    "저장과 활성화": activate,
    "로그인 언어와 Text Table": texttable,
    "INNER JOIN과 LEFT OUTER JOIN": joins,
}


# ------------------------------------------------------------------ LOOP INTO vs ASSIGNING (stepper)
def into_assign():
    rows = [["0001", "민수", "85"], ["0002", "지아", "92"], ["0003", "도윤", "78"]]
    b = [_t(24, 26, "Internal Table lt_std", "d-ink d-mono", 12.5, 700)]
    W = [70, 70, 70]
    b.append(S([0, 1], table(24, 36, ["SID", "SNAME", "SCORE"], rows, W, rh=30, hl_rows=(0,))))
    b.append(S([2], table(24, 36, ["SID", "SNAME", "SCORE"], [["0001", "민수", "90"]] + rows[1:], W, rh=30, hl_rows=(0,), hl2_cells=((0, 2),))))
    b.append(S([3], table(24, 36, ["SID", "SNAME", "SCORE"], rows, W, rh=30, hl_rows=(0,))))
    b.append(S([4], table(24, 36, ["SID", "SNAME", "SCORE"], [["0001", "민수", "90"]] + rows[1:], W, rh=30, hl_rows=(0,), hl2_cells=((0, 2),))))
    # INTO side: copy box
    box = lambda score, hl: (_t(420, 26, "ls_std (복사본)", "d-ink d-mono", 12.5, 700)
                             + table(420, 36, ["SID", "SNAME", "SCORE"], [["0001", "민수", score]], W, rh=30,
                                     hl2_cells=((0, 2),) if hl else ()))
    b.append(S([0], box("85", False) + arrow("M240 81H414", "d-line-accent", "ia", "b") + _t(327, 72, "INTO: 복사", "d-accent", 12, 700, "middle")))
    b.append(S([1], box("90", True) + "<path d='M240 81H414' class='d-line' stroke-dasharray='5 4'/>"
               + _t(420, 140, "ls_std만 90이 됐어요", "d-amber", 12, 700) + _t(24, 186, "lt_std는 아직 85 그대로예요", "d-amber", 12, 700)))
    b.append(S([2], box("90", False) + arrow("M414 81H240", "d-line-accent", "ia", "b") + _t(327, 72, "MODIFY: 다시 넣기", "d-accent", 12, 700, "middle")
               + _t(24, 186, "MODIFY lt_std FROM ls_std. 로 다시 넣어야 바뀌어요", "d-accent", 12, 700)))
    tag = (rect(420, 64, 120, 34, "d-hl", 17) + _t(480, 86, "<ls_std>", "d-accent d-mono", 12.5, 700, "middle")
           + arrow("M416 81H240", "d-line-accent", "ia", "b"))
    b.append(S([3], tag + _t(327, 72, "ASSIGNING: 가리키기", "d-accent", 12, 700, "middle")
               + _t(420, 126, "복사본 없이 그 줄에 이름표만 붙여요", "d-quiet", 12)))
    b.append(S([4], tag + _t(420, 126, "<ls_std>-score = 90.", "d-ink d-mono", 12.5, 700)
               + _t(24, 186, "줄이 바로 바뀌어요. MODIFY가 필요 없어요", "d-accent", 12, 700)))
    return stepper("INTO와 ASSIGNING · 복사와 직접 가리키기",
                   svg("ia", 206, "INTO는 줄을 복사하고, ASSIGNING은 줄을 직접 가리켜요", "".join(b)), [
                       ("INTO: 줄을 복사해요", "LOOP AT lt_std INTO ls_std.는 첫 줄의 내용을 ls_std에 복사해요. ls_std는 따로 떨어진 복사본이에요."),
                       ("복사본을 고치면", "ls_std-score를 90으로 바꿔도 lt_std의 첫 줄은 85 그대로예요. 복사본만 바뀌었기 때문이에요."),
                       ("MODIFY로 다시 넣어요", "MODIFY lt_std FROM ls_std.를 실행해야 고친 복사본이 테이블의 지금 줄에 들어가요."),
                       ("ASSIGNING: 줄에 이름표를 붙여요", "LOOP AT lt_std ASSIGNING FIELD-SYMBOL(<ls_std>).는 복사하지 않고, 테이블의 첫 줄 자체에 <ls_std>라는 이름표를 붙여요."),
                       ("이름표로 고치면 줄이 바로 바뀌어요", "<ls_std>-score = 90.을 실행하는 순간 테이블의 첫 줄이 90이 돼요. MODIFY가 필요 없어요."),
                   ])


STEPPERS["INTO와 ASSIGNING"] = into_assign
