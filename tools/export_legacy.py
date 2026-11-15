"""파이썬 그림·아이콘·refpeek 모듈의 결과를 Astro가 읽는 정적 조각으로 뽑아요.

    python tools/export_legacy.py

결과: src/legacy/ (커밋해요). 그림 모듈이나 icon_map2.py를 고쳤을 때만 다시 실행하면 돼요.
Astro 빌드(npm run build)에는 파이썬이 필요 없어요.
"""
import json
import shutil
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path[:0] = [str(TOOLS), str(TOOLS / "figures")]

import icon3d  # noqa: E402
import icon_map2  # noqa: E402
import refpeek  # noqa: E402
import registry  # noqa: E402
import toss_icons  # noqa: E402

OUT = ROOT / "src" / "legacy"
# 교재 설정(content/*/book.yaml)과 build.py에서 쓰는 아이콘 중 icon_map2에 없는 것
EXTRA_ICONS = [("keyboard", None), ("folder", None), ("book", None), ("book", "teal"), ("table", "blue"),
               ("db", "slate"), ("chain", "indigo"), ("magnifier", "indigo"), ("console", "ink"),
               ("window", "blue"), ("erd", "teal")]


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def main() -> None:
    if (OUT / "figures").exists():
        shutil.rmtree(OUT / "figures")

    # 1) 그림: 이름 -> 파일. 파일 이름은 그림 함수 이름(영문)
    index = {}
    for name, fn in registry.figures().items():
        fname = f"{fn.__name__}.html"
        assert fname not in index.values(), fname
        write(OUT / "figures" / fname, fn())
        index[name] = fname
    write(OUT / "figures" / "index.json", json.dumps(index, ensure_ascii=False, indent=1) + "\n")

    # 2) 그림 안에서 쓰는 2.5D 아이콘 심볼(모든 그림을 만든 뒤에 모아요)
    write(OUT / "figure-icons.svg", icon3d.ns_defs() + "\n")

    # 3) 제목·목차 아이콘: 심볼 정의와 개념 -> 아이콘 표
    combos = set(icon_map2.CONCEPT.values()) | set(icon_map2.PART.values()) | set(EXTRA_ICONS)
    symbols = {f"{o}|{h or ''}|{m}": toss_icons.symbol(o, h, m) for o, h in combos for m in ("D", "E")}
    write(OUT / "icons.json", json.dumps({"gradients": toss_icons.defs(), "symbols": dict(sorted(symbols.items()))},
                                         ensure_ascii=False, indent=1) + "\n")
    write(OUT / "icon-map.json", json.dumps({"concept": icon_map2.CONCEPT,
                                             "part": {str(k): v for k, v in icon_map2.PART.items()}},
                                            ensure_ascii=False, indent=1) + "\n")

    # 4) refpeek(테이블·필드 미리보기 카드): 교재별 <style>+<script> 묶음
    write(OUT / "refpeek" / "sap-backend.html",
          refpeek.assets(refpeek.BE, ".concept", "이 섹션에서 쓰는 테이블", models=refpeek.MODELS) + "\n")
    write(OUT / "refpeek" / "sap-ui5.html", refpeek.assets(refpeek.UI5, ".concept", None, code_only=True) + "\n")

    print(f"figures {len(index)}, icon symbols {len(symbols)} -> {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
