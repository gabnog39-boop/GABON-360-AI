#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-NATIVE-INTERACTIONS-V3 -->'
P=r'''<!-- GABON360-NATIVE-INTERACTIONS-V3 -->
<style>
#g360-native-io-status{position:fixed;left:90px;bottom:120px;z-index:2147483647;background:#071522;color:#dff;border:1px solid #31506d;border-radius:9px;padding:5px 8px;font:11px system-ui,sans-serif}
#g360-native-avatar-life{position:relative;display:flex;justify-content:center;align-items:center;max-width:100%}
#g360-native-avatar-life.g360-speaking{animation:g360NativeBody 1.35s ease-in-out infinite}
#g360-native-avatar-life img{display:block;max-width:100%}
#g360-native-avatar-life .g360-mouth{position:absolute;left:50%;top:56%;width:12%;height:3%;min-width:12px;background:#111;border-radius:50%;transform:translateX(-50%) scaleY(.35);opacity:0}
#g360-native-avatar-life.g360-speaking .g360-mouth{opacity:.9;animation:g360NativeMouth .14s ease-in-out infinite alternate}
#g360-native-avatar-life .g360-eye{position:absolute;top:35%;width:4%;height:2%;border-radius:50%;background:#111;opacity:0}
#g360-native-avatar-life.g360-speaking .g360-eye{opacity:.22;animation:g360NativeBlink 4s infinite}
#g360-native-avatar-life .g360-hand{position:absolute;top:67%;width:14%;height:5%;border:2px solid #9ff2d0;border-radius:50%;opacity:0}
#g360-native-avatar-life.g360-speaking .g360-hand{opacity:.35;animation:g360NativeHands 1.1s ease-in-out infinite alternate}
#g360-native-avatar-life .g360-hand.l{left:3%}.g360-hand.r{right:3%}
@keyframes g360NativeBody{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-2px) rotate(.5deg)}}
@keyframes g360NativeMouth{from{transform:translateX(-50%) scaleY(.3)}to{transform:translateX(-50%) scaleY(2.1)}}
@keyframes g360NativeBlink{0%,44%,48%,100%{transform:scaleY(1)}46%{transform:scaleY(.08)}}
@keyframes g360NativeHands{from{transform:translateY(0) rotate(-5deg)}to{transform:translateY(-5px) rotate(7deg)}}
</style>
<script>
(function(){if(window.__G360_NATIVE_V3)return;window.__G360_NATIVE_V3=true;
function status(t){var s=document.getElementById('g360-native-io-status');if(!s){s=document.createElement('div');s.id='g360-native-io-status';document.body.appendChild(s)}s.textContent=t}
function img(){return document.querySelector('#g360-avatar-modal img,#g360-avatar-home-dock img,#g360-avatar-launch img,img[alt*="avatar" i],img[alt*="IA" i]')}
function life(){var im=img();if(!im||document.getElementById('g360-native-avatar-life'))return;var w=document.createElement('div');w.id='g360-native-avatar-life';im.parentNode.insertBefore(w,im);w.appendChild(im);var m=document.createElement('span');m.className='g360-mouth';var e1=document.createElement('span');e1.className='g360-eye';e1.style.left='38%';var e2=document.createElement('span');e2.className='g360-eye';e2.style.right='38%';var h1=document.createElement('span');h1.className='g360-hand l';var h2=document.createElement('span');h2.className='g360-hand r';w.append(m,e1,e2,h1,h2);window.G360NativeLife=w}
function start(){life();if(window.G360NativeLife)window.G360NativeLife.classList.add('g360-speaking');status('IA parle…')}
function end(){if(window.G360NativeLife)window.G360NativeLife.classList.remove('g360-speaking');status('IA prête')}
function speak(t){t=String(t||'').trim();if(!t)return;if(window.G360Android&&window.G360Android.speak){start();window.G360Android.speak(t);setTimeout(end,Math.max(1600,t.length*65));return}if('speechSynthesis'in window){start();var u=new SpeechSynthesisUtterance(t);u.lang='fr-FR';u.onend=end;u.onerror=end;speechSynthesis.cancel();speechSynthesis.speak(u)}else status('Voix non disponible')}
function listen(){if(window.G360Android&&window.G360Android.startListening){status('Écoute…');window.G360Android.startListening();return}var R=window.SpeechRecognition||window.webkitSpeechRecognition;if(!R){status('Micro non disponible');return}try{var r=new R();r.lang='fr-FR';r.onstart=function(){status('Écoute…')};r.onresult=function(e){window.G360NativeSpeechResult(e.results[0][0].transcript)};r.onerror=function(e){status('Micro : '+e.error)};r.start()}catch(e){status('Micro : autorisation requise')}}
window.G360NativeSpeechResult=function(t){var i=document.querySelector('input[placeholder*="commande" i],textarea[placeholder*="commande" i]');if(i){i.value=t;i.dispatchEvent(new Event('input',{bubbles:true}));i.dispatchEvent(new Event('change',{bubbles:true}))}window.dispatchEvent(new CustomEvent('gabon360:ai-command',{detail:{text:t,source:'native-microphone'}}));status('Commande reçue')};window.G360NativeSpeechError=function(e){status('Micro : '+e)};window.G360NativeSpeechState=function(s){status(s==='listening'?'Écoute…':s==='processing'?'Analyse…':'Micro prêt')};window.GABON360_NATIVE_IO={version:'3.0',speak:speak,listen:listen};window.addEventListener('gabon360:ai-speak',function(e){if(e.detail&&e.detail.text)speak(e.detail.text)});
function boot(){life();status(window.G360Android?'Micro + voix natifs prêts':'Initialisation…')}boot();window.addEventListener('load',boot);setTimeout(boot,800);setTimeout(boot,2200);document.addEventListener('click',function(e){var b=e.target.closest('#g360-avatar-mic,#g360-t2-voice');if(!b)return;if(b.id==='g360-avatar-mic')listen();else speak('Navigation terrain active. Dites-moi votre destination ou sélectionnez un waypoint.')})})();
</script>
'''
def main():
 for p in sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts)):
  t=p.read_text(encoding='utf-8');
  if MARK in t: print('already',p);return
  i=t.lower().rfind('</body>')
  if i>=0:p.write_text(t[:i]+P+'\n'+t[i:],encoding='utf-8');print('injected',p);return
 raise SystemExit('No index.html found')
if __name__=='__main__':main()
