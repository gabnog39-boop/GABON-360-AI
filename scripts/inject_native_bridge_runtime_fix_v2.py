#!/usr/bin/env python3
from pathlib import Path

MARK='GABON360-NATIVE-BRIDGE-RUNTIME-FIX-V2'


def patch_bridge(p):
    t=p.read_text(encoding='utf-8',errors='ignore')
    if MARK in t:
        return False
    # Make the JS bridge visible to the page after it is attached. WebView interfaces
    # are reliably available to page JavaScript after a reload.
    old='w.addJavascriptInterface(new Bridge(a,w),"G360Android");'
    new=old+'\n    w.postDelayed(new Runnable(){public void run(){w.reload();}},180);'
    if old in t and 'w.postDelayed(new Runnable(){public void run(){w.reload();}},180);' not in t:
        t=t.replace(old,new,1)
    # Queue TTS until TextToSpeech has finished initialization.
    t=t.replace('final Activity a; final WebView w; SpeechRecognizer sr; TextToSpeech tts;',
                'final Activity a; final WebView w; SpeechRecognizer sr; TextToSpeech tts; boolean ttsReady=false; String pendingSpeech="";')
    t=t.replace('@JavascriptInterface public void speak(String text){if(text!=null&&!text.isEmpty())tts.speak(text,TextToSpeech.QUEUE_FLUSH,null,"g360");}',
                '@JavascriptInterface public void speak(String text){if(text==null||text.isEmpty())return; if(!ttsReady){pendingSpeech=text;return;} tts.speak(text,TextToSpeech.QUEUE_FLUSH,null,"g360");}')
    t=t.replace('@JavascriptInterface public void stopListening(){if(sr!=null)sr.stopListening();}',
                '@JavascriptInterface public void stopListening(){if(sr!=null)sr.stopListening();}\n    @JavascriptInterface public void stopSpeaking(){if(tts!=null)tts.stop(); pendingSpeech="";}')
    t=t.replace('public void onInit(int status){if(status==TextToSpeech.SUCCESS)tts.setLanguage(Locale.FRENCH);}',
                'public void onInit(int status){if(status==TextToSpeech.SUCCESS){ttsReady=true;tts.setLanguage(Locale.FRENCH);js("window.G360NativeSpeechState&&window.G360NativeSpeechState(\\\'voice-ready\\\')");if(pendingSpeech!=null&&!pendingSpeech.isEmpty()){String s=pendingSpeech;pendingSpeech="";tts.speak(s,TextToSpeech.QUEUE_FLUSH,null,"g360");}}else{js("window.G360NativeSpeechError&&window.G360NativeSpeechError(\\\'TTS Android indisponible\\\')");}}')
    p.write_text(t,encoding='utf-8')
    return True


def patch_js(p):
    t=p.read_text(encoding='utf-8',errors='ignore')
    if 'GABON360-NATIVE-BRIDGE-RUNTIME-FIX-V2-JS' in t:
        return False
    payload=r'''<!-- GABON360-NATIVE-BRIDGE-RUNTIME-FIX-V2-JS -->
<script>
(function(){
  if(window.__G360_NATIVE_BRIDGE_RUNTIME_FIX_V2)return;window.__G360_NATIVE_BRIDGE_RUNTIME_FIX_V2=true;
  function bridge(){return window.G360Android&&typeof window.G360Android.speak==='function'?window.G360Android:null}
  function status(t){
    var ids=['g360-native-io-status','g360-avatar-mic-status','g360-avatar-life-text','g360-avatar-status'];
    for(var i=0;i<ids.length;i++){var e=document.getElementById(ids[i]);if(e)e.textContent=t;}
  }
  function ready(){status(bridge()?'Micro + voix natifs prêts':'Initialisation…');}
  function say(){var b=bridge();if(!b){status('Voix native en cours d’initialisation');return}status('IA parle…');b.speak('Bonjour Ngoua Obame. Je suis l’IA centrale de GABON 360 AI. Je suis prête à vous assister.');}
  function listen(){var b=bridge();if(!b){status('Micro natif en cours d’initialisation');return}status('Écoute…');b.startListening();}
  function stop(){var b=bridge();if(b){try{b.stopListening()}catch(e){}try{b.stopSpeaking()}catch(e){}}if(window.speechSynthesis)window.speechSynthesis.cancel();status('IA arrêtée');}
  document.addEventListener('click',function(e){
    var b=e.target.closest('button,a,[role="button"]');if(!b)return;
    var label=(b.innerText||b.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
    if(label.indexOf('faire parler')>=0){e.preventDefault();e.stopImmediatePropagation();say();return}
    if(label==='écouter'||label.indexOf('écouter')===0){e.preventDefault();e.stopImmediatePropagation();listen();return}
    if(label==='arrêter'||label.indexOf('arrêter')===0){e.preventDefault();e.stopImmediatePropagation();stop();return}
  },true);
  window.addEventListener('gabon360:ai-speak',function(e){var t=e&&e.detail&&e.detail.text,b=bridge();if(t&&b){status('IA parle…');b.speak(String(t));}},true);
  window.addEventListener('gabon360:native-ready',ready);
  ready();window.addEventListener('load',ready);var n=0;var timer=setInterval(function(){ready();if(bridge()||++n>40)clearInterval(timer)},250);
})();
</script>
'''
    i=t.lower().rfind('</body>')
    if i<0: raise SystemExit('</body> introuvable')
    p.write_text(t[:i]+payload+'\n'+t[i:],encoding='utf-8')
    return True


def main():
    root=Path('android_project')
    bridges=list(root.rglob('G360NativeBridge.java'))
    if not bridges: raise SystemExit('G360NativeBridge.java introuvable')
    changed=patch_bridge(bridges[0])
    htmls=sorted([p for p in root.rglob('index.html') if 'build' not in p.parts],key=lambda p:len(p.parts))
    if not htmls: raise SystemExit('index.html introuvable')
    changed=patch_js(htmls[0]) or changed
    print(MARK,'installed' if changed else 'already installed')

if __name__=='__main__': main()
