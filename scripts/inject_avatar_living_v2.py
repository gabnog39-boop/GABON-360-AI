#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-AVATAR-LIVING-V2 -->'
PAYLOAD=r'''<!-- GABON360-AVATAR-LIVING-V2 -->
<style>
#g360-avatar-life-engine{position:relative;display:flex;flex-direction:column;align-items:center;gap:7px;margin-top:8px;z-index:50}
#g360-avatar-life-engine .g360-life-badge{padding:6px 10px;border-radius:999px;background:#061725eF;border:1px solid #2adf9b66;color:#bff5df;font:600 12px system-ui,sans-serif}
#g360-avatar-life-engine.speaking .g360-life-badge{box-shadow:0 0 18px #18e77b66}
#g360-avatar-life-engine .g360-life-stage{position:relative;display:inline-block;transform-origin:50% 85%;}
#g360-avatar-life-engine .g360-life-stage.speaking{animation:g360BodyTalk 1.8s ease-in-out infinite}
#g360-avatar-life-engine .g360-life-stage.speaking::after{content:'';position:absolute;inset:8% 20% 35% 20%;border-radius:50%;pointer-events:none;box-shadow:0 0 28px #25e49a55;animation:g360Aura .8s ease-in-out infinite alternate}
#g360-avatar-life-engine .g360-life-mouth{position:absolute;left:50%;top:57%;width:12%;height:2.8%;min-width:14px;background:#090b10;border-radius:50%;transform:translateX(-50%) scaleY(.35);opacity:0;pointer-events:none}
#g360-avatar-life-engine.speaking .g360-life-mouth{opacity:.88;animation:g360Mouth .16s ease-in-out infinite alternate}
#g360-avatar-life-engine .g360-life-eye{position:absolute;top:35%;width:3.5%;height:1.7%;border-radius:50%;background:#101820;opacity:0;pointer-events:none}
#g360-avatar-life-engine .g360-life-eye.left{left:39%}.g360-life-eye.right{right:39%}
#g360-avatar-life-engine.speaking .g360-life-eye{opacity:.25;animation:g360Blink 4.2s ease-in-out infinite}
#g360-avatar-life-engine .g360-life-hands{position:absolute;inset:0;pointer-events:none;opacity:0}
#g360-avatar-life-engine.speaking .g360-life-hands{opacity:.25;animation:g360Hands 1.35s ease-in-out infinite alternate}
#g360-avatar-life-engine .g360-life-hand{position:absolute;width:12%;height:5%;border:2px solid #9ff2d0;border-radius:50%;filter:blur(.3px)}
#g360-avatar-life-engine .g360-life-hand.l{left:5%;top:66%;transform:rotate(-18deg)}.g360-life-hand.r{right:5%;top:66%;transform:rotate(18deg)}
@keyframes g360BodyTalk{0%,100%{transform:translateY(0) rotate(0deg) scale(1)}25%{transform:translateY(-1px) rotate(-.35deg) scale(1.008)}50%{transform:translateY(-2px) rotate(.35deg) scale(1.012)}75%{transform:translateY(-1px) rotate(-.2deg) scale(1.006)}}
@keyframes g360Mouth{from{transform:translateX(-50%) scaleY(.35)}to{transform:translateX(-50%) scaleY(2.2)}}
@keyframes g360Blink{0%,45%,49%,100%{transform:scaleY(1)}47%{transform:scaleY(.08)}}
@keyframes g360Hands{from{transform:translateY(0) rotate(-2deg)}to{transform:translateY(-4px) rotate(3deg)}}
@keyframes g360Aura{from{opacity:.2}to{opacity:.8}}
</style>
<script>
(function(){
  if(window.__G360_LIVING_V2)return;window.__G360_LIVING_V2=true;
  function ready(){
    var stage=document.getElementById('g360-avatar-stage');
    if(!stage)return;
    var img=stage.querySelector('img');
    if(!img)return;
    var engine=document.getElementById('g360-avatar-life-engine');
    if(!engine){
      engine=document.createElement('div');engine.id='g360-avatar-life-engine';
      var badge=document.createElement('div');badge.className='g360-life-badge';badge.textContent='● IA vivante — prête à parler';
      var wrap=document.createElement('div');wrap.className='g360-life-stage';
      var mouth=document.createElement('span');mouth.className='g360-life-mouth';
      var eyeL=document.createElement('span');eyeL.className='g360-life-eye left';var eyeR=document.createElement('span');eyeR.className='g360-life-eye right';
      var hands=document.createElement('span');hands.className='g360-life-hands';hands.innerHTML='<i class="g360-life-hand l"></i><i class="g360-life-hand r"></i>';
      img.parentNode.insertBefore(engine,img);wrap.appendChild(img);wrap.appendChild(mouth);wrap.appendChild(eyeL);wrap.appendChild(eyeR);wrap.appendChild(hands);engine.appendChild(badge);engine.appendChild(wrap);
      engine._badge=badge;engine._stage=wrap;
    }
    var uttering=false;
    function start(){uttering=true;engine.classList.add('speaking');engine._stage.classList.add('speaking');engine._badge.textContent='● IA parle — animation active';}
    function end(){uttering=false;engine.classList.remove('speaking');engine._stage.classList.remove('speaking');engine._badge.textContent='● IA vivante — prête à parler';}
    function speak(text){text=String(text||'').trim();if(!text)return false;if(!('speechSynthesis'in window)){engine._badge.textContent='● Voix non disponible sur cet appareil';return false}speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang='fr-FR';u.rate=.92;u.pitch=1.02;u.onstart=start;u.onend=end;u.onerror=end;speechSynthesis.speak(u);return true}
    window.GABON360_AVATAR_LIVING_V2={version:'2.0',speak:speak,eyes:true,mouth:true,body:true,hands:true};
    window.GABON360_AVATAR_ANNOUNCE=speak;
    window.addEventListener('gabon360:ai-speak',function(e){var t=e&&e.detail&&e.detail.text;if(t)speak(t)});
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',ready);else ready();
  setTimeout(ready,800);setTimeout(ready,2000);
})();
</script>
'''

def main():
    candidates=sorted([p for p in Path('android_project').rglob('index.html') if 'build' not in p.parts],key=lambda p:len(p.parts))
    for p in candidates:
        t=p.read_text(encoding='utf-8')
        if MARK in t: print('already:',p); return
        i=t.lower().rfind('</body>')
        if i<0: continue
        p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8');print('injected:',p);return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__':main()
