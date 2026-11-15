import base64, html, re, subprocess, sys, os, tempfile
from pathlib import Path
from markdown_it import MarkdownIt
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(TOOLS / "figures"))

# 사용법: python tools/build.py ui5 | backend | all
CLI_BOOKS = {"ui5": "ui5", "backend": "be"}
if __name__ == "__main__":
    _arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if _arg == "all":
        # 교재마다 별도 프로세스로 빌드(이 파일은 모듈 수준에서 한 교재를 빌드해요)
        for _b in CLI_BOOKS:
            subprocess.run([sys.executable, str(Path(__file__).resolve()), _b], check=True)
        import index_page
        index_page.build(ROOT)
        sys.exit(0)
    if _arg not in CLI_BOOKS:
        sys.exit("사용법: python tools/build.py [ui5|backend|all]")
    BOOK = CLI_BOOKS[_arg]


FONT_DIR = ROOT / "fonts"
_EXT_ERD = ("https://wangjagom.github.io/erd-designer/", ("erd", "teal"), "ERD 설계 도구", "ERD")
BOOKS = {
    "ui5": dict(
        src=ROOT / "content/sap-ui5/doc.md", out=ROOT / "site/sap-ui5/index.html",
        title="SAPUI5 총정리", sub="자바스크립트 기초부터 데이터 바인딩까지",
        part_max=15, term_parts=(2, 16), off=1,
        groups=[("시작하기", [0]), ("자바스크립트 기초", range(1, 7)), ("UI5 개념", range(7, 15)),
                ("문제 해결", [15]), ("개발 도구", [16]), ("부록", [17])],
        part_icons={**{i: v for i, v in __import__("icon_map2").PART.items() if i <= 15}, 16: ("keyboard", None), 17: ("folder", None)},
        coming={},
        meta="<span>2026년 11월 6일</span><span>수업 프로젝트 0108–0213 · Lev05 기준</span>",
        extras=[_EXT_ERD, ("../sap-backend/", ("db", "slate"), "SAP 백엔드 총정리", "백엔드")],
    ),
    "be": dict(
        src=ROOT / "content/sap-backend/doc.md", out=ROOT / "site/sap-backend/index.html",
        title="SAP 백엔드 총정리", sub="DB 기초부터 SQL, ABAP 데이터까지",
        part_max=6, term_parts=(1, 6), off=0,
        groups=[("시작하기", [0]), ("DB 기초", [1]), ("ABAP Dictionary", [2, 3]), ("SQL과 ABAP", [4, 5]), ("UI5 연결", [6]), ("부록", [7, 8])],
        part_icons={0: ("book", None), 1: ("table", "blue"), 2: ("db", "slate"), 3: ("chain", "indigo"), 4: ("magnifier", "indigo"), 5: ("console", "ink"), 6: ("window", "blue"), 7: ("folder", None), 8: ("book", "teal")},
        meta="<span>2026년 11월 12일</span><span>SAPUI5 총정리와 짝을 이루는 교재</span>",
        coming={},
        extras=[_EXT_ERD, ("../sap-ui5/", ("window", "blue"), "SAPUI5 총정리", "UI5")],
    ),
}
CFG = BOOKS[BOOK]
SRC, OUT = CFG["src"], CFG["out"]

md_src = SRC.read_text(encoding="utf-8")
import re as _re


def _fix_bold(text):
    """CommonMark cannot close `**…**` when it is followed directly by a Korean letter
    (e.g. `**순서**로`). Pair the `**` markers in each line in order, outside code, and
    turn those pairs into <strong> tags."""
    out, in_fence = [], False
    for line in text.split("\n"):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence or "**" not in line:
            out.append(line)
            continue
        masked = _re.sub(r"`[^`\n]*`", lambda m: "\0" * len(m.group(0)), line)
        pos = [m.start() for m in _re.finditer(r"\*\*", masked)]
        repl = {}
        for k in range(0, len(pos) - 1, 2):
            i, j = pos[k], pos[k + 1]
            if "|" in line[i + 2:j]:
                continue
            if j + 2 < len(line) and _re.match(r"[가-힣]", line[j + 2]):
                repl[i], repl[j] = "<strong>", "</strong>"
        if repl:
            res, idx = [], 0
            for q in sorted(repl):
                res.append(line[idx:q])
                res.append(repl[q])
                idx = q + 2
            res.append(line[idx:])
            line = "".join(res)
        out.append(line)
    return "\n".join(out)


md_src = _fix_bold(md_src)

# --- clean up source -------------------------------------------------------
lines = md_src.split("\n")
assert lines[0].startswith("# ")
body_md = "\n".join(lines[3:])  # drop title + byline (rebuilt in the header)

# diagram placeholders -> markers
body_md = re.sub(r"^&#91;embedded content:\s*([^\n]*?)\\\]\s*$",
                 lambda m: f"<!--DIAGRAM:{m.group(1).split(' · ')[0].strip()}-->", body_md, flags=re.M)

# --- markdown -> html ------------------------------------------------------
LANG_LABEL = {"js": "JavaScript", "xml": "XML", "sql": "SQL", "abap": "ABAP", "": "구조"}


SYNTAX_KW = ("function return if else for of in const let while async await new break continue try catch class this "
             "true false null undefined "
             "SELECT FROM WHERE ORDER BY ASC DESC GROUP INSERT INTO VALUES UPDATE SET DELETE INNER JOIN ON AS "
             "COUNT SUM AVG MAX MIN AND OR").split()
_SYN_RE = re.compile(
    r"(?P<ph>[가-힣]+[0-9]*(?: [가-힣]+[0-9]*)*)|(?P<kw>\b(?:" + "|".join(SYNTAX_KW) + r")\b)"
)


def syntax_fence(code):
    """'문법 틀' block: Korean words are fill-in slots, everything else is fixed syntax."""
    def line_html(line):
        left, sep, comment = line.partition("//")
        out, pos = [], 0
        for m in _SYN_RE.finditer(left):
            out.append(html.escape(left[pos:m.start()]))
            if m.group("ph"):
                out.append(f'<span class="ph">{html.escape(m.group("ph"))}</span>')
            else:
                out.append(f'<span class="kw">{m.group("kw")}</span>')
            pos = m.end()
        out.append(html.escape(left[pos:]))
        if sep:
            out.append(f'<span class="cm">//{html.escape(comment)}</span>')
        return "".join(out)
    inner = "\n".join(line_html(l) for l in code.split("\n"))
    return (
        '<figure class="code syntax"><figcaption><span>문법 틀</span>'
        '<span class="hint">한글로 쓴 곳은 직접 채우는 자리예요</span></figcaption>'
        f'<pre><code>{inner}</code></pre></figure>'
    )


_QUIZ_N = [0]


def _inline(t):
    return re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", html.escape(t, quote=False))


def quiz_fence(code):
    """```quiz blocks -> one-question-at-a-time multiple choice that unlocks the gate body.
    Q: text line / '| code line' / '- option' (end with ' ✓' for the answer) / '> hint shown on a wrong answer'."""
    import random
    gi = _QUIZ_N[0]; _QUIZ_N[0] += 1
    qs = []
    for blk in re.split(r"\n\s*\n", code.strip()):
        stem, opts, hint = [], [], ""
        for line in blk.split("\n"):
            if line.startswith("- "):
                t = line[2:].strip()
                ok = t.endswith("✓")
                opts.append((t[:-1].strip() if ok else t, ok))
            elif line.startswith("> "):
                hint = line[2:].strip()
            elif line.startswith("| ") or line == "|":
                stem.append(("code", line[2:]))
            elif line.startswith("Q:"):
                stem.append(("text", line[2:].strip()))
        assert len(opts) >= 2 and sum(o[1] for o in opts) == 1, blk
        random.Random(gi * 31 + len(qs) * 7 + 3).shuffle(opts)
        qs.append((stem, opts, hint))
    n = len(qs)
    parts = []
    for qi, (stem, opts, hint) in enumerate(qs):
        ans = [i for i, o in enumerate(opts) if o[1]][0]
        items, codebuf = [], []

        def flush():
            if codebuf:
                src = "\n".join(codebuf)
                st = src.lstrip()
                if st.startswith("<"):
                    lg = "xml"
                elif re.match(r"(SELECT|UPDATE|INSERT|DELETE)\b", st) and src.rstrip().endswith(";"):
                    lg = "sql"
                elif re.search(r"\b(LOOP AT|ENDLOOP|DATA|WRITE|READ TABLE|MODIFY|APPEND|SORT)\b", src):
                    lg = "abap"
                else:
                    lg = "js"
                items.append(f'<figure class="code q-fig" data-lang="{lg}"><figcaption><span>{LANG_LABEL.get(lg, lg)}</span></figcaption>'
                             f'<pre class="q-code"><code>' + hl(src, lg) + '</code></pre></figure>')
                codebuf.clear()
        first_text = True
        for kind, text in stem:
            if kind == "code":
                codebuf.append(text)
            else:
                flush()
                badge = f'<span class="q-num">문제 {qi + 1} / {n}</span>' if first_text else ""
                first_text = False
                items.append(f'<p class="q-text">{badge}{_inline(text)}</p>')
        flush()
        labels = "".join(
            f'<label class="opt"><input type="radio" name="g{gi}q{qi}" value="{i}"><span>{_inline(o[0])}</span></label>'
            for i, o in enumerate(opts))
        last = qi == n - 1
        parts.append(
            f'<div class="q" role="radiogroup" data-answer="{ans}"' + ("" if qi == 0 else " hidden") + '>'
            f'<div class="q-stem">{"".join(items)}</div>{labels}'
            f'<p class="q-hint" hidden>{_inline(hint)}</p>'
            f'<div class="quiz-bar"><button type="button" class="quiz-check" data-last="{1 if last else 0}">정답 확인</button>'
            '<p class="quiz-result" role="status" aria-live="polite"></p></div></div>')
    return ('<div class="quiz">' + "".join(parts) + '<p class="quiz-done" hidden></p>'
            '<button type="button" class="gate-skip">문제 건너뛰고 내용 보기</button></div>')


def hl(code, lang):
    """syntax-highlight js/xml (function-call names get their own class)."""
    if lang in ("js", "xml", "sql", "abap"):
        lexer = get_lexer_by_name({"js": "javascript", "xml": "xml", "sql": "sql", "abap": "abap"}[lang])
        inner = highlight(code, lexer, HtmlFormatter(nowrap=True))
        if lang == "js":
            inner = re.sub(r'<span class="nx">([A-Za-z_$][\w$]*)</span>(?=<span class="p">\()', r'<span class="nf">\1</span>', inner)
        return inner
    return html.escape(code)


def fence(code, lang):
    if lang == "quiz":
        return quiz_fence(code)
    if lang == "syntax":
        return syntax_fence(code)
    label = LANG_LABEL.get(lang, lang)
    inner = hl(code, "abap" if lang == "abap-old" else lang)
    return (
        f'<figure class="code" data-lang="{lang}"><figcaption><span>{label}</span>'
        f'<button type="button" class="copy" aria-label="코드 복사">복사</button></figcaption>'
        f'<pre><code>{inner}</code></pre></figure>'
    )


md = MarkdownIt("commonmark", {"html": True, "typographer": False}).enable("table")


def render_fence(self, tokens, idx, options, env):
    t = tokens[idx]
    return fence(t.content.rstrip("\n"), (t.info or "").strip())


md.add_render_rule("fence", render_fence)
html_body = md.render(body_md)


# old / new ABAP syntax pairs -> one code box with two tabs
def _syn_pair(m):
    new_pre, old_pre = m.group(1), m.group(2)
    return ('<figure class="code syn-pair" data-lang="abap"><figcaption>'
            '<span class="syn-tabs" role="group" aria-label="문법 고르기">'
            '<button type="button" class="syn-tab" data-set-syn="new">요즘 문법 <small>7.40+</small></button>'
            '<button type="button" class="syn-tab" data-set-syn="old">옛 문법</button></span>'
            '<button type="button" class="copy" aria-label="코드 복사">복사</button></figcaption>'
            f'<pre class="syn-pane syn-new">{new_pre}</pre><pre class="syn-pane syn-old">{old_pre}</pre></figure>')


html_body, _n_pairs = re.subn(
    r'<figure class="code" data-lang="abap"><figcaption>(?:(?!</figcaption>).)*</figcaption><pre>((?:(?!</pre>).)*)</pre></figure>\s*'
    r'<figure class="code" data-lang="abap-old"><figcaption>(?:(?!</figcaption>).)*</figcaption><pre>((?:(?!</pre>).)*)</pre></figure>',
    _syn_pair, html_body, flags=re.S)
assert 'data-lang="abap-old"' not in html_body, "unpaired abap-old block"

# task list items
html_body = html_body.replace("<li>[ ] ", '<li class="task"><span class="tick" aria-hidden="true"></span>')

# project tags like [0205], [0108~0202], [0220, Lev05] outside <pre>
parts = re.split(r"(<pre>.*?</pre>)", html_body, flags=re.S)
tag_re = re.compile(r"\[((?:0\d{3}|Lev05)(?:[~,\s]*(?:0\d{3}|Lev05))*)\]")
for i, p in enumerate(parts):
    if not p.startswith("<pre>"):
        parts[i] = tag_re.sub(lambda m: f'<span class="tag">{m.group(1).replace("~", "–")}</span>', p)
html_body = "".join(parts)

# tables scroll on their own
html_body = html_body.replace("<table>", '<div class="table-wrap"><table>').replace("</table>", "</table></div>")

# diagrams and interactive demos
import icon3d as _icon3d
import registry as _registry
for key, fn in _registry.figures().items():
    html_body = html_body.replace(f"<!--DIAGRAM:{key}-->", fn())
assert "<!--DIAGRAM:" not in html_body, re.findall(r"<!--DIAGRAM:[^>]*-->", html_body)

# headings: ids + part eyebrows, collect TOC
toc = []
sec = 0


def h2(m):
    global sec
    text = m.group(1)
    sid = f"part-{sec}"
    sec += 1
    plain = re.sub(r"<[^>]+>", "", re.sub(r'\s*<span class="tag">.*?</span>', "", text)).strip()
    mm = re.match(r"^(\d+부|부록)\.\s*(.*)$", plain)
    if mm:
        eyebrow, title = mm.group(1), mm.group(2)
    else:
        eyebrow, title = "시작", plain
    title_html = re.sub(r"^(\d+부|부록)\.\s*", "", text)
    short = re.split(r"\s—\s", title)[0]
    short = re.sub(r"<[^>]+>", "", short)
    toc.append((sid, eyebrow, short))
    close = "</section>\n" if sec > 1 else ""
    return (f'{close}<section class="part" id="{sid}" aria-labelledby="{sid}-h">'
            f'<h2 id="{sid}-h"><span class="eyebrow">{eyebrow}</span><span class="h2t">{title_html}</span></h2>')


html_body = re.sub(r"<h2>(.*?)</h2>", h2, html_body) + "</section>"

h3n = 0
cur_sec = {"id": None}
h3_by_sec = {}


def h3(m):
    global h3n
    h3n += 1
    hid = f"s{h3n}"
    text = m.group(1)
    plain = re.sub(r"<[^>]+>", "", re.sub(r'\s*<span class="tag">.*?</span>', "", text)).strip()
    return (f'<h3 id="{hid}" data-plain="{html.escape(html.unescape(plain))}">'
            f'<a class="anchor" href="#{hid}" aria-hidden="true" tabindex="-1">#</a>{text}</h3>')


html_body = re.sub(r"<h3>(.*?)</h3>", h3, html_body)


# --- paged site: cross-reference links + prev/next pager ---------------------
SKIP_TAGS = {"pre", "code", "a", "h2", "h3", "script", "style", "svg", "figcaption", "button"}


_ALIASES = {"함수 기본": ["함수"], "async / await": ["async/await", "async"], "Dialog 팝업": ["Dialog"], "id와 byId": ["byId"],
            "컨트롤러 파일 읽기": ["컨트롤러 파일"], "바인딩 전": ["바인딩"], "프로젝트 폴더 구조": ["폴더 구조"],
            "기본 모델과 이름 있는 모델": ["이름 있는 모델", "기본 모델"], "XML View 읽는 법": ["XML View"],
            "정렬과 간격": ["정렬 설정"], "배열 vs 객체": ["배열과 객체의 차이"]}


def concept_heads(htm):
    """{part number N: [(phrase, h3 id), ...]} so that '3부 배열 메서드' can link to that section."""
    heads = {}
    for sm in re.finditer(r'<section class="part" id="part-(\d+)".*?(?=<section class="part"|\Z)', htm, flags=re.S):
        n = int(sm.group(1)) - CFG["off"]
        lst = []
        for hid, plain in re.findall(r'<h3 id="(s\d+)" data-plain="([^"]*)"', sm.group(0)):
            plain = html.unescape(plain).strip()
            head = re.split(r":| — |\(| \{", plain)[0].strip()
            cands = {head} | set(_ALIASES.get(head, []))
            lst += [(c, hid) for c in cands if c]
        heads[n] = sorted(lst, key=lambda t: -len(t[0]))
    return heads


def link_parts(htm):
    """Turn '3부' into a link to that page, and '3부 배열 메서드' into a link to that concept's section."""
    heads = concept_heads(htm)

    def link(piece):
        out, pos = [], 0
        for m in re.finditer(r"(?<![\d~–\-])(\d{1,2})부(?!록|터|분)", piece):
            n = int(m.group(1))
            if not 0 <= n <= CFG["part_max"] or m.start() < pos:
                continue
            _pre = piece[max(0, m.start() - 8):m.start()]
            if _pre.endswith("총정리 ") or _pre.endswith("UI5 "):
                continue
            out.append(piece[pos:m.start()])
            rest = piece[m.end():]
            mm = re.match(r"(의)? ", rest)
            target, label_end, shown = f"#part-{n + CFG['off']}", m.end(), piece[m.start():m.end()]
            title = f"{n}부로 이동"
            if mm:
                after = rest[mm.end():]
                for phrase, hid in heads.get(n, []):
                    if after.startswith(phrase):
                        target, shown = f"#{hid}", phrase
                        title = f"{n}부 · {phrase}"
                        label_end = m.end() + mm.end() + len(phrase)
                        break
            out.append(f'<a class="xref" href="{target}" title="{title}">{shown}</a>')
            pos = label_end
        out.append(piece[pos:])
        return "".join(out)

    out, depth = [], 0
    for piece in re.split(r"(<[^>]+>)", htm):
        if piece.startswith("<"):
            mt = re.match(r"<(/?)([a-zA-Z0-9]+)", piece)
            if mt and mt.group(2).lower() in SKIP_TAGS and not piece.endswith("/>"):
                depth += -1 if mt.group(1) else 1
            out.append(piece)
        elif depth <= 0:
            out.append(link(piece))
        else:
            out.append(piece)
    return "".join(out)


# Words that link (first mention per concept page) to the concept that explains them. Backward links only.
TERMS = [
    ("변수", 1, "변수"), ("자료형", 1, "자료형"), ("문자열", 1, "문자열"), ("형 변환", 1, "형 변환"),
    ("객체", 1, "객체"), ("배열", 1, "배열"), ("JSON", 1, "JSON"),
    ("반복문", 2, "반복문"), ("삼항 연산자", 2, "삼항 연산자"),
    ("함수", 3, "함수"), ("콜백 함수", 3, "콜백 함수"), ("콜백", 3, "콜백 함수"), ("화살표 함수", 3, "화살표 함수"),
    ("배열 메서드", 3, "배열 메서드"), ("메서드", 4, "메서드"), ("메서드 체이닝", 4, "메서드 체이닝"), ("스코프", 4, "스코프"),
    ("Promise", 5, "Promise"), ("async / await", 5, "async / await"), ("async/await", 5, "async / await"),
    ("이벤트 객체", 6, "이벤트 객체"), ("헝가리안 표기", 6, "변수 이름 규칙"),
    ("Fragment", 7, "Fragment"), ("Dialog", 7, "Dialog 팝업"), ("여백 클래스", 7, "여백 클래스"),
    ("바인딩", 8, "바인딩"), ("이름 있는 모델", 8, "이름 있는 모델"), ("바인딩 컨텍스트", 9, "바인딩 컨텍스트"),
    ("포매터", 11, "포매터"), ("Expression Binding", 12, "Expression Binding"),
]
if BOOK != "ui5":
    TERMS = []
AUTO_SKIP = SKIP_TAGS | {"summary", "kbd", "th", "figure"}
AUTO_MAX = 5


def auto_terms(htm):
    heads = concept_heads(htm)
    table = {}
    for term, n, head in TERMS:
        hid = next((h for ph, h in heads.get(n, []) if ph == head), None)
        if hid:
            table[term] = (hid, int(hid[1:]), n, head)
    if not table:
        return htm
    rx = re.compile(r"(?<![가-힣A-Za-z0-9_])(" + "|".join(re.escape(t) for t in sorted(table, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")

    def run(text, cur, seen):
        def sub(m):
            term = m.group(1)
            hid, num, n, head = table[term]
            key = hid
            if num >= cur or key in seen or len(seen) >= AUTO_MAX:
                if num >= cur:
                    return m.group(0)
                return m.group(0)
            seen.add(key)
            return f'<a class="xref term" href="#{hid}" title="{n}부 · {head}">{term}</a>'
        return rx.sub(sub, text)

    out = []
    part_no, cur, seen, depth = None, None, set(), 0
    for chunk in re.split(r'(<section class="part" id="part-\d+"[^>]*>|<h3 id="s\d+"[^>]*>)', htm):
        mp = re.match(r'<section class="part" id="part-(\d+)"', chunk)
        mh = re.match(r'<h3 id="s(\d+)"', chunk)
        if mp:
            part_no, cur, depth = int(mp.group(1)), None, 0
            out.append(chunk); continue
        if mh:
            cur, seen, depth = int(mh.group(1)), set(), 1
            out.append(chunk); continue
        if cur is None or part_no is None or not CFG["term_parts"][0] <= part_no <= CFG["term_parts"][1]:
            out.append(chunk); continue
        for piece in re.split(r"(<[^>]+>)", chunk):
            if piece.startswith("<"):
                mt = re.match(r"<(/?)([a-zA-Z0-9]+)", piece)
                if mt and mt.group(2).lower() in AUTO_SKIP and not piece.endswith("/>"):
                    depth += -1 if mt.group(1) else 1
                out.append(piece)
            elif depth <= 0:
                out.append(run(piece, cur, seen))
            else:
                out.append(piece)
    return "".join(out)


def page_label(i):
    _, eyebrow, short = toc[i]
    return short if eyebrow in ("시작", "부록") else f"{eyebrow} · {short}"


import sys
from toss_icons import use as _icon_use, defs_svg as _icon_defs
from icon_map2 import CONCEPT as _IC_CONCEPT
_IC_PART = CFG["part_icons"]
ICONS_USED = set()
COMING_IDS = set(CFG["coming"])  # parts shown as 추가 예정 (content kept, hidden)
UNMAPPED = []


def _head_of(plain):
    return re.split(r" \{", html.unescape(plain).split(":")[0].strip())[0].strip()


def _ic(key, cls, flat=False):
    mode = "D" if flat else "E"
    ICONS_USED.add((key[0], key[1], mode))
    return _icon_use(key[0], key[1], mode, cls)


def _concept_icon(plain, part_idx, cls, flat=False):
    key = _IC_CONCEPT.get(_head_of(plain))
    if key is None:
        UNMAPPED.append(_head_of(plain))
        key = _IC_PART[part_idx]
    return _ic(key, cls, flat)


def _first_sentence(chunk_html):
    m = re.search(r"<p>(.*?)</p>", chunk_html, flags=re.S)
    if not m:
        return ""
    t = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip()
    t = re.split(r"(?<=[.!?])\s", t)[0]
    return t if len(t) <= 78 else t[:76].rstrip() + "…"


def _head_wrap(ch, ic_html):
    i = ch.index("</h3>") + 5
    return f'<div class="c-head">{ic_html}{ch[:i]}</div>{ch[i:]}'


def build_pages(htm):
    """Split every part into a part page (intro + concept list) and one page per concept (h3)."""
    secs = []
    for m in re.finditer(r'<section class="part" id="(part-\d+)"[^>]*>(.*?)</section>', htm, flags=re.S):
        sid, inner = m.group(1), m.group(2)
        h2m = re.match(r"\s*(<h2 .*?</h2>)(.*)", inner, flags=re.S)
        h2_html, rest = h2m.group(1), h2m.group(2)
        chunks = re.split(r'(?=<h3 id="s\d+")', rest)
        intro, concepts = chunks[0], []
        for ch in chunks[1:]:
            hm = re.match(r'<h3 id="(s\d+)" data-plain="([^"]*)"', ch)
            plain = html.unescape(hm.group(2)).strip()
            concepts.append((hm.group(1), plain, ch))
        secs.append(dict(sid=sid, idx=int(sid.split("-")[1]), h2=h2_html, intro=intro, concepts=concepts, span=m.span()))
    # reading order of every page in the book
    pages = []
    for sc in secs:
        pages.append((sc["sid"], page_label(sc["idx"])))
        for hid, plain, _ in ([] if sc["sid"] in COMING_IDS else sc["concepts"]):
            pages.append((hid, f'{toc[sc["idx"]][1]} · {plain.split(":")[0].strip()}' if toc[sc["idx"]][1] not in ("시작", "부록")
                          else plain.split(":")[0].strip()))
    pos = {pid: k for k, (pid, _) in enumerate(pages)}

    def pager(pid):
        if pid not in pos:
            return '<nav class="pager" aria-label="페이지 이동"></nav>'
        k = pos[pid]
        prev_html = next_html = ""
        if k > 0:
            prev_html = (f'<a class="prev" href="#{pages[k - 1][0]}"><span class="dir">← 이전</span>'
                         f'<span class="ttl">{html.escape(pages[k - 1][1])}</span></a>')
        if k < len(pages) - 1:
            next_html = (f'<a class="next" href="#{pages[k + 1][0]}"><span class="dir">다음 →</span>'
                         f'<span class="ttl">{html.escape(pages[k + 1][1])}</span></a>')
        return f'<nav class="pager" aria-label="페이지 이동">{prev_html}{next_html}</nav>'

    out, last = [], 0
    for sc in secs:
        a, b = sc["span"]
        out.append(htm[last:a]); last = b
        sid = sc["sid"]
        crumb = html.escape(page_label(sc["idx"]))
        lst = ""
        if sc["concepts"]:
            items = "".join(
                f'<li><a href="#{hid}">{_concept_icon(plain, sc["idx"], "cl-ic", True)}<span class="cl-body">'
                f'<span class="cl-t">{html.escape(plain.split(":")[0].strip())}</span>'
                f'<span class="cl-d">{html.escape(_first_sentence(ch))}</span></span></a></li>'
                for n, (hid, plain, ch) in enumerate(sc["concepts"], 1))
            lst = (f'<nav class="concept-list" aria-label="이 부의 개념"><p class="cl-title">이 부에서 배울 개념 {len(sc["concepts"])}개</p>'
                   f'<ol>{items}</ol></nav>')
        cons = "".join(
            f'<div class="concept" id="c-{hid}"><p class="crumb"><a href="#{sid}">{crumb}</a></p>'
            f'{_head_wrap(ch, _concept_icon(plain, sc["idx"], "c-ic"))}{pager(hid)}</div>'
            for hid, plain, ch in sc["concepts"])
        out.append(f'<section class="part" id="{sid}" aria-labelledby="{sid}-h"><div class="part-head">{_ic(_IC_PART[sc["idx"]], "p-ic")}{sc["h2"]}</div>{sc["intro"]}{lst}{cons}'
                   f'<nav class="pager part-pager" aria-label="페이지 이동">{pager(sid)[len('<nav class="pager" aria-label="페이지 이동">'):-6]}</nav></section>')
    out.append(htm[last:])
    return "".join(out)



# ---- keycaps (<kbd>) and extension icons ----
_KEYWORDS = {"Ctrl", "Shift", "Alt", "Tab", "Enter", "Esc", "Home", "End", "Cmd", "Win", "Space", "Backspace", "Delete",
             "PageUp", "PageDown", "↑", "↓", "←", "→"} | {f"F{i}" for i in range(1, 13)}
_LABELS = {"마우스 휠"}


def _key_ok(t):
    return t in _KEYWORDS or t in _LABELS or (len(t) == 1 and not t.isspace())


def _keycaps_one(m):
    raw = html.unescape(m.group(1))
    if " → " in raw:
        chord = raw.split(" → ")
    else:
        chord = [raw]
    groups = []
    for c in chord:
        keys = c.split(" + ")
        if not all(_key_ok(k) for k in keys):
            return m.group(0)
        groups.append(keys)
    flat = [k for g in groups for k in g]
    if len(flat) == 1 and flat[0] not in _KEYWORDS:
        return m.group(0)
    def cap(k):
        return f'<span class="kl">{html.escape(k)}</span>' if k in _LABELS else f'<kbd>{html.escape(k)}</kbd>'
    parts = ['<i class="plus">+</i>'.join(cap(k) for k in g) for g in groups]
    return '<span class="keys" role="text">' + '<i class="then">후</i>'.join(parts) + '</span>'


def keycaps(htm):
    # 7부 (part-8) writes UI5 values such as `End` / `Center`; those are not keyboard keys.
    bits = re.split(r'(?=<section class="part" id="part-\d+")', htm)
    return "".join(b if b.startswith('<section class="part" id="part-8"') else
                   re.sub(r"<code>([^<]+)</code>", _keycaps_one, b) for b in bits)


def ext_icons(htm):
    def one(m):
        obj, hue, name = m.group(1), m.group(2) or None, m.group(3).strip()
        return f'<span class="ext">{_ic((obj, hue), "ext-ic", True)}<span class="ext-n">{name}</span></span>'
    return re.sub(r"\{\{ic:(\w+):?(\w*)\}\}\s*([^<]*)", one, htm)



def label_tables(htm):
    """add data-label to every cell (for stacked mobile cards) and data-cols to the table."""
    def one(m):
        t = m.group(0)
        heads = [html.unescape(re.sub(r"<[^>]+>", "", h)).strip() for h in re.findall(r"<th[^>]*>(.*?)</th>", t, flags=re.S)]
        if not heads:
            return t
        if all(re.fullmatch(r"[A-Z][A-Z0-9_]*(?: \(키\))?", h) or not h for h in heads) and any(heads):
            return t.replace("<table>", '<table class="dbt">', 1)
        def row(rm):
            cells = iter(range(len(heads)))
            def td(cm):
                i = next(cells, None)
                lab = html.escape(heads[i], quote=True) if i is not None and heads[i] else ""
                return f'<td data-label="{lab}"{cm.group(1)}>' if lab else cm.group(0)
            return re.sub(r"<td([^>]*)>", td, rm.group(0))
        t = re.sub(r"<tr>.*?</tr>", row, t, flags=re.S)
        t = re.sub(r"(<td[^>]*>)(.*?)(</td>)", r'\1<span class="cv">\2</span>\3', t, flags=re.S)
        return t.replace("<table>", f'<table data-cols="{len(heads)}">', 1)
    return re.sub(r"<table>.*?</table>", one, htm, flags=re.S)


html_body = label_tables(html_body)


def tips(htm):
    """{? 설명 ?} -> small "?" help tip right after the word."""
    return re.sub(r"\{\?\s(.+?)\s\?\}",
                  lambda m: '<span class="tip" tabindex="0" role="button" aria-label="설명 보기">?<span class="tip-body">' + m.group(1) + "</span></span>",
                  htm, flags=re.S)


def li_titles(htm):
    """List items that start with a bold sentence: put that title on its own line."""
    return re.sub(r"<li>(<p>)?<strong>((?:(?!</strong>).)*?[.!?][\"”)]?)</strong>(?=\s*\S)",
                  lambda m: "<li>" + (m.group(1) or "") + '<strong class="li-t">' + m.group(2) + "</strong>",
                  htm, flags=re.S)


html_body = tips(html_body)
html_body = li_titles(html_body)


def wrap_fix(htm):
    """Keep ")" together with a following Korean particle and keep short inline code in one piece."""
    parts = re.split(r"(<pre\b.*?</pre>|<script\b.*?</script>|<style\b.*?</style>|<[^>]*>)", htm, flags=re.S)
    for i, seg in enumerate(parts):
        if i % 2 == 0:
            parts[i] = re.sub(r"([)\]])(?=[가-힣])", "\\1\u2060", seg)
    htm = "".join(parts)
    htm = re.sub(r"<code>((?:[^<&]|&\w+;){1,16})</code>", r'<code class="nw">\1</code>', htm)
    return htm


html_body = wrap_fix(html_body)
html_body = re.sub(r"<p><strong>((?:(?!</strong>).)*?[.!?][\"”)]?)</strong>(?=\s+[^<\s])",
                   lambda m: '<p><strong class="li-t">' + m.group(1) + "</strong>", html_body, flags=re.S)
html_body = ext_icons(keycaps(html_body))
html_body = auto_terms(link_parts(html_body))
html_body = build_pages(html_body)
print('unmapped icons:', sorted(set(UNMAPPED)))
# collect h3 per section
for sm in re.finditer(r'<section class="part" id="(part-\d+)".*?(?=<section class="part"|\Z)', html_body, flags=re.S):
    h3_by_sec[sm.group(1)] = re.findall(r'<h3 id="(s\d+)" data-plain="([^"]*)"', sm.group(0))

GROUPS = CFG["groups"]


_SVG_CHEV = ('<svg class="chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M6 3.5l4.5 4.5L6 12.5" '
             'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
_SVG_FOLDER = ('<svg class="ico ico-folder" viewBox="0 0 16 16" width="16" height="16" aria-hidden="true"><path d="M2 4.5A1.5 1.5 0 0 1 3.5 3h2.6l1.4 1.6h5A1.5 1.5 0 0 1 14 6.1v5.4a1.5 1.5 0 0 1-1.5 1.5h-9A1.5 1.5 0 0 1 2 11.5z" '
               'fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round"/></svg>')
_SVG_FILE = ('<svg class="ico ico-file" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M4 2.5h5l3 3v8H4zM9 2.5v3h3" '
             'fill="none" stroke="currentColor" stroke-width="1.3" stroke-linejoin="round" stroke-linecap="round"/></svg>')


def toc_block(cls):
    out = []
    for gname, idxs in GROUPS:
        def sub(i):
            hs = h3_by_sec.get(toc[i][0], [])
            if not hs:
                return ""
            return '<div class="toc-sub-wrap"><ul class="toc-sub">' + "".join(
                f'<li><a href="#{hid}"><span class="toc-t">{html.escape(html.unescape(pl).split(":")[0].strip())}</span></a></li>'
                for hid, pl in hs) + '</ul></div>'

        def row(i):
            has = bool(h3_by_sec.get(toc[i][0]))
            num = toc[i][1] if toc[i][1] not in ("시작", "부록") else ""
            btn = (f'<button type="button" class="tree-btn" aria-expanded="false" aria-label="{html.escape(toc[i][2])} 펼치기·접기">{_SVG_CHEV}</button>'
                   if has else '<span class="tree-btn tree-gap"></span>')
            return (f'<li class="tree-item{" has-sub" if has else ""}" data-part="{toc[i][0]}"><div class="tree-row">{btn}'
                    f'<a href="#{toc[i][0]}"><span class="toc-num">{num}</span><span class="toc-t">{html.escape(toc[i][2])}</span></a></div>{sub(i)}</li>')
        items = "".join(row(i) for i in idxs)
        out.append(f'<div class="toc-group open"><button type="button" class="toc-head" aria-expanded="true">{_SVG_CHEV}<span>{gname}</span></button>'
                   f'<div class="toc-sub-wrap group-wrap"><ul class="{cls}">{items}</ul></div></div>')
    _EXT_SVG = ('<svg class="ext" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
                '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>')
    _items = "".join('<li class="tree-item"><div class="tree-row"><span class="tree-btn tree-gap"></span>'
                     f'<a href="{u}" target="_blank" rel="noopener" class="ext-link" title="새 창에서 열기"><span class="toc-ic">' + _ic(ic, "t-ic", True) + f'</span><span class="toc-t">{lab}</span>' + _EXT_SVG + '</a></div></li>'
                     for u, ic, lab, _s in CFG["extras"])
    out.append('<div class="toc-group open tool-group"><button type="button" class="toc-head" aria-expanded="true">' + _SVG_CHEV + '<span>부가 기능</span></button>'
               '<div class="toc-sub-wrap group-wrap"><ul class="' + cls + '">' + _items + '</ul></div></div>')
    return "".join(out)


toc_html = toc_block("toc")
rail_html = "".join(
    f'<a href="#{toc[i][0]}" title="{html.escape(toc[i][2])}">'
    f'{toc[i][1] if toc[i][1] not in ("시작", "부록") else ("안내" if toc[i][1] == "시작" else "부록")}</a>'
    for i in range(len(toc))) + "".join(f'<a href="{u}" target="_blank" rel="noopener" title="{lab} (새 창)" class="rail-ic">' + _ic(ic, "t-ic", True) + '</a>' for u, ic, lab, _s in CFG["extras"])
otp_html = "".join(
    f'<ul class="otp-list" data-sec="{sid}"' + (' hidden' if j else '') + '>' +
    "".join(f'<li><a href="#{hid}">{p}</a></li>' for hid, p in ([] if sid in COMING_IDS else h3_by_sec.get(sid, []))) + '</ul>'
    for j, (sid, _, _) in enumerate(toc))

# --- pygments token colours via tokens -------------------------------------
# --- parts marked "추가 예정": content stays in doc.md and in the page, only hidden behind a notice
COMING = CFG["coming"]
for _cid, _msg in COMING.items():
    _m = re.search(r'<section class="part" id="' + _cid + r'"([^>]*)>(.*?</div>)', html_body, flags=re.S)
    html_body = (html_body[:_m.start()] + f'<section class="part coming" id="{_cid}"{_m.group(1)}>{_m.group(2)}'
                 + f'<div class="coming-box"><p class="cb-t">추가 예정</p><p>{_msg}</p></div>' + html_body[_m.end():])
    toc_html = re.sub(r'(<li class="tree-item[^"]*)("[^>]*data-part="' + _cid + r'"[^>]*>.*?<span class="toc-t">[^<]*</span>)',
                      r'\1 coming\2<span class="soon">추가 예정</span>', toc_html, flags=re.S)

# --- font subset -------------------------------------------------------------
TITLE = CFG["title"]
META = CFG["meta"]
SUB = CFG["sub"]
all_text = re.sub(r"<[^>]+>", "", html_body) + TITLE + SUB + re.sub(r"<[^>]+>", "", toc_html) + \
    "문제 건너뛰고 내용 보기아래 내용이 열렸어요.모두 맞혔어요!목차이 부분에서시작하기자바스크립트 기초UI5 개념문제 해결↑#복사됨복사 실패맨 위로부가 기능ERD 설계 도구SAPUI5 총정리SAP 백엔드 총정리DB와 SQLABAP개발 도구새 창 2026년 11월 12일SAPUI5 총정리와 짝을 이루는 교재2026년 11월 6일수업 프로젝트 0108–0213 · Lev05 기준부록시작0123456789"
chars = "".join(sorted(set(html.unescape(all_text)) | set(" !\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~·–—→←✓")))
_TMP = Path(tempfile.mkdtemp(prefix="facula_font_"))
(_TMP / "chars.txt").write_text(chars, encoding="utf-8")
faces = []
for w, name in [(400, "Regular"), (600, "SemiBold"), (700, "Bold")]:
    out = str(_TMP / f"p-{w}.woff")
    subprocess.run([sys.executable, "-m", "fontTools.subset", str(FONT_DIR / f"Pretendard-{name}.otf"),
                    f"--text-file={_TMP / 'chars.txt'}", "--flavor=woff",
                    "--layout-features=*", f"--output-file={out}"], check=True)
    b64 = base64.b64encode(open(out, "rb").read()).decode()
    faces.append(f"@font-face{{font-family:'Pretendard';font-weight:{w};font-style:normal;font-display:swap;"
                 f"src:url(data:font/woff;base64,{b64}) format('woff');}}")

css = (TOOLS / "assets" / "style.css").read_text(encoding="utf-8")
js = (TOOLS / "assets" / "app.js").read_text(encoding="utf-8")

page = f"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLE}</title>
<script>document.documentElement.className += " paged"; try {{ if (localStorage.getItem("sideCollapsed") === "1") document.documentElement.className += " side-collapsed"; }} catch (e) {{}}</script>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600&amp;display=swap" rel="stylesheet">
<style>
{''.join(faces)}
{css}
</style>
</head>
<body>
<script>try{{if(localStorage.getItem("abapSyn")!=="new")document.documentElement.dataset.syn="old"}}catch(e){{document.documentElement.dataset.syn="old"}}</script>
<header class="m-bar"><button class="m-menu" type="button" aria-label="목차 열기" aria-controls="m-drawer" aria-expanded="false"><svg width='22' height='22' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' aria-hidden='true'><path d='M4 7h16M4 12h16M4 17h16'/></svg><span>목차</span></button><span class="m-cur" aria-live="polite"></span></header>
<div class="m-scrim"></div>
<aside class="m-drawer" id="m-drawer" aria-label="목차" aria-hidden="true"><div class="m-drawer-head"><b>목차</b><button class="m-close" type="button" aria-label="목차 닫기"><svg width='20' height='20' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' aria-hidden='true'><path d='M6 6l12 12M18 6L6 18'/></svg></button></div><nav>{toc_html}</nav></aside>
{_icon_defs(ICONS_USED)}{_icon3d.ns_defs()}
<a class="skip" href="#main">본문으로 건너뛰기</a>
<div class="shell">
  <aside class="sidebar" id="sidebar" aria-label="목차">
    <div class="side-stack">
      <div class="side-inner">
        <div class="brand-row">
          <a class="brand" href="#part-0">{TITLE}</a>
          <button class="side-toggle" type="button" aria-label="목차 접기" title="목차 접기" aria-controls="sidebar" aria-expanded="true"><svg width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><rect x='3' y='4' width='18' height='16' rx='2'/><path d='M9 4v16'/></svg></button>
        </div>
        <nav>{toc_html}</nav>
      </div>
      <nav class="rail" aria-label="부 바로가기">
        <button class="side-toggle" type="button" aria-label="목차 펼치기" title="목차 펼치기" aria-controls="sidebar" aria-expanded="false"><svg width='18' height='18' viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' stroke-linecap='round' stroke-linejoin='round' aria-hidden='true'><rect x='3' y='4' width='18' height='16' rx='2'/><path d='M9 4v16'/></svg></button>
        <div class="rail-list">{rail_html}</div>
      </nav>
    </div>
  </aside>
  <main id="main" class="content">
    <div class="content-grid">
      <div class="col">
        <header class="masthead">
          <p class="kicker">SAP CODE 스터디 자료</p>
          <h1>{TITLE}</h1>
          <p class="sub">{SUB}</p>
          <p class="meta">{META}</p>
        </header>
        <article class="prose">
{html_body}
        </article>
        <footer class="foot"><a href="#main">맨 위로 ↑</a></footer>
      </div>
      <aside class="otp" aria-label="이 부분의 소제목">
        <div class="otp-inner">
          <p class="otp-title">이 부의 개념</p>
          {otp_html}
        </div>
      </aside>
    </div>
  </main>
</div>
<script>
{js}
</script>
</body>
</html>
"""
import refpeek as _refpeek
if BOOK == "be":
    _peek = _refpeek.assets(_refpeek.BE, ".concept", "이 섹션에서 쓰는 테이블", models=_refpeek.MODELS)
else:
    _peek = _refpeek.assets(_refpeek.UI5, ".concept", None, code_only=True)
page = page.replace("</body>", _peek + "\n</body>", 1)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(page, encoding="utf-8", newline="\n")
import shutil; shutil.rmtree(_TMP, ignore_errors=True)
print("bytes", len(page.encode()), "sections", len(toc), "h3", h3n)
