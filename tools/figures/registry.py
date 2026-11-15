"""그림 이름(마크다운의 `&#91;embedded content: 이름 · 설명\\]`) -> 최종 HTML을 만드는 함수.
build.py(파이썬 빌드)와 export_legacy.py(Astro용 조각 추출)가 함께 써요."""
import html

from diagrams import FIGURES as _FIGURES  # 먼저 import해야 해요(dbdiagrams와 순환 참조)
import befigs as _befigs
import demos as _demos
import demos2 as _demos2
import flowanim as _flowanim
import guifigs as _guifigs
import se11fk as _se11fk


def _static(title, fn):
    def make():
        return (f'<figure class="diagram"><figcaption>{html.escape(title)}</figcaption>'
                f'<div class="diagram-scroll">{fn()}</div></figure>')
    make.__name__ = fn.__name__
    return make


def figures():
    """{그림 이름: 인자 없는 함수}. 정적 그림은 figure.diagram 틀까지 씌운 HTML을 돌려줘요."""
    out = {}
    static = dict(_FIGURES)
    static.update(_befigs.STATIC)
    for key, (title, fn) in static.items():
        out[key] = _static(title, fn)
    out.update({
        "setTimeout 실행 순서": _demos2.settimeout_steps, "정렬 연습장": _demos.flexlab, "경로 찾기 연습장": _demos.pathlab,
        "Promise 상태 변화": _demos2.promise_steps, "async await 실행 순서": _demos2.async_steps,
        "양방향 바인딩 연습장": _demos2.twolab, "템플릿 복사 연습장": _demos2.tmpllab,
        "for 한 바퀴씩": _demos2.for_steps, "필터 정렬 연습장": _demos2.filtlab, "ERD 연습장": _demos2.erdlab,
        "데이터 왕복 애니메이션": _flowanim.flowanim, "SE11 외래키 따라 하기": _se11fk.se11fk,
        **_befigs.STEPPERS, **_guifigs.STEPPERS,
    })
    return out
