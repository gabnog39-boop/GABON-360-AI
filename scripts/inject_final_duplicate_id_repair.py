#!/usr/bin/env python3
"""Remove only repeated HTML id attributes while preserving the first owner.

This runs after all injectors. It deliberately edits only real opening HTML
 tags, not JavaScript strings, so it cannot 'fix' an ID by damaging JS code.
The first occurrence remains unchanged; later occurrences lose only their id
attribute. Existing event handlers can still target the first canonical node.
"""
from pathlib import Path
import re

MARKER = '<!-- GABON360-FINAL-DUPLICATE-ID-REPAIR -->'
TAG_RE = re.compile(r'<(?P<tag>[A-Za-z][^>]*?)\bid=(?P<q>[\"\'])(?P<id>[^\"\']+)(?P=q)(?P<tail>[^>]*)>', re.S)


def repair(html: str):
    if MARKER in html:
        return html, []
    seen = set()
    duplicates = []

    def repl(m):
        ident = m.group('id')
        if ident not in seen:
            seen.add(ident)
            return m.group(0)
        duplicates.append(ident)
        # Remove only the repeated id attribute; preserve the rest of the tag.
        tag = m.group('tag')
        tail = m.group('tail')
        return '<' + tag + tail + '>'

    out = TAG_RE.sub(repl, html)
    out = out.replace('</body>', MARKER + '\n</body>', 1) if '</body>' in out else out + '\n' + MARKER + '\n'
    return out, duplicates


def main():
    root = Path('android_project')
    htmls = sorted(root.rglob('index.html'), key=lambda p: len(p.parts))
    if not htmls:
        raise SystemExit('DUPLICATE-ID-REPAIR FAIL: index.html introuvable')
    path = htmls[0]
    html = path.read_text(encoding='utf-8', errors='ignore')
    repaired, duplicates = repair(html)
    if duplicates:
        path.write_text(repaired, encoding='utf-8')
        print('DUPLICATE-ID-REPAIR: corrected', len(duplicates), 'duplicate HTML id occurrence(s):', ', '.join(sorted(set(duplicates))[:20]))
    else:
        if repaired != html:
            path.write_text(repaired, encoding='utf-8')
        print('DUPLICATE-ID-REPAIR: no duplicate HTML ids found')


if __name__ == '__main__':
    main()
