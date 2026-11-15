/** GFM 중 표만 켜요(build.py: MarkdownIt("commonmark").enable("table")). 체크박스·취소선·자동 링크는 켜지 않아요. */
import { gfmTable } from 'micromark-extension-gfm-table';
import { gfmTableFromMarkdown, gfmTableToMarkdown } from 'mdast-util-gfm-table';

export default function remarkGfmTable(this: any) {
  const data = this.data();
  (data.micromarkExtensions ??= []).push(gfmTable());
  (data.fromMarkdownExtensions ??= []).push(gfmTableFromMarkdown());
  (data.toMarkdownExtensions ??= []).push(gfmTableToMarkdown());
}
