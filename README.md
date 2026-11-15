# Facula

차근차근 따라가는 학습 노트 사이트예요. 지금은 SAP 교재가 첫 주제이고, 다른 주제(자바스크립트, 국어 문법 등)도 계속 추가할 거예요.

주소: https://wangjagom.github.io/facula/

## 폴더 구조

```
facula/
├─ content/                 글(원본)
│   ├─ site.json            첫 화면의 카드·링크 목록
│   ├─ sap-ui5/doc.md       SAPUI5 총정리
│   ├─ sap-backend/doc.md   SAP 백엔드 총정리
│   └─ select-single/index.html   손으로 만든 단독 페이지 (빌드 안 함, 그대로 복사)
├─ tools/                   빌드 코드
│   ├─ build.py             빌드 진입점
│   ├─ index_page.py        첫 화면 생성
│   ├─ figures/             그림·애니메이션 모듈
│   ├─ assets/              style.css, app.js
│   ├─ icon_map2.py 등      아이콘 모듈
│   ├─ audit.py             모바일 점검 (playwright 필요)
│   └─ _archive/            빌드에 안 쓰는 옛 실험 파일
├─ fonts/                   Pretendard (OFL)
├─ site/                    빌드 결과 (git에 안 올라가요)
└─ .github/workflows/deploy.yml   main에 push하면 GitHub Pages로 배포
```

## 로컬에서 빌드하기

Python 3.10 이상이 필요해요.

```bash
python -m venv .venv
# macOS/Linux: source .venv/bin/activate    Windows: .venv\Scripts\activate
pip install -r requirements.txt
python tools/build.py all        # 또는 ui5 / backend
python -m http.server -d site 8000
```

`http://localhost:8000/` 에서 확인해요. 모바일 점검(`tools/audit.py`)에는 `pip install playwright`가 따로 필요해요.

## 새 주제 추가하기

- **마크다운 교재**: `content/<주제>/doc.md`를 만들고, `tools/build.py`의 `BOOKS`에 교재 설정(제목·부 구성·아이콘)을 추가해요. 첫 화면 카드는 `content/site.json`의 `cards`에 한 줄 추가하면 돼요.
- **손으로 만든 페이지**: `content/<주제>/index.html`을 두고 `site.json`의 `cards`에만 추가하면 빌드할 때 그대로 `site/<주제>/`로 복사돼요.
- 교재끼리 링크는 `../sap-ui5/`처럼 사이트 안 상대 경로로 걸어요.

## 교재 작성 규칙

- 토스 스타일 해요체, 초보자가 읽기 쉽게.
- 아직 안 배운 개념을 먼저 쓰지 않아요 (순서 지키기).
- SAP 고유 개념은 영어 그대로 (Domain, Data Element, Check Table, Structure, Internal Table 등).
- ABAP 코드는 옛 문법/요즘 문법을 같은 비중의 탭으로, 기본은 옛 문법. ` ```abap ` 바로 다음에 ` ```abap-old `를 붙이면 탭이 돼요. 두 문법이 같으면 탭 없이 한 블록이에요.
- "SQL은 에스큐엘이라고 읽어요" 같은 뻔한 설명은 넣지 않아요.
- 그림·애니메이션: 아이콘에 색 배경을 넣지 않고, 스크롤로 진행되는 애니메이션을 선호해요.
- 새 섹션(`### 제목`)을 만들면 `tools/icon_map2.py`의 `CONCEPT`에 제목의 `:` 앞부분을 키로 아이콘을 추가해요.
- 문제는 `<details class="more practice">` 안의 ` ```quiz ` 블록에 써요.

## 라이선스

| 영역 | 라이선스 |
|---|---|
| 글 (`content/`) | [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.ko) |
| 코드 (`tools/`) | MIT |
| 글꼴 (`fonts/`) | [Pretendard](https://github.com/orioncactus/pretendard), SIL OFL 1.1 |

자세한 내용은 [LICENSE](LICENSE)를 보세요.
