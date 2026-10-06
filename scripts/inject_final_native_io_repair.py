#!/usr/bin/env python3
from pathlib import Path

MARK='<!-- GABON360-FINAL-NATIVE-IO-REPAIR -->'
JS=r'''<!-- GABON360-FINAL-NATIVE-IO-REPAIR -->
<script>
(function(){
  if(window.__G360_FINAL_NATIVE_IO_REPAIR)return; window.__G360_FINAL_NATIVE_IO_REPAIR=true;
  function status(t){var s=document.getElementById('g360-avatar-mic-status')||document.getElementById('g360-native-io-status')||document.getElementById('g360-avatar-status');if(s)s.textContent=t;}
  function nativeSpeak(t){if(window.GABON360_NATIVE_IO&&window.GABON360_NATIVE_IO.speak){window.GABON360_NATIVE_IO.speak(t);return true}if(window.G360Android&&window.G360Android.speak){window.G360Android.speak(t);return true}return false}
  function nativeListen(){if(window.G360Android&&window.G360Android.startListening){status('Écoute…');window.G360Android.startListening();return true}return false}
  function nativeStopListen(){if(window.G360Android&&window.G360Android.stopListening){window.G360Android.stopListening();return true}return false}
  document.addEventListener('click',function(e){
    var b=e.target.closest('#g360-avatar-mic,#g360-avatar-speak,#g360-avatar-listen,#g360-avatar-stop'); if(!b)return;
    if(b.id==='g360-avatar-mic'||b.id==='g360-avatar-listen'){
      e.preventDefault();e.stopImmediatePropagation(); if(!nativeListen())status('Micro natif indisponible'); return;
    }
    if(b.id==='g360-avatar-speak'){
      e.preventDefault();e.stopImmediatePropagation();
      var t='Bonjour Ngoua Obame. Je suis l’IA centrale de GABON 360 AI. Je suis intégrée au Centre national de situation et je peux vous guider vers les pages et les informations disponibles.';
      if(!nativeSpeak(t))status('Voix native indisponible'); return;
    }
    if(b.id==='g360-avatar-stop'){
      e.preventDefault();e.stopImmediatePropagation();nativeStopListen();
      if('speechSynthesis' in window)speechSynthesis.cancel();
      if(window.G360Android&&window.G360Android.stopSpeaking)window.G360Android.stopSpeaking();
      status('IA arrêtée');
    }
  },true);
  window.addEventListener('gabon360:ai-speak',function(e){var t=e.detail&&e.detail.text;if(t&&!nativeSpeak(t)){} });
  window.G360_FINAL_NATIVE_IO={version:'1.0',nativeTTS:true,nativeSTT:true,stop:true};
})();
</script>
'''

def main():
  root=Path('android_project')
  htmls=sorted(root.rglob('index.html'),key=lambda p:len(p.parts))
  if not htmls: raise SystemExit('No index.html found')
  p=htmls[0]; t=p.read_text(encoding='utf-8',errors='ignore')
  if MARK not in t:
    i=t.lower().rfind('</body>')
    if i<0: raise SystemExit('No </body> found')
    p.write_text(t[:i]+JS+'\n'+t[i:],encoding='utf-8')
  bridges=list(root.rglob('G360NativeBridge.java'))
  if bridges:
    b=bridges[0]; bt=b.read_text(encoding='utf-8',errors='ignore')
    needle='@JavascriptInterface public void stopSpeaking()'
    if needle not in bt:
      target='@JavascriptInterface public void stopListening(){if(sr!=null)sr.stopListening();}'
      repl=target+'\n    @JavascriptInterface public void stopSpeaking(){if(tts!=null)tts.stop();}'
      if target not in bt: raise SystemExit('Expected stopListening method not found in native bridge')
      b.write_text(bt.replace(target,repl,1),encoding='utf-8')
  print('Final native I/O repair installed')
if __name__=='__main__': main()
