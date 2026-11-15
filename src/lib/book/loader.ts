/**
 * Content Collections 로더: content/<주제>/book.yaml 이 있는 폴더를 교재로 읽어요.
 * doc.md는 고치지 않고 그대로 읽고, 처리 결과(BookModel)를 컬렉션에 저장해요.
 */
import { readdirSync, readFileSync, existsSync } from 'node:fs';
import { join, resolve } from 'node:path';
import { parse as parseYaml } from 'yaml';
import type { Loader } from 'astro/loaders';
import { buildBook } from './pipeline';
import type { BookConfig } from './types';

const DEFAULTS = { kicker: '', meta: [], aliases: {}, terms: [], keycapSkip: [], extras: [], termParts: [0, 0], off: 0 };

export function legacyBookLoader({ base = 'content' } = {}): Loader {
  return {
    name: 'facula-legacy-book',
    load: async ({ store, logger, generateDigest, watcher }) => {
      const root = resolve(process.cwd(), base);
      const legacy = resolve(process.cwd(), 'src', 'legacy');
      const loadAll = async () => {
        store.clear();
        for (const slug of readdirSync(root).sort()) {
          const yml = join(root, slug, 'book.yaml');
          const doc = join(root, slug, 'doc.md');
          if (!existsSync(yml) || !existsSync(doc)) continue;
          const cfg = { ...DEFAULTS, ...parseYaml(readFileSync(yml, 'utf-8')), slug } as BookConfig;
          const md = readFileSync(doc, 'utf-8');
          const t0 = Date.now();
          const model = await buildBook(cfg, md);
          logger.info(`${slug}: ${model.parts.length}부, 개념 ${model.parts.reduce((n, p) => n + p.concepts.length, 0)}개 (${Date.now() - t0}ms)`);
          logger.info(`${slug}: unmapped icons: [${model.unmapped.join(', ')}]`);
          store.set({ id: slug, data: model as unknown as Record<string, unknown>, digest: generateDigest(md + JSON.stringify(cfg)), filePath: `${base}/${slug}/doc.md` });
        }
      };
      await loadAll();
      if (watcher) {
        watcher.add([root, legacy]);
        const re = async (p: string) => {
          if (p.startsWith(root) || p.startsWith(legacy)) {
            try { await loadAll(); } catch (e) { logger.error(String(e)); }
          }
        };
        watcher.on('change', re);
        watcher.on('add', re);
      }
    },
  };
}
