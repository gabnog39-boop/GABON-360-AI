#!/usr/bin/env python3
from pathlib import Path
import re, sys

REQ_IDS = [
    'g360-avatar-launch','g360-avatar-mic','g360-avatar-modal',
    'g360-real-map','g360-terrain-v2-open','g360-pages-modal',
    'g360-satellite-panel','g360-satellite-open','g360-complete-modal'
]
REQ_PAGES = ['map','nav','sat','drones','cameras','maritime','alerts','reports','stats','weather','sources','security','avatar','field-analysis']
REQ_SECTIONS = ['dashboard','sources','infra','alerts','events','history','mapmod','logistics','missions','fieldnav','reports','offline','vision','owner','settings']


def html_ids(html: str):
    """Read IDs from actual HTML opening tags, not JavaScript strings."""
    return re.findall(r'<[A-Za-z][^>]*?\bid=[\"\']([^\"\']+)[\"\']', html, flags=re.S)


def page_is_present(html: str, page: str) -> bool:
    # 1) Explicit manual-page marker is the preferred form.
    if re.search(r'data-g360-page=[\"\']' + re.escape(page) + r'[\"\']', html):
        return True
    # 2) National module registry is a valid source of truth for pages that
    #    are rendered dynamically by inject_national_pages.py.
    if re.search(r'(?<![A-Za-z0-9_])' + re.escape(page) + r'\s*:\s*\{', html):
        if 'GABON360_NATIONAL_MODULES' in html or 'GABON360_HANDLE_COMMAND' in html:
            return True
    # 3) Avatar is a dedicated central interface, not a national module card.
    if page == 'avatar':
        return all(('id="' + x + '"' in html) or ("id='" + x + "'" in html)
                   for x in ('g360-avatar-launch','g360-avatar-modal','g360-avatar-mic'))
    return False


def main():
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('android_project')
    htmls = sorted(root.rglob('index.html'), key=lambda p: len(p.parts))
    if not htmls:
        raise SystemExit('PREFLIGHT FAIL: index.html introuvable')
    html = htmls[0].read_text(encoding='utf-8', errors='ignore')
    failures = []

    ids = html_ids(html)
    seen = set()
    dup = []
    for x in ids:
        if x in seen:
            dup.append(x)
        seen.add(x)
    if dup:
        failures.append('IDs HTML dupliqués: ' + ', '.join(sorted(set(dup))[:20]))

    for x in REQ_IDS:
        if ('id="' + x + '"' not in html) and ("id='" + x + "'" not in html):
            failures.append('ID requis absent: ' + x)

    for x in REQ_PAGES:
        if not page_is_present(html, x):
            failures.append('Page manuelle absente ou non reconnue: ' + x)

    # The field-analysis screen is injected separately and must remain reachable
    # from the page catalogue, with its own analysis engine and action handlers.
    if 'GABON360_OPEN_DATA_ANALYSIS' not in html:
        failures.append('Ouverture de la page Analyse des données terrain absente')
    if 'function analyze()' not in html or 'GABON360_FIELD_ANALYSIS' not in html:
        failures.append('Moteur IA de la page Analyse des données terrain absent')

    for x in REQ_SECTIONS:
        if not re.search(r'<section[^>]+id=[\"\']' + re.escape(x) + r'[\"\']', html):
            failures.append('Section absente: ' + x)

    if 'GABON360_REAL_LEAFLET_MAP' not in html:
        failures.append('Pont carte Leaflet réel absent')
    if 'GABON360_SELECTED_COORDINATES' not in html:
        failures.append('Pont coordonnées carte absent')
    if 'G360Android' not in html:
        failures.append('Pont JS voix/micro natif absent')
    if ('G360NativeBridge.attach(this);' not in html and
            'G360NativeBridge.attach(this);' not in ''.join(
                p.read_text(encoding='utf-8', errors='ignore') for p in root.rglob('*.java'))):
        failures.append('Attache du pont Android natif absente')

    manifests = list(root.rglob('AndroidManifest.xml'))
    if not manifests:
        failures.append('AndroidManifest.xml absent')
    else:
        mt = manifests[0].read_text(encoding='utf-8', errors='ignore')
        for perm in ['android.permission.RECORD_AUDIO', 'android.permission.ACCESS_FINE_LOCATION', 'android.permission.INTERNET']:
            if perm not in mt:
                failures.append('Permission requise absente: ' + perm)

    if failures:
        print('PREFLIGHT FAIL')
        for f in failures:
            print(' -', f)
        raise SystemExit(2)

    print('PREFLIGHT OK')
    print(' - HTML:', htmls[0])
    print(' - Pages reconnues:', len(REQ_PAGES), 'sections:', len(REQ_SECTIONS))
    print(' - Avatar + micro + carte + coordonnées + navigation + satellite: présents')
    print(' - Manifest permissions: RECORD_AUDIO, LOCATION, INTERNET')


if __name__ == '__main__':
    main()
