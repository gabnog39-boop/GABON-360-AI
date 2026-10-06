#!/usr/bin/env python3
"""Final mobile repair for the central avatar controls.

The repair is deliberately additive: it keeps the original avatar image and
wires the visible buttons directly, with a WebView/native bridge path and a
browser speech fallback when Android native voice is not yet exposed.
"""
from pathlib import Path

MARK = "GABON360-AVATAR-CONTROLS-REPAIR-V3"

PAYLOAD = r'''<!-- GABON360-AVATAR-CONTROLS-REPAIR-V3 -->
<style>
/* Keep the central avatar usable on small screens. */
#g360-avatar-panel,
#g360-avatar-card,
#g360-avatar-central,
.g360-avatar-panel,
.g360-avatar-card { max-width:100vw!important; box-sizing:border-box!important; }
#g360-avatar-home-dock { z-index:2147483000!important; }
#g360-avatar-launch { z-index:2147483001!important; }
.g360-avatar-panel button,
.g360-avatar-card button,
#g360-avatar-panel button,
#g360-avatar-card button { position:relative!important; z-index:2147483002!important; pointer-events:auto!important; touch-action:manipulation!important; }
.g360-avatar-panel img,
.g360-avatar-card img { max-width:100%!important; height:auto!important; }
.g360-avatar-speaking { animation:g360AvatarPulse 1.1s ease-in-out infinite!important; }
@keyframes g360AvatarPulse { 0%,100%{transform:scale(1)} 50%{transform:scale(1.012)} }
</style>
<script>
(function(){
  if(window.__G360_AVATAR_CONTROLS_REPAIR_V3)return;
  window.__G360_AVATAR_CONTROLS_REPAIR_V3=true;

  var speaking=false;
  function setStatus(text){
    ['g360-native-io-status','g360-avatar-mic-status','g360-avatar-life-text','g360-avatar-status'].forEach(function(id){
      var e=document.getElementById(id); if(e)e.textContent=text;
    });
  }
  function native(){
    return window.G360Android && typeof window.G360Android.speak==='function' ? window.G360Android : null;
  }
  function avatarImages(){
    var a=[];
    document.querySelectorAll('#g360-avatar-panel img,#g360-avatar-card img,#g360-avatar-central img,#g360-avatar-launch img,#g360-avatar-home-dock img,.g360-avatar-panel img,.g360-avatar-card img').forEach(function(e){
      if(a.indexOf(e)<0)a.push(e);
    });
    return a;
  }
  function animate(on){
    avatarImages().forEach(function(e){e.classList.toggle('g360-avatar-speaking',!!on);});
  }
  function speak(text){
    text=String(text||'Bonjour Ngoua Obame. Je suis l’IA centrale de GABON 360 AI. Je suis prête à vous assister.');
    var b=native();
    speaking=true; animate(true); setStatus('IA parle…');
    if(b){try{b.speak(text);return;}catch(e){}}
    try{
      if(window.speechSynthesis){
        window.speechSynthesis.cancel();
        var u=new SpeechSynthesisUtterance(text); u.lang='fr-FR'; u.rate=0.95;
        u.onend=function(){speaking=false;animate(false);setStatus('IA prête à parler');};
        u.onerror=function(){speaking=false;animate(false);setStatus('Voix indisponible');};
        window.speechSynthesis.speak(u); return;
      }
    }catch(e){}
    speaking=false; animate(false); setStatus('Voix native en cours d’initialisation');
  }
  function listen(){
    var b=native();
    if(b && typeof b.startListening==='function'){setStatus('Écoute…');try{b.startListening();return;}catch(e){}}
    setStatus('Micro Android en cours d’autorisation');
  }
  function stop(){
    var b=native();
    try{if(b&&b.stopListening)b.stopListening();}catch(e){}
    try{if(b&&b.stopSpeaking)b.stopSpeaking();}catch(e){}
    try{if(window.speechSynthesis)window.speechSynthesis.cancel();}catch(e){}
    speaking=false;animate(false);setStatus('IA arrêtée');
  }
  function labelOf(el){return ((el.innerText||el.textContent||el.getAttribute('aria-label')||'')+'').replace(/\s+/g,' ').trim().toLowerCase();}
  function action(el){
    var l=labelOf(el);
    if(l.indexOf('faire parler')>=0 || l.indexOf('parler')>=0){speak();return true;}
    if(l==='écouter' || l.indexOf('écouter')===0 || l.indexOf('ecouter')===0){listen();return true;}
    if(l==='arrêter' || l.indexOf('arrêter')===0 || l.indexOf('arreter')===0){stop();return true;}
    return false;
  }
  function bind(){
    var nodes=[];
    document.querySelectorAll('button,a,[role="button"],input[type="button"],input[type="submit"]').forEach(function(e){if(actionable(e))nodes.push(e);});
    nodes.forEach(function(e){
      if(e.dataset.g360AvatarRepair==='1')return;
      e.dataset.g360AvatarRepair='1';
      e.addEventListener('click',function(ev){if(action(this)){ev.preventDefault();ev.stopPropagation();}},false);
      e.addEventListener('touchend',function(ev){if(action(this)){ev.preventDefault();}}, {passive:false});
    });
  }
  function actionable(e){var l=labelOf(e);return l.indexOf('faire parler')>=0||l==='écouter'||l.indexOf('écouter')===0||l==='ecouter'||l.indexOf('ecouter')===0||l==='arrêter'||l.indexOf('arrêter')===0||l==='arreter'||l.indexOf('arreter')===0;}
  window.G360AvatarSpeak=speak; window.G360AvatarListen=listen; window.G360AvatarStop=stop;
  window.G360NativeSpeechState=function(s){
    if(s==='voice-ready'||s==='ready')setStatus('IA vivante — prête à parler');
    else if(s==='listening')setStatus('Écoute…');
    else if(s==='processing')setStatus('Analyse de la commande…');
  };
  window.G360NativeSpeechResult=function(text){
    var inputs=document.querySelectorAll('input,textarea');
    var target=null; inputs.forEach(function(e){if(!target&&e.offsetParent!==null)target=e;});
    if(target){target.value=String(text||'');target.dispatchEvent(new Event('input',{bubbles:true}));target.dispatchEvent(new Event('change',{bubbles:true}));}
    setStatus('Commande reçue');
  };
  window.G360NativeSpeechError=function(text){setStatus(String(text||'Voix/micro indisponible'));};
  function ready(){bind(); if(native())setStatus('IA vivante — prête à parler');}
  ready(); window.addEventListener('load',ready); document.addEventListener('DOMContentLoaded',ready);
  new MutationObserver(function(){bind();}).observe(document.documentElement,{subtree:true,childList:true});
  var timer=setInterval(function(){bind();if(native())clearInterval(timer);},300);
})();
</script>
'''

def main():
    candidates=sorted([p for p in Path('android_project').rglob('index.html') if 'build' not in p.parts], key=lambda p:len(p.parts))
    if not candidates: raise SystemExit('index.html introuvable')
    for p in candidates:
        text=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in text:
            print('already:',p); return
        i=text.lower().rfind('</body>')
        if i<0: continue
        p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('aucun index.html exploitable')

if __name__=='__main__': main()
