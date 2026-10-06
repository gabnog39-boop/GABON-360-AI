#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-NATIVE-AVATAR-STATUS-FIX-V1 -->'
PAYLOAD=r'''<!-- GABON360-NATIVE-AVATAR-STATUS-FIX-V1 -->
<script>
(function(){
  if(window.__G360_NATIVE_AVATAR_STATUS_FIX)return;
  window.__G360_NATIVE_AVATAR_STATUS_FIX=true;
  function nativeReady(){return !!(window.G360Android&&typeof window.G360Android.speak==='function');}
  function setStatus(t){var s=document.getElementById('g360-avatar-life-text');if(s)s.textContent=t;}
  function ready(){setStatus(nativeReady()?'IA centrale prête — voix native Android active':'IA centrale prête — initialisation de la voix');}
  function speaking(){setStatus('IA centrale en train de parler…');}
  function nativeAnnounce(text){
    text=String(text||'').trim(); if(!text)return false;
    if(nativeReady()){speaking();try{window.G360Android.speak(text);return true}catch(e){}}
    return false;
  }
  if(window.GABON360_AVATAR_LIVE){
    window.GABON360_AVATAR_LIVE.voiceReady=nativeReady;
    window.GABON360_AVATAR_LIVE.announce=function(t){return nativeAnnounce(t)||('speechSynthesis' in window);};
  }
  window.GABON360_AVATAR_ANNOUNCE=nativeAnnounce;
  window.addEventListener('gabon360:ai-speak',function(e){
    var t=e&&e.detail&&e.detail.text;
    if(t&&nativeAnnounce(t))setTimeout(ready,Math.max(1800,String(t).length*65));
  },true);
  ready(); window.addEventListener('load',ready);
  var n=0,timer=setInterval(function(){ready();if(nativeReady()||++n>20)clearInterval(timer);},250);
})();
</script>
'''

def main():
    htmls=sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts))
    if not htmls: raise SystemExit('index.html introuvable')
    p=htmls[0]; t=p.read_text(encoding='utf-8')
    if MARK in t:
        print('Avatar native status fix déjà présente'); return
    i=t.lower().rfind('</body>')
    if i<0: raise SystemExit('</body> introuvable')
    p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
    print('Avatar native status fix installée:',p)
if __name__=='__main__': main()
