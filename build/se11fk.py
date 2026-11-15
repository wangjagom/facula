"""SE11 foreign-key walkthrough: a simplified SE11 screen that follows the scroll (generic .stepper)."""
from demos2 import PLAY, PAUSE

KEY = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="8" cy="15" r="4"/>'
       '<path d="M11 12l9-9M16 7l3 3M14 9l2 2"/></svg>')
SAVE = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 3h11l3 3v15H5z"/>'
        '<path d="M8 3v6h8V3M8 21v-7h8v7"/></svg>')
ACT = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20L15 9"/>'
       '<path d="M15 4v3M20 9h-3M18.5 5.5l-2 2M12 6l1 1M18 12l-1-1"/></svg>')
SRCH = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="6"/>'
        '<path d="M20 20l-4.5-4.5"/></svg>')
CHAIN = ('<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/>'
         '<path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>')
CHECK = '<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12.5l4.5 4.5L19 7"/></svg>'
CROSS = '<svg class="se-ic" viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18"/></svg>'

NOTES = [
    ("SE11에서 ZSTUDENT를 변경 모드로 열어요",
     "SE11에 테이블 이름 ZSTUDENT를 적고 Change를 눌러요. Fields 탭이 보이면 준비 끝이에요. 아래로 스크롤하면 한 단계씩 진행돼요."),
    ("외래키로 쓸 필드를 골라요", "필드 목록에서 CID를 눌러 커서를 둬요. 외래키는 커서가 있는 필드에 걸려요."),
    ("외래키 버튼을 눌러요", "필드 목록 위에 있는 열쇠 모양 Foreign Keys 버튼을 눌러요."),
    ("Check Table을 적어요", "Create Foreign Key 창이 열려요. Check table 칸에 부모 테이블 ZCLASS를 적어요."),
    ("제안 생성으로 필드 짝을 채워요",
     "Generate proposal을 누르면 두 테이블의 필드 짝이 자동으로 채워져요. MANDT끼리, CID끼리 짝이 맞는지 확인해요."),
    ("종류와 카디널리티를 고르고 복사해요",
     "CID는 학생 테이블의 키가 아니니까 외래키 필드 종류는 Non-key-fields/candidates예요. 반 1개에 학생 여러 명이라 카디널리티는 1 : CN이에요. Copy(✓)를 누르면 창이 닫혀요."),
    ("저장하고 활성화해요",
     "저장(Ctrl+S)하고 활성화(Ctrl+F3)해요. Input Help/Check 탭에서 CID의 Check table 칸에 ZCLASS가 보이면 성공이에요."),
]


def _s(*steps):
    return ",".join(str(s) for s in steps)


def se11fk():
    n = len(NOTES)
    fields_rows = [
        ("MANDT", True, "MANDT", ""),
        ("SID", True, "ZSID", ""),
        ("SNAME", False, "ZSNAME", ""),
        ("CID", False, "ZCID", "cid"),
    ]
    frows = "".join(
        f'<div class="se-tr{" se-hl se-sel" if k else ""}"{" data-steps=" + chr(34) + _s(1, 2) + chr(34) if k else ""}>'
        f'<span class="mono">{f}</span><span class="se-ck">{"✓" if key else ""}</span>'
        f'<span class="se-ck">{"✓" if key else ""}</span><span class="mono">{de}</span></div>'
        for f, key, de, k in fields_rows)
    entry_rows = [("MANDT", "MANDT", "CLNT", "T000", False), ("SID", "ZSID", "NUMC", "", False),
                  ("SNAME", "ZSNAME", "CHAR", "", False), ("CID", "ZCID", "CHAR", "ZCLASS", True)]
    erows = "".join(
        f'<div class="se-tr{" se-hl" if hl else ""}"{" data-steps=" + chr(34) + "6" + chr(34) if hl else ""}>'
        f'<span class="mono">{f}</span><span class="mono">{de}</span><span class="mono">{t}</span>'
        f'<span class="se-fk">{CHAIN if ct else ""}</span><span class="mono">{ct}</span></div>'
        for f, de, t, ct, hl in entry_rows)
    tabs = "".join(
        f'<span class="se-tab{cls}"{(" data-steps=" + chr(34) + st + chr(34)) if st else ""}>{t}</span>'
        for t, cls, st in [("Attributes", "", ""), ("Delivery and Maint.", "", ""),
                           ("Fields", " se-tab-on", _s(0, 1, 2, 3, 4, 5)),
                           ("Input Help/Check", " se-tab-on", "6"), ("Currency/Quant. Fields", "", "")])
    pairs = "".join(
        f'<div class="se-tr st-item" data-steps="{_s(4, 5)}"><span class="mono">ZCLASS</span><span class="mono">{a}</span>'
        f'<span class="mono">ZSTUDENT</span><span class="mono">{a}</span></div>' for a in ("MANDT", "CID"))
    radios = "".join(
        f'<span class="se-radio"><i class="se-dot{" st-item" if on else ""}"{(" data-steps=" + chr(34) + "5" + chr(34)) if on else ""}></i>{t}</span>'
        for t, on in [("Not specified", False), ("Non-key-fields/candidates", True),
                      ("Key fields/candidates", False), ("Key fields of a text table", False)])
    pop = (
        f'<div class="se-pop st-item" data-steps="{_s(3, 4, 5)}" role="dialog" aria-label="외래키 만들기 창">'
        '<div class="se-pop-t">Create Foreign Key <span class="mono">ZSTUDENT-CID</span></div>'
        '<div class="se-pop-b">'
        '<div class="se-frm"><span>Short text</span><span class="se-in">반 코드 체크</span></div>'
        f'<div class="se-frm"><span>Check table</span><span class="se-in se-hl mono" data-steps="3">'
        f'<span class="st-item" data-steps="{_s(3, 4, 5)}">ZCLASS</span></span>'
        f'<span class="se-btn se-hl" data-steps="4">Generate proposal</span></div>'
        '<div class="se-grid se-g4"><div class="se-th"><span>Check Table</span><span>ChkTablFld</span>'
        '<span>For.key Table</span><span>Foreign Key Field</span></div>'
        f'<div class="se-pairs se-hl" data-steps="4">{pairs}'
        f'<div class="se-tr se-empty st-item" data-steps="3"><span>비어 있어요</span></div></div></div>'
        f'<div class="se-sem se-hl" data-steps="5"><div class="se-sem-h">Foreign key field type</div>{radios}'
        '<div class="se-card"><span>Cardinality</span>'
        f'<span class="se-in se-in-s mono"><span class="st-item" data-steps="5">1</span></span>:'
        f'<span class="se-in se-in-s mono"><span class="st-item" data-steps="5">CN</span></span></div></div>'
        '</div>'
        f'<div class="se-pop-f"><span class="se-btn se-ok se-hl" data-steps="5">{CHECK}Copy</span>'
        f'<span class="se-btn">{CROSS}Cancel</span></div>'
        '</div>'
    )
    win = (
        '<div class="se-win">'
        '<div class="se-title">Dictionary: Change Table <span class="mono">ZSTUDENT</span><span class="se-badge">변경 모드</span></div>'
        f'<div class="se-tool"><span class="se-tb se-hl" data-steps="6">{SAVE}<em>Save</em></span>'
        f'<span class="se-tb se-hl" data-steps="6">{ACT}<em>Activate</em></span></div>'
        f'<div class="se-tabs">{tabs}</div>'
        f'<div class="se-body st-item" data-steps="{_s(0, 1, 2, 3, 4, 5)}">'
        f'<div class="se-ftool"><span class="se-tb">{SRCH}<em>Srch Help</em></span>'
        f'<span class="se-tb se-fkbtn se-hl" data-steps="2">{KEY}<em>Foreign Keys</em></span>'
        '<span class="se-tb"><em>Built-In Type</em></span></div>'
        '<div class="se-grid se-g4f"><div class="se-th"><span>Field</span><span>Key</span><span>Initial</span><span>Data element</span></div>'
        f'{frows}</div></div>'
        '<div class="se-body st-item" data-steps="6">'
        '<div class="se-grid se-g5"><div class="se-th"><span>Field</span><span>Data element</span><span>Type</span>'
        f'<span>FK</span><span>Check table</span></div>{erows}</div></div>'
        f'<div class="se-status"><span class="st-item" data-steps="6">{CHECK}Table ZSTUDENT was activated</span></div>'
        f'<div class="se-dim st-item" data-steps="{_s(3, 4, 5)}"></div>'
        f'{pop}'
        '</div>'
    )
    notes = "".join(
        f'<div class="st-note st-item se-note" data-steps="{i}"><b><i>{i + 1}</i>{t}</b><span>{d}</span></div>'
        for i, (t, d) in enumerate(NOTES))
    dots = "".join(f'<i class="st-dot" data-steps="{",".join(str(k) for k in range(i, n))}"></i>' for i in range(n))
    return (
        f'<figure class="diagram demo stepper se11" data-step="0" data-max="{n - 1}">'
        "<figcaption>SE11에서 외래키 걸기 · 일곱 단계</figcaption>"
        f'{win}<div class="st-notes" aria-live="polite">{notes}</div>'
        '<div class="st-foot"><div class="st-btns">'
        f'<button type="button" class="dm-btn st-run">{PLAY}실행</button>'
        f'<button type="button" class="dm-btn st-pause">{PAUSE}<span class="t-pause">정지</span><span class="t-resume">이어서</span></button>'
        f'</div><div class="st-dots" aria-hidden="true">{dots}</div></div>'
        "</figure>"
    )
