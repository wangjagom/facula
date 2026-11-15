/** content/<주제>/book.yaml 의 모양 */
import type { IconKey } from './icons';

export interface BookConfig {
  slug: string;
  title: string;
  sub: string;
  kicker: string;
  /** 머리말 아래 작은 글씨 줄들 */
  meta: string[];
  /** "N부" 자동 링크가 허용하는 가장 큰 N */
  partMax: number;
  /** 용어 자동 링크를 거는 부(section 번호) 범위 */
  termParts: [number, number];
  /** "N부" -> part-(N + off) */
  off: number;
  groups: { name: string; parts: number[] }[];
  /** 부(section 번호) -> 아이콘 */
  partIcons: Record<string, IconKey>;
  extras: { url: string; icon: IconKey; label: string }[];
  /** 개념 제목 -> 별칭 ("3부 함수"가 "함수 기본"을 가리키게) */
  aliases: Record<string, string[]>;
  /** [용어, 부 번호, 개념 제목] */
  terms: [string, number, string][];
  /** 키캡 변환을 건너뛰는 부 id (예: part-8) */
  keycapSkip: string[];
  /** src/legacy/refpeek/<이름>.html */
  refpeek?: string;
}

export interface Concept {
  hid: string;
  /** data-plain 속성값 그대로(이스케이프된 상태) */
  plainAttr: string;
  plain: string;
  html: string;
  icon: IconKey;
}

export interface Part {
  sid: string;
  idx: number;
  eyebrow: string;
  short: string;
  h2: string;
  intro: string;
  concepts: Concept[];
  icon: IconKey;
  /** 이 부 앞에 붙는 HTML (부 사이 줄바꿈 등) */
  lead: string;
}

/** 로더가 만들어 컬렉션에 저장하는 교재 하나 */
export interface BookModel {
  config: BookConfig;
  parts: Part[];
  /** 마지막 부 뒤에 남는 HTML (보통 비어 있어요) */
  after: string;
  unmapped: string[];
}
