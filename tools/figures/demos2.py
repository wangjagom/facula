"""More interactive figures (5부 steppers, 8부 two-way binding, 9부 template copy).
All visible text is rendered into the HTML; JS only toggles state (plus digits / the demo's own words)."""
from demos import _e, _hl_line

_SV = '<svg class="st-ic" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
from icon3d import html3 as _h3
ICONS = {
    "var": _h3("box", "amber", "st-ic st-ic3"),
    "queue": _h3("hourglass", None, "st-ic st-ic3"),
    "console": _h3("console", "ink", "st-ic st-ic3"),
    "state": _h3("traffic", None, "st-ic st-ic3"),
    "func": _h3("play", "green", "st-ic st-ic3"),
}
PLAY = '<svg class="bt-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4.5v15l12-7.5z" fill="currentColor"/></svg>'
PAUSE = '<svg class="bt-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M7 4h3.5v16H7zM13.5 4H17v16h-3.5z" fill="currentColor"/></svg>'


def _items(kind, rows):
    out = []
    for st, t, state in rows:
        if kind == "console" and state == "out":
            body = "".join(f'<span class="co-line">{_e(x)}</span>' for x in t.split("\n"))
        else:
            body = "<br>".join(_e(x) for x in t.split("\n"))
        out.append(f'<span class="st-item chip c-{state}" data-steps="{st}">{body}</span>')
    return "".join(out)


def _steps_fig(caption, lines, boxes, notes, aria):
    code = "".join(
        f'<span class="st-line" data-steps="{",".join(map(str, st))}">{_hl_line(t)}</span>' for t, st in lines
    )
    box_html = "".join(
        f'<div class="st-box k-{kind}"><b class="st-h">{ICONS[kind]}{_e(title)}</b><div class="st-val">{_items(kind, rows)}</div></div>'
        for title, kind, rows in boxes
    )
    note_html = "".join(f'<p class="st-note st-item" data-steps="{i}">{_e(n)}</p>' for i, n in enumerate(notes))
    n = len(notes)
    dots = "".join(f'<i class="st-dot" data-steps="{",".join(str(k) for k in range(i, n))}"></i>' for i in range(n))
    return (
        f'<figure class="diagram demo stepper" data-step="0" data-max="{n - 1}">'
        f"<figcaption>{_e(caption)}</figcaption>"
        '<div class="st-grid">'
        f'<pre class="st-code" aria-label="{_e(aria)}">{code}</pre>'
        f'<div class="st-side">{box_html}</div></div>'
        f'<div class="st-notes" aria-live="polite">{note_html}</div>'
        '<div class="st-foot"><div class="st-btns">'
        f'<button type="button" class="dm-btn st-run">{PLAY}실행</button>'
        f'<button type="button" class="dm-btn st-pause">{PAUSE}<span class="t-pause">정지</span><span class="t-resume">이어서</span></button>'
        f'</div><div class="st-dots" aria-hidden="true">{dots}</div></div>'
        "</figure>"
    )


_PROMISE = ("Promise 상자 상태", "state", [("0", "아직 없어요", "empty"), ("1,2", "기다리는 중 (pending) · 비어 있어요", "wait"),
                                       ("3", "성공 (fulfilled) · 상자 안에 90", "ok")])


_GETSCORE = [
    ("function getScore() {", [0]),
    ("    return new Promise(resolve => {", [0]),
    ("        setTimeout(() => resolve(90), 1000);", [0]),
    ("    });", [0]),
    ("}", [0]),
]


def settimeout_steps():
    lines = [
        ('let sResult = "아직 없음";', [1]),
        ("setTimeout(() => {", [2]),
        ('    sResult = "도착!";', [4]),
        ("}, 1000);", [2]),
        ("console.log(sResult);", [3]),
    ]
    boxes = [
        ("변수 sResult", "var", [("0", "아직 만들기 전이에요", "empty"), ("1,2,3", '"아직 없음"', "val"), ("4", '"도착!"', "val")]),
        ("대기실", "queue", [("0,1", "비어 있어요", "empty"), ("2,3", "콜백 함수 · 1초 뒤에 실행", "wait"),
                           ("4", "비어 있어요 (방금 실행했어요)", "empty")]),
        ("콘솔", "console", [("0,1,2", "아직 아무것도 없어요", "empty"), ("3,4", "아직 없음", "out")]),
    ]
    notes = [
        "코드는 위에서 아래로 한 줄씩 실행돼요. 아래로 스크롤하면 한 단계씩 진행되고, 위로 올리면 되돌아가요.",
        '상자 sResult를 만들고 "아직 없음"을 넣어요.',
        "setTimeout은 함수를 대기실에 맡기고, 1초를 기다리지 않고 바로 다음 줄로 넘어가요.",
        'console.log가 바로 실행돼요. 대기실의 함수는 아직 실행 전이라서 sResult는 "아직 없음" 그대로예요.',
        '1초가 지나자 대기실의 함수가 실행돼서 sResult가 "도착!"으로 바뀌어요. 하지만 console.log는 이미 끝난 뒤라서 콘솔에는 "아직 없음"이 남아요.',
    ]
    return _steps_fig("setTimeout 코드가 실행되는 순서", lines, boxes, notes, "실행할 코드")


def promise_steps():
    lines = _GETSCORE + [
        (" ", []),
        ("const p = getScore();", [1]),
        ("console.log(p);", [2]),
        ("setTimeout(() => console.log(p), 1500);", [3]),
    ]
    boxes = [
        ("변수 p", "var", [("0", "아직 만들기 전이에요", "empty"), ("1,2,3", "Promise 상자 (진동벨)", "val")]),
        _PROMISE,
        ("콘솔", "console", [("0,1", "아직 아무것도 없어요", "empty"), ("2", "Promise {<pending>}", "out"),
                           ("3", "Promise {<pending>}\nPromise {<fulfilled>: 90}", "out")]),
    ]
    notes = [
        "getScore()는 1초 걸려서 90을 알려 주는 함수예요. 결과가 아니라 진동벨(Promise)을 먼저 돌려줘요.",
        "p에는 90이 아니라 Promise 상자가 들어와요. 상자는 처음에 기다리는 중이고 비어 있어요.",
        "바로 찍으면 아직 기다리는 중(pending)이에요. 1초가 아직 지나지 않았기 때문이에요.",
        "1초가 지나 일이 끝나면 상자가 성공(fulfilled)으로 바뀌고 90이 들어와요. 이 상태는 다시 바뀌지 않아요.",
    ]
    return _steps_fig("Promise 상자의 상태가 바뀌는 순서", lines, boxes, notes, "실행할 코드")


def async_steps():
    lines = _GETSCORE + [
        (" ", []),
        ("async function showScore() {", [0]),
        ("    const nScore = await getScore();", [2, 4]),
        ("    console.log(nScore);", [4]),
        ("}", [0]),
        ("showScore();", [1]),
        ('console.log("이 줄이 먼저 찍혀요");', [3]),
    ]
    boxes = [
        ("showScore 함수", "func", [("0", "아직 실행 전이에요", "empty"), ("1", "실행을 시작했어요", "val"),
                                  ("2,3", "await에서 멈춰 있어요", "wait"), ("4", "멈춘 자리에서 다시 이어져요", "ok")]),
        ("getScore()의 Promise", "state", [("0,1", "아직 없어요", "empty"), ("2,3", "기다리는 중 (pending) · 비어 있어요", "wait"),
                                         ("4", "성공 (fulfilled) · 상자 안에 90", "ok")]),
        ("콘솔", "console", [("0,1,2", "아직 아무것도 없어요", "empty"), ("3", "이 줄이 먼저 찍혀요", "out"),
                           ("4", "이 줄이 먼저 찍혀요\n90", "out")]),
    ]
    notes = [
        "먼저 getScore와 showScore 함수를 만들어 두기만 해요. 함수는 부르기 전에는 실행되지 않아요.",
        "showScore()를 불러서 함수 안으로 들어가요.",
        "getScore()가 진동벨(Promise)을 돌려주고, await는 벨이 울릴 때까지 이 함수 안에서만 멈춰요.",
        "함수 안은 멈춰 있지만 바깥 코드는 기다리지 않고 계속 실행돼요. 그래서 이 줄이 먼저 찍혀요.",
        "1초 뒤 Promise가 성공해서 상자에 90이 들어오면, await가 90을 꺼내 nScore에 담고 멈췄던 자리부터 이어서 실행해요.",
    ]
    return _steps_fig("async / await 코드가 실행되는 순서", lines, boxes, notes, "실행할 코드")


def twolab():
    return (
        '<figure class="diagram demo twolab" data-from="view">'
        "<figcaption>Input에 글자를 쳐 보세요. Text와 모델이 같이 바뀌어요</figcaption>"
        '<div class="tw-grid">'
        '<div class="tw-box"><b>화면</b>'
        '<label class="tw-row"><code>Input</code><input class="tw-input" type="text" value="SAPUI5" aria-label="Input 컨트롤의 값"></label>'
        '<div class="tw-row"><code>Text</code><span class="tw-text">SAPUI5</span></div>'
        '<p class="tw-xml mono">&lt;Input value="{/bookInfo/name}" /&gt;<br>&lt;Text text="{/bookInfo/name}" /&gt;</p></div>'
        '<div class="tw-mid"><span class="tw-dir tw-d-view">화면 → 모델</span><span class="tw-dir tw-d-model">모델 → 화면</span></div>'
        '<div class="tw-box"><b>모델 (JSONModel)</b>'
        '<p class="tw-model mono">{ bookInfo: { name: "<span class="tw-val">SAPUI5</span>" } }</p>'
        '<button type="button" class="dm-btn tw-set">setProperty("/bookInfo/name", "ABAP")</button></div>'
        "</div></figure>"
    )


TL_ROWS = [("S1001", "SAPUI5"), ("S2001", "ABAP"), ("S3001", "Fiori"), ("S4001", "CDS"), ("S5001", "OData")]


def tmpllab(n0=2):
    data = "".join(
        f'<span class="tl-item{" is-on" if i < n0 else ""}" data-i="{i + 1}">    {{ sCode: "{c}", sName: "{nm}" }}{"," if i < len(TL_ROWS) - 1 else ""}</span>'
        for i, (c, nm) in enumerate(TL_ROWS)
    )
    rows = "".join(
        f'<li class="tl-row{" is-on" if i < n0 else ""}" data-i="{i + 1}"><span>{nm}</span><small>/skillList/{i}</small></li>'
        for i, (c, nm) in enumerate(TL_ROWS)
    )
    return (
        f'<figure class="diagram demo tmpllab" data-n="{n0}" data-max="{len(TL_ROWS)}">'
        "<figcaption>데이터를 늘리고 줄여 보세요. 같은 틀이 복사돼서 줄이 늘어나요</figcaption>"
        '<div class="tl-grid">'
        '<div class="tl-box"><b>데이터 (모델)</b><pre class="tl-code">skillList: ['
        f'{data}]</pre></div>'
        '<div class="tl-box tl-tmpl"><b>템플릿 (한 번만 적어요)</b><pre class="tl-code">&lt;core:Item\n    key="{sCode}"\n    text="{sName}" /&gt;</pre>'
        '<span class="tl-x">데이터 한 건마다 복사</span></div>'
        f'<div class="tl-box"><b>화면 (ComboBox 항목)</b><ul class="tl-list">{rows}</ul></div>'
        "</div>"
        '<div class="tl-foot"><button type="button" class="dm-btn tl-add">+ 항목 추가</button>'
        '<button type="button" class="dm-btn tl-del">− 항목 빼기</button>'
        f'<span class="tl-count">데이터 <b class="tl-n">{n0}</b>개 → 화면 줄 <b class="tl-n">{n0}</b>개</span></div>'
        "</figure>"
    )


def for_steps():
    lines = [
        ("for (let i = 0; i < 3; i++) {", [1, 3, 4, 5]),
        ("    console.log(i);", [2, 3, 4]),
        ("}", []),
    ]
    boxes = [
        ("변수 i", "var", [("0", "아직 만들기 전이에요", "empty"), ("1,2", "0", "val"), ("3", "1", "val"),
                         ("4", "2", "val"), ("5", "3", "val")]),
        ("조건 i < 3", "state", [("0,1", "아직 검사 전이에요", "empty"), ("2", "0 < 3 → 참", "ok"), ("3", "1 < 3 → 참", "ok"),
                              ("4", "2 < 3 → 참", "ok"), ("5", "3 < 3 → 거짓, 반복을 끝내요", "no")]),
        ("콘솔", "console", [("0,1", "아직 아무것도 없어요", "empty"), ("2", "0", "out"), ("3", "0\n1", "out"),
                           ("4,5", "0\n1\n2", "out")]),
    ]
    notes = [
        "for는 괄호 안 세 부분(시작, 조건, 한 바퀴 끝날 때마다)대로 움직여요. 아래로 스크롤하면 한 단계씩 진행되고, 위로 올리면 되돌아가요.",
        "시작: i를 0으로 만들어요. 이 부분은 처음에 딱 한 번만 실행돼요.",
        "조건 i < 3이 참이라서 한 바퀴를 돌아요. console.log(0)이 실행돼요.",
        "한 바퀴가 끝나서 i++로 i가 1이 되고, 조건이 또 참이라서 console.log(1)이 실행돼요.",
        "i가 2가 돼도 아직 3보다 작아서 한 바퀴 더 돌아요. console.log(2)가 실행돼요.",
        "i++로 i가 3이 되면 조건이 거짓이라서 반복을 끝내요. 콘솔에는 0, 1, 2만 남아요.",
    ]
    return _steps_fig("for문이 한 바퀴씩 도는 순서", lines, boxes, notes, "실행할 코드")


FL_ROWS = [("민수", "CL303"), ("지아", "CL301"), ("도윤", "CL303"), ("서연", "CL301"), ("하준", "CL303"), ("가온", "CL301")]


def filtlab():
    names = sorted(n for n, _ in FL_ROWS)
    def seg(key, label, opts, on):
        btns = "".join(f'<button type="button" data-v="{v}" aria-pressed="{"true" if v == on else "false"}">{t}</button>' for v, t in opts)
        return f'<div class="demo-row"><span class="demo-lab">{label}</span><div class="seg" data-k="{key}">{btns}</div></div>'

    ctrl = (seg("f", "필터", [("all", "필터 없음"), ("CL301", "반 = CL301"), ("CL303", "반 = CL303")], "all")
            + seg("s", "정렬", [("o", "정렬 없음"), ("a", "이름 오름차순"), ("d", "이름 내림차순")], "o"))
    model = "".join(f'<li><span>{n}</span><span>{c}</span></li>' for n, c in FL_ROWS)
    table = "".join(
        f'<li class="ft-row is-on" data-c="{c}" data-o="{i}" data-a="{names.index(n)}" data-d="{len(names) - 1 - names.index(n)}">'
        f'<span>{n}</span><span>{c}</span></li>' for i, (n, c) in enumerate(FL_ROWS))
    code = (
        '<pre class="ft-code">'
        f'<span class="ft-c is-on" data-key="f:all">{_hl_line("oBinding.filter([]);                       // 필터 해제")}</span>'
        f'<span class="ft-c" data-key="f:CL301">{_hl_line("oBinding.filter([new Filter(" + chr(34) + "Cid" + chr(34) + ", FilterOperator.EQ, " + chr(34) + "CL301" + chr(34) + ")]);")}</span>'
        f'<span class="ft-c" data-key="f:CL303">{_hl_line("oBinding.filter([new Filter(" + chr(34) + "Cid" + chr(34) + ", FilterOperator.EQ, " + chr(34) + "CL303" + chr(34) + ")]);")}</span>'
        f'<span class="ft-c is-on" data-key="s:o">{_hl_line("// 정렬 안 함: 모델에 있는 순서 그대로")}</span>'
        f'<span class="ft-c" data-key="s:a">{_hl_line("oBinding.sort(new Sorter(" + chr(34) + "Sname" + chr(34) + "));")}</span>'
        f'<span class="ft-c" data-key="s:d">{_hl_line("oBinding.sort(new Sorter(" + chr(34) + "Sname" + chr(34) + ", true));")}</span>'
        "</pre>"
    )
    n = len(FL_ROWS)
    return (
        f'<figure class="diagram demo filtlab" data-f="all" data-s="o">'
        "<figcaption>필터와 정렬을 눌러 보세요. 모델(왼쪽)은 그대로예요</figcaption>"
        f"{ctrl}"
        '<div class="ft-grid">'
        f'<div class="ft-box"><b>모델 (원본 {n}건)</b><ul class="ft-list ft-model">{model}</ul></div>'
        f'<div class="ft-box"><b>테이블에 보이는 줄</b><ul class="ft-list ft-body">{table}</ul>'
        f'<p class="ft-count">모델 {n}건 → 테이블 <b class="ft-n">{n}</b>건</p></div></div>'
        f"{code}</figure>"
    )


# ---------------------------------------------------------------- ERD lab
import json as _json

ERD_DATA = {
    "tables": {
        "ZCLASS": {"ko": "반", "f": [["CID", "키"], ["CNAME", ""]]},
        "ZSTUDENT": {"ko": "학생", "f": [["SID", "키"], ["SNAME", ""], ["CID", "외래키"]]},
        "ZENROLL": {"ko": "수강", "f": [["SID", "키·외래키"], ["SUBJ", "키·외래키"]]},
        "ZSUBJECT": {"ko": "과목", "f": [["SUBJ", "키"], ["SUBJNAME", ""]]},
    },
    "order": ["ZCLASS", "ZSTUDENT", "ZENROLL", "ZSUBJECT"],
    "expect": [["ZCLASS", "ZSTUDENT"], ["ZSTUDENT", "ZENROLL"], ["ZSUBJECT", "ZENROLL"]],
    "m": {
        "start": "위에서 테이블을 놓은 뒤, 테이블 두 개를 차례로 눌러 관계선을 그어 보세요. 1:N은 먼저 누른 테이블이 1쪽이에요. 테이블은 끌어서 옮길 수 있고, 선을 누르면 지워져요.",
        "pick": "{a} 테이블을 골랐어요. 이어서 연결할 테이블을 누르세요. 같은 테이블을 다시 누르면 취소돼요.",
        "made": "{a} - {b} 선을 그었어요. 아래 '정답 확인'을 눌러 보세요.",
        "same": "이미 같은 선이 있어요.",
        "ok": "{one} 1 : {many} N. 맞아요.",
        "rev": "{one} 1 : {many} N이 맞아요. 방향이 반대예요. 1쪽 테이블을 먼저 눌러서 다시 그려 보세요.",
        "kind": "{one} - {many} 관계 종류가 달라요. 한 {oko}에 {mko}이 여러 개이고, {mko} 한 명(건)은 {oko}이 하나예요.",
        "todo": "{one} - {many} 사이의 선을 아직 안 그렸어요.",
        "nm": "학생과 과목은 N:M이라 테이블 둘로는 이을 수 없어요. 가운데 연결 테이블(ZENROLL)을 두고, 학생 1 : 수강 N, 과목 1 : 수강 N 두 줄로 풀어 보세요.",
        "extra": "필요 없는 선이 있어요. 선을 눌러 지워 보세요.",
        "notable": "먼저 테이블을 놓으세요: {t}",
        "done": "완성했어요! 학생과 과목의 N:M을 연결 테이블(ZENROLL)로 풀어서, 모든 선이 1:N이 됐어요.",
        "answer": "정답이에요. 연결 테이블 ZENROLL을 가운데 둬서 선이 모두 1:N이 돼요.",
        "reset": "모두 지웠어요. 다시 그려 보세요.",
    },
}


def erdlab():
    btns = "".join(
        f'<button type="button" class="erd-add" data-t="{k}" aria-pressed="false">{k} <small>{v["ko"]}</small></button>'
        for k, v in ERD_DATA["tables"].items()
    )
    return (
        '<figure class="diagram demo erdlab" data-rel="1N">'
        "<figcaption>ERD 연습장: 학생, 반, 과목의 관계를 직접 그려 보세요</figcaption>"
        '<p class="erd-mission"><b>미션</b> 학생은 한 반에 속해요. 학생은 여러 과목을 듣고, 과목 하나는 여러 학생이 들어요. 이 관계를 테이블 4개로 그려 보세요.</p>'
        f'<div class="erd-bar"><span class="erd-lbl">① 테이블 놓기</span><div class="seg erd-tables">{btns}</div></div>'
        '<div class="erd-bar"><span class="erd-lbl">② 관계 종류</span><div class="seg erd-rels" role="group" aria-label="관계 종류">'
        '<button type="button" data-rel="1N" aria-pressed="true">1:N</button>'
        '<button type="button" data-rel="11" aria-pressed="false">1:1</button>'
        '<button type="button" data-rel="NM" aria-pressed="false">N:M</button></div>'
        '<span class="erd-tip">③ 테이블 두 개를 차례로 누르면 선이 그려져요</span></div>'
        '<div class="erd-scroll"><svg class="erd-svg" viewBox="0 0 760 240" role="img" aria-label="ERD를 그리는 판"></svg></div>'
        '<p class="erd-msg" aria-live="polite"></p>'
        '<div class="erd-foot"><button type="button" class="dm-btn erd-check">정답 확인</button>'
        '<button type="button" class="dm-btn erd-answer">정답 보기</button>'
        '<button type="button" class="dm-btn erd-reset">모두 지우기</button></div>'
        f'<script type="application/json" class="erd-json">{_json.dumps(ERD_DATA, ensure_ascii=False)}</script>'
        "</figure>"
    )
