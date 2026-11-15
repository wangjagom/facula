"""Interactive / stepping figures. All visible text is rendered into the HTML (JS only toggles state)."""
import html
import re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def _e(s):
    return html.escape(s, quote=True)


# ---- 1. setTimeout stepper (5부) -------------------------------------------------
def _hl_line(t):
    inner = highlight(t, get_lexer_by_name("javascript"), HtmlFormatter(nowrap=True)).rstrip("\n")
    return re.sub(r'<span class="nx">([A-Za-z_$][\w$]*)</span>(?=<span class="p">\()', r'<span class="nf">\1</span>', inner)


def stepper():
    lines = [
        ('let sResult = "아직 없음";', [1]),
        ("setTimeout(() => {", [2]),
        ('    sResult = "도착!";', [4]),
        ("}, 1000);", [2]),
        ("console.log(sResult);", [3]),
    ]
    code = "".join(
        f'<span class="st-line" data-steps="{",".join(map(str, st))}">{_hl_line(t)}</span>' for t, st in lines
    )

    def items(rows):
        return "".join(f'<span class="st-item" data-steps="{st}">{_e(t)}</span>' for st, t in rows)

    var = items([("0", "아직 만들기 전이에요"), ("1,2,3", '"아직 없음"'), ("4", '"도착!"')])
    queue = items([("0,1", "비어 있어요"), ("2,3", "콜백 함수 (1초 뒤에 실행)"), ("4", "비어 있어요 (방금 실행했어요)")])
    cons = items([("0,1,2", "아직 아무것도 없어요"), ("3,4", "아직 없음")])
    notes = [
        "코드는 위에서 아래로 한 줄씩 실행돼요. 아래로 스크롤하면 한 단계씩 진행되고, 위로 올리면 되돌아가요.",
        '상자 sResult를 만들고 "아직 없음"을 넣어요.',
        "setTimeout은 함수를 대기실에 맡기고, 1초를 기다리지 않고 바로 다음 줄로 넘어가요.",
        'console.log가 바로 실행돼요. 대기실의 함수는 아직 실행 전이라서 sResult는 "아직 없음" 그대로예요.',
        '1초가 지나자 대기실의 함수가 실행돼서 sResult가 "도착!"으로 바뀌어요. 하지만 console.log는 이미 끝난 뒤라서 콘솔에는 "아직 없음"이 남아요.',
    ]
    note_html = "".join(f'<p class="st-note st-item" data-steps="{i}">{_e(n)}</p>' for i, n in enumerate(notes))
    return (
        '<figure class="diagram demo stepper" data-step="0" data-max="4">'
        "<figcaption>setTimeout 코드가 실행되는 순서</figcaption>"
        '<div class="st-grid">'
        f'<pre class="st-code" aria-label="실행할 코드">{code}</pre>'
        '<div class="st-side">'
        f'<div class="st-box"><b>변수 sResult</b><div class="st-val mono">{var}</div></div>'
        f'<div class="st-box"><b>대기실</b><div class="st-val">{queue}</div></div>'
        f'<div class="st-box"><b>콘솔</b><div class="st-val mono">{cons}</div></div>'
        "</div></div>"
        f'<div class="st-notes" aria-live="polite">{note_html}</div>'
        '<div class="st-foot"><button type="button" class="st-run">▶ 실행</button>'
        '<div class="st-dots" aria-hidden="true">'
        + "".join(f'<i class="st-dot" data-steps="{",".join(str(k) for k in range(i, 5))}"></i>' for i in range(5))
        + "</div></div></figure>"
    )


# ---- 2. HBox / VBox playground (7부) ---------------------------------------------
def flexlab():
    def seg(key, label, opts, on):
        btns = "".join(
            f'<button type="button" data-css="{css}" aria-pressed="{"true" if name == on else "false"}">{name}</button>'
            for name, css in opts
        )
        return f'<div class="demo-row"><span class="demo-lab">{label}</span><div class="seg" data-k="{key}">{btns}</div></div>'

    rows = (
        seg("dir", "컨트롤", [("HBox", "row"), ("VBox", "column")], "HBox")
        + seg("j", "justifyContent", [("Start", "flex-start"), ("Center", "center"), ("End", "flex-end"),
                                      ("SpaceBetween", "space-between"), ("SpaceAround", "space-around")], "Start")
        + seg("a", "alignItems", [("Stretch", "stretch"), ("Start", "flex-start"), ("Center", "center"),
                                  ("End", "flex-end"), ("Baseline", "baseline")], "Stretch")
    )
    return (
        '<figure class="diagram demo flexlab">'
        "<figcaption>정렬 값을 눌러서 안의 컨트롤이 어떻게 움직이는지 보세요</figcaption>"
        f"{rows}"
        '<div class="fl-stage" style="flex-direction:row;justify-content:flex-start;align-items:stretch">'
        '<div class="fl-item fl-1">Title</div><div class="fl-item fl-2">Input</div><div class="fl-item fl-3">Button</div>'
        "</div>"
        '<pre class="fl-code"><code>&lt;<span class="fl-tag">HBox</span> justifyContent="<span class="fl-j">Start</span>" '
        'alignItems="<span class="fl-a">Stretch</span>"&gt;</code></pre>'
        '<p class="demo-hint">값이 저절로 바뀌어요. 직접 눌러 보면 멈추고, 누른 값대로 움직여요. VBox에서는 justifyContent가 세로, alignItems가 가로로 바뀌어요.</p>'
        "</figure>"
    )


# ---- 3. path explorer (8부) ------------------------------------------------------
_TREE = [
    ("bookInfo", "객체", [("code", '"UX400"'), ("name", '"SAPUI5"')]),
    ("esStdList", "배열", [
        ("0", "객체", [("Sid", '"25010001"'), ("Sname", '"민수"')]),
        ("1", "객체", [("Sid", '"25010002"'), ("Sname", '"지아"')]),
    ]),
]


def pathlab():
    default = ("esStdList", "1", "Sname")

    def paths(keys, parent_kinds):
        bind = "/" + "/".join(keys)
        js = "oData"
        for k, kind in zip(keys, parent_kinds):
            js += f"[{k}]" if kind == "배열" else f".{k}"
        return bind, js

    def render(nodes, keys, kinds, parent_kind):
        out = ['<ul>']
        for node in nodes:
            name, third = node[0], node[1]
            k2 = keys + [name]
            kd2 = kinds + [parent_kind]
            bind, js = paths(k2, kd2)
            if len(node) == 3:  # container
                label = f"[{name}]" if parent_kind == "배열" else name
                val = "배열" if third == "배열" else "객체"
                chip = f'<span class="pl-chip">{val}</span>'
                on = tuple(k2) == tuple(default[: len(k2)])
                out.append(
                    f'<li class="{"on-path" if on else ""}"><button type="button" class="pl-node" data-bind="{_e(bind)}" '
                    f'data-js="{_e(js)}" data-val="{val}">{_e(label)}{chip}</button>'
                )
                out.append(render(node[2], k2, kd2, third))
                out.append("</li>")
            else:
                sel = tuple(k2) == default
                out.append(
                    f'<li class="{"on-path" if sel else ""}"><button type="button" class="pl-node{" is-sel" if sel else ""}" '
                    f'data-bind="{_e(bind)}" data-js="{_e(js)}" data-val="{_e(third)}">{_e(name)}'
                    f'<span class="pl-chip pl-val">{_e(third)}</span></button></li>'
                )
        out.append("</ul>")
        return "".join(out)

    tree = '<div class="pl-tree"><div class="pl-root">oData</div>' + render(_TREE, [], [], "객체") + "</div>"
    dbind, djs = paths(list(default), ["객체", "배열", "객체"])
    out = (
        '<dl class="pl-out">'
        f'<div><dt>Binding Path</dt><dd class="pl-o-bind mono">{{{_e(dbind)}}}</dd></div>'
        f'<div><dt>자바스크립트 경로</dt><dd class="pl-o-js mono">{_e(djs)}</dd></div>'
        '<div><dt>가리키는 값</dt><dd class="pl-o-val mono">"지아"</dd></div></dl>'
    )
    return (
        '<figure class="diagram demo pathlab">'
        "<figcaption>왼쪽 칸을 눌러서 각 데이터가 어떤 경로로 불리는지 보세요</figcaption>"
        f'<div class="pl-grid">{tree}{out}</div></figure>'
    )
