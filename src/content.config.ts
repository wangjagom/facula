import { defineCollection } from 'astro:content';
import { legacyBookLoader } from './lib/book/loader';

export const collections = {
  /** content/<주제>/doc.md + book.yaml (기존 마크다운 문법 그대로) */
  books: defineCollection({ loader: legacyBookLoader({ base: 'content' }) }),
};
