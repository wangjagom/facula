/**
 * build.py(파이썬)와 똑같이 동작하게 하는 작은 도구들.
 * - esc / unescape: html.escape / html.unescape
 * - W: 파이썬 정규식의 \w (유니코드 글자 포함). JS의 \w, \b는 ASCII만 봐요.
 * - PyRandom: random.Random(seed).shuffle 과 같은 순서를 내는 메르센 트위스터
 */
import { decodeHTML } from 'entities';

export function esc(s: string, quote = true): string {
  s = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  if (quote) s = s.replace(/"/g, '&quot;').replace(/'/g, '&#x27;');
  return s;
}

export const unescape = (s: string): string => decodeHTML(s);

/** 태그 지우기: re.sub(r"<[^>]+>", "", s) */
export const stripTags = (s: string): string => s.replace(/<[^>]+>/g, '');

/** 파이썬 \w 에 해당하는 문자 클래스(정규식 u 플래그와 함께 써요) */
export const W = '[\\p{L}\\p{N}\\p{M}_]';
/** 파이썬 \b 앞뒤 경계 */
export const B_START = `(?<!${W})`;
export const B_END = `(?!${W})`;

/** 파이썬 str 길이(코드 포인트 수) */
export const pyLen = (s: string): number => Array.from(s).length;
export const pySlice = (s: string, a: number, b?: number): string => Array.from(s).slice(a, b).join('');

/** CPython random.Random(int) 와 같은 수열 */
export class PyRandom {
  private mt = new Uint32Array(624);
  private idx = 625;

  constructor(seed: number) {
    let n = Math.abs(Math.trunc(seed));
    const key: number[] = [];
    if (n === 0) key.push(0);
    while (n > 0) {
      key.push(n % 0x100000000);
      n = Math.floor(n / 0x100000000);
    }
    this.initByArray(key);
  }

  private initGenrand(s: number) {
    const mt = this.mt;
    mt[0] = s >>> 0;
    for (let i = 1; i < 624; i++) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = (Math.imul(1812433253, prev) + i) >>> 0;
    }
    this.idx = 624;
  }

  private initByArray(key: number[]) {
    const mt = this.mt;
    this.initGenrand(19650218);
    let i = 1, j = 0;
    for (let k = Math.max(624, key.length); k > 0; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(prev, 1664525)) + key[j] + j) >>> 0;
      i++; j++;
      if (i >= 624) { mt[0] = mt[623]; i = 1; }
      if (j >= key.length) j = 0;
    }
    for (let k = 623; k > 0; k--) {
      const prev = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(prev, 1566083941)) - i) >>> 0;
      i++;
      if (i >= 624) { mt[0] = mt[623]; i = 1; }
    }
    mt[0] = 0x80000000;
  }

  private genrand(): number {
    const mt = this.mt;
    if (this.idx >= 624) {
      for (let k = 0; k < 624; k++) {
        const y = (mt[k] & 0x80000000) | (mt[(k + 1) % 624] & 0x7fffffff);
        mt[k] = (mt[(k + 397) % 624] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0)) >>> 0;
      }
      this.idx = 0;
    }
    let y = mt[this.idx++];
    y ^= y >>> 11;
    y = (y ^ ((y << 7) & 0x9d2c5680)) >>> 0;
    y = (y ^ ((y << 15) & 0xefc60000)) >>> 0;
    y ^= y >>> 18;
    return y >>> 0;
  }

  /** getrandbits(k), k <= 32 */
  private getrandbits(k: number): number {
    return this.genrand() >>> (32 - k);
  }

  private randbelow(n: number): number {
    const k = n.toString(2).length;
    let r = this.getrandbits(k);
    while (r >= n) r = this.getrandbits(k);
    return r;
  }

  shuffle<T>(x: T[]): void {
    for (let i = x.length - 1; i > 0; i--) {
      const j = this.randbelow(i + 1);
      [x[i], x[j]] = [x[j], x[i]];
    }
  }
}
