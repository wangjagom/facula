/**
 * build.py 전용 코드 블록 문법을 HTML로 바꾸는 remark 플러그인.
 *  - ```quiz    문제 카드 (Q:, | 코드, - 보기 ✓, > 힌트)
 *  - ```syntax  문법 틀 (한글은 채우는 자리)
 *  - ```abap 바로 뒤 ```abap-old  옛/요즘 문법 탭 한 상자
 *  - 그 밖의 코드 블록: 언어 이름표 + 복사 버튼
 * 결과 HTML은 build.py와 같아요(색칠만 Pygments -> Shiki).
 */
import type { Root, Code, Html, Parent } from 'mdast';
import { highlight, initHighlighter } from '../lib/book/highlight';
import { esc, PyRandom, B_START, B_END } from '../lib/book/py';

const LANG_LABEL: Record<string, string> = { js: 'JavaScript', xml: 'XML', sql: 'SQL', abap: 'ABAP', '': '구조' };

const SYNTAX_KW = ('function return if else for of in const let while async await new break continue try catch class this ' +
  'true false null undefined ' +
  'SELECT FROM WHERE ORDER BY ASC DESC GROUP INSERT INTO VALUES UPDATE SET DELETE INNER JOIN ON AS ' +
  'COUNT SUM AVG MAX MIN AND OR').split(' ');
const SYN_RE = new RegExp(`(?<ph>[가-힣]+[0-9]*(?: [가-힣]+[0-9]*)*)|(?<kw>${B_START}(?:${SYNTAX_KW.join('|')})${B_END})`, 'gu');

function syntaxFence(code: string): string {
  const lineHtml = (line: string) => {
    const k = line.indexOf('//');
    const left = k < 0 ? line : line.slice(0, k);
    const comment = k < 0 ? null : line.slice(k + 2);
    const out: string[] = [];
    let pos = 0;
    for (const m of left.matchAll(SYN_RE)) {
      out.push(esc(left.slice(pos, m.index)));
      if (m.groups!.ph) out.push(`<span class="ph">${esc(m.groups!.ph)}</span>`);
      else out.push(`<span class="kw">${m.groups!.kw}</span>`);
      pos = m.index! + m[0].length;
    }
    out.push(esc(left.slice(pos)));
    if (comment !== null) out.push(`<span class="cm">//${esc(comment)}</span>`);
    return out.join('');
  };
  const inner = code.split('\n').map(lineHtml).join('\n');
  return '<figure class="code syntax"><figcaption><span>문법 틀</span>' +
    '<span class="hint">한글로 쓴 곳은 직접 채우는 자리예요</span></figcaption>' +
    `<pre><code>${inner}</code></pre></figure>`;
}

const inline = (t: string) => esc(t, false).replace(/`([^`]+)`/g, (_m, c) => `<code>${c}</code>`);

/** 책마다 문제 번호가 0부터 이어져요(보기 섞는 시드에 쓰여요) */
export interface FenceState { quizN: number }

function quizFence(code: string, st: FenceState): string {
  const gi = st.quizN++;
  type Stem = [kind: 'code' | 'text', text: string];
  const qs: [Stem[], [string, boolean][], string][] = [];
  for (const blk of code.trim().split(/\n\s*\n/)) {
    const stem: Stem[] = [];
    const opts: [string, boolean][] = [];
    let hint = '';
    for (const line of blk.split('\n')) {
      if (line.startsWith('- ')) {
        const t = line.slice(2).trim();
        const ok = t.endsWith('✓');
        opts.push([ok ? t.slice(0, -1).trim() : t, ok]);
      } else if (line.startsWith('> ')) hint = line.slice(2).trim();
      else if (line.startsWith('| ') || line === '|') stem.push(['code', line.slice(2)]);
      else if (line.startsWith('Q:')) stem.push(['text', line.slice(2).trim()]);
    }
    if (opts.length < 2 || opts.filter((o) => o[1]).length !== 1) throw new Error(`quiz 블록 오류:\n${blk}`);
    new PyRandom(gi * 31 + qs.length * 7 + 3).shuffle(opts);
    qs.push([stem, opts, hint]);
  }
  const n = qs.length;
  const parts = qs.map(([stem, opts, hint], qi) => {
    const ans = opts.findIndex((o) => o[1]);
    const items: string[] = [];
    let codebuf: string[] = [];
    const flush = () => {
      if (!codebuf.length) return;
      const src = codebuf.join('\n');
      const s = src.trimStart();
      let lg: string;
      if (s.startsWith('<')) lg = 'xml';
      else if (/^(SELECT|UPDATE|INSERT|DELETE)(?![\p{L}\p{N}_])/u.test(s) && src.trimEnd().endsWith(';')) lg = 'sql';
      else if (new RegExp(`${B_START}(LOOP AT|ENDLOOP|DATA|WRITE|READ TABLE|MODIFY|APPEND|SORT)${B_END}`, 'u').test(src)) lg = 'abap';
      else lg = 'js';
      items.push(`<figure class="code q-fig" data-lang="${lg}"><figcaption><span>${LANG_LABEL[lg] ?? lg}</span></figcaption>` +
        `<pre class="q-code"><code>` + highlight(src, lg) + '</code></pre></figure>');
      codebuf = [];
    };
    let firstText = true;
    for (const [kind, text] of stem) {
      if (kind === 'code') codebuf.push(text);
      else {
        flush();
        const badge = firstText ? `<span class="q-num">문제 ${qi + 1} / ${n}</span>` : '';
        firstText = false;
        items.push(`<p class="q-text">${badge}${inline(text)}</p>`);
      }
    }
    flush();
    const labels = opts.map((o, i) =>
      `<label class="opt"><input type="radio" name="g${gi}q${qi}" value="${i}"><span>${inline(o[0])}</span></label>`).join('');
    const last = qi === n - 1;
    return `<div class="q" role="radiogroup" data-answer="${ans}"` + (qi === 0 ? '' : ' hidden') + '>' +
      `<div class="q-stem">${items.join('')}</div>${labels}` +
      `<p class="q-hint" hidden>${inline(hint)}</p>` +
      `<div class="quiz-bar"><button type="button" class="quiz-check" data-last="${last ? 1 : 0}">정답 확인</button>` +
      '<p class="quiz-result" role="status" aria-live="polite"></p></div></div>';
  });
  return '<div class="quiz">' + parts.join('') + '<p class="quiz-done" hidden></p>' +
    '<button type="button" class="gate-skip">문제 건너뛰고 내용 보기</button></div>';
}

function plainFence(code: string, lang: string): string {
  const label = LANG_LABEL[lang] ?? lang;
  const inner = highlight(code, lang === 'abap-old' ? 'abap' : lang);
  return `<figure class="code" data-lang="${lang}"><figcaption><span>${label}</span>` +
    '<button type="button" class="copy" aria-label="코드 복사">복사</button></figcaption>' +
    `<pre><code>${inner}</code></pre></figure>`;
}

function synPair(newCode: string, oldCode: string): string {
  return '<figure class="code syn-pair" data-lang="abap"><figcaption>' +
    '<span class="syn-tabs" role="group" aria-label="문법 고르기">' +
    '<button type="button" class="syn-tab" data-set-syn="new">요즘 문법 <small>7.40+</small></button>' +
    '<button type="button" class="syn-tab" data-set-syn="old">옛 문법</button></span>' +
    '<button type="button" class="copy" aria-label="코드 복사">복사</button></figcaption>' +
    `<pre class="syn-pane syn-new"><code>${highlight(newCode, 'abap')}</code></pre>` +
    `<pre class="syn-pane syn-old"><code>${highlight(oldCode, 'abap')}</code></pre></figure>`;
}

const info = (c: Code) => [c.lang, c.meta].filter(Boolean).join(' ').trim();
const value = (c: Code) => c.value.replace(/\n+$/, '');

export function fenceHtml(code: string, lang: string, st: FenceState): string {
  if (lang === 'quiz') return quizFence(code, st);
  if (lang === 'syntax') return syntaxFence(code);
  return plainFence(code, lang);
}

export default function remarkLegacyFences(this: unknown, opts: { state?: FenceState } = {}) {
  return async (tree: Root) => {
    await initHighlighter();
    const st = opts.state ?? { quizN: 0 };
    const walk = (node: Parent) => {
      const kids = node.children as any[];
      for (let i = 0; i < kids.length; i++) {
        const k = kids[i];
        if (k.type === 'code') {
          const lang = info(k);
          let htmlStr: string;
          const nx = kids[i + 1];
          if (lang === 'abap' && nx?.type === 'code' && info(nx) === 'abap-old') {
            htmlStr = synPair(value(k), value(nx));
            kids.splice(i + 1, 1);
          } else {
            if (lang === 'abap-old') throw new Error('짝 없는 ```abap-old 블록 (바로 앞에 ```abap 이 있어야 해요)');
            htmlStr = fenceHtml(value(k), lang, st);
          }
          kids[i] = { type: 'html', value: htmlStr } satisfies Html;
        } else if ('children' in k) walk(k);
      }
    };
    walk(tree);
  };
}
