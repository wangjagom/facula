/**
 * BookModel -> 페이지 조각(본문, 목차, 레일, "이 부의 개념"). build.py의 build_pages / toc_block 등과 같은 HTML.
 *
 * 다음 단계(A2: 개념마다 실제 주소)를 위해 링크 주소는 모두 href()에서만 만들어요.
 * 지금은 한 페이지 안의 해시(#part-N, #sN)예요.
 */
import { esc, unescape } from './py';
import { firstSentence } from './passes';
import { iconUse, newIconCtx, type IconKey } from './icons';
import type { BookModel, Part } from './types';

/** 페이지(부 또는 개념) id -> 링크 주소. A2로 바꿀 때는 여기만 바꾸면 돼요. */
export const href = (id: string) => `#${id}`;

const ic = (key: IconKey, cls: string, flat = false) => iconUse(newIconCtx(), key, cls, flat);
const noNum = (e: string) => e === '시작' || e === '부록';
const pageLabel = (p: Part) => noNum(p.eyebrow) ? p.short : `${p.eyebrow} · ${p.short}`;
const headText = (plain: string) => plain.split(':')[0].trim();

/** 책 전체를 읽는 순서: 부 페이지 -> 그 부의 개념 페이지들 -> 다음 부 … */
export function readingOrder(book: BookModel): [id: string, label: string][] {
  const pages: [string, string][] = [];
  for (const p of book.parts) {
    pages.push([p.sid, pageLabel(p)]);
    for (const c of p.concepts) pages.push([c.hid, noNum(p.eyebrow) ? headText(c.plain) : `${p.eyebrow} · ${headText(c.plain)}`]);
  }
  return pages;
}

function pagerInner(pages: [string, string][], pid: string): string {
  const k = pages.findIndex(([id]) => id === pid);
  if (k < 0) return '';
  let prev = '', next = '';
  if (k > 0) prev = `<a class="prev" href="${href(pages[k - 1][0])}"><span class="dir">← 이전</span><span class="ttl">${esc(pages[k - 1][1])}</span></a>`;
  if (k < pages.length - 1) next = `<a class="next" href="${href(pages[k + 1][0])}"><span class="dir">다음 →</span><span class="ttl">${esc(pages[k + 1][1])}</span></a>`;
  return prev + next;
}

const headWrap = (ch: string, icHtml: string) => {
  const i = ch.indexOf('</h3>') + 5;
  return `<div class="c-head">${icHtml}${ch.slice(0, i)}</div>${ch.slice(i)}`;
};

/** 부 하나(부 페이지 + 그 안의 개념 페이지들) */
export function renderPart(book: BookModel, p: Part, pages = readingOrder(book)): string {
  const crumb = esc(pageLabel(p));
  let lst = '';
  if (p.concepts.length) {
    const items = p.concepts.map((c) =>
      `<li><a href="${href(c.hid)}">${ic(c.icon, 'cl-ic', true)}<span class="cl-body">` +
      `<span class="cl-t">${esc(headText(c.plain))}</span>` +
      `<span class="cl-d">${esc(firstSentence(c.html))}</span></span></a></li>`).join('');
    lst = `<nav class="concept-list" aria-label="이 부의 개념"><p class="cl-title">이 부에서 배울 개념 ${p.concepts.length}개</p><ol>${items}</ol></nav>`;
  }
  const cons = p.concepts.map((c) =>
    `<div class="concept" id="c-${c.hid}"><p class="crumb"><a href="${href(p.sid)}">${crumb}</a></p>` +
    `${headWrap(c.html, ic(c.icon, 'c-ic'))}<nav class="pager" aria-label="페이지 이동">${pagerInner(pages, c.hid)}</nav></div>`).join('');
  return `<section class="part" id="${p.sid}" aria-labelledby="${p.sid}-h"><div class="part-head">${ic(p.icon, 'p-ic')}${p.h2}</div>${p.intro}${lst}${cons}` +
    `<nav class="pager part-pager" aria-label="페이지 이동">${pagerInner(pages, p.sid)}</nav></section>`;
}

export function renderBody(book: BookModel): string {
  const pages = readingOrder(book);
  return book.parts.map((p) => p.lead + renderPart(book, p, pages)).join('') + book.after;
}

const SVG_CHEV = '<svg class="chev" viewBox="0 0 16 16" width="14" height="14" aria-hidden="true"><path d="M6 3.5l4.5 4.5L6 12.5" ' +
  'fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>';
const EXT_SVG = '<svg class="ext" width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
  '<path d="M14 4h6v6M20 4l-9 9M18 14v5a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h5"/></svg>';

/** 왼쪽 목차(그룹 -> 부 -> 개념) */
export function renderToc(book: BookModel, cls = 'toc'): string {
  const out: string[] = [];
  for (const g of book.config.groups) {
    const row = (i: number) => {
      const p = book.parts[i];
      const has = p.concepts.length > 0;
      const num = noNum(p.eyebrow) ? '' : p.eyebrow;
      const btn = has
        ? `<button type="button" class="tree-btn" aria-expanded="false" aria-label="${esc(p.short)} 펼치기·접기">${SVG_CHEV}</button>`
        : '<span class="tree-btn tree-gap"></span>';
      const sub = has ? '<div class="toc-sub-wrap"><ul class="toc-sub">' + p.concepts.map((c) =>
        `<li><a href="${href(c.hid)}"><span class="toc-t">${esc(headText(unescape(c.plainAttr)))}</span></a></li>`).join('') + '</ul></div>' : '';
      return `<li class="tree-item${has ? ' has-sub' : ''}" data-part="${p.sid}"><div class="tree-row">${btn}` +
        `<a href="${href(p.sid)}"><span class="toc-num">${num}</span><span class="toc-t">${esc(p.short)}</span></a></div>${sub}</li>`;
    };
    out.push(`<div class="toc-group open"><button type="button" class="toc-head" aria-expanded="true">${SVG_CHEV}<span>${g.name}</span></button>` +
      `<div class="toc-sub-wrap group-wrap"><ul class="${cls}">${g.parts.map(row).join('')}</ul></div></div>`);
  }
  const items = book.config.extras.map((x) => '<li class="tree-item"><div class="tree-row"><span class="tree-btn tree-gap"></span>' +
    `<a href="${x.url}" target="_blank" rel="noopener" class="ext-link" title="새 창에서 열기"><span class="toc-ic">` + ic(x.icon, 't-ic', true) +
    `</span><span class="toc-t">${x.label}</span>` + EXT_SVG + '</a></div></li>').join('');
  out.push('<div class="toc-group open tool-group"><button type="button" class="toc-head" aria-expanded="true">' + SVG_CHEV + '<span>부가 기능</span></button>' +
    '<div class="toc-sub-wrap group-wrap"><ul class="' + cls + '">' + items + '</ul></div></div>');
  return out.join('');
}

/** 목차를 접었을 때의 좁은 레일 */
export function renderRail(book: BookModel): string {
  return book.parts.map((p) => `<a href="${href(p.sid)}" title="${esc(p.short)}">` +
    `${noNum(p.eyebrow) ? (p.eyebrow === '시작' ? '안내' : '부록') : p.eyebrow}</a>`).join('') +
    book.config.extras.map((x) => `<a href="${x.url}" target="_blank" rel="noopener" title="${x.label} (새 창)" class="rail-ic">` + ic(x.icon, 't-ic', true) + '</a>').join('');
}

/** 오른쪽 "이 부의 개념" */
export function renderOtp(book: BookModel): string {
  return book.parts.map((p, j) => `<ul class="otp-list" data-sec="${p.sid}"` + (j ? ' hidden' : '') + '>' +
    p.concepts.map((c) => `<li><a href="${href(c.hid)}">${c.plainAttr}</a></li>`).join('') + '</ul>').join('');
}
