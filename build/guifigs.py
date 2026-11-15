"""SAP GUI style scroll steppers: how MANDT gets filled, and a default currency via TMG event 05."""
import html
from demos2 import PLAY, PAUSE
from se11fk import KEY, SAVE, ACT, CHECK

EDIT = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20h4L19 9l-4-4L4 16z"/></svg>')
NEW = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3h9l4 4v14H6z"/><path d="M12 10v7M8.5 13.5h7"/></svg>')


def _s(*n):
    return ",".join(str(x) for x in n)


def on(steps, body, tag="div", cls=""):
    return f'<{tag} class="st-item {cls}" data-steps="{_s(*steps)}">{body}</{tag}>'


def hl(steps, body, tag="span", cls=""):
    return f'<{tag} class="se-hl {cls}" data-steps="{_s(*steps)}">{body}</{tag}>'


def grid(cols, head, rows, hl_rows=None):
    """rows: list of lists; hl_rows: {row index: steps tuple}"""
    hl_rows = hl_rows or {}
    h = "".join(f"<span>{c}</span>" for c in head)
    out = []
    for i, r in enumerate(rows):
        cells = "".join(f'<span class="mono">{c}</span>' for c in r)
        st = hl_rows.get(i)
        out.append(f'<div class="se-tr se-hl" data-steps="{_s(*st)}">{cells}</div>' if st else f'<div class="se-tr">{cells}</div>')
    return f'<div class="se-grid se-gx" style="--cols:{cols}"><div class="se-th">{h}</div>{"".join(out)}</div>'


def frm(label, val, steps=None, cls=""):
    v = f'<span class="se-in mono {cls}">{val}</span>'
    if steps:
        v = f'<span class="se-in mono se-hl {cls}" data-steps="{_s(*steps)}">{val}</span>'
    return f'<div class="se-frm"><span>{label}</span>{v}</div>'


def wrap(caption, win, notes, extra_cls=""):
    n = len(notes)
    nt = "".join(f'<div class="st-note st-item se-note" data-steps="{i}"><b><i>{i + 1}</i>{html.escape(t)}</b><span>{html.escape(d)}</span></div>'
                 for i, (t, d) in enumerate(notes))
    dots = "".join(f'<i class="st-dot" data-steps="{",".join(str(k) for k in range(i, n))}"></i>' for i in range(n))
    return (f'<figure class="diagram demo stepper se11 gui2 {extra_cls}" data-step="0" data-max="{n - 1}">'
            f"<figcaption>{html.escape(caption)}</figcaption>{win}"
            f'<div class="st-notes" aria-live="polite">{nt}</div>'
            '<div class="st-foot"><div class="st-btns">'
            f'<button type="button" class="dm-btn st-run">{PLAY}실행</button>'
            f'<button type="button" class="dm-btn st-pause">{PAUSE}<span class="t-pause">정지</span><span class="t-resume">이어서</span></button>'
            f'</div><div class="st-dots" aria-hidden="true">{dots}</div></div></figure>')


# ------------------------------------------------------------------ MANDT
def mandt():
    login = on([0], (
        '<div class="se-title">SAP 로그인</div>'
        '<div class="se-body g2-form">'
        + frm("Client", "100", (0,)) + frm("User", "RCODE-C-05") + frm("Password", "••••••••") + frm("Language", "EN")
        + '<p class="g2-cap">로그인한 Client 번호는 시스템 변수 <b class="mono">sy-mandt</b>에 들어가요</p></div>'))
    fields = grid("1.1fr .5fr .6fr 1.2fr", ["Field", "Key", "Initial", "Data element"],
                  [["MANDT", "✓", "✓", "MANDT"], ["CID", "✓", "✓", "ZCID"], ["CNAME", "", "", "ZCNAME"]], {0: (1,)})
    check = grid("1fr 1fr .7fr 1fr", ["Field", "Data element", "Type", "Check table"],
                 [["MANDT", "MANDT", "CLNT", "T000"], ["CID", "ZCID", "CHAR", ""], ["CNAME", "ZCNAME", "CHAR", ""]], {0: (2,)})
    tabs = "".join(f'<span class="se-tab{c}"{st}>{t}</span>' for t, c, st in [
        ("Attributes", "", ""), ("Delivery and Maint.", "", ""),
        ("Fields", " se-tab-on", ' data-steps="1"'), ("Input Help/Check", " se-tab-on", ' data-steps="2"')])
    se11 = on([1, 2], (
        '<div class="se-title">Dictionary: Display Table <span class="mono">ZCLASS</span></div>'
        f'<div class="se-tabs">{tabs}</div>'
        f'<div class="se-body">{on([1], fields)}{on([2], check)}</div>'))
    create = on([3], (
        '<div class="se-title">Table ZCLASS Insert</div>'
        f'<div class="se-tool"><span class="se-tb">{SAVE}<em>Save</em></span></div>'
        '<div class="se-body g2-form">'
        + frm("CID", "CL305") + frm("CNAME", "SAP반")
        + '<p class="g2-cap g2-warn">MANDT 칸이 없어요. 저장하면 100이 자동으로 들어가요</p></div>'))
    lst = grid(".7fr 1fr 1.2fr", ["MANDT", "CID", "CNAME"],
               [["100", "CL301", "ABAP반"], ["100", "CL303", "UI5반"], ["100", "CL305", "SAP반"]], {2: (4,)})
    result = on([4], (
        '<div class="se-title">Data Browser: Table ZCLASS · 3 Hits</div>'
        f'<div class="se-body">{lst}'
        '<p class="g2-cap">200번 Client의 레코드는 같은 테이블에 있어도 보이지 않아요</p></div>'))
    win = f'<div class="se-win">{login}{se11}{create}{result}</div>'
    return wrap("MANDT는 어떻게 채워질까 · 로그인부터 저장까지", win, [
        ("로그인할 때 Client를 골라요", "로그인 화면의 Client 칸에 적은 번호(100)가 이번 접속의 Client예요. SAP는 이 번호를 sy-mandt라는 시스템 변수에 기억해 둬요."),
        ("테이블 맨 앞 키가 MANDT예요", "SE11의 Fields 탭에서 MANDT가 첫 번째 키 필드예요. 이것 때문에 이 테이블은 Client마다 데이터가 따로 나뉘는 테이블이 돼요."),
        ("MANDT는 CLNT 타입이고 T000을 검사해요", "Input Help/Check 탭을 보면 MANDT의 타입은 CLNT(3자리), Check Table은 Client 목록 T000이에요. 개발자가 할 설정은 여기까지예요."),
        ("입력 화면에는 MANDT 칸이 없어요", "SE16이나 SM30에서 새 레코드를 넣을 때 MANDT는 묻지 않아요. 저장하는 순간 로그인한 Client 100이 자동으로 들어가요."),
        ("조회하면 내 Client 데이터만 나와요", "SE16으로 조회하면 MANDT가 100인 레코드만 보여요. ABAP의 SELECT도 같아서, WHERE에 MANDT를 안 적어도 로그인한 Client 조건이 자동으로 붙어요."),
    ], "g2-mandt")


# ------------------------------------------------------------------ TMG event 05
def tmg_default():
    menu = on([0], (
        '<div class="g2-menu"><span class="g2-mi">Edit</span><span class="g2-mi">Goto</span>'
        '<span class="g2-mi g2-open">Utilities<span class="g2-drop">'
        '<span>Where-Used List</span><span class="se-hl is-on" data-steps="0">Table Maintenance Generator</span><span>Database Utility</span>'
        '</span></span></div>'
        '<div class="se-body">'
        + grid("1.1fr .5fr 1.2fr .9fr", ["Field", "Key", "Data element", "Type"],
               [["MANDT", "✓", "MANDT", "CLNT"], ["CID", "✓", "ZCID", "CHAR"], ["CNAME", "", "ZCNAME", "CHAR"],
                ["FEE", "", "ZFEE", "CURR"], ["WAERS", "", "WAERS", "CUKY"]])
        + '</div>'))
    tmgform = (frm("Auth. Group", "&amp;NC&amp;") + frm("Function group", "ZFG_CLASS")
               + frm("Maint. type", "one step") + frm("Overview screen", "0001"))
    tmg = on([1], (
        '<div class="g2-menu"><span class="g2-mi">Table Maintenance Dialog</span>'
        '<span class="g2-mi g2-open">Environment<span class="g2-drop">'
        '<span>Authorization Groups</span><span class="g2-sub se-hl is-on" data-steps="1">Modification ▸ Events</span>'
        '</span></span></div>'
        f'<div class="se-body g2-form">{tmgform}</div>'))
    events = on([2], (
        f'<div class="se-tool"><span class="se-tb se-hl" data-steps="2">{NEW}<em>New Entries</em></span></div>'
        '<div class="se-body">'
        + grid(".4fr 1.4fr .5fr", ["T", "FORM routine", "Editor"], [["05", "SET_DEFAULT", "✎"]], {0: (2,)})
        + '<p class="g2-cap">05 = Creating a new entry (새 줄을 만들 때)</p></div>'))
    code = on([3], (
        f'<div class="se-tool"><span class="se-tb">{SAVE}<em>Save</em></span><span class="se-tb se-hl" data-steps="3">{ACT}<em>Activate</em></span></div>'
        '<pre class="g2-code"><span class="k">FORM</span> set_default.\n'
        '  <span class="se-hl" data-steps="3">zclass-waers = <span class="s">\'KRW\'</span>.</span>   <span class="c">" 새 줄의 통화 칸을 KRW로</span>\n'
        '<span class="k">ENDFORM</span>.</pre>'))
    sm30 = on([4], (
        f'<div class="se-tool"><span class="se-tb">{SAVE}<em>Save</em></span><span class="se-tb">{NEW}<em>New Entries</em></span></div>'
        '<div class="se-body">'
        + grid(".9fr 1fr .8fr .8fr", ["CID", "CNAME", "FEE", "WAERS"],
               [["CL301", "ABAP반", "370000", "KRW"], ["CL305", "SAP반", "", "<b class='g2-kr'>KRW</b>"]], {1: (4,)})
        + '<p class="g2-cap">새 줄을 추가하자마자 WAERS 칸에 KRW가 들어가 있어요. 다른 통화로 바꿀 수도 있어요</p></div>'))
    title = (on([0], '<div class="se-title">Dictionary: Change Table <span class="mono">ZCLASS</span><span class="se-badge">변경 모드</span></div>')
             + on([1], '<div class="se-title">Generate Table Maintenance Dialog: <span class="mono">ZCLASS</span></div>')
             + on([2], '<div class="se-title">Change View "Event": Overview</div>')
             + on([3], '<div class="se-title">ABAP Editor: Include <span class="mono">LZFG_CLASSF01</span></div>')
             + on([4], '<div class="se-title">SM30 · Maintain Table Views: <span class="mono">ZCLASS</span></div>'))
    status = (f'<div class="se-status"><span class="st-item" data-steps="3">{CHECK}Object activated</span>'
              f'<span class="st-item" data-steps="4">{CHECK}새 줄에 기본값이 들어갔어요</span></div>')
    win = f'<div class="se-win">{title}{menu}{tmg}{events}{code}{sm30}{status}</div>'
    return wrap("통화 키 기본값 넣기 · TMG 이벤트 05", win, [
        ("SE11에서 TMG를 열어요", "수강료 FEE(CURR)와 통화 WAERS(CUKY)가 있는 ZCLASS를 Change 모드로 열고, 메뉴 Utilities → Table Maintenance Generator를 눌러요."),
        ("Events 화면으로 가요", "TMG 화면이 이미 만들어져 있어야 해요. 메뉴 Environment → Modification → Events를 눌러요."),
        ("이벤트 05를 등록해요", "New Entries를 누르고 T 칸에 05(새 줄을 만들 때), FORM routine 칸에 SET_DEFAULT를 적어요. 옆의 편집 아이콘을 누르면 코드 창이 열려요."),
        ("기본값을 넣는 코드를 적어요", "FORM 안에 테이블이름-필드 = 'KRW'.를 적어요. 여기서 zclass는 지금 만드는 새 줄 한 건이에요. 저장하고 활성화해요."),
        ("SM30에서 확인해요", "SM30으로 ZCLASS를 열고 New Entries를 누르면 WAERS 칸에 KRW가 미리 들어가 있어요. SE16으로 넣을 때는 이 이벤트가 동작하지 않아요."),
    ], "g2-tmg")


# ------------------------------------------------------------------ SAP GUI first screen
def gui_start():
    cmd_txt = (on([1], "SE11", "span") + on([2], "/nSE38", "span") + on([3], "/oSE16", "span"))
    cmd = on([1, 2, 3], (
        '<div class="se-tool"><span class="se-in mono se-hl is-on" data-steps="1,2,3" style="min-width:150px">'
        f'{cmd_txt}</span><span class="g2-cap" style="margin:0;align-self:center">← 명령 입력칸 (Enter)</span></div>'))
    titles = (on([0], '<div class="se-title">SAP 로그인</div>')
              + on([1], '<div class="se-title">SAP Easy Access</div>')
              + on([2], '<div class="se-title">ABAP Editor: Initial Screen</div>')
              + on([3], '<div class="se-title">Data Browser: Initial Screen<span class="se-badge">새 창 (세션 2)</span></div>')
              + on([4], '<div class="se-title">System: Status</div>'))
    login = on([0], (
        '<div class="se-body g2-form">'
        + frm("Client", "100", (0,)) + frm("User", "RCODE-C-05") + frm("Password", "••••••••") + frm("Language", "EN")
        + '<p class="g2-cap">Client는 데이터 칸막이 번호예요 (다음 섹션)</p></div>'))
    easy = on([1], (
        '<div class="se-body">'
        + grid("1fr", ["메뉴"], [["▸ Favorites (즐겨찾기)"], ["▸ SAP Menu"]])
        + '<p class="g2-cap">T-code를 치고 Enter → 그 화면이 열려요. 자주 쓰는 T-code는 Favorites에 넣어 둬요</p></div>'))
    se38 = on([2], (
        '<div class="se-body g2-form">' + frm("Program", "ZC05_SELECT")
        + '<p class="g2-cap">/n은 지금 하던 화면을 닫고 이동해요. 다른 T-code 화면 안에서도 바로 갈 수 있어요</p></div>'))
    sess = on([3], (
        '<div class="se-body g2-form">' + frm("Table Name", "ZTC0503")
        + '<p class="g2-cap">/o는 새 창(세션)을 열어요. 첫 번째 창의 SE38은 그대로 남아요</p></div>'))
    status = on([4], (
        '<div class="g2-menu"><span class="g2-mi">Menu</span><span class="g2-mi">Edit</span>'
        '<span class="g2-mi g2-open">System<span class="g2-drop">'
        '<span>Create Session</span><span>End Session</span><span class="se-hl is-on" data-steps="4">Status...</span>'
        '</span></span></div>'
        '<div class="se-body g2-form" style="margin-top:124px">'
        + frm("Client", "100") + frm("User", "RCODE-C-05") + frm("Language", "EN") + frm("Transaction", "SE38", (4,))
        + '<p class="g2-cap">지금 화면의 T-code와 프로그램 이름을 알려줘요</p></div>'))
    win = f'<div class="se-win">{titles}{cmd}{login}{easy}{se38}{sess}{status}</div>'
    return wrap("SAP GUI 첫 화면 · 로그인부터 T-code까지", win, [
        ("로그인해요", "Client(수업은 100), User, Password, Language(EN)를 적고 Enter를 눌러요."),
        ("명령 입력칸에 T-code를 쳐요", "첫 화면 SAP Easy Access의 왼쪽 위 칸에 SE11처럼 T-code를 적고 Enter를 누르면 그 화면이 열려요."),
        ("/n: 지금 창에서 바로 이동해요", "다른 화면을 쓰는 중이면 그냥 SE38은 안 먹혀요. /nSE38처럼 앞에 /n을 붙이면 지금 화면을 끝내고 SE38로 가요."),
        ("/o: 새 창을 열어요", "/oSE16은 새 창(세션)에 SE16을 열어요. 테이블 구조(SE11)와 데이터(SE16)를 나란히 볼 때 편해요."),
        ("System → Status로 지금 화면을 확인해요", "메뉴 System → Status를 누르면 로그인한 Client, User, 지금 화면의 T-code와 프로그램 이름이 나와요."),
    ], "g2-start")


# ------------------------------------------------------------------ SE93
def se93():
    titles = (on([0], '<div class="se-title">Maintain Transaction</div>')
              + on([1], '<div class="se-title">Create Transaction</div>')
              + on([2], '<div class="se-title">Create Report Transaction <span class="mono">ZC05_EDU</span></div>')
              + on([3], '<div class="se-title">Create Object Directory Entry</div>')
              + on([4], '<div class="se-title">교육과정 조회</div>'))
    first = on([0], (
        f'<div class="se-tool"><span class="se-tb">{EDIT}<em>Change</em></span><span class="se-tb se-hl" data-steps="0">{NEW}<em>Create</em></span></div>'
        '<div class="se-body g2-form">' + frm("Transaction Code", "ZC05_EDU", (0,))
        + '<p class="g2-cap">이름은 Z나 Y로 시작해요. 기존 T-code를 넣고 Display를 누르면 어떤 프로그램인지 볼 수 있어요</p></div>'))
    kind = on([1], (
        '<div class="se-body g2-form">' + frm("Short text", "교육과정 조회")
        + grid("1fr", ["Start object"],
               [["Program and screen (dialog transaction)"], ["Program and selection screen (report transaction)"],
                ["Method of a class (OO transaction)"], ["Transaction with variant"], ["Transaction with parameters"]],
               {1: (1,)})
        + '</div>'))
    det = on([2], (
        f'<div class="se-tool"><span class="se-tb se-hl" data-steps="2">{SAVE}<em>Save</em></span></div>'
        '<div class="se-body g2-form">' + frm("Program", "ZC05_SELECT", (2,)) + frm("Selection screen", "1000", (2,))
        + grid("1.6fr .5fr", ["GUI support", ""], [["SAP GUI for HTML", ""], ["SAP GUI for Java", ""], ["SAP GUI for Windows", "✓"]], {2: (2,)})
        + '</div>'))
    pkg = on([3], (
        f'<div class="se-tool"><span class="se-tb">{SAVE}<em>Save</em></span><span class="se-tb">Local Object</span></div>'
        '<div class="se-body g2-form">' + frm("Package", "(수업 패키지)", (3,))
        + '<p class="g2-cap">패키지로 저장하면 Transport Request 번호를 물어요. 연습용은 Local Object($TMP)</p></div>'))
    run = on([4], (
        '<div class="se-tool"><span class="se-in mono se-hl is-on" data-steps="4" style="min-width:150px">/nZC05_EDU</span></div>'
        '<div class="se-body g2-form">' + frm("교육과정", "A001")
        + '<p class="g2-cap">SE38을 거치지 않고 프로그램의 입력 화면(1000번)이 바로 열려요</p></div>'))
    status = '<div class="se-status"><span class="st-item" data-steps="3">' + CHECK + 'Transaction ZC05_EDU saved</span></div>'
    win = f'<div class="se-win">{titles}{first}{kind}{det}{pkg}{run}{status}</div>'
    return wrap("SE93으로 T-code 만들기 · 내 REPORT 프로그램에", win, [
        ("SE93에서 새 이름을 적어요", "SE93을 열고 Transaction Code에 ZC05_EDU를 적은 뒤 Create를 눌러요."),
        ("종류를 골라요", "Short text를 적고, PARAMETERS 입력 화면이 있는 REPORT 프로그램이니까 Program and selection screen (report transaction)을 골라요."),
        ("실행할 프로그램을 적어요", "Program에 프로그램 이름, Selection screen에 1000(PARAMETERS가 만든 기본 입력 화면)을 적어요. GUI support에서 SAP GUI for Windows에 체크하고 저장해요."),
        ("저장할 곳을 정해요", "테이블이나 프로그램처럼 Package와 Transport Request를 정해요."),
        ("T-code로 실행해요", "명령 입력칸에 /nZC05_EDU를 치면 프로그램의 입력 화면이 바로 열려요."),
    ], "g2-se93")


STEPPERS = {"MANDT는 어떻게 채워질까": mandt, "통화 키 기본값 넣기": tmg_default,
            "SAP GUI 첫 화면": gui_start, "SE93으로 T-code 만들기": se93}
