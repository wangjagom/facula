/**
 * 코드 색칠(Shiki). 색은 style.css에 있던 Pygments 색(Tokyo Night 계열)을 그대로 옮겼어요.
 * 결과는 <span style="color:…">만 이어 붙인 문자열이라 기존 <pre><code> 틀에 그대로 들어가요.
 */
import { createHighlighter, type Highlighter, type ThemeRegistration } from 'shiki';
import { esc } from './py';

const FG = '#c0caf5';
export const faculaTheme: ThemeRegistration = {
  name: 'facula',
  type: 'dark',
  colors: { 'editor.background': '#1a1b26', 'editor.foreground': FG },
  settings: [
    { settings: { foreground: FG } },
    { scope: ['comment', 'punctuation.definition.comment'], settings: { foreground: '#7a84ad', fontStyle: 'italic' } },
    { scope: ['string', 'punctuation.definition.string', 'string.quoted', 'string.template'], settings: { foreground: '#9ece6a' } },
    { scope: ['punctuation.definition.template-expression', 'punctuation.section.embedded', 'constant.character.escape'], settings: { foreground: '#89ddff' } },
    { scope: ['constant.numeric', 'constant.language', 'constant.language.boolean'], settings: { foreground: '#ff9e64' } },
    { scope: ['keyword', 'storage', 'storage.type', 'storage.modifier', 'keyword.control', 'keyword.other', 'keyword.operator.new',
              'keyword.operator.expression', 'variable.language.this'], settings: { foreground: '#bb9af7' } },
    { scope: ['keyword.operator', 'punctuation', 'meta.brace'], settings: { foreground: '#89ddff' } },
    { scope: ['entity.name.function', 'support.function', 'meta.function-call entity.name.function'], settings: { foreground: '#7aa2f7' } },
    { scope: ['support.class', 'support.type', 'support.constant', 'support.variable'], settings: { foreground: '#7dcfff' } },
    { scope: ['entity.name.tag', 'punctuation.definition.tag'], settings: { foreground: '#f7768e' } },
    { scope: ['entity.other.attribute-name'], settings: { foreground: '#e0af68' } },
    { scope: ['string.quoted.double.xml', 'string.quoted.single.xml', 'string.quoted.double.html'], settings: { foreground: '#9ece6a' } },
    // Pygments와 맞추기: 화살표는 연산자색, SQL 집계 함수·ABAP 내장 함수는 키워드색, ABAP 기본 타입(i, c …)은 기본색
    { scope: ['storage.type.function.arrow'], settings: { foreground: '#89ddff' } },
    { scope: ['support.function.aggregate.sql', 'entity.name.function.builtin.abap'], settings: { foreground: '#bb9af7' } },
    { scope: ['support.type.abap'], settings: { foreground: FG } },
  ],
};

const OP = '#89ddff';
const PUNCT = /([.,:;()[\]\-]+)/;
const LANGS = { js: 'javascript', xml: 'xml', sql: 'sql', abap: 'abap' } as const;
let hl: Highlighter | null = null;

export async function initHighlighter(): Promise<void> {
  if (!hl) hl = await createHighlighter({ themes: [faculaTheme], langs: Object.values(LANGS) });
}

/** build.py hl(code, lang)과 같은 자리: js/xml/sql/abap만 색칠, 나머지는 이스케이프만 */
export function highlight(code: string, lang: string): string {
  const name = (LANGS as Record<string, string>)[lang];
  if (!name) return esc(code, false);
  if (!hl) throw new Error('initHighlighter()를 먼저 불러야 해요');
  const { tokens } = hl.codeToTokens(code, { lang: name as any, theme: 'facula' });
  const span = (text: string, color: string, italic = false) =>
    color === FG && !italic ? esc(text, false) : `<span style="color:${color}${italic ? ';font-style:italic' : ''}">${esc(text, false)}</span>`;
  const symbolic = lang === 'abap' || lang === 'sql';
  return tokens.map((line) => line.map((t) => {
    const color = (t.color || FG).toLowerCase();
    const italic = t.fontStyle !== undefined && (t.fontStyle & 1) === 1;
    if (symbolic) {
      // Shiki의 ABAP/SQL 문법은 기호에 범위를 안 줘요(기본색). Pygments처럼 기호는 연산자색으로.
      if (color === FG && !italic) return t.content.split(PUNCT).map((p, i) => (i % 2 ? span(p, OP) : span(p, FG))).join('');
      if (lang === 'abap' && /^[=+\-/*<>]+$/.test(t.content.trim())) return span(t.content, OP);
    }
    return span(t.content, color, italic);
  }).join('')).join('\n') + '\n'; // Pygments처럼 끝에 줄바꿈 하나
}
