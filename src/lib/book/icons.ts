/** toss_icons.py의 use()/defs_svg()와 같은 출력. 심볼은 src/legacy/icons.json에서 읽어요. */
import { readFileSync } from 'node:fs';
import { legacyPath } from './legacy';

export type IconKey = [obj: string, hue: string | null];
type Mode = 'D' | 'E';

let data: { gradients: string; symbols: Record<string, string> } | null = null;
const load = () => (data ??= JSON.parse(readFileSync(legacyPath('icons.json'), 'utf-8')));

/** 한 페이지에서 쓴 아이콘을 모아 마지막에 심볼 묶음을 만들어요 */
export interface IconCtx { used: Set<string> }
export const newIconCtx = (): IconCtx => ({ used: new Set() });

export function iconUse(ctx: IconCtx, key: IconKey, cls: string, flat = false): string {
  const mode: Mode = flat ? 'D' : 'E';
  const [obj, hue] = key;
  ctx.used.add(`${obj}|${hue ?? ''}|${mode}`);
  return `<svg class="ti ${cls}" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><use href="#t-${obj}-${hue || 'x'}-${mode}"/></svg>`;
}

/** 페이지 HTML에 실제로 나온 <use href="#t-물체-색-모드">를 모아 심볼 묶음을 만들어요 */
export function iconDefs(...htmls: string[]): string {
  const d = load();
  const used = new Set<string>();
  for (const h of htmls) for (const m of h.matchAll(/<use href="#t-([a-z0-9]+)-([a-z]+)-([DE])"/g)) used.add(`${m[1]}|${m[2] === 'x' ? '' : m[2]}|${m[3]}`);
  const keys = [...used].map((k) => k.split('|')).sort((a, b) =>
    a[0] < b[0] ? -1 : a[0] > b[0] ? 1 : a[1] < b[1] ? -1 : a[1] > b[1] ? 1 : a[2] < b[2] ? -1 : a[2] > b[2] ? 1 : 0);
  const syms = keys.map((k) => {
    const s = d.symbols[k.join('|')];
    if (!s) throw new Error(`아이콘 심볼이 없어요: ${k.join('|')} (tools/export_legacy.py의 EXTRA_ICONS에 추가하고 다시 실행하세요)`);
    return s;
  }).join('');
  return `<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false"><defs>${d.gradients}${syms}</defs></svg>`;
}
