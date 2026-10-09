#!/usr/bin/env python3
from pathlib import Path
import re
import subprocess
import tempfile

MARKER = "GABON360-JS-SYNTAX-REPAIR-V4"
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
  fetch(url).then(function(response){return response.json();}).then(function(data){
    var c=data.current||{};
    out(label+'\\nTempérature : '+(c.temperature_2m??'—')+' °C\\nHumidité : '+(c.relative_humidity_2m??'—')+' %\\nPluie : '+(c.precipitation??'—')+' mm\\nVent : '+(c.wind_speed_10m??'—')+' km/h\\nCode météo : '+(c.weather_code??'—'));
  }).catch(function(error){out('Météo indisponible : '+error.message);});
}
var weatherLibreville=card.querySelector('#g360-weather-lib');
var weatherGps=card.querySelector('#g360-weather-gps');
if(weatherLibreville)weatherLibreville.onclick=function(){load(0.3901,9.4544,'Libreville');};
if(weatherGps)weatherGps.onclick=function(){
  if(!navigator.geolocation){out('GPS indisponible.');return;}
  navigator.geolocation.getCurrentPosition(function(position){
    load(position.coords.latitude,position.coords.longitude,'Position GPS');
  },function(error){out('GPS indisponible : '+error.message);},{enableHighAccuracy:true,timeout:15000});
};
}

'''

MAP_FIX = r'''function mapPage(){
shell('🗺️ Carte / SIG — sélection interactive','<div class="g360-v2-box">Touchez ou cliquez directement sur la carte pour placer un point.</div><div id="g360-v2-map" class="g360-v2-map"></div><div class="g360-v2-box"><b>Point sélectionné</b><div id="g360-v2-coord">Aucun point.</div><div class="g360-v2-actions"><button id="g360-v2-savepoint">📌 Enregistrer</button><button id="g360-v2-gps">📍 GPS</button><button id="g360-v2-clearpoints">🗑 Effacer</button></div></div><div class="g360-v2-box"><b>Points enregistrés</b><div id="g360-v2-list" class="g360-v2-list"></div></div><div class="g360-v2-box g360-v2-result">Touchez la carte.</div>');
var m=window.GABON360_REAL_LEAFLET_MAP||null;
function ready(mm){
 if(!mm)return;
 window.GABON360_REAL_LEAFLET_MAP=mm;
 var marker=null;
 function pick(e){
  var c={lat:e.latlng.lat,lon:e.latlng.lng,time:Date.now()};
  window.GABON360_SELECTED_COORDINATES=c;
  if(marker)mm.removeLayer(marker);
  marker=L.marker([c.lat,c.lon]).addTo(mm);
  card.querySelector('#g360-v2-coord').textContent=c.lat.toFixed(6)+'°, '+c.lon.toFixed(6)+'°';
  out('Point sélectionné : '+c.lat.toFixed(6)+'°, '+c.lon.toFixed(6)+'°');
  window.dispatchEvent(new CustomEvent('gabon360:coordinates-selected',{detail:c}));
 }
 mapClickSetup(mm,pick);
 card.querySelector('#g360-v2-savepoint').onclick=function(){
  var c=selected();
  if(!c){out('Sélectionnez d’abord un point.');return;}
  var d=db();d.waypoints=d.waypoints||[];
  d.waypoints.push({lat:c.lat,lon:c.lon,created_at:new Date().toISOString(),source:'carte'});
  save(d);renderList();out('Point enregistré.');
 };
 card.querySelector('#g360-v2-gps').onclick=function(){
  if(!navigator.geolocation){out('GPS indisponible.');return;}
  navigator.geolocation.getCurrentPosition(function(p){
   var c=p.coords;mm.setView([c.latitude,c.longitude],15);
   pick({latlng:L.latLng(c.latitude,c.longitude)});
  },function(e){out('GPS indisponible : '+e.message);},{enableHighAccuracy:true,timeout:15000,maximumAge:5000});
 };
 card.querySelector('#g360-v2-clearpoints').onclick=function(){
  var d=db();d.waypoints=[];save(d);renderList();out('Points locaux effacés.');
 };
 function renderList(){
  var d=db(),l=card.querySelector('#g360-v2-list');
  l.innerHTML=(d.waypoints||[]).slice(-50).reverse().map(function(w){
   return '<div class="g360-v2-item">📌 '+Number(w.lat).toFixed(6)+', '+Number(w.lon).toFixed(6)+'<br><small>'+esc(w.created_at||'')+'</small></div>';
  }).join('')||'Aucun point enregistré.';
 }
 renderList();
}
if(m)ready(m);else mapLoader(card.querySelector('#g360-v2-map'),[-0.65,11.65],6).then(ready);
}

'''

def node_check(src):
    with tempfile.NamedTemporaryFile("w", suffix=".js", encoding="utf-8", delete=False) as f:
        f.write(src)
        name=f.name
    try:
        r=subprocess.run(["node","--check",name],capture_output=True,text=True)
        return r.returncode==0,(r.stderr or "")
    finally:
        Path(name).unlink(missing_ok=True)

def select_index():
    htmls=sorted(Path("android_project").rglob("index.html"),key=lambda p:(len(p.parts),str(p)))
    if not htmls: raise SystemExit("JS-SYNTAX-REPAIR FAIL: index.html introuvable")
    candidates=[]
    for p in htmls:
        h=p.read_text(encoding="utf-8",errors="ignore")
        candidates.append((sum(x in h for x in REQUIRED),p,h))
    score,path,html=max(candidates,key=lambda x:(x[0],-len(x[1].parts),str(x[1])))
    if score<len(REQUIRED): raise SystemExit(f"JS-SYNTAX-REPAIR FAIL: mauvais index.html sélectionné score={score}/{len(REQUIRED)}")
    return path,html

def replace_function(html,name,next_name,fixed):
    start=html.find("function "+name+"(){")
    if start<0:return html,False
    end=html.find("function "+next_name+"(){",start)
    if end<0:return html,False
    current=html[start:end]
    ok,_=node_check(current)
    if ok:return html,False
    ok2,err2=node_check(fixed)
    if not ok2: raise SystemExit("JS-SYNTAX-REPAIR FAIL: correction invalide pour "+name+": "+err2)
    return html[:start]+fixed+html[end:],True

def main():
    path,html=select_index()
    changes=0

    html,changed=replace_function(html,"mapPage","satPage",MAP_FIX)
    changes+=int(changed)
    if changed: print("JS-SYNTAX-REPAIR: correction ciblée mapPage()")

    html,changed=replace_function(html,"weatherPage","maritimePage",WEATHER_FIX)
    changes+=int(changed)
    if changed: print("JS-SYNTAX-REPAIR: correction ciblée weatherPage()")

    # Confirmed defect in the Memory AI page: a ternary expression was missing its ':' branch.
    bad="}).join('')||'<div>Aucun historique enregistré. Aucune donnée fictive n’est ajoutée.</div>';"
    good="}).join(''):'<div>Aucun historique enregistré. Aucune donnée fictive n’est ajoutée.</div>';"
    if bad in html:
        html=html.replace(bad,good,1)
        changes+=1
        print("JS-SYNTAX-REPAIR: correction ciblée du rendu de la Mémoire territoriale")

    # Validate every inline JavaScript block after the targeted repairs.
    pattern=re.compile(r"(<script(?:\s[^>]*)?>)(.*?)(</script>)",re.I|re.S)
    failures=[]
    for idx,m in enumerate(pattern.finditer(html)):
        ok,err=node_check(m.group(2))
        if not ok: failures.append((idx,err))

    if failures:
        print("JS-SYNTAX-REPAIR: blocs encore invalides:")
        for idx,err in failures: print(f" - bloc {idx}: {err}")
        raise SystemExit("JS-SYNTAX-REPAIR FAIL: syntaxe JavaScript encore invalide")

    if changes:
        marker=f"<!-- {MARKER} -->\\n"
        if MARKER not in html:
            pos=html.lower().rfind("</body>")
            html=html[:pos]+marker+html[pos:] if pos>=0 else html+"\\n"+marker
        path.write_text(html,encoding="utf-8")
        print("JS-SYNTAX-REPAIR: corrections=",changes)
    else:
        print("JS-SYNTAX-REPAIR: aucune correction nécessaire")

if __name__=="__main__":
    main()
