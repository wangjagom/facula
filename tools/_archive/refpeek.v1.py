"""Preview cards for tables, fields, controls and sample data.

Desktop (wide screens): a small card floats next to the word on hover / focus / click.
Narrow screens (<= 760px): tap opens a bottom sheet.
The client script finds registered names inside each concept section, marks the first
mention per block (tables, controls) or per section (fields), and adds a strip of
"tables used in this section" under the section title.
"""
import json

KEY = ('<svg viewBox="0 0 24 24" class="pk-ic" aria-hidden="true"><circle cx="8" cy="15" r="4"/>'
       '<path d="M11 12l9-9M16 7l3 3M14 9l2 2"/></svg>')
CHAIN = ('<svg viewBox="0 0 24 24" class="fk-ic" aria-hidden="true"><path d="M10 14a4 4 0 0 0 5.7 0l3-3a4 4 0 0 0-5.7-5.7l-1 1"/>'
         '<path d="M14 10a4 4 0 0 0-5.7 0l-3 3a4 4 0 0 0 5.7 5.7l1-1"/></svg>')

# ---------------------------------------------------------------- back-end book
def T(ko, key, cols, rows, chain=(), note=""):
    return dict(kind="table", ko=ko, key=key, cols=cols, rows=rows, chain=list(chain), note=note)


def F(ko, typ, where):
    return dict(kind="field", ko=ko, type=typ, where=where)


BE = {
    "ZSTUDENT": T("학생", "MANDT + SID", [("SID", "pk"), ("SNAME", ""), ("CID", "fk"), ("SCORE", "")],
                  [["0001", "민수", "CL301", "85"], ["0002", "지아", "CL303", "92"], ["0003", "도윤", "CL301", "78"]],
                  ["ZCLASS", "ZSTUDENT"], "이 교재의 기본 예제예요. CID로 반(ZCLASS)을 가리켜요."),
    "ZCLASS": T("반", "MANDT + CID", [("CID", "pk"), ("CNAME", "")], [["CL301", "ABAP반"], ["CL303", "UI5반"]],
                ["ZCLASS", "ZSTUDENT"], "반 이름은 여기에 한 번만 적어요."),
    "ZENROLL": T("수강 (연결 테이블)", "MANDT + SID + SUBJ", [("SID", "pkfk"), ("SUBJ", "pkfk")],
                 [["0001", "JS101"], ["0001", "UI5101"], ["0002", "UI5101"]],
                 ["ZSTUDENT", "ZENROLL", "ZSUBJECT"], "학생과 과목의 다대다를 1:N 두 개로 풀어 주는 테이블이에요."),
    "ZSUBJECT": T("과목", "MANDT + SUBJ", [("SUBJ", "pk"), ("SUBJNAME", "")], [["JS101", "자바스크립트 기초"], ["UI5101", "SAPUI5 입문"]],
                  ["ZSUBJECT", "ZENROLL"], ""),
    "ZCOUNTRY": T("운영 국가", "MANDT + LAND1", [("LAND1", "pkfk")], [["KR"], ["US"], ["JP"]],
                  ["T005", "ZCOUNTRY"], "T005 안에서 고른 일부 나라만 담은 예제 테이블이에요."),
    "ZCOUNTRYT": T("운영 국가 이름 (Text Table)", "MANDT + SPRAS + LAND1", [("SPRAS", "pk"), ("LAND1", "pkfk"), ("LANDX", "")],
                   [["3", "KR", "대한민국"], ["E", "KR", "South Korea"]], ["ZCOUNTRY", "ZCOUNTRYT"], ""),
    "SCARR": T("항공사", "MANDT + CARRID", [("CARRID", "pk"), ("CARRNAME", ""), ("CURRCODE", "")],
               [["LH", "Lufthansa", "EUR"], ["AA", "American Airlines", "USD"], ["JL", "Japan Airlines", "JPY"]],
               ["SCARR", "SPFLI", "SFLIGHT"], "SAP 연습용 항공 모델의 항공사 목록이에요."),
    "SPFLI": T("운항 노선", "MANDT + CARRID + CONNID", [("CARRID", "pkfk"), ("CONNID", "pk"), ("CITYFROM", ""), ("CITYTO", "")],
               [["LH", "0400", "FRANKFURT", "NEW YORK"], ["LH", "0402", "FRANKFURT", "NEW YORK"], ["AA", "0017", "NEW YORK", "SAN FRANCISCO"]],
               ["SCARR", "SPFLI", "SFLIGHT"], "항공사마다 노선 번호(CONNID)를 따로 매겨요."),
    "SFLIGHT": T("날짜별 운항편", "MANDT + CARRID + CONNID + FLDATE", [("CARRID", "pkfk"), ("CONNID", "pkfk"), ("FLDATE", "pk"), ("PRICE", "")],
                 [["LH", "0400", "2026-11-20", "666.00"], ["LH", "0400", "2026-11-21", "666.00"], ["AA", "0017", "2026-11-20", "422.94"]],
                 ["SCARR", "SPFLI", "SFLIGHT"], "같은 노선이 날짜마다 1건씩 있어요."),
    "SAPLANE": T("기종", "MANDT + PLANETYPE", [("PLANETYPE", "pk"), ("SEATSMAX", ""), ("PRODUCER", "")],
                 [["747-400", "385", "BOE"], ["A380-800", "475", "A"]], ["SAPLANE", "SFLIGHT"], "SFLIGHT의 PLANETYPE이 가리키는 기종 정보예요(비식별 관계)."),
    "T005": T("나라 목록 (SAP 표준)", "MANDT + LAND1", [("LAND1", "pk"), ("(나라별 설정)", "")], [["KR", "…"], ["US", "…"], ["JP", "…"]],
              [], "나라 이름은 Text Table T005T에 언어별로 있어요."),
    "T005T": T("나라 이름 (Text Table)", "MANDT + SPRAS + LAND1", [("SPRAS", "pk"), ("LAND1", "pkfk"), ("LANDX", ""), ("NATIO", "")],
               [["3", "KR", "대한민국", "한국인"], ["E", "KR", "South Korea", "Korean"]], ["T005", "T005T"], ""),
    "MARA": T("자재 마스터 (SAP 표준)", "MANDT + MATNR", [("MATNR", "pk"), ("MTART", "")], [["100-100", "FERT"]], [],
              "자재 번호와 기본 정보예요. 이름은 MAKT에 언어별로 있어요."),
    "MAKT": T("자재 이름 (Text Table)", "MANDT + MATNR + SPRAS", [("MATNR", "pkfk"), ("SPRAS", "pk"), ("MAKTX", "")],
              [["100-100", "3", "볼트"], ["100-100", "E", "Bolt"]], ["MARA", "MAKT"], ""),
    "VBAK": T("판매 문서 헤더 (SAP 표준)", "MANDT + VBELN", [("VBELN", "pk"), ("KUNNR", "fk")], [["0000012345", "0000001000"]],
              ["VBAK", "VBAP"], "문서 1건에 품목(VBAP)이 여러 건 달려요."),
    "VBAP": T("판매 문서 품목 (SAP 표준)", "MANDT + VBELN + POSNR", [("VBELN", "pkfk"), ("POSNR", "pk"), ("MATNR", "fk")],
              [["0000012345", "000010", "100-100"], ["0000012345", "000020", "100-200"]], ["VBAK", "VBAP"], ""),
    "KNA1": T("고객 마스터 (SAP 표준)", "MANDT + KUNNR", [("KUNNR", "pk"), ("NAME1", ""), ("LAND1", "fk")],
              [["0000001000", "Becker Berlin", "DE"]], [], "LAND1은 Check Table T005로 검사해요."),
    "MANDT": F("Client 번호", "CLNT 3", [("모든 SAP 테이블", "맨 앞 키 · Check Table T000")]),
    "SID": F("학번", "NUMC 4", [("ZSTUDENT", "키"), ("ZENROLL", "키 · 외래키 → ZSTUDENT")]),
    "SNAME": F("학생 이름", "CHAR", [("ZSTUDENT", "일반 필드")]),
    "CID": F("반 코드", "CHAR 5", [("ZCLASS", "키"), ("ZSTUDENT", "일반 필드 · 외래키 → ZCLASS")]),
    "CNAME": F("반 이름", "CHAR", [("ZCLASS", "일반 필드")]),
    "SCORE": F("점수", "INT", [("ZSTUDENT", "일반 필드")]),
    "SUBJ": F("과목 코드", "CHAR 6", [("ZSUBJECT", "키"), ("ZENROLL", "키 · 외래키 → ZSUBJECT")]),
    "CARRID": F("항공사 코드", "CHAR 3", [("SCARR", "키"), ("SPFLI", "키 · 외래키 → SCARR"), ("SFLIGHT", "키 · 외래키 → SPFLI")]),
    "CONNID": F("노선 번호 (항공사 안에서만 유일)", "NUMC 4", [("SPFLI", "키"), ("SFLIGHT", "키 · 외래키 → SPFLI")]),
    "FLDATE": F("운항 날짜", "DATS 8", [("SFLIGHT", "키")]),
    "PLANETYPE": F("기종", "CHAR 10", [("SAPLANE", "키"), ("SFLIGHT", "일반 필드 · 외래키 → SAPLANE")]),
    "NATIO": F("국적", "CHAR 3 (Domain LAND1)", [("강사 테이블", "일반 필드 · 외래키 → T005"), ("T005T", "국적 이름")]),
    "LAND1": F("나라 코드", "CHAR 3", [("T005", "키"), ("KNA1 등", "일반 필드 · 외래키 → T005")]),
    "SPRAS": F("언어 키 (3 한국어, E 영어)", "LANG 1", [("Text Table들", "키의 일부")]),
}

# ---------------------------------------------------------------- UI5 book
def C(lib, desc, items, xml):
    return dict(kind="ctrl", lib=lib, desc=desc, items=items, xml=xml)


UI5 = {
    "Page": C("sap.m", "화면 한 장. 제목 줄과 내용 영역이 있어요.", [("title", "제목"), ("content", "안에 넣을 컨트롤들 (애그리게이션)")],
              '<Page title="학생 목록">\n  <content> … </content>\n</Page>'),
    "Button": C("sap.m", "누르는 버튼.", [("text", "버튼 글자"), ("type", "Emphasized, Reject 등 모양"), ("press", "눌렀을 때 실행할 함수 (이벤트)")],
                '<Button text="검색" press=".onSearch" />'),
    "Input": C("sap.m", "글자를 입력받는 칸.", [("value", "입력된 값 (바인딩 가능)"), ("placeholder", "빈칸일 때 흐린 안내 글자"), ("liveChange", "칠 때마다 실행 (이벤트)")],
               '<Input value="{/name}" placeholder="이름" />'),
    "Text": C("sap.m", "글자를 보여 주기만 하는 컨트롤.", [("text", "보여 줄 글자")], '<Text text="{/bookInfo/name}" />'),
    "Label": C("sap.m", "입력칸 앞에 붙는 이름표 글자.", [("text", "글자"), ("labelFor", "어느 입력칸의 이름인지 id")], '<Label text="이름" labelFor="nameInput" />'),
    "Title": C("sap.m", "굵은 제목 글자.", [("text", "글자"), ("level", "제목 수준 H1~H6")], '<Title text="학생 정보" level="H2" />'),
    "Panel": C("sap.m", "제목이 있고 접을 수 있는 영역.", [("headerText", "제목"), ("expandable", "접기 가능 여부"), ("content", "안의 컨트롤들")],
               '<Panel headerText="상세" expandable="true">\n  …\n</Panel>'),
    "HBox": C("sap.m", "안의 컨트롤을 가로로 나열하는 레이아웃 컨트롤.", [("justifyContent", "가로 정렬 (Start, Center, SpaceBetween)"), ("alignItems", "세로 정렬"), ("items", "안의 컨트롤들")],
              '<HBox justifyContent="SpaceBetween">\n  <Text text="A" /><Text text="B" />\n</HBox>'),
    "VBox": C("sap.m", "안의 컨트롤을 세로로 쌓는 레이아웃 컨트롤.", [("justifyContent", "세로 정렬"), ("alignItems", "가로 정렬"), ("items", "안의 컨트롤들")],
              '<VBox>\n  <Text text="A" /><Text text="B" />\n</VBox>'),
    "SimpleForm": C("sap.ui.layout.form", "라벨과 입력칸을 짝지어 정렬해 주는 입력 양식.", [("layout", "배치 방식 (ResponsiveGridLayout 등)"), ("content", "Label, Input을 번갈아 넣어요")],
                    '<f:SimpleForm layout="ResponsiveGridLayout">\n  <Label text="이름" /><Input />\n</f:SimpleForm>'),
    "Table": C("sap.m", "열과 줄로 데이터를 보여 주는 컨트롤.", [("items", "줄 목록 (애그리게이션 바인딩)"), ("columns", "열 정의"), ("mode", "줄 고르는 방식"), ("selectionChange", "줄을 골랐을 때 (이벤트)")],
               '<Table items="{/esStdList}">\n  <columns> … </columns>\n  <items> <ColumnListItem> … </ColumnListItem> </items>\n</Table>'),
    "List": C("sap.m", "한 줄짜리 항목을 세로로 나열하는 목록.", [("items", "항목 목록 (바인딩)"), ("mode", "고르는 방식"), ("selectionChange", "골랐을 때 (이벤트)")],
              '<List items="{/esStdList}">\n  <StandardListItem title="{Sname}" />\n</List>'),
    "Select": C("sap.m", "펼쳐서 하나를 고르는 드롭다운.", [("items", "선택지 목록"), ("selectedKey", "고른 항목의 key"), ("change", "바꿨을 때 (이벤트)")],
                '<Select items="{/classes}">\n  <core:Item key="{Cid}" text="{Cname}" />\n</Select>'),
    "Dialog": C("sap.m", "화면 위에 뜨는 팝업 창.", [("title", "제목"), ("content", "안의 컨트롤"), ("beginButton / endButton", "아래 버튼")],
                '<Dialog title="확인">\n  <content> … </content>\n</Dialog>'),
    "ScrollContainer": C("sap.m", "안의 내용을 스크롤할 수 있게 감싸는 컨트롤.", [("height", "높이"), ("vertical", "세로 스크롤 여부")],
                         '<ScrollContainer height="300px" vertical="true">\n  …\n</ScrollContainer>'),
    "MessageToast": C("sap.m (모듈)", "화면 아래에 잠깐 떴다 사라지는 알림. 화면에 놓는 컨트롤이 아니라 코드에서 불러 써요.", [("show(text)", "알림 띄우기")],
                      'MessageToast.show("저장했어요");'),
    "JSONModel": C("sap.ui.model.json (모듈)", "자바스크립트 객체를 데이터로 쓰는 모델.", [("setData / getData", "데이터 넣기, 꺼내기"), ("getProperty / setProperty", "경로로 값 읽기, 바꾸기"), ("loadData", "JSON 파일 불러오기")],
                   'const oModel = new JSONModel(oData);\nthis.getView().setModel(oModel);'),
    "ODataModel": C("sap.ui.model.odata.v2 (모듈)", "SAP 서버(OData 서비스)와 데이터를 주고받는 모델.", [("read / create / update", "서버 요청")], "new ODataModel('/sap/opu/odata/…')"),
    "ResourceModel": C("sap.ui.model.resource (모듈)", "i18n 번역 파일의 글자를 쓰는 모델.", [("{i18n>키}", "바인딩으로 글자 가져오기")], '<Text text="{i18n>appTitle}" />'),
    "esStdList": dict(kind="table", ko="수업 예제 학생 목록 (모델 데이터)", key="배열 · 0번부터",
                      cols=[("Sid", ""), ("Sname", "")], rows=[["25010001", "민수"], ["25010002", "지아"]], chain=[],
                      note="모델 데이터의 배열이에요. Binding Path로는 {/esStdList/0/Sname}처럼 적어요."),
}


def assets(registry, scope=".concept", strip_label="이 섹션에서 쓰는 테이블", code_only=False):
    data = json.dumps(registry, ensure_ascii=False)
    css = """
<style>
.pk-ic,.fk-ic{width:13px;height:13px;flex:none;fill:none;stroke-width:2;stroke-linecap:round;stroke-linejoin:round;vertical-align:-2px}
.pk-ic{stroke:#e0a800}.fk-ic{stroke:#4338ca}
.peek{cursor:help;border-bottom:1.5px dotted rgb(14 165 233 / .65);border-radius:2px;transition:background .15s;outline:none}
code.peek{border-bottom-color:rgb(14 165 233 / .75)}
.peek:hover,.peek:focus-visible,.peek.on{background:var(--accent-soft)}
.peek-strip{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:-4px 0 18px;padding:10px 12px;border-radius:12px;background:#f8fafc;box-shadow:inset 0 0 0 1px var(--line)}
.peek-strip>span{font-size:12.5px;color:var(--muted);margin-right:2px}
.peek-chip{display:inline-flex;align-items:center;gap:6px;padding:4px 10px;border-radius:999px;background:#fff;border:0;box-shadow:inset 0 0 0 1px rgb(3 7 18 / .1);font:600 12.5px var(--font-mono);color:var(--ink);cursor:pointer}
.peek-chip em{font:400 12px var(--font-body,inherit);font-style:normal;color:var(--muted)}
.peek-chip:hover,.peek-chip.on{box-shadow:inset 0 0 0 1.5px var(--accent)}
.peek-pop{position:absolute;z-index:60;width:min(400px,calc(100vw - 24px));padding:14px 14px 12px;border-radius:14px;background:#fff;box-shadow:0 14px 40px rgb(17 24 39 / .18),0 0 0 1px rgb(3 7 18 / .08);font-size:13px;line-height:1.55;color:var(--ink);opacity:0;transform:translateY(4px);transition:opacity .14s,transform .14s;pointer-events:none}
.peek-pop.show{opacity:1;transform:none;pointer-events:auto}
.peek-pop h5{display:flex;flex-wrap:wrap;align-items:baseline;gap:4px 8px;margin:0 0 2px;font:700 15px var(--font-mono)}
.peek-pop h5 em{font:500 13px var(--font-body,inherit);font-style:normal;color:var(--muted)}
.peek-pop .pk-line{margin:0 0 8px;font-size:12px;color:var(--muted)}
.peek-pop .tw{overflow-x:auto;margin:6px -4px 8px;padding:0 4px}
.peek-pop table{min-width:100%;border-collapse:collapse;font:12px var(--font-mono);margin:0}
.peek-pop th{text-align:left;font-weight:600;color:#374151;background:#f3f4f6;padding:5px 7px;white-space:nowrap}
.peek-pop th span{display:inline-flex;align-items:center;gap:3px}
.peek-pop td{padding:5px 7px;border-top:1px solid rgb(3 7 18 / .06);white-space:nowrap}
.peek-pop .chain{display:flex;flex-wrap:wrap;align-items:center;gap:4px;margin:2px 0 6px;font:12px var(--font-mono);color:var(--muted)}
.peek-pop .chain b{color:var(--ink);background:var(--accent-soft);padding:1px 6px;border-radius:6px}
.peek-pop .note{margin:0;color:#4b5563;font-size:12.5px}
.peek-pop .where{list-style:none;margin:6px 0 4px;padding:0}
.peek-pop .where li{display:flex;justify-content:space-between;gap:10px;padding:4px 0;border-top:1px solid rgb(3 7 18 / .06);font-size:12.5px}
.peek-pop .where li b{font:600 12px var(--font-mono);white-space:nowrap}
.peek-pop .where li span{color:#4b5563;text-align:right}
.peek-pop pre.px{margin:8px 0 2px;padding:9px 11px;border-radius:9px;background:#0f172a;color:#e2e8f0;font:12px/1.6 var(--font-mono);white-space:pre;overflow-x:auto}
.peek-pop .go{display:inline-block;margin-top:8px;font-size:12px;color:var(--accent-ink,#0369a1);text-decoration:none}
.peek-veil{position:fixed;inset:0;z-index:59;background:rgb(17 24 39 / .32);opacity:0;transition:opacity .16s;pointer-events:none}
.peek-veil.show{opacity:1;pointer-events:auto}
@media (max-width:760px){
 .peek-pop{position:fixed;left:0!important;right:0;top:auto!important;bottom:0;width:auto;max-height:72vh;overflow:auto;border-radius:18px 18px 0 0;padding:10px 18px calc(22px + env(safe-area-inset-bottom));transform:translateY(100%);transition:transform .22s ease,opacity .1s}
 .peek-pop.show{transform:none}
 .peek-pop:before{content:"";display:block;width:38px;height:4px;margin:0 auto 12px;border-radius:2px;background:#d1d5db}
}
</style>"""
    js = r"""
<script>
(function(){
var D=__DATA__, STRIP=__STRIP__, CODE_ONLY=__CODEONLY__;
var KEY='__KEY__', CHAIN='__CHAIN__';
var names=Object.keys(D).sort(function(a,b){return b.length-a.length;});
if(!names.length)return;
var RE=new RegExp('(^|[^A-Za-z0-9_])('+names.join('|')+')(?![A-Za-z0-9_])','g');
var SKIP={PRE:1,A:1,BUTTON:1,H1:1,H2:1,H3:1,H4:1,H5:1,SVG:1,SCRIPT:1,STYLE:1,FIGURE:1,LABEL:1,SUMMARY:1,TEXTAREA:1};
var FIRST={};
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
function blockOf(n){while(n&&!/^(P|LI|TD|TH|DD|DT|BLOCKQUOTE)$/.test(n.nodeName))n=n.parentNode;return n;}
function bad(p,scope){for(;p&&p!==scope;p=p.parentNode){if(SKIP[p.nodeName])return true;var c=p.classList;if(c&&(c.contains('quiz')||c.contains('peek')||c.contains('peek-strip')||c.contains('tip')||c.contains('xref')||c.contains('pager')||c.contains('crumb')||c.contains('stepper')))return true;}return false;}
function hidOf(scope){var h=scope.querySelector('h3[id]');return h?[h.id,(scope.querySelector('.crumb a')||{}).textContent?((scope.querySelector('.crumb a').textContent.split('·')[0]||'').trim()+' · '+(h.getAttribute('data-plain')||h.textContent).split(':')[0]):(h.getAttribute('data-plain')||h.textContent)]:null;}
document.querySelectorAll('__SCOPE__').forEach(function(scope){
  var seen=[],fseen={},here=hidOf(scope);
  var walker=document.createTreeWalker(scope,NodeFilter.SHOW_TEXT,{acceptNode:function(t){
    if(CODE_ONLY&&!(t.parentNode&&t.parentNode.nodeName==='CODE'))return NodeFilter.FILTER_SKIP;
    if(bad(t.parentNode,scope))return NodeFilter.FILTER_REJECT;
    RE.lastIndex=0;return RE.test(t.nodeValue)?NodeFilter.FILTER_ACCEPT:NodeFilter.FILTER_SKIP;}});
  var list=[];while(walker.nextNode())list.push(walker.currentNode);
  list.forEach(function(t){
    var blk=blockOf(t)||scope; blk._peek=blk._peek||{};
    if(CODE_ONLY){
      var nm=t.nodeValue.trim();if(!D[nm])return;var code=t.parentNode;
      if(D[nm].kind==='table'&&seen.indexOf(nm)<0)seen.push(nm);
      if(here&&!FIRST[nm])FIRST[nm]=here;
      if(blk._peek[nm])return;blk._peek[nm]=1;
      code.classList.add('peek');code.dataset.peek=nm;code.tabIndex=0;code.setAttribute('role','button');code.setAttribute('aria-label',nm+' 미리보기');return;
    }
    var s=t.nodeValue,out=document.createDocumentFragment(),last=0,m;RE.lastIndex=0;
    while((m=RE.exec(s))){
      var nm=m[2],st=m.index+m[1].length,e=D[nm];
      if(e.kind==='table'&&seen.indexOf(nm)<0)seen.push(nm);
      if(here&&!FIRST[nm])FIRST[nm]=here;
      if(e.kind==='field'){if(fseen[nm])continue;fseen[nm]=1;}
      if(blk._peek[nm])continue;blk._peek[nm]=1;
      out.appendChild(document.createTextNode(s.slice(last,st)));
      var sp=document.createElement('span');sp.className='peek';sp.textContent=nm;sp.dataset.peek=nm;sp.tabIndex=0;sp.setAttribute('role','button');
      sp.setAttribute('aria-label',nm+(e.kind==='table'?' 테이블 미리보기':' 설명 보기'));
      out.appendChild(sp);last=st+nm.length;
    }
    if(last){out.appendChild(document.createTextNode(s.slice(last)));t.parentNode.replaceChild(out,t);}
  });
  if(STRIP&&seen.length){
    var strip=document.createElement('div');strip.className='peek-strip';
    strip.innerHTML='<span>'+STRIP+'</span>'+seen.map(function(n){return '<button type="button" class="peek-chip" data-peek="'+n+'">'+n+'<em>'+esc(D[n].ko)+'</em></button>';}).join('');
    var head=scope.querySelector('.c-head');if(head)head.insertAdjacentElement('afterend',strip);
  }
});
var pop=document.createElement('div');pop.className='peek-pop';pop.setAttribute('role','dialog');document.body.appendChild(pop);
var veil=document.createElement('div');veil.className='peek-veil';document.body.appendChild(veil);
function ic(k){return k==='pk'?KEY:k==='fk'?CHAIN:k==='pkfk'?KEY+CHAIN:'';}
function render(nm,from){
  var e=D[nm],h='';
  if(e.kind==='table'){
    h='<h5>'+esc(nm)+'<em>'+esc(e.ko)+'</em></h5><p class="pk-line">키: '+esc(e.key)+'</p>';
    if(e.chain&&e.chain.length)h+='<div class="chain">'+e.chain.map(function(c){return c===nm?'<b>'+c+'</b>':c;}).join(' → ')+'</div>';
    h+='<div class="tw"><table><thead><tr>'+e.cols.map(function(c){return '<th><span>'+ic(c[1])+esc(c[0])+'</span></th>';}).join('')+'</tr></thead><tbody>'+
      e.rows.map(function(r){return '<tr>'+r.map(function(v){return '<td>'+esc(v)+'</td>';}).join('')+'</tr>';}).join('')+'</tbody></table></div>';
    var note=e.note||'';if(/^MANDT/.test(e.key))note=(note?note+' ':'')+'MANDT는 생략했어요.';
    if(note)h+='<p class="note">'+esc(note)+'</p>';
  }else if(e.kind==='field'){
    h='<h5>'+esc(nm)+'<em>'+esc(e.ko)+'</em></h5><p class="pk-line">타입 '+esc(e.type)+'</p><ul class="where">'+
      e.where.map(function(w){return '<li><b>'+esc(w[0])+'</b><span>'+esc(w[1])+'</span></li>';}).join('')+'</ul>';
  }else{
    h='<h5>'+esc(nm)+'<em>'+esc(e.lib)+'</em></h5><p class="note">'+esc(e.desc)+'</p><ul class="where">'+
      e.items.map(function(w){return '<li><b>'+esc(w[0])+'</b><span>'+esc(w[1])+'</span></li>';}).join('')+'</ul><pre class="px">'+esc(e.xml)+'</pre>';
  }
  var f=FIRST[nm];
  if(f&&f[0]!==from)h+='<a class="go" href="#'+f[0]+'">처음 나온 곳: '+esc(f[1])+' →</a>';
  return h;
}
var cur=null,hideT=null,narrow=matchMedia('(max-width:760px)');
function show(el){
  clearTimeout(hideT);if(cur)cur.classList.remove('on');cur=el;el.classList.add('on');
  var sc=el.closest('__SCOPE__'),h3=sc&&sc.querySelector('h3[id]');
  pop.innerHTML=render(el.dataset.peek,h3&&h3.id);
  if(narrow.matches){veil.classList.add('show');}
  else{var r=el.getBoundingClientRect(),w=pop.offsetWidth||400,x=Math.min(Math.max(12,r.left+scrollX),scrollX+document.documentElement.clientWidth-w-12);
    pop.style.left=x+'px';pop.style.top=(r.bottom+scrollY+8)+'px';
    requestAnimationFrame(function(){var ph=pop.offsetHeight;if(r.bottom+ph+16>innerHeight&&r.top>ph+16)pop.style.top=(r.top+scrollY-ph-8)+'px';});}
  pop.classList.add('show');
}
function hide(){pop.classList.remove('show');veil.classList.remove('show');if(cur){cur.classList.remove('on');cur=null;}}
document.addEventListener('mouseover',function(e){if(narrow.matches)return;var el=e.target.closest('[data-peek]');
  if(el){if(el!==cur)show(el);else clearTimeout(hideT);}
  else if(cur&&!e.target.closest('.peek-pop')){clearTimeout(hideT);hideT=setTimeout(hide,200);}
  else if(e.target.closest('.peek-pop'))clearTimeout(hideT);});
document.addEventListener('click',function(e){var el=e.target.closest('[data-peek]');
  if(el){e.preventDefault();if(cur===el&&pop.classList.contains('show')&&narrow.matches)hide();else show(el);return;}
  if(e.target.closest('.peek-pop .go')){hide();return;}
  if(!e.target.closest('.peek-pop'))hide();});
document.addEventListener('keydown',function(e){if(e.key==='Escape')hide();var el=e.target.closest&&e.target.closest('[data-peek]');if(el&&(e.key==='Enter'||e.key===' ')){e.preventDefault();show(el);}});
document.addEventListener('focusin',function(e){if(narrow.matches)return;var el=e.target.closest&&e.target.closest('[data-peek]');if(el)show(el);});
veil.addEventListener('click',hide);
addEventListener('scroll',function(){if(!narrow.matches&&cur&&!pop.matches(':hover'))hide();},{passive:true});
addEventListener('hashchange',hide);
})();
</script>"""
    js = (js.replace("__DATA__", data).replace("__SCOPE__", scope)
            .replace("__STRIP__", json.dumps(strip_label, ensure_ascii=False))
            .replace("__CODEONLY__", "true" if code_only else "false")
            .replace("__KEY__", KEY).replace("__CHAIN__", CHAIN))
    return css + js
