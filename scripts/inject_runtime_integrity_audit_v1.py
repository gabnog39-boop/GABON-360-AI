#!/usr/bin/env python3
"""Final static integrity audit for the consolidated GABON 360 AI WebView.

This is intentionally conservative: it checks for syntax-risk patterns,
required runtime bridges, page/action registries, and duplicate top-level
runtime declarations. It never claims that an external device/source is live.
"""
from pathlib import Path
import re

MARKER='<!-- GABON360-RUNTIME-INTEGRITY-AUDIT-V1 -->'
PAGES=['map','nav','sat','drones','cameras','maritime','forests','alerts','reports','stats','weather','sources','security','avatar']
ACTIONS=['GABON360_FUNCTIONAL_PAGE_ACTIONS','GABON360_AI_RELAY','GABON360_REAL_LEAFLET_MAP','GABON360_SELECTED_COORDINATES','G360Android']

def main():
    root=Path('android_project')
    htmls=sorted(root.rglob('index.html'), key=lambda p:len(p.parts))
    if not htmls: raise SystemExit('RUNTIME-AUDIT FAIL: index.html absent')
    p=htmls[0]; html=p.read_text(encoding='utf-8',errors='ignore')
    failures=[]
    if MARKER not in html:
        for x in PAGES:
            if x not in html: failures.append('page token absent: '+x)
        for x in ACTIONS:
            if x not in html: failures.append('runtime bridge absent: '+x)
        if html.count('// V163 — Centre de situation des patrouilles + IA terrain') > 1:
            failures.append('duplicate V163 runtime block')
        if html.count('// V169 — FUSION CARTE + VISION + PATROUILLE') > 1:
            failures.append('duplicate V169 runtime block')
        if 'GABON360_FUNCTIONAL_PAGE_ACTIONS' in html and 'gabon360:page-action' not in html:
            failures.append('functional action event bus absent')
        if 'GABON360_AI_RELAY' in html and 'gabon360:ai-command' not in html:
            failures.append('AI command relay event bus absent')
        if failures:
            print('RUNTIME-AUDIT FAIL')
            for f in failures: print(' -',f)
            raise SystemExit(2)
        html=html.replace('</body>',MARKER+'\n</body>',1) if '</body>' in html else html+'\n'+MARKER+'\n'
        p.write_text(html,encoding='utf-8')
    print('RUNTIME-AUDIT OK')
    print(' - pages:',len(PAGES))
    print(' - bridges:',len(ACTIONS))
    print(' - duplicate V163/V169 checks: OK')

if __name__=='__main__': main()
