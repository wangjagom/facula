/**
 * 교재 하나: doc.md(원본 그대로) -> BookModel(부 -> 개념 구조).
 * 순서는 build.py와 같아요: 원본 손질 -> 마크다운 -> HTML 후처리 -> 부/개념으로 나누기.
 */
import { unified } from 'unified';
import remarkParse from 'remark-parse';
import remarkRehype from 'remark-rehype';
import rehypeStringify from 'rehype-stringify';
import remarkGfmTable from '../../plugins/remark-gfm-table';
import remarkLegacyFences from '../../plugins/remark-legacy-fences';
import * as P from './passes';
import { unescape } from './py';
import { allFigures, iconMap } from './legacy';
import { newIconCtx } from './icons';
import type { BookConfig, BookModel, Part, Concept } from './types';
import type { IconKey } from './icons';

/** CommonMark는 `**순서**로`처럼 닫는 ** 뒤에 한글이 오면 굵게를 못 닫아요. 줄마다 짝을 맞춰 <strong>으로 바꿔요. */
export function fixBold(text: string): string {
  const out: string[] = [];
  let inFence = false;
  for (let line of text.split('\n')) {
    if (line.trimStart().startsWith('```')) { inFence = !inFence; out.push(line); continue; }
    if (inFence || !line.includes('**')) { out.push(line); continue; }
    const masked = line.replace(/`[^`\n]*`/g, (m) => '\0'.repeat(m.length));
    const pos = [...masked.matchAll(/\*\*/g)].map((m) => m.index!);
    const repl = new Map<number, string>();
    for (let k = 0; k + 1 < pos.length; k += 2) {
      const i = pos[k], j = pos[k + 1];
      if (line.slice(i + 2, j).includes('|')) continue;
      if (j + 2 < line.length && /[가-힣]/.test(line[j + 2])) { repl.set(i, '<strong>'); repl.set(j, '</strong>'); }
    }
    if (repl.size) {
      const res: string[] = [];
      let idx = 0;
      for (const q of [...repl.keys()].sort((a, b) => a - b)) { res.push(line.slice(idx, q), repl.get(q)!); idx = q + 2; }
      res.push(line.slice(idx));
      line = res.join('');
    }
    out.push(line);
  }
  return out.join('\n');
}

/** 원본 손질: 굵게 보정, 제목·날짜 3줄 빼기(머리말은 book.yaml로 새로 만들어요), 그림 자리 표시 */
export function prepareSource(md: string): string {
  md = fixBold(md);
  const lines = md.split('\n');
  if (!lines[0].startsWith('# ')) throw new Error('doc.md 첫 줄은 "# 제목" 이어야 해요');
  return lines.slice(3).join('\n')
    .replace(/^&#91;embedded content:\s*([^\n]*?)\\\]\s*$/gm, (_m, g: string) => `<!--DIAGRAM:${g.split(' · ')[0].trim()}-->`);
}

export async function markdownToHtml(md: string): Promise<string> {
  const file = await unified()
    .use(remarkParse)
    .use(remarkGfmTable)
    .use(remarkLegacyFences, { state: { quizN: 0 } })
    .use(remarkRehype, { allowDangerousHtml: true })
    .use(rehypeStringify, { allowDangerousHtml: true, characterReferences: { useNamedReferences: true } })
    .process(md);
  return String(file);
}

const headOf = (plain: string) => unescape(plain).split(':')[0].trim().split(' {')[0].trim();

/** 부(section)와 개념(h3)으로 나누고 아이콘을 정해요 */
function splitParts(h: string, cfg: BookConfig, toc: P.TocEntry[], unmapped: Set<string>) {
  const im = iconMap();
  const parts: Part[] = [];
  let last = 0;
  for (const m of h.matchAll(/<section class="part" id="(part-\d+)"[^>]*>([\s\S]*?)<\/section>/g)) {
    const sid = m[1], inner = m[2];
    const idx = parseInt(sid.split('-')[1], 10);
    const h2m = inner.match(/^\s*(<h2 [\s\S]*?<\/h2>)([\s\S]*)$/)!;
    const chunks = h2m[2].split(/(?=<h3 id="s\d+")/);
    const partIcon = cfg.partIcons[String(idx)];
    if (!partIcon) throw new Error(`${cfg.slug}: partIcons에 ${idx}번 부 아이콘이 없어요`);
    const concepts: Concept[] = chunks.slice(1).map((ch) => {
      const hm = ch.match(/^<h3 id="(s\d+)" data-plain="([^"]*)"/)!;
      const plain = unescape(hm[2]).trim();
      const key = im.concept[headOf(plain)] as IconKey | undefined;
      if (!key) unmapped.add(headOf(plain));
      return { hid: hm[1], plainAttr: hm[2], plain, html: ch, icon: key ?? partIcon };
    });
    const t = toc[idx];
    parts.push({ sid, idx, eyebrow: t.eyebrow, short: t.short, h2: h2m[1], intro: chunks[0], concepts, icon: partIcon,
      lead: h.slice(last, m.index) });
    last = m.index! + m[0].length;
  }
  return { parts, after: h.slice(last) };
}

export async function buildBook(cfg: BookConfig, docMd: string): Promise<BookModel> {
  let h = await markdownToHtml(prepareSource(docMd));
  h = P.tasks(h);
  h = P.projectTags(h);
  h = P.tableWrap(h);
  h = P.insertFigures(h, allFigures());
  const hd = P.headings(h);
  h = hd.html;
  h = P.labelTables(h);
  h = P.tips(h);
  h = P.liTitles(h);
  h = P.wrapFix(h);
  h = P.pTitles(h);
  // 아이콘 심볼 묶음은 페이지를 다 만든 뒤 실제로 쓴 <use href="#t-…">를 모아 만들어요(icons.ts iconDefs)
  h = P.extIcons(P.keycaps(h, cfg.keycapSkip), newIconCtx());
  h = P.autoTerms(P.linkParts(h, cfg), cfg);
  const unmapped = new Set<string>();
  const { parts, after } = splitParts(h, cfg, hd.toc, unmapped);
  return { config: cfg, parts, after, unmapped: [...unmapped].sort() };
}
