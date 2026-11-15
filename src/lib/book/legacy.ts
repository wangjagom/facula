/** src/legacy/ (파이썬 tools/export_legacy.py 결과) 읽기 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

export const legacyPath = (...p: string[]) => join(process.cwd(), 'src', 'legacy', ...p);
const read = (...p: string[]) => readFileSync(legacyPath(...p), 'utf-8');

let figIndex: Record<string, string> | null = null;
export const figureIndex = (): Record<string, string> => (figIndex ??= JSON.parse(read('figures', 'index.json')));

/** 그림 이름(마크다운의 embedded content 이름) -> HTML */
export function legacyFigure(name: string): string {
  const f = figureIndex()[name];
  if (!f) throw new Error(`레거시 그림이 없어요: ${name}`);
  return read('figures', f);
}

export const allFigures = (): Record<string, string> =>
  Object.fromEntries(Object.keys(figureIndex()).map((n) => [n, legacyFigure(n)]));

export const figureIconDefs = () => read('figure-icons.svg').trimEnd();
export const refpeekAssets = (name: string) => read('refpeek', `${name}.html`).trimEnd();
export const iconMap = (): { concept: Record<string, [string, string | null]>; part: Record<string, [string, string | null]> } =>
  JSON.parse(read('icon-map.json'));
