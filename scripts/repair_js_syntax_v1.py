#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import tempfile

MARKER = "GABON360-JS-SYNTAX-REPAIR-V3"
REQUIRED = [
    "GABON360-UNIVERSAL-MODULE-PAGES-V1",
    "GABON360-PAGE-FUNCTIONALITY-V2",
    "GABON360-AI-OPTION-RUNTIME-V2",
    "GABON360-AVATAR-HOME-V1",
]

WEATHER_FIX = r'''function weatherPage(){
shell('🌦️ Météo opérationnelle','<div class="g360-v2-actions"><button id="g360-weather-gps" type="button">📍 Position GPS</button><button id="g360-weather-lib" type="button">🇬🇦 Libreville</button></div><div class="g360-v2-box g360-v2-result">Sélectionnez une zone.</div>');
function load(lat,lon,label){
  var url='https://api.open-meteo.com/v1/forecast?latitude='+lat+'&longitude='+lon+'&current=temperature_2m,relative_humidity_2m,precipitation,wind_speed_10m,weather_code&forecast_days=3';
  fetch(url)
    .then(function(response){ return response.json(); })
    .then(function(data){
      var c=data.current||{};
      var message=label+
        '\\nTempérature : '+(c.temperature_2m??'—')+' °C'+
        '\\nHumidité : '+(c.relative_humidity_2m??'—')+' %'+
        '\\nPluie : '+(c.precipitation??'—')+' mm'+
        '\\nVent : '+(c.wind_speed_10m??'—')+' km/h'+
        '\\nCode météo : '+(c.weather_code??'—');
      out(message);
    })
    .catch(function(error){ out('Météo indisponible : '+error.message); });
}
var weatherLibreville=card.querySelector('#g360-weather-lib');
var weatherGps=card.querySelector('#g360-weather-gps');
if(weatherLibreville)weatherLibreville.onclick=function(){ load(0.3901,9.4544,'Libreville'); };
if(weatherGps)weatherGps.onclick=function(){
  if(!navigator.geolocation){ out('GPS indisponible.'); return; }
  navigator.geolocation.getCurrentPosition(
    function(position){ load(position.coords.latitude,position.coords.longitude,'Position GPS'); },
    function(error){ out('GPS indisponible : '+error.message); },
    {enableHighAccuracy:true,timeout:15000}
  );
};
}

'''

def node_check(src):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(src)
        name = f.name
    try:
        r = subprocess.run(["node", "--check", name], capture_output=True, text=True)
        return r.returncode == 0, (r.stderr or "")
    finally:
        Path(name).unlink(missing_ok=True)

def select_index():
    htmls = sorted(Path("android_project").rglob("index.html"), key=lambda p: (len(p.parts), str(p)))
    if not htmls:
        raise SystemExit("JS-SYNTAX-REPAIR FAIL: index.html introuvable")
    candidates = []
    for p in htmls:
        h = p.read_text(encoding="utf-8", errors="ignore")
        score = sum(x in h for x in REQUIRED)
        candidates.append((score, p, h))
    score, path, html = max(candidates, key=lambda x: (x[0], -len(x[1].parts), str(x[1])))
    if score < len(REQUIRED):
        raise SystemExit(f"JS-SYNTAX-REPAIR FAIL: mauvais index.html sélectionné score={score}/{len(REQUIRED)}")
    return path, html

def repair_confirmed_weather(html):
    start = html.find("function weatherPage(){")
    if start < 0:
        return html, False
    end = html.find("function maritimePage(){", start)
    if end < 0:
        return html, False
    current = html[start:end]
    ok, _ = node_check(current)
    if ok:
        return html, False
    repaired = html[:start] + WEATHER_FIX + html[end:]
    ok2, err2 = node_check(WEATHER_FIX)
    if not ok2:
        raise SystemExit("JS-SYNTAX-REPAIR FAIL: correction météo invalide: " + err2)
    return repaired, True

def repair_script_block(block):
    ok, err = node_check(block)
    if ok:
        return block, False
    if "Unexpected token ')'" not in err and "Unexpected token ')' " not in err:
        return block, False
    m = re.search(r"\.js:(\d+)", err)
    if not m:
        return block, False
    line_no = int(m.group(1))
    lines = block.splitlines(keepends=True)
    if not (1 <= line_no <= len(lines)):
        return block, False
    line = lines[line_no - 1]
    candidates = []
    for idx, ch in enumerate(line):
        if ch != ")":
            continue
        trial_lines = list(lines)
        trial_lines[line_no - 1] = line[:idx] + line[idx + 1:]
        trial = "".join(trial_lines)
        ok2, _ = node_check(trial)
        if ok2:
            candidates.append(trial)
            if len(candidates) > 1:
                return block, False
    if len(candidates) == 1:
        return candidates[0], True
    return block, False

def main():
    path, html = select_index()
    html, weather_changed = repair_confirmed_weather(html)
    if weather_changed:
        print("JS-SYNTAX-REPAIR: correction ciblée du bloc weatherPage() confirmée")
        path.write_text(html, encoding="utf-8")

    pattern = re.compile(r"(<script(?:\s[^>]*)?>)(.*?)(</script>)", re.I | re.S)
    matches = list(pattern.finditer(html))
    out = []
    last = 0
    changes = 0
    failing_blocks = []

    for idx, m in enumerate(matches):
        out.append(html[last:m.start()])
        opening, body, closing = m.group(1), m.group(2), m.group(3)
        fixed, changed = repair_script_block(body)
        if changed:
            changes += 1
            print(f"JS-SYNTAX-REPAIR: correction sûre dans le bloc {idx}")
        else:
            ok, err = node_check(body)
            if not ok:
                failing_blocks.append((idx, err))
        out.append(opening + fixed + closing)
        last = m.end()
    out.append(html[last:])

    html2 = "".join(out)
    if failing_blocks:
        print("JS-SYNTAX-REPAIR: blocs encore invalides:")
        for idx, err in failing_blocks:
            print(f" - bloc {idx}: {err}")
        raise SystemExit("JS-SYNTAX-REPAIR FAIL: syntaxe JavaScript encore invalide")

    if changes or weather_changed:
        if MARKER not in html2:
            marker = f"<!-- {MARKER} -->\n"
            pos = html2.lower().rfind("</body>")
            html2 = html2[:pos] + marker + html2[pos:] if pos >= 0 else html2 + "\n" + marker
        path.write_text(html2, encoding="utf-8")
        print("JS-SYNTAX-REPAIR: corrections=", changes + int(weather_changed))
    else:
        print("JS-SYNTAX-REPAIR: aucune correction nécessaire")

if __name__ == "__main__":
    main()
