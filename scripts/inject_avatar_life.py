#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-AVATAR-LIFE-V1 -->'
PAYLOAD=r'''<!-- GABON360-AVATAR-LIFE-V1 -->
<style>
#g360-avatar-life{display:flex;align-items:center;gap:8px;margin-top:9px;padding:7px 9px;border:1px solid #2adf9b55;border-radius:10px;background:#04131d;color:#bdebd9;font-size:12px}
#g360-avatar-life-dot{width:9px;height:9px;border-radius:50%;background:#18e77b;box-shadow:0 0 9px #18e77b;flex:0 0 auto}
#g360-avatar-life.speaking #g360-avatar-life-dot{animation:g360pulse .35s infinite alternate}
#g360-avatar-wave{display:flex;align-items:center;gap:2px;height:16px;margin-left:auto}
#g360-avatar-wave i{display:block;width:3px;height:5px;border-radius:3px;background:#35e6a0;opacity:.85}
#g360-avatar-life.speaking #g360-avatar-wave i{animation:g360wave .42s infinite ease-in-out alternate}
#g360-avatar-wave i:nth-child(2){animation-delay:.07s}.g360-avatar-wave i:nth-child(3){animation-delay:.14s}.g360-avatar-wave i:nth-child(4){animation-delay:.21s}.g360-avatar-wave i:nth-child(5){animation-delay:.28s}
@keyframes g360pulse{to{transform:scale(1.45);box-shadow:0 0 16px #18e77b}}
@keyframes g360wave{to{height:15px;opacity:1}}
#g360-avatar-stage.speaking img{animation:g360living .42s infinite alternate!important;filter:drop-shadow(0 0 20px #22e39a)!important}
#g360-avatar-launch.speaking img{animation:g360livingSmall .42s infinite alternate!important}
@keyframes g360living{to{transform:translateY(-2px) scale(1.018) rotate(.25deg)}}
@keyframes g360livingSmall{to{transform:scale(1.045) rotate(.5deg)}}
</style>
<div id="g360-avatar-life"><span id="g360-avatar-life-dot"></span><span id="g360-avatar-life-text">IA centrale prête — voix activable</span><span id="g360-avatar-wave"><i></i><i></i><i></i><i></i><i></i></span></div>
<script>
(function(){
  const launch=document.getElementById('g360-avatar-launch');
  const stage=document.getElementById('g360-avatar-stage');
  const modal=document.getElementById('g360-avatar-modal');
  const life=document.getElementById('g360-avatar-life');
  const lifeText=document.getElementById('g360-avatar-life-text');
  if(!launch||!stage||!life)return;
  const old=window.GABON360_AVATAR||{};
  const originalSpeak=typeof old.speak==='function'?old.speak:null;
  let unlocked=false;
  let voices=[];
  function loadVoices(){voices=('speechSynthesis' in window)?speechSynthesis.getVoices():[];}
  loadVoices();
  if('speechSynthesis' in window) speechSynthesis.onvoiceschanged=loadVoices;
  function bestVoice(){return voices.find(v=>/^fr-FR$/i.test(v.lang))||voices.find(v=>/^fr/i.test(v.lang))||voices[0]||null;}
  function speakLive(text){
    if(!('speechSynthesis' in window)){lifeText.textContent='Voix non disponible sur cet appareil';return false;}
    const value=String(text||'').trim(); if(!value)return false;
    speechSynthesis.cancel();
    const u=new SpeechSynthesisUtterance(value);
    u.lang='fr-FR'; u.rate=.94; u.pitch=1.02; u.volume=1;
    const v=bestVoice(); if(v)u.voice=v;
    const start=()=>{unlocked=true;life.classList.add('speaking');stage.classList.add('speaking');launch.classList.add('speaking');lifeText.textContent='IA centrale en train de parler…';};
    const end=()=>{life.classList.remove('speaking');stage.classList.remove('speaking');launch.classList.remove('speaking');lifeText.textContent='IA centrale prête — en écoute';};
    u.onstart=start;u.onend=end;u.onerror=end;
    speechSynthesis.speak(u);return true;
  }
  function announce(text){return speakLive(text)}
  window.GABON360_AVATAR_LIVE={version:'1.0',announce,voiceReady:()=>('speechSynthesis' in window),unlocked:()=>unlocked};
  window.GABON360_AVATAR_ANNOUNCE=announce;
  if(originalSpeak){old.speak=(text)=>speakLive(text);window.GABON360_AVATAR=old;}
  launch.addEventListener('click',function(){
    setTimeout(function(){
      if(!unlocked && modal && getComputedStyle(modal).display!=='none')
        speakLive('Bonjour Ngoua Obame. Je suis l’IA centrale de GABON 360 AI. Je suis en ligne.');
    },180);
  },{passive:true});
  document.addEventListener('click',function(e){
    const b=e.target&&e.target.closest?e.target.closest('button'):null;
    if(b && /Faire parler/i.test(b.textContent||'')) unlocked=true;
  },true);
  window.addEventListener('gabon360:ai-speak',function(e){
    const text=e&&e.detail&&e.detail.text?e.detail.text:'';
    if(text)announce(text);
  });
  window.addEventListener('gabon360:alert',function(e){
    const d=e&&e.detail||{};
    if(d&&d.announce&&d.text)announce(String(d.text));
  });
  lifeText.textContent=('speechSynthesis' in window)?'IA centrale prête — appuyez sur l’avatar pour l’entendre':'Voix non disponible sur cet appareil';
})();
</script>
'''

def main():
    roots=[Path('android_project'),Path('.')]
    candidates=[]
    for root in roots:
        if root.exists():
            candidates += [p for p in root.rglob('index.html') if 'build' not in p.parts and '.git' not in p.parts]
    if not candidates:
        raise SystemExit('Aucun index.html trouvé')
    target=candidates[0]
    text=target.read_text(encoding='utf-8')
    if MARK in text:
        print('Avatar life déjà injecté:',target)
        return
    if '</body>' in text:
        text=text.replace('</body>',PAYLOAD+'\n</body>',1)
    else:
        text += '\n'+PAYLOAD
    target.write_text(text,encoding='utf-8')
    print('Avatar life injecté dans',target)

if __name__=='__main__':
    main()
