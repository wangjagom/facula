/**
 * build.py의 HTML 후처리를 같은 순서·같은 규칙으로 옮긴 것.
 * 각 함수는 HTML 문자열 -> HTML 문자열이에요(파이썬 정규식과 1:1로 대응).
 */
import { esc, unescape, stripTags, W, pyLen, pySlice } from './py';
import { iconUse, type IconKey, type IconCtx } from './icons';
import type { BookConfig } from './types';

/** `- [ ] 할 일` -> 체크 목록 */
export const tasks = (h: string) => h.split('<li>[ ] ').join('<li class="task"><span class="tick" aria-hidden="true"></span>');

/** [0205], [0108~0202, Lev05] -> 수업 날짜 태그 (<pre>…</pre> 밖에서만) */
export function projectTags(h: string): string {
  const tagRe = /\[((?:0\d{3}|Lev05)(?:[~,\s]*(?:0\d{3}|Lev05))*)\]/g;
  return h.split(/(<pre>[\s\S]*?<\/pre>)/).map((p) =>
    p.startsWith('<pre>') ? p : p.replace(tagRe, (_m, g: string) => `<span class="tag">${g.replace(/~/g, '–')}</span>`)).join('');
}

/** 표는 혼자 가로 스크롤 */
export const tableWrap = (h: string) => h.split('<table>').join('<div class="table-wrap"><table>').split('</table>').join('</table></div>');

/** <!--DIAGRAM:이름--> 자리에 그림 HTML */
export function insertFigures(h: string, figures: Record<string, string>): string {
  for (const [name, fig] of Object.entries(figures)) h = h.split(`<!--DIAGRAM:${name}-->`).join(fig);
  const left = h.match(/<!--DIAGRAM:[^>]*-->/g);
  if (left) throw new Error(`그림을 찾을 수 없어요: ${left.join(', ')} (python tools/export_legacy.py 를 다시 실행했나요?)`);
  return h;
}

export interface TocEntry { sid: string; eyebrow: string; short: string }

/** ## -> 부(section), ### -> 개념 제목(id sN, data-plain) */
export function headings(h: string): { html: string; toc: TocEntry[]; h3n: number } {
  const toc: TocEntry[] = [];
  let sec = 0;
  h = h.replace(/<h2>(.*?)<\/h2>/g, (_m, text: string) => {
    const sid = `part-${sec}`;
    sec += 1;
    const plain = stripTags(text.replace(/\s*<span class="tag">.*?<\/span>/g, '')).trim();
    const mm = plain.match(/^(\d+부|부록)\.\s*(.*)$/);
    const [eyebrow, title] = mm ? [mm[1], mm[2]] : ['시작', plain];
    const titleHtml = text.replace(/^(\d+부|부록)\.\s*/, '');
    const short = stripTags(title.split(/\s—\s/)[0]);
    toc.push({ sid, eyebrow, short });
    const close = sec > 1 ? '</section>\n' : '';
    return `${close}<section class="part" id="${sid}" aria-labelledby="${sid}-h">` +
      `<h2 id="${sid}-h"><span class="eyebrow">${eyebrow}</span><span class="h2t">${titleHtml}</span></h2>`;
  }) + '</section>';
  let h3n = 0;
  h = h.replace(/<h3>(.*?)<\/h3>/g, (_m, text: string) => {
    h3n += 1;
    const hid = `s${h3n}`;
    const plain = stripTags(text.replace(/\s*<span class="tag">.*?<\/span>/g, '')).trim();
    return `<h3 id="${hid}" data-plain="${esc(unescape(plain))}">` +
      `<a class="anchor" href="#${hid}" aria-hidden="true" tabindex="-1">#</a>${text}</h3>`;
  });
  return { html: h, toc, h3n };
}

/** 표 칸마다 data-label(모바일 카드용), 영어 대문자 헤더만 있는 표는 dbt */
export function labelTables(h: string): string {
  return h.replace(/<table>[\s\S]*?<\/table>/g, (t) => {
    const heads = [...t.matchAll(/<th[^>]*>([\s\S]*?)<\/th>/g)].map((m) => unescape(stripTags(m[1])).trim());
    if (!heads.length) return t;
    if (heads.every((x) => /^[A-Z][A-Z0-9_]*(?: \(키\))?$/.test(x) || !x) && heads.some(Boolean)) {
      return t.replace('<table>', '<table class="dbt">');
    }
    t = t.replace(/<tr>[\s\S]*?<\/tr>/g, (row) => {
      let i = 0;
      return row.replace(/<td([^>]*)>/g, (m0, attrs: string) => {
        const k = i < heads.length ? i++ : null;
        const lab = k !== null && heads[k] ? esc(heads[k], true) : '';
        return lab ? `<td data-label="${lab}"${attrs}>` : m0;
      });
    });
    t = t.replace(/(<td[^>]*>)([\s\S]*?)(<\/td>)/g, '$1<span class="cv">$2</span>$3');
    return t.replace('<table>', `<table data-cols="${heads.length}">`);
  });
}

/** {? 설명 ?} -> "?" 도움말 */
export const tips = (h: string) => h.replace(/\{\?\s([\s\S]+?)\s\?\}/g, (_m, body: string) =>
  '<span class="tip" tabindex="0" role="button" aria-label="설명 보기">?<span class="tip-body">' + body + '</span></span>');

/** 굵은 문장으로 시작하는 목록 항목: 그 문장을 제목 줄로 */
export const liTitles = (h: string) => h.replace(/<li>(<p>)?<strong>((?:(?!<\/strong>)[\s\S])*?[.!?]["”)]?)<\/strong>(?=\s*\S)/g,
  (_m, p: string | undefined, t: string) => '<li>' + (p || '') + '<strong class="li-t">' + t + '</strong>');

/** ")" 뒤 한글 조사가 떨어지지 않게(U+2060), 짧은 인라인 코드는 한 덩어리로 */
export function wrapFix(h: string): string {
  const parts = h.split(/(<pre\b[\s\S]*?<\/pre>|<script\b[\s\S]*?<\/script>|<style\b[\s\S]*?<\/style>|<[^>]*>)/);
  for (let i = 0; i < parts.length; i += 2) parts[i] = parts[i].replace(/([)\]])(?=[가-힣])/g, '$1⁠');
  h = parts.join('');
  return h.replace(/<code>((?:[^<&]|&\w+;){1,16})<\/code>/g, '<code class="nw">$1</code>');
}

/** 굵은 문장으로 시작하는 문단도 제목 줄로 */
export const pTitles = (h: string) => h.replace(/<p><strong>((?:(?!<\/strong>)[\s\S])*?[.!?]["”)]?)<\/strong>(?=\s+[^<\s])/g,
  (_m, t: string) => '<p><strong class="li-t">' + t + '</strong>');

// ---- keycaps ----
const KEYWORDS = new Set(['Ctrl', 'Shift', 'Alt', 'Tab', 'Enter', 'Esc', 'Home', 'End', 'Cmd', 'Win', 'Space', 'Backspace', 'Delete',
  'PageUp', 'PageDown', '↑', '↓', '←', '→', ...Array.from({ length: 12 }, (_, i) => `F${i + 1}`)]);
const LABELS = new Set(['마우스 휠']);
const keyOk = (t: string) => KEYWORDS.has(t) || LABELS.has(t) || (pyLen(t) === 1 && !/^\s$/.test(t));

function keycapsOne(m0: string, g1: string): string {
  const raw = unescape(g1);
  const chord = raw.includes(' → ') ? raw.split(' → ') : [raw];
  const groups: string[][] = [];
  for (const c of chord) {
    const keys = c.split(' + ');
    if (!keys.every(keyOk)) return m0;
    groups.push(keys);
  }
  const flat = groups.flat();
  if (flat.length === 1 && !KEYWORDS.has(flat[0])) return m0;
  const cap = (k: string) => LABELS.has(k) ? `<span class="kl">${esc(k)}</span>` : `<kbd>${esc(k)}</kbd>`;
  return '<span class="keys" role="text">' + groups.map((g) => g.map(cap).join('<i class="plus">+</i>')).join('<i class="then">후</i>') + '</span>';
}

/** `Ctrl + S` 같은 인라인 코드 -> 키캡. keycapSkip 부(예: UI5 part-8)는 건너뛰어요 */
export function keycaps(h: string, skip: string[]): string {
  return h.split(/(?=<section class="part" id="part-\d+")/).map((b) =>
    skip.some((sid) => b.startsWith(`<section class="part" id="${sid}"`)) ? b
      : b.replace(/<code>([^<]+)<\/code>/g, keycapsOne)).join('');
}

/** {{ic:이름:색}} 이름 -> 아이콘 */
export function extIcons(h: string, ctx: IconCtx): string {
  return h.replace(new RegExp(`\\{\\{ic:(${W}+):?(${W}*)\\}\\}\\s*([^<]*)`, 'gu'), (_m, obj: string, hue: string, name: string) =>
    `<span class="ext">${iconUse(ctx, [obj, hue || null], 'ext-ic', true)}<span class="ext-n">${name.trim()}</span></span>`);
}

// ---- 교차 링크 ----
const SKIP_TAGS = new Set(['pre', 'code', 'a', 'h2', 'h3', 'script', 'style', 'svg', 'figcaption', 'button']);
const AUTO_SKIP = new Set([...SKIP_TAGS, 'summary', 'kbd', 'th', 'figure']);
const AUTO_MAX = 5;

/** {부 번호: [(표현, h3 id)]} — '3부 배열 메서드'를 그 개념으로 잇기 위해 */
function conceptHeads(h: string, cfg: BookConfig): Map<number, [string, string][]> {
  const heads = new Map<number, [string, string][]>();
  for (const sm of h.matchAll(/<section class="part" id="part-(\d+)"[\s\S]*?(?=<section class="part"|$)/g)) {
    const n = parseInt(sm[1], 10) - cfg.off;
    const lst: [string, string][] = [];
    for (const m of sm[0].matchAll(/<h3 id="(s\d+)" data-plain="([^"]*)"/g)) {
      const plain = unescape(m[2]).trim();
      const head = plain.split(/:| — |\(| \{/)[0].trim();
      const cands = new Set([head, ...(cfg.aliases[head] ?? [])]);
      for (const c of cands) if (c) lst.push([c, m[1]]);
    }
    heads.set(n, lst.sort((a, b) => pyLen(b[0]) - pyLen(a[0])));
  }
  return heads;
}

/** 태그 밖 글자에만 fn 적용(skip 태그 안은 그대로) */
function outsideTags(h: string, skip: Set<string>, fn: (s: string) => string, depth0 = 0): string {
  let depth = depth0;
  return h.split(/(<[^>]+>)/).map((piece) => {
    if (piece.startsWith('<')) {
      const mt = piece.match(/^<(\/?)([a-zA-Z0-9]+)/);
      if (mt && skip.has(mt[2].toLowerCase()) && !piece.endsWith('/>')) depth += mt[1] ? -1 : 1;
      return piece;
    }
    return depth <= 0 ? fn(piece) : piece;
  }).join('');
}

/** '3부' -> 그 부로, '3부 배열 메서드' -> 그 개념으로 가는 링크 */
export function linkParts(h: string, cfg: BookConfig): string {
  const heads = conceptHeads(h, cfg);
  const link = (piece: string) => {
    const out: string[] = [];
    let pos = 0;
    for (const m of piece.matchAll(/(?<![\d~–\-])(\d{1,2})부(?!록|터|분)/g)) {
      const n = parseInt(m[1], 10);
      const start = m.index!;
      const end = start + m[0].length;
      if (!(n >= 0 && n <= cfg.partMax) || start < pos) continue;
      const pre = piece.slice(Math.max(0, start - 8), start);
      if (pre.endsWith('총정리 ') || pre.endsWith('UI5 ')) continue;
      out.push(piece.slice(pos, start));
      const rest = piece.slice(end);
      const mm = rest.match(/^(의)? /);
      let target = `#part-${n + cfg.off}`, labelEnd = end, shown = piece.slice(start, end), title = `${n}부로 이동`;
      if (mm) {
        const after = rest.slice(mm[0].length);
        for (const [phrase, hid] of heads.get(n) ?? []) {
          if (after.startsWith(phrase)) {
            target = `#${hid}`; shown = phrase; title = `${n}부 · ${phrase}`;
            labelEnd = end + mm[0].length + phrase.length;
            break;
          }
        }
      }
      out.push(`<a class="xref" href="${target}" title="${title}">${shown}</a>`);
      pos = labelEnd;
    }
    out.push(piece.slice(pos));
    return out.join('');
  };
  return outsideTags(h, SKIP_TAGS, link);
}

/** 앞에서 배운 개념 이름에 그 개념으로 가는 링크(개념 페이지마다 처음 한 번, 최대 5개) */
export function autoTerms(h: string, cfg: BookConfig): string {
  if (!cfg.terms.length) return h;
  const heads = conceptHeads(h, cfg);
  const table = new Map<string, [string, number, number, string]>();
  for (const [term, n, head] of cfg.terms) {
    const hid = (heads.get(n) ?? []).find(([ph]) => ph === head)?.[1];
    if (hid) table.set(term, [hid, parseInt(hid.slice(1), 10), n, head]);
  }
  if (!table.size) return h;
  const alts = [...table.keys()].sort((a, b) => pyLen(b) - pyLen(a)).map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'));
  const rx = new RegExp(`(?<![가-힣A-Za-z0-9_])(${alts.join('|')})(?![A-Za-z0-9_])`, 'g');
  const out: string[] = [];
  let partNo: number | null = null, cur: number | null = null, seen = new Set<string>(), depth = 0;
  for (const chunk of h.split(/(<section class="part" id="part-\d+"[^>]*>|<h3 id="s\d+"[^>]*>)/)) {
    const mp = chunk.match(/^<section class="part" id="part-(\d+)"/);
    const mh = chunk.match(/^<h3 id="s(\d+)"/);
    if (mp) { partNo = parseInt(mp[1], 10); cur = null; depth = 0; out.push(chunk); continue; }
    if (mh) { cur = parseInt(mh[1], 10); seen = new Set(); depth = 1; out.push(chunk); continue; }
    if (cur === null || partNo === null || !(cfg.termParts[0] <= partNo && partNo <= cfg.termParts[1])) { out.push(chunk); continue; }
    const c = cur;
    for (const piece of chunk.split(/(<[^>]+>)/)) {
      if (piece.startsWith('<')) {
        const mt = piece.match(/^<(\/?)([a-zA-Z0-9]+)/);
        if (mt && AUTO_SKIP.has(mt[2].toLowerCase()) && !piece.endsWith('/>')) depth += mt[1] ? -1 : 1;
        out.push(piece);
      } else if (depth <= 0) {
        out.push(piece.replace(rx, (m0, term: string) => {
          const [hid, num, n, head] = table.get(term)!;
          if (num >= c || seen.has(hid) || seen.size >= AUTO_MAX) return m0;
          seen.add(hid);
          return `<a class="xref term" href="#${hid}" title="${n}부 · ${head}">${term}</a>`;
        }));
      } else out.push(piece);
    }
  }
  return out.join('');
}

/** 개념 목록의 한 줄 요약: 첫 문단의 첫 문장 */
export function firstSentence(chunk: string): string {
  const m = chunk.match(/<p>([\s\S]*?)<\/p>/);
  if (!m) return '';
  let t = unescape(stripTags(m[1])).trim();
  t = t.split(/(?<=[.!?])\s/)[0];
  return pyLen(t) <= 78 ? t : pySlice(t, 0, 76).trimEnd() + '…';
}

export type { IconKey };
