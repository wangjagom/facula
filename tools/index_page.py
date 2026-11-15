"""site/index.html(첫 화면)과 단독 페이지 복사. content/site.json 의 카드 목록으로 만들어요."""
import base64, html, json, shutil, subprocess, sys, tempfile
from pathlib import Path

CSS = """
:root{--bg:#fff;--ink:#030712;--ink-2:#374151;--muted:#6b7280;--line:rgb(3 7 18/.07);--line-strong:rgb(3 7 18/.16);
--wash:#f9fafb;--accent:#0ea5e9;--accent-ink:#0369a1;--accent-soft:rgb(14 165 233/.1);
--font-body:'Pretendard',-apple-system,BlinkMacSystemFont,'Apple SD Gothic Neo','Malgun Gothic',sans-serif;color-scheme:light}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink-2);font-family:var(--font-body);font-size:16.5px;line-height:1.85;
letter-spacing:-.012em;word-break:keep-all;overflow-wrap:anywhere;-webkit-font-smoothing:antialiased}
main{max-width:760px;margin:0 auto;padding:72px 24px 96px}
.kicker{margin:0 0 8px;font-size:14px;font-weight:600;color:var(--accent);line-height:1.5}
h1{margin:0;color:var(--ink);font-size:40px;line-height:1.3;font-weight:700;letter-spacing:-.028em}
.intro{margin:12px 0 40px}
h2{margin:40px 0 12px;font-size:14px;font-weight:600;color:var(--muted)}
.cards{display:grid;gap:12px;padding:0;margin:0;list-style:none}
.card{display:block;padding:20px 22px;border:1px solid var(--line-strong);border-radius:14px;background:var(--bg);
color:inherit;text-decoration:none;font-weight:400;transition:background .15s,border-color .15s}
.card:hover{background:var(--wash);border-color:var(--accent)}
.card:focus-visible{outline:2px solid var(--accent);outline-offset:2px}
.card .tag{display:inline-block;margin-bottom:4px;padding:0 8px;border-radius:999px;background:var(--accent-soft);
color:var(--accent-ink);font-size:12.5px;font-weight:600;line-height:1.7}
.card b{display:block;color:var(--ink);font-size:18px;font-weight:700;line-height:1.5}
.card span.d{display:block;font-size:15px;color:var(--ink-2);line-height:1.6}
footer{margin-top:56px;font-size:13.5px;color:var(--muted)}
@media(max-width:560px){main{padding:48px 20px 72px}h1{font-size:32px}}
"""


def _fonts(text: str, root: Path) -> str:
    chars = "".join(sorted(set(text) | set(" !\"#$%&'()*+,-./:;<=>?@[]()·–—→←0123456789")))
    tmp = Path(tempfile.mkdtemp(prefix="facula_idx_"))
    (tmp / "chars.txt").write_text(chars, encoding="utf-8")
    faces = []
    for w, name in [(400, "Regular"), (600, "SemiBold"), (700, "Bold")]:
        out = tmp / f"p-{w}.woff"
        subprocess.run([sys.executable, "-m", "fontTools.subset", str(root / "fonts" / f"Pretendard-{name}.otf"),
                        f"--text-file={tmp / 'chars.txt'}", "--flavor=woff", "--layout-features=*",
                        f"--output-file={out}"], check=True)
        b64 = base64.b64encode(out.read_bytes()).decode()
        faces.append(f"@font-face{{font-family:'Pretendard';font-weight:{w};font-style:normal;font-display:swap;"
                     f"src:url(data:font/woff;base64,{b64}) format('woff');}}")
    shutil.rmtree(tmp, ignore_errors=True)
    return "".join(faces)


def build(root: Path) -> None:
    root = Path(root)
    cfg = json.loads((root / "content" / "site.json").read_text(encoding="utf-8"))
    site = root / "site"
    site.mkdir(exist_ok=True)

    # 손으로 만든 단독 페이지(content/<slug>/index.html, doc.md 없음)는 그대로 복사
    for card in cfg["cards"]:
        src = root / "content" / card["slug"]
        if not (src / "doc.md").exists() and (src / "index.html").exists():
            dst = site / card["slug"]
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst)

    e = html.escape
    cards = "".join(
        f'<li><a class="card" href="{e(c["slug"])}/"><span class="tag">{e(c.get("tag", ""))}</span>'
        f'<b>{e(c["title"])}</b><span class="d">{e(c["desc"])}</span></a></li>' for c in cfg["cards"])
    links = "".join(
        f'<li><a class="card" href="{e(l["url"])}" target="_blank" rel="noopener"><b>{e(l["title"])} ↗</b>'
        f'<span class="d">{e(l["desc"])}</span></a></li>' for l in cfg.get("links", []))
    body = (f'<main><p class="kicker">학습 노트</p><h1>{e(cfg["title"])}</h1>'
            f'<p class="intro">{e(cfg["tagline"])}<br>{e(cfg["intro"])}</p>'
            f'<h2>교재</h2><ul class="cards">{cards}</ul>'
            + (f'<h2>도구</h2><ul class="cards">{links}</ul>' if links else "")
            + '<footer>글은 CC BY-NC-SA 4.0 · 코드는 MIT · 글꼴 Pretendard(OFL)</footer></main>')
    import re
    text = re.sub(r"<[^>]+>", "", html.unescape(body)) + cfg["title"] + "학습 노트도구교재"
    page = (f'<!DOCTYPE html><html lang="ko"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{e(cfg["title"])}</title><style>{_fonts(text, root)}{CSS}</style></head><body>{body}</body></html>')
    (site / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print("index.html", len(page.encode()), "bytes,", len(cfg["cards"]), "cards")


if __name__ == "__main__":
    build(Path(__file__).resolve().parent.parent)
