"""Static SVG figures for the DB basics part (15부)."""
from diagrams import _box, _t, _g

DEFS = (
    "<defs>"
    "<marker id='{p}-a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='d-arrowhead'/></marker>"
    "<marker id='{p}-b' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='d-arrowhead-accent'/></marker>"
    "<marker id='{p}-c' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='d-arrowhead-amber'/></marker>"
    "</defs>"
)


def svg(p, h, label, body):
    return (f"<svg viewBox='0 0 760 {h}' role='img' aria-label='{label}' class='diagram-svg' font-size='13'>"
            + DEFS.format(p=p) + body + "</svg>")


def rect(x, y, w, h, cls, rx=0):
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='{rx}' class='{cls}'/>"


def table(x, y, cols, rows, widths, rh=30, hl_col=None, hl_rows=(), hl_cells=(), hl2_cells=(), size=12):
    """Draw a table. Returns svg string. hl_col: amber column, hl_rows: accent rows (data row index),
    hl_cells: accent (r, c), hl2_cells: amber (r, c)."""
    out = []
    cx = x
    for ci, (c, w) in enumerate(zip(cols, widths)):
        cls = "d-head"
        if hl_col == ci:
            cls = "d-hl2"
        out.append(rect(cx, y, w, rh, cls))
        out.append(_t(cx + w / 2, y + rh / 2 + 4.5, c, "d-ink d-mono", size - 0.5, 650, "middle"))
        cx += w
    for ri, row in enumerate(rows):
        cx = x
        for ci, (v, w) in enumerate(zip(row, widths)):
            cls = "d-cell"
            if ri in hl_rows:
                cls = "d-hl"
            if hl_col == ci:
                cls = "d-hl2"
            if (ri, ci) in hl_cells:
                cls = "d-hl"
            if (ri, ci) in hl2_cells:
                cls = "d-hl2"
            out.append(rect(cx, y + rh * (ri + 1), w, rh, cls))
            out.append(_t(cx + w / 2, y + rh * (ri + 1) + rh / 2 + 4.5, v, "d-ink d-mono", size - 0.5, None, "middle"))
            cx += w
    return "".join(out)


# ------------------------------------------------------------------ 1. DB and tables
def db_tables():
    b = [rect(24, 30, 712, 252, "d-zone-a", 16),
         _t(44, 56, "데이터베이스(Database)", "d-accent", 14, 700),
         _t(228, 56, "= 엑셀 파일 하나. 안에 시트(테이블)가 여러 장 들어 있어요", "d-quiet", 12.5)]
    items = [
        (48, "ZSTUDENT", ["SID", "SNAME", "CID"], [["0001", "민수", "CL301"], ["0002", "지아", "CL303"], ["0003", "도윤", "CL301"]], [52, 56, 62], "학생 테이블"),
        (278, "ZCLASS", ["CID", "CNAME"], [["CL301", "ABAP반"], ["CL303", "UI5반"]], [62, 76], "반 테이블"),
        (480, "ZENROLL", ["SID", "SUBJ"], [["0001", "JS101"], ["0001", "UI5101"], ["0002", "UI5101"]], [56, 72], "수강 테이블"),
    ]
    for x, name, cols, rows, widths, desc in items:
        b.append(_t(x, 100, name, "d-ink d-mono", 13, 700))
        b.append(table(x, 112, cols, rows, widths, rh=28))
        b.append(_t(x, 112 + 28 * (len(rows) + 1) + 22, f"테이블 = 시트 한 장 ({desc})", "d-quiet", 11.5))
    b.append(_t(650, 170, "…", "d-quiet", 22, None, "middle"))
    b.append(_t(650, 192, "다른 테이블들", "d-quiet", 11.5, None, "middle"))
    return svg("dbt", 306, "데이터베이스는 테이블 여러 장을 담고 있어요", "".join(b))


# ------------------------------------------------------------------ 2. table anatomy
def anatomy():
    x0, y0, rh = 230, 78, 34
    widths = [70, 80, 80, 80, 70]
    cols = ["MANDT", "SID", "SNAME", "CID", "SCORE"]
    rows = [["100", "0001", "민수", "CL301", "85"], ["100", "0002", "지아", "CL303", "92"],
            ["100", "0003", "도윤", "CL301", "78"], ["100", "0004", "서연", "CL303", "88"]]
    b = []
    b.append(table(x0, y0, cols, rows, widths, rh=rh, hl_col=1, hl_rows=(1,), hl2_cells=[(1, 4)]))
    # field bracket
    b.append(f"<path d='M{x0} {y0-8}V{y0-14}H{x0+380}V{y0-8}' class='d-bracket'/>")
    b.append(_t(x0 + 190, y0 - 26, "필드(Field) = 열. 어떤 정보인지 이름이 붙은 세로줄", "d-accent", 12.5, 700, "middle"))
    # record
    ry = y0 + rh * 2
    b.append(_t(24, ry + 16, "레코드(Record) = 행", "d-accent", 12.5, 700))
    b.append(_t(24, ry + 33, "한 줄 = 학생 한 명의 정보", "d-quiet", 11.5))
    b.append(f"<path d='M200 {ry+rh/2}H{x0-3}' class='d-line-accent' marker-end='url(#anat-b)'/>")
    # key
    kx = x0 + 70 + 40
    ky = y0 + rh * 5
    b.append(f"<path d='M{kx} {ky+34}V{ky+4}' class='d-line-amber' marker-end='url(#anat-c)'/>")
    b.append(_t(kx + 12, ky + 24, "키(Key) = 줄마다 겹치지 않는 번호 (이 테이블에서는 SID)", "d-amber", 12.5, 700))
    # value
    vx = x0 + 310 + 70
    b.append(f"<path d='M{vx+22} {ry+rh/2}H{vx+6}' class='d-line-amber' marker-end='url(#anat-c)'/>")
    b.append(_t(vx + 28, ry + 14, "값(Value)", "d-amber", 12.5, 700))
    b.append(_t(vx + 28, ry + 31, "= 칸 하나", "d-quiet", 11.5))
    b.append(_t(x0 + 190, ky + 66, "테이블 이름: ZSTUDENT", "d-quiet d-mono", 12, None, "middle"))
    return svg("anat", 330, "테이블은 필드(열)와 레코드(행)로 이루어지고, 키가 레코드를 구분해요", "".join(b))


# ------------------------------------------------------------------ 3. why split
def split_tables():
    b = [_t(24, 34, "한 테이블에 다 쓰면", "d-ink", 14, 700), _t(330, 34, "나눠서 쓰면", "d-ink", 14, 700)]
    b.append(table(24, 54, ["SID", "SNAME", "CNAME"], [["0001", "민수", "ABAP반"], ["0003", "도윤", "ABAP반"], ["0005", "하준", "ABAP반"]],
                   [52, 56, 72], rh=30, hl2_cells=[(0, 2), (1, 2), (2, 2)]))
    b.append(_t(24, 208, "반 이름이 바뀌면", "d-amber", 12.5, 700))
    b.append(_t(24, 227, "같은 글자를 300줄 고쳐야 해요", "d-quiet", 11.5))
    b.append(f"<path d='M222 114H300' class='d-line' marker-end='url(#spl-a)'/>")
    b.append(_t(261, 104, "나누기", "d-quiet", 11.5, None, "middle"))
    b.append(table(330, 54, ["SID", "SNAME", "CID"], [["0001", "민수", "CL301"], ["0003", "도윤", "CL301"], ["0005", "하준", "CL301"]],
                   [52, 56, 62], rh=30, hl_cells=[(0, 2), (1, 2), (2, 2)]))
    b.append(table(590, 54, ["CID", "CNAME"], [["CL301", "ABAP반"]], [62, 76], rh=30, hl_rows=(0,)))
    for yy in (99, 129, 159):
        b.append(f"<path d='M492 {yy}C540 {yy} 548 99 588 99' class='d-line-accent' marker-end='url(#spl-b)'/>")
    b.append(_t(330, 208, "반 이름이 바뀌면", "d-accent", 12.5, 700))
    b.append(_t(330, 227, "ZCLASS의 한 줄만 고치면 돼요", "d-quiet", 11.5))
    return svg("spl", 250, "반 이름을 한 번만 적고 코드로 가리키면 수정이 한 곳에서 끝나요", "".join(b))


# ------------------------------------------------------------------ 4. foreign key
def foreign_key():
    sx, sy, rh = 60, 78, 32
    b = [_t(sx, 58, "ZSTUDENT (학생)", "d-ink d-mono", 12.5, 700), _t(470, 58, "ZCLASS (반)", "d-ink d-mono", 12.5, 700)]
    rows = [["0001", "민수", "CL301"], ["0002", "지아", "CL303"], ["0003", "도윤", "CL301"], ["0004", "서연", "CL303"], ["0005", "하준", "CL301"]]
    b.append(table(sx, sy, ["SID", "SNAME", "CID"], rows, [64, 64, 80], rh=rh, hl_col=2))
    cy = 118
    b.append(table(470, cy, ["CID", "CNAME"], [["CL301", "ABAP반"], ["CL303", "UI5반"]], [80, 90], rh=34, hl_col=0))
    b.append(_t(sx + 168, sy - 8, "외래키", "d-amber", 11.5, 700, "middle"))
    b.append(_t(470 + 40, cy - 8, "키", "d-amber", 11.5, 700, "middle"))
    c301, c303 = cy + 34 + 17, cy + 34 * 2 + 17
    for i, r in enumerate(rows):
        y1 = sy + rh * (i + 1) + rh / 2
        y2 = c301 if r[2] == "CL301" else c303
        cls, mk = ("d-line-accent", "fk-b") if r[2] == "CL301" else ("d-line-amber", "fk-c")
        b.append(f"<path d='M{sx+208} {y1}C{sx+300} {y1} {380} {y2} 468 {y2}' class='{cls}' marker-end='url(#{mk})'/>")
    b.append(_t(380, 290, "CID가 같은 줄끼리 이어 붙이는 것이 조인(Join)이에요", "d-quiet", 12.5, None, "middle"))
    return svg("fk", 316, "학생 테이블의 CID가 반 테이블의 CID를 가리켜요", "".join(b))


# ------------------------------------------------------------------ 5. relationships
def relations():
    panels = [
        (24, "1 : 1", "일대일", "학생", "학생증", [(0, 0), (1, 1), (2, 2)], "한 줄에 한 줄", "학생 1명 ↔ 학생증 1장"),
        (266, "1 : N", "일대다", "반", "학생", [(1, 0), (1, 1), (1, 2)], "한 줄에 여러 줄", "반 1개 ↔ 학생 여러 명"),
        (508, "N : M", "다대다", "학생", "과목", [(0, 0), (0, 1), (1, 1), (1, 2), (2, 0), (2, 2)], "양쪽 모두 여러 줄", "테이블 둘로는 못 이어요"),
    ]
    b = []
    ys = [114, 154, 194]
    for x, ratio, ko, ln, rn, links, short, ex in panels:
        b.append(rect(x, 24, 228, 232, "d-box", 12))
        b.append(_t(x + 18, 54, ratio, "d-accent", 17, 700))
        b.append(_t(x + 78, 54, ko, "d-ink", 13, 650))
        b.append(_t(x + 20 + 35, 82, ln, "d-quiet", 11.5, None, "middle"))
        b.append(_t(x + 138 + 35, 82, rn, "d-quiet", 11.5, None, "middle"))
        for (a, c) in links:
            amber = ratio == "N : M"
            cls = "d-line-amber" if amber else "d-line-accent"
            b.append(f"<path d='M{x+90} {ys[a]}L{x+138} {ys[c]}' class='{cls}' style='stroke-width:1.6'/>")
        for i, y in enumerate(ys):
            b.append(rect(x + 20, y - 14, 70, 28, "d-hl" if ratio != "N : M" else "d-hl2", 6))
            b.append(rect(x + 138, y - 14, 70, 28, "d-cell", 6))
        b.append(_t(x + 114, 236, ex, "d-quiet", 11.5, None, "middle"))
    return svg("rel", 280, "테이블과 테이블의 관계는 1:1, 1:N, N:M 세 가지예요", "".join(b))


# ------------------------------------------------------------------ 6. N:M via connecting table
def nm_connect():
    b = [_t(24, 36, "ZSTUDENT 학생", "d-ink d-mono", 12.5, 700), _t(300, 36, "ZENROLL 연결 테이블", "d-amber d-mono", 12.5, 700),
         _t(600, 36, "ZSUBJECT 과목", "d-ink d-mono", 12.5, 700)]
    stu = [("0001 민수", 118), ("0002 지아", 178), ("0003 도윤", 238)]
    enr = [("0001 · JS101", 98, 0, 0), ("0001 · UI5101", 134, 0, 1), ("0002 · UI5101", 170, 1, 1), ("0002 · ABAP101", 206, 1, 2), ("0003 · JS101", 242, 2, 0)]
    sub = [("JS101", 118), ("UI5101", 178), ("ABAP101", 238)]
    for t, y in stu:
        b.append(rect(24, y - 16, 130, 32, "d-cell", 8))
        b.append(_t(89, y + 4.5, t, "d-ink d-mono", 12, None, "middle"))
    for t, y, si, bi in enr:
        b.append(f"<path d='M154 {stu[si][1]}C220 {stu[si][1]} 240 {y} 298 {y}' class='d-line-accent' style='stroke-width:1.6'/>")
        b.append(f"<path d='M452 {y}C510 {y} 530 {sub[bi][1]} 598 {sub[bi][1]}' class='d-line-amber' style='stroke-width:1.6'/>")
        b.append(rect(300, y - 15, 152, 30, "d-hl2", 6))
        b.append(_t(376, y + 4.5, t, "d-ink d-mono", 11.5, None, "middle"))
    for t, y in sub:
        b.append(rect(600, y - 16, 130, 32, "d-cell", 8))
        b.append(_t(665, y + 4.5, t, "d-ink d-mono", 12, None, "middle"))
    b.append(_t(226, 288, "1 : N", "d-accent", 13, 700, "middle"))
    b.append(_t(526, 288, "N : 1", "d-amber", 13, 700, "middle"))
    b.append(_t(376, 316, "N:M 관계는 1:N 두 개로 풀려요", "d-quiet", 12.5, None, "middle"))
    return svg("nm", 336, "다대다는 연결 테이블을 가운데 두면 일대다 두 개로 풀려요", "".join(b))


# ------------------------------------------------------------------ 7. frontend / backend
from icon3d import use3  # noqa: E402


def front_back():
    b = [rect(20, 28, 300, 244, "d-zone-a", 16), rect(440, 28, 300, 244, "d-zone-b", 16)]
    b.append(use3("window", "blue", 38, 39, 24))
    b.append(_t(68, 56, "프론트엔드", "d-accent", 15, 700))
    b.append(_t(150, 56, "사용자의 브라우저", "d-quiet", 12))
    b.append(use3("server", "violet", 458, 39, 24))
    b.append(_t(488, 56, "백엔드", "d-amber", 15, 700))
    b.append(_t(544, 56, "SAP 서버", "d-quiet", 12))
    for y, n, d, ic in [(76, "View (XML)", "화면 모양", ("layout", None)), (140, "Controller (JS)", "클릭 처리, 서버에 요청", ("gear", "slate")), (204, "Model", "받은 데이터 보관", ("box", "amber"))]:
        b.append(_box(44, y, 252, 50))
        b.append(use3(ic[0], ic[1], 260, y + 12, 26))
        b.append(_t(60, y + 22, n, weight=650))
        b.append(_t(60, y + 40, d, "d-quiet", 11.5))
    for y, n, d, ic in [(84, "ABAP 프로그램", "규칙 검사, 데이터 가공", ("console", "ink")), (196, "데이터베이스", "테이블들 (ZSTUDENT, ZCLASS …)", ("db", "violet"))]:
        b.append(_box(464, y, 252, 54))
        b.append(use3(ic[0], ic[1], 678, y + 13, 28))
        b.append(_t(480, y + 24, n, weight=650))
        b.append(_t(480, y + 43, d, "d-quiet", 11.5))
    b.append(f"<path d='M590 138V194' class='d-line' marker-start='url(#fb-a)' marker-end='url(#fb-a)'/>")
    b.append(_t(602, 172, "SQL", "d-quiet d-mono", 12))
    b.append(f"<path d='M324 112H436' class='d-line-accent' marker-end='url(#fb-b)'/>")
    b.append(_t(380, 102, "요청", "d-accent", 12.5, 700, "middle"))
    b.append(f"<path d='M436 168H324' class='d-line-amber' marker-end='url(#fb-c)'/>")
    b.append(_t(380, 188, "응답", "d-amber", 12.5, 700, "middle"))
    b.append(_t(380, 208, "(JSON)", "d-quiet", 11.5, None, "middle"))
    b.append(_t(380, 134, "OData", "d-quiet d-mono", 11.5, None, "middle"))
    b.append(_t(170, 296, "사용자가 보는 곳", "d-quiet", 12, None, "middle"))
    b.append(_t(590, 296, "사용자가 못 보는, 데이터가 보관되는 곳", "d-quiet", 12, None, "middle"))
    return svg("fb", 316, "프론트엔드는 브라우저에서 화면을, 백엔드는 서버에서 데이터를 맡아요", "".join(b))


# ------------------------------------------------------------------ 8. data dictionary
def ddic():
    b = []
    b.append(_t(24, 34, "Domain", "d-accent", 14, 700))
    b.append(_t(24, 52, "그릇의 크기와 모양", "d-quiet", 11.5))
    b.append(_box(24, 66, 212, 104))
    for i, t in enumerate(["ZDOM_GENDER", "타입 CHAR, 길이 1", "Fixed Value 1 = 남성, 2 = 여성"]):
        b.append(_t(40, 92 + i * 26, t, "d-ink d-mono" if i == 0 else "d-ink", 12 if i == 0 else 12, 650 if i == 0 else None))
    b.append(_t(272, 34, "Data Element", "d-accent", 14, 700))
    b.append(_t(272, 52, "그릇에 붙이는 라벨", "d-quiet", 11.5))
    b.append(_box(272, 66, 212, 104, True))
    for i, t in enumerate(["ZGENDER", "화면 제목: 성별", "위 Domain을 가져와요"]):
        b.append(_t(288, 92 + i * 26, t, "d-ink d-mono" if i == 0 else "d-ink", 12, 650 if i == 0 else None))
    b.append(_t(520, 34, "테이블 필드", "d-accent", 14, 700))
    b.append(_t(520, 52, "테이블에 실제로 놓인 그릇", "d-quiet", 11.5))
    for y, t in [(66, "ZSTUDENT-GENDER"), (126, "ZTEACHER-GENDER")]:
        b.append(_box(520, y, 216, 44))
        b.append(_t(536, y + 27, t, "d-ink d-mono", 12, 650))
    b.append(f"<path d='M238 118H270' class='d-line-accent' marker-end='url(#dd-b)'/>")
    b.append(f"<path d='M486 118C500 118 504 88 518 88' class='d-line-accent' marker-end='url(#dd-b)'/>")
    b.append(f"<path d='M486 118C500 118 504 148 518 148' class='d-line-accent' marker-end='url(#dd-b)'/>")
    b.append(_t(380, 214, "같은 Data Element를 쓰면 어느 테이블에서나 같은 모양, 같은 이름이에요", "d-quiet", 12.5, None, "middle"))
    return svg("dd", 232, "필드는 Domain, Data Element, 테이블 필드 세 단계로 만들어져요", "".join(b))


# ------------------------------------------------------------------ 9. data flow DB -> screen
def data_flow():
    W, H, gap, x0, y = 120, 124, 25, 30, 44
    items = [("DB 테이블", "영구 저장", "ZSTUDENT"), ("Internal Table", "임시, 서버 메모리", "lt_std"),
             ("OData · JSON", "객체와 배열", "[{ }, { }]"), ("UI5 모델", "받은 데이터 보관", "JSONModel"), ("화면", "바인딩으로 표시", "Table, Input")]
    icons = [("db", "violet"), ("table", "violet"), ("doc", "slate"), ("box", "amber"), ("layout", None)]
    b = []
    for i, (n, d, c) in enumerate(items):
        x = x0 + i * (W + gap)
        if i:
            b.append(f"<path d='M{x-gap+2} {y+H/2}H{x-2}' class='d-line-accent' marker-end='url(#df-b)'/>")
        b.append(_box(x, y, W, H, i == 2))
        b.append(use3(icons[i][0], icons[i][1], x + W / 2 - 16, y + 12, 32))
        b.append(_t(x + W / 2, y + 62, n, "d-ink", 13, 650, "middle"))
        b.append(_t(x + W / 2, y + 84, d, "d-quiet", 11.5, None, "middle"))
        b.append(_t(x + W / 2, y + 104, c, "d-quiet d-mono", 11.5, None, "middle"))
    ex = lambda i: x0 + i * (W + gap)
    yy = y + H + 22
    b.append(f"<path d='M{ex(0)} {yy}H{ex(1)+W}' class='d-bracket' style='stroke:#f59e0b'/>")
    b.append(_t((ex(0) + ex(1) + W) / 2, yy + 22, "백엔드 (서버)", "d-amber", 12.5, 700, "middle"))
    b.append(f"<path d='M{ex(2)} {yy}H{ex(2)+W}' class='d-bracket'/>")
    b.append(_t(ex(2) + W / 2, yy + 22, "통신", "d-quiet", 12.5, 700, "middle"))
    b.append(f"<path d='M{ex(3)} {yy}H{ex(4)+W}' class='d-bracket' style='stroke:#0ea5e9'/>")
    b.append(_t((ex(3) + ex(4) + W) / 2, yy + 22, "프론트엔드 (브라우저)", "d-accent", 12.5, 700, "middle"))
    return svg("df", 228, "DB 테이블의 데이터가 화면까지 오는 길", "".join(b))



def value_check():
    b = []
    # domain + data element
    b.append(_t(24, 30, "Domain", "d-accent", 13.5, 700))
    b.append(_box(24, 40, 230, 104))
    b.append(_t(40, 66, "ZCID", "d-ink d-mono", 12.5, 650))
    b.append(_t(40, 90, "타입 CHAR, 길이 5", "d-ink", 12))
    b.append(rect(34, 104, 210, 28, "d-hl2", 6))
    b.append(_t(44, 123, "Value Table: ZCLASS", "d-ink", 12, 650))
    b.append(_t(24, 196, "Data Element", "d-accent", 13.5, 700))
    b.append(_box(24, 206, 230, 78, True))
    b.append(_t(40, 232, "ZCID", "d-ink d-mono", 12.5, 650))
    b.append(_t(40, 256, "라벨: 반 코드 · Domain ZCID 사용", "d-ink", 12))
    b.append("<path d='M139 146V202' class='d-line-accent' marker-end='url(#vc-b)'/>")
    # check table
    b.append(_t(400, 30, "Check Table ZCLASS", "d-accent", 13.5, 700))
    b.append(table(400, 40, ["MANDT", "CID", "CNAME"], [["100", "CL301", "ABAP반"], ["100", "CL303", "UI5반"]],
                   [70, 90, 110], rh=28, hl_col=1))
    b.append(_t(505, 142, "Check Table Field(키)", "d-quiet", 11.5, None, "end"))
    # foreign key table
    b.append(_t(400, 196, "Foreign Key Table ZSTUDENT", "d-accent", 13.5, 700))
    b.append(table(400, 206, ["MANDT", "SID", "SNAME", "CID"], [["100", "0001", "민수", "CL301"]],
                   [64, 64, 72, 90], rh=28, hl_col=3))
    b.append(_t(400 + 200 + 45, 284, "Check Field", "d-amber", 12, 700, "middle"))
    # arrows
    b.append("<path d='M246 118C320 118 330 70 396 70' class='d-line-amber' stroke-dasharray='5 4' marker-end='url(#vc-c)'/>")
    b.append(_t(318, 132, "① Check Table로 제안", "d-amber", 11.5, 700, "middle"))
    b.append("<path d='M256 248H396' class='d-line-accent' marker-end='url(#vc-b)'/>")
    b.append(_t(326, 240, "필드의 타입", "d-quiet", 11.5, None, "middle"))
    b.append("<path d='M645 204C645 160 600 150 515 128' class='d-line-amber' marker-end='url(#vc-c)'/>")
    b.append(_t(690, 170, "② 이 값이", "d-amber", 11.5, 700, "middle"))
    b.append(_t(690, 186, "여기 있나 검사", "d-amber", 11.5, 700, "middle"))
    b.append(_t(380, 322, "Value Table은 Domain에 적는 제안, Check Table은 외래키로 거는 실제 검사예요", "d-quiet", 12.5, None, "middle"))
    return svg("vc", 340, "Domain의 Value Table이 외래키의 Check Table로 제안되고, Check Field 값을 Check Table 키에서 검사해요", "".join(b))

DB_FIGURES = {
    "데이터베이스와 테이블": ("데이터베이스는 테이블 여러 장을 담고 있어요", db_tables),
    "테이블의 구조": ("테이블은 필드(열)와 레코드(행)로 이루어지고, 키가 레코드를 구분해요", anatomy),
    "테이블을 나누는 그림": ("반 이름을 한 번만 적고 코드로 가리키면 수정이 한 곳에서 끝나요", split_tables),
    "외래키로 이어진 테이블": ("학생 테이블의 CID가 반 테이블의 CID를 가리켜요", foreign_key),
    "테이블 사이의 관계 세 가지": ("테이블과 테이블의 관계는 1:1, 1:N, N:M 세 가지예요", relations),
    "연결 테이블로 푸는 다대다": ("다대다는 연결 테이블을 가운데 두면 일대다 두 개로 풀려요", nm_connect),
    "프론트엔드와 백엔드 구조": ("프론트엔드는 브라우저에서 화면을, 백엔드는 서버에서 데이터를 맡아요", front_back),
    "필드가 만들어지는 세 단계": ("필드는 Domain, Data Element, 테이블 필드 세 단계로 만들어져요", ddic),
    "Value Table과 Check Table": ("Domain의 Value Table → 외래키의 Check Table → Check Field 검사", value_check),
    "DB에서 화면까지": ("DB 테이블의 데이터가 화면까지 오는 길", data_flow),
}


def erd_notation():
    b = []
    b.append(table(60, 66, ["CID", "CNAME"], [["CL301", "ABAP반"]], [70, 80], rh=30, hl_col=0))
    b.append(_t(60, 52, "ZCLASS (반)", "d-ink d-mono", 12.5, 700))
    b.append(table(470, 66, ["SID", "SNAME", "CID"], [["0001", "민수", "CL301"]], [60, 60, 70], rh=30))
    b.append(_t(470, 52, "ZSTUDENT (학생)", "d-ink d-mono", 12.5, 700))
    # relationship line: one bar at ZCLASS, crow's foot at ZSTUDENT
    y = 111
    b.append(f"<path d='M210 {y}H470' class='d-line-accent'/>")
    b.append(f"<path d='M228 {y-9}V{y+9}' class='d-line-accent'/>")
    b.append(f"<path d='M448 {y}L470 {y-9}M448 {y}L470 {y}M448 {y}L470 {y+9}' class='d-line-accent'/>")
    b.append(_t(228, y - 20, "1", "d-accent d-mono", 14, 700, "middle"))
    b.append(_t(448, y - 20, "N", "d-accent d-mono", 14, 700, "middle"))
    b.append(_t(240, 172, "막대(|) = 1, 한 줄", "d-accent", 12.5, 700, "middle"))
    b.append(_t(240, 190, "반 한 개", "d-quiet", 11.5, None, "middle"))
    b.append(_t(450, 172, "까마귀 발(세 갈래) = N, 여러 줄", "d-accent", 12.5, 700, "middle"))
    b.append(_t(450, 190, "그 반의 학생 여러 명", "d-quiet", 11.5, None, "middle"))
    b.append(_t(95, 160, "키", "d-amber", 11.5, 700, "middle"))
    b.append(_t(95, 176, "(PK)", "d-quiet", 11, None, "middle"))
    b.append(_t(625, 160, "외래키", "d-amber", 11.5, 700, "middle"))
    b.append(_t(625, 176, "(FK)", "d-quiet", 11, None, "middle"))
    b.append(f"<path d='M95 152V134' class='d-line-amber' marker-end='url(#erdn-c)'/>")
    b.append(f"<path d='M625 152V134' class='d-line-amber' marker-end='url(#erdn-c)'/>")
    b.append(_t(380, 232, "선은 PK(키)에서 FK(외래키)로 이어져요", "d-quiet", 12.5, None, "middle"))
    return svg("erdn", 256, "ERD에서 선 끝의 모양으로 1과 N을 나타내요", "".join(b))


DB_FIGURES["ERD 읽는 법"] = ("ERD에서 선 끝의 모양으로 1과 N을 나타내요", erd_notation)
