#!/usr/bin/env python3
from pathlib import Path
import re

MARK='G360NativeBridge.attach(this);'
JAVA=r'''
package {pkg};

import android.Manifest;
import android.app.Activity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.Bundle;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import android.view.View;
import android.view.ViewGroup;
import java.util.ArrayList;
import java.util.Locale;

public final class G360NativeBridge {{
  private static WebView find(View v) {{
    if (v instanceof WebView) return (WebView)v;
    if (v instanceof ViewGroup) {{ ViewGroup g=(ViewGroup)v; for(int i=0;i<g.getChildCount();i++) {{ WebView w=find(g.getChildAt(i)); if(w!=null)return w; }} }}
    return null;
  }}
  public static void attach(final Activity a) {{
    final WebView w=find(a.getWindow().getDecorView());
    if(w==null){{ a.getWindow().getDecorView().postDelayed(new Runnable(){{public void run(){{attach(a);}}}},500); return; }}
    w.getSettings().setJavaScriptEnabled(true);
    w.addJavascriptInterface(new Bridge(a,w),"G360Android");
  }}
  private static final class Bridge implements RecognitionListener, TextToSpeech.OnInitListener {{
    final Activity a; final WebView w; SpeechRecognizer sr; TextToSpeech tts;
    Bridge(Activity a,WebView w){{this.a=a;this.w=w;tts=new TextToSpeech(a,this);}}
    @JavascriptInterface public void speak(String text){{if(text!=null&&!text.isEmpty())tts.speak(text,TextToSpeech.QUEUE_FLUSH,null,"g360");}}
    @JavascriptInterface public void startListening(){{a.runOnUiThread(new Runnable(){{public void run(){{
      if(a.checkSelfPermission(Manifest.permission.RECORD_AUDIO)!=PackageManager.PERMISSION_GRANTED){{a.requestPermissions(new String[]{{Manifest.permission.RECORD_AUDIO}},3601);return;}}
      if(!SpeechRecognizer.isRecognitionAvailable(a)){{error("reconnaissance vocale indisponible");return;}}
      if(sr==null){{sr=SpeechRecognizer.createSpeechRecognizer(a);sr.setRecognitionListener(Bridge.this);}}
      Intent i=new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);i.putExtra(RecognizerIntent.EXTRA_LANGUAGE,"fr-FR");i.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);i.putExtra(RecognizerIntent.EXTRA_PARTIAL_RESULTS,false);sr.startListening(i);
    }}}});}}
    @JavascriptInterface public void stopListening(){{if(sr!=null)sr.stopListening();}}\n    @JavascriptInterface public void stopSpeaking(){{if(tts!=null)tts.stop();}}
    void js(String s){{w.post(new Runnable(){{public void run(){{w.evaluateJavascript(s,null);}}}});}}
    String q(String s){{return "'"+s.replace("\\","\\\\").replace("'","\\'").replace("\n"," ")+"'";}}
    void error(String s){{js("window.G360NativeSpeechError&&window.G360NativeSpeechError("+q(s)+")");}}
    public void onReadyForSpeech(Bundle b){{js("window.G360NativeSpeechState&&window.G360NativeSpeechState('ready')");}}
    public void onBeginningOfSpeech(){{js("window.G360NativeSpeechState&&window.G360NativeSpeechState('listening')");}}
    public void onEndOfSpeech(){{js("window.G360NativeSpeechState&&window.G360NativeSpeechState('processing')");}}
    public void onResults(Bundle b){{ArrayList<String>x=b.getStringArrayList(SpeechRecognizer.RESULTS_RECOGNITION);if(x!=null&&!x.isEmpty())js("window.G360NativeSpeechResult&&window.G360NativeSpeechResult("+q(x.get(0))+")");}}
    public void onError(int e){{error("erreur "+e);}} public void onRmsChanged(float r){{}} public void onBufferReceived(byte[] b){{}} public void onPartialResults(Bundle b){{}} public void onEvent(int a,Bundle b){{}}
    public void onInit(int status){{if(status==TextToSpeech.SUCCESS){{tts.setLanguage(Locale.FRENCH);js("window.G360NativeSpeechState&&window.G360NativeSpeechState(\'voice-ready\')");}}}}
  }}
}}
'''

def main():
    root=Path('android_project'); candidates=[]
    for p in root.rglob('*'):
        if p.suffix.lower() in ('.java','.kt'):
            t=p.read_text(encoding='utf-8',errors='ignore')
            if 'onCreate' in t and ('Activity' in t or 'AppCompatActivity' in t): candidates.append((p,t))
    if not candidates: raise SystemExit('No Android Activity found')
    p,t=candidates[0]
    m=re.search(r'^\s*package\s+([A-Za-z0-9_.]+)',t,re.M)
    if not m: raise SystemExit('No package found')
    pkg=m.group(1)
    # Put the bridge beside MainActivity, not at the Android project root.
    target=p.parent/'G360NativeBridge.java'
    target.write_text(JAVA.format(pkg=pkg),encoding='utf-8')
    if MARK not in t:
        oc=re.search(r'onCreate\s*\([^)]*\)\s*\{',t)
        if not oc: raise SystemExit('No onCreate found')
        t=t[:oc.end()]+'\n        '+MARK+'\n'+t[oc.end():];p.write_text(t,encoding='utf-8')
    for mf in root.rglob('AndroidManifest.xml'):
        mt=mf.read_text(encoding='utf-8')
        if 'android.permission.RECORD_AUDIO' not in mt:
            mt=mt.replace('</manifest>','    <uses-permission android:name="android.permission.RECORD_AUDIO" />\n</manifest>',1);mf.write_text(mt,encoding='utf-8')
    print('Native Android bridge installed beside MainActivity:',target)
if __name__=='__main__':main()
