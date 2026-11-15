"""Static SVG versions of the three diagrams in the doc, themed through CSS classes."""

DEFS = (
    "<defs>"
    "<marker id='{p}-a' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='d-arrowhead'/></marker>"
    "<marker id='{p}-b' viewBox='0 0 10 10' refX='9' refY='5' markerWidth='6' markerHeight='6' orient='auto-start-reverse'><path d='M0 0L10 5L0 10z' class='d-arrowhead-accent'/></marker>"
    "</defs>"
)


def _box(x, y, w, h, accent=False):
    cls = "d-box d-box-accent" if accent else "d-box"
    return f"<rect x='{x}' y='{y}' width='{w}' height='{h}' rx='10' class='{cls}'/>"


def _t(x, y, s, cls="d-ink", size=None, weight=None, anchor=None):
    a = []
    if size:
        a.append(f"font-size='{size}'")
    if weight:
        a.append(f"font-weight='{weight}'")
    if anchor:
        a.append(f"text-anchor='{anchor}'")
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"<text x='{x}' y='{y}' class='{cls}' {' '.join(a)}>{s}</text>"


def _g(i, body):
    return f"<g class='rv' style='--i:{i}'>{body}</g>"


def _svg(p, h, label, body, anim=False):
    return (
        f"<svg viewBox='0 0 760 {h}' role='img' aria-label='{label}' class='diagram-svg{' anim' if anim else ''}' font-size='13'>"
        + DEFS.format(p=p)
        + body
        + "</svg>"
    )


from icon3d import use3  # noqa: E402


def mvc():
    W, H, vx, mx, cx, rowA, rowB = 226, 88, 24, 510, 267, 30, 210
    b = []
    b.append(f"<path d='M{vx+W} {rowA+44}H{mx}' class='d-line-accent' marker-start='url(#mvc-b)' marker-end='url(#mvc-b)'/>")
    b.append(f"<path d='M{vx+W/2} {rowA+H}V{rowB+H/2}H{cx}' class='d-line' marker-start='url(#mvc-a)' marker-end='url(#mvc-a)'/>")
    b.append(f"<path d='M{cx+W} {rowB+H/2}H{mx+W/2}V{rowA+H}' class='d-line' marker-end='url(#mvc-a)'/>")
    for x, y, name, f, role, ex, ic in [
        (vx, rowA, "View (XML)", "view/View1.view.xml", "무엇을 어디에 보여줄지", "Table, ComboBox, Panel", ("layout", None)),
        (mx, rowA, "Model (JSONModel)", "model/data.json", "화면이 보여줄 데이터", "esStdList, classList 배열", ("box", "amber")),
        (cx, rowB, "Controller (JS)", "controller/View1.controller.js", "누르면 무엇을 할지", "onInit, onSearch, onSelect", ("gear", "slate")),
    ]:
        b.append(_box(x, y, W, H))
        b.append(use3(ic[0], ic[1], x + W - 40, y + 10, 28))
        b.append(_t(x + 16, y + 26, name, weight=650))
        b.append(_t(x + 16, y + 46, f, "d-quiet d-mono", 11.5))
        b.append(_t(x + 16, y + 62, role, "d-ink", 12))
        b.append(_t(x + 16, y + 78, ex, "d-quiet", 11.5))
    mid = (vx + W + mx) / 2
    b.append(_t(mid, rowA + 34, "바인딩", "d-accent", 13.5, 700, "middle"))
    b.append(_t(mid, rowA + 66, "입력하면 모델도 같이 바뀌어요", "d-quiet", 11.5, None, "middle"))
    b.append(_t(vx + W / 2 + 12, 172, "이벤트 (press, selectionChange)", "d-quiet", 11.5))
    b.append(_t(vx + W / 2 + 12, 190, "byId · bindElement", "d-quiet d-mono", 11.5))
    b.append(_t(mx + W / 2 - 12, 172, "setModel · setProperty", "d-quiet d-mono", 11.5, None, "end"))
    b.append(_t(mx + W / 2 - 12, 190, "getProperty", "d-quiet d-mono", 11.5, None, "end"))
    return _svg("mvc", 322, "바인딩이 화면과 데이터를 잇고, 컨트롤러는 이벤트를 처리해요", "".join(b))


def bindings():
    W, H = 220, 72
    cols = [
        (24, "프로퍼티 바인딩", [
            ("잡는 데이터: 값 하나", "/bookInfo/code", "→ \"UX400\""),
            ("쓰는 법", "Input value = /bookInfo/code", "절대경로 (/로 시작)"),
            ("화면 결과", "Text 하나에 UX400", "0203 · 0204"),
        ]),
        (270, "애그리게이션 바인딩", [
            ("잡는 데이터: 배열", "/esStdList", "→ 학생 210명"),
            ("쓰는 법", "Table items = /esStdList", "템플릿 안: Sname (상대경로)"),
            ("화면 결과", "템플릿을 210번 복사 → 210줄", "0205 · 0206 · 0212"),
        ]),
        (516, "엘리먼트 바인딩", [
            ("잡는 데이터: 객체 한 건", "/esStdList/63", "→ 학생 1명"),
            ("쓰는 법", "bindElement('/esStdList/63')", "안쪽: Sname (상대경로)"),
            ("화면 결과", "패널 안 컨트롤들이 그 학생 정보", "0210 · 0211 · 0213"),
        ]),
    ]
    ys = [48, 144, 240]
    b = []
    for x, head, boxes in cols:
        b.append(_t(x + W / 2, 30, head, "d-accent", 14, 700, "middle"))
        for i, (name, l1, l2) in enumerate(boxes):
            y = ys[i]
            if i < 2:
                b.append(f"<path d='M{x+W/2} {y+H}V{y+H+22}' class='d-line' marker-end='url(#bind-a)'/>")
            b.append(_box(x, y, W, H))
            b.append(_t(x + 16, y + 25, name, weight=650))
            mono = "d-mono" if i == 1 or (i == 0) else ""
            b.append(_t(x + 16, y + 45, l1, f"d-quiet {mono if i < 2 else ''}".strip(), 11.5))
            b.append(_t(x + 16, y + 61, l2, "d-quiet", 11.5))
    return _svg("bind", 336, "세 가지 바인딩은 데이터의 어디를 잡느냐가 달라요", "".join(b))


def flow():
    W, H, x1, x2, x3, rowA, rowB = 200, 72, 24, 280, 536, 24, 152
    b = []
    b.append(f"<path d='M{x1+W} {rowA+H/2}H{x2}' class='d-line' marker-end='url(#flow-a)'/>")
    b.append(f"<path d='M{x2+W} {rowA+H/2}H{x3}' class='d-line-accent' marker-end='url(#flow-b)'/>")
    b.append(f"<path d='M{x3+W/2} {rowA+H}V{rowB}' class='d-line-accent' marker-end='url(#flow-b)'/>")
    b.append(f"<path d='M{x3} {rowB+H/2}H{x2+W}' class='d-line-accent' marker-end='url(#flow-b)'/>")
    for x, y, name, l1, l2 in [
        (x1, rowA, "1. 검색 조건", "ComboBox: 반, 조", "검색 버튼 → onSearch"),
        (x2, rowA, "2. 학생 목록", "binding.filter().sort()", "행 선택 → onSelect"),
        (x3, rowA, "3. 학생 상세", "getPath() → 학생 경로", "패널.bindElement(경로)"),
        (x3, rowB, "4. 반 상세", "학생의 Cid로 findIndex", "bindElement('/classList/i')"),
        (x2, rowB, "5. 강사 팝업", "this._oDialog 한 번만 로드", "반 경로로 bindElement"),
    ]:
        b.append(_box(x, y, W, H))
        b.append(_t(x + 16, y + 25, name, weight=650))
        b.append(_t(x + 16, y + 45, l1, "d-quiet", 11.5))
        b.append(_t(x + 16, y + 61, l2, "d-quiet", 11.5))
    b.append(_t(x1, rowB + 30, "파란 화살표", "d-accent", 12, 700))
    b.append(_t(x1, rowB + 48, "경로(문자열)가 넘어가는 길", "d-quiet", 11.5))
    return _svg("flow", 248, "고른 한 줄의 경로가 상세와 팝업까지 이어져요", "".join(b))


def define_map():
    rows = [("sap/ui/core/mvc/Controller", "Controller"), ("sap/ui/model/json/JSONModel", "JSONModel"), ("sap/ui/model/Filter", "Filter")]
    b = [_g(0, _t(24, 28, "① 모듈 경로 (대괄호 안)", "d-accent", 13.5, 700) + _t(536, 28, "② 받을 이름 (함수의 괄호 안)", "d-accent", 13.5, 700))]
    for i, (path, name) in enumerate(rows):
        y = 44 + i * 64
        r = [_box(24, y, 400, 44),
             f"<circle cx='50' cy='{y+22}' r='11' class='d-badge'/>",
             _t(50, y + 27, str(i + 1), "d-badge-t", 12.5, 700, "middle"),
             _t(74, y + 27, f'"{path}"', "d-ink d-mono", 12.5),
             f"<path d='M424 {y+22}H536' class='d-line-accent' marker-end='url(#def-b)'/>",
             _box(536, y, 200, 44),
             f"<circle cx='562' cy='{y+22}' r='11' class='d-badge'/>",
             _t(562, y + 27, str(i + 1), "d-badge-t", 12.5, 700, "middle"),
             _t(586, y + 27, name, "d-ink d-mono", 12.5)]
        b.append(_g(i + 1, "".join(r)))
    b.append(_g(4, _t(24, 252, "n번째 경로의 모듈이 n번째 이름으로 들어와요. 순서가 어긋나면 엉뚱한 모듈이 들어와요.", "d-quiet", 12)
                + _t(24, 272, "새 모듈을 쓰려면 목록 끝에 경로를, 괄호 끝에 이름을 같은 순서로 추가해요.", "d-quiet", 12)))
    return _svg("def", 288, "경로 목록의 n번째가 함수 괄호의 n번째 이름으로 들어와요", "".join(b), anim=True)


def lifecycle():
    W, H, gap, x0, y = 128, 72, 22, 16, 60
    items = [
        ("앱이 열려요", "index.html", False),
        ("View와 Controller가", "만들어져요", False),
        ("onInit 실행", "자동으로 딱 한 번", True),
        ("화면이 보여요", "사용자가 쓰기 시작", False),
        ("버튼을 누르면", "연결한 함수 실행", True),
    ]
    b = []
    for i, (l1, l2, acc) in enumerate(items):
        x = x0 + i * (W + gap)
        g = []
        if i > 0:
            cls = "d-line-accent" if i == 3 else "d-line"
            mk = "life-b" if i == 3 else "life-a"
            g.append(f"<path d='M{x-gap} {y+H/2}H{x}' class='{cls}' marker-end='url(#{mk})'/>")
        g += [_box(x, y, W, H, acc), _t(x + W / 2, y + 31, l1, "d-ink", 12, 650, "middle"),
              _t(x + W / 2, y + 51, l2, "d-quiet", 11.5, None, "middle"), _t(x + 10, y - 8, str(i + 1), "d-accent", 12, 700)]
        b.append(_g(i, "".join(g)))
    x3, x5 = x0 + 3 * (W + gap), x0 + 4 * (W + gap)
    b.append(_g(5, f"<path d='M{x0} {y+H+14}H{x0+3*(W+gap)-gap}' class='d-bracket'/>" + _t(x0, y + H + 34, "앱이 시작될 때 한 번만", "d-quiet", 12)
                + f"<path d='M{x3} {y+H+14}H{x5+W}' class='d-bracket'/>" + _t(x3, y + H + 34, "사용하는 동안 누를 때마다 계속", "d-quiet", 12)))
    return _svg("life", 190, "onInit은 앱이 시작될 때 한 번, 버튼에 연결한 함수는 누를 때마다 실행돼요", "".join(b), anim=True)


def filter_flow():
    W, H, x1, x2, x3, y = 220, 88, 24, 270, 516, 30
    b = []
    for i, (x, name, l1, l2, acc) in enumerate([
        (x1, "Model (데이터)", "/esStdList", "학생 210명, 원본은 그대로", False),
        (x2, "바인딩 (items 연결)", "filter(aFilter)", "sort(oSorter)를 여기에 걸어요", True),
        (x3, "Table (화면)", "조건에 맞는 줄만", "화면에 보여요", False),
    ]):
        g = []
        if i > 0:
            cls, mk = ("d-line-accent", "filt-b") if i == 2 else ("d-line", "filt-a")
            g.append(f"<path d='M{x-26} {y+H/2}H{x}' class='{cls}' marker-end='url(#{mk})'/>")
        g += [_box(x, y, W, H, acc), _t(x + 16, y + 28, name, weight=650), _t(x + 16, y + 50, l1, "d-quiet d-mono", 11.5),
              _t(x + 16, y + 68, l2, "d-quiet", 11.5)]
        b.append(_g(i, "".join(g)))
    b.append(_g(3, f"<path d='M{x3+W/2} {y+H}V{y+H+40}H{x2+W/2}V{y+H+4}' class='d-dash' marker-end='url(#filt-b)'/>"
                + _t(x2 + W + 20, y + H + 30, 'getBinding("items")로 꺼내요', "d-accent d-mono", 11.5)))
    return _svg("filt", 178, "필터와 정렬은 데이터가 아니라 테이블의 바인딩에 걸어요", "".join(b), anim=True)


FIGURES = {
    "UI5 앱의 세 부분": ("바인딩이 화면과 데이터를 잇고, 컨트롤러는 이벤트를 처리해요", mvc),
    "바인딩 세 가지 비교": ("세 가지 바인딩은 데이터의 어디를 잡느냐가 달라요", bindings),
    "검색-목록-상세-팝업 흐름": ("고른 한 줄의 경로가 상세와 팝업까지 이어져요", flow),
    "define 매핑": ("경로 목록의 n번째가 함수 괄호의 n번째 이름으로 들어와요", define_map),
    "컨트롤러가 움직이는 때": ("onInit은 한 번, 연결한 함수는 누를 때마다 실행돼요", lifecycle),
    "필터가 걸리는 곳": ("필터와 정렬은 데이터가 아니라 테이블의 바인딩에 걸어요", filter_flow),
}

from dbdiagrams import DB_FIGURES  # noqa: E402
FIGURES.update(DB_FIGURES)
