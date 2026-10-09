#!/usr/bin/env python3
"""Final deterministic mobile overlay repair, applied after every other UI injector."""
from pathlib import Path

MARK = "GABON360-FINAL-OVERLAY-REPAIR-V1"
PAYLOAD = r'''<!-- GABON360-FINAL-OVERLAY-REPAIR-V1 -->
<style>
/* Satellite catalogue must never cover the dashboard on startup. */
#g360-satellite-panel { display:none!important; }
#g360-satellite-panel.g360-visible { display:block!important; }
#g360-satellite-open {
  position:fixed!important;
  right:12px!important;
  bottom:82px!important;
  z-index:100020!important;
  max-width:calc(100vw - 24px)!important;
}
#g360-satellite-panel.g360-visible {
  position:fixed!important;
  left:12px!important;
  right:12px!important;
  bottom:148px!important;
  width:auto!important;
  max-height:55dvh!important;
  z-index:100030!important;
  box-sizing:border-box!important;
}
#g360-satellite-panel .g360-body { max-height:calc(55dvh - 55px)!important; overflow:auto!important; }
#g360-satellite-panel.g360-hidden { display:none!important; }
@media (max-width:680px) {
  #g360-avatar-home-button { right:12px!important; bottom:18px!important; width:48px!important; height:48px!important; }
  #g360-avatar-launch { left:12px!important; bottom:18px!important; width:54px!important; height:54px!important; }
}
/* A closed overlay must not intercept taps even if another injector leaves its styles behind. */
#g360-universal[aria-hidden="true"],
#g360-v2[aria-hidden="true"],
#g360-pages-modal[aria-hidden="true"],
#g360-cm-modal[aria-hidden="true"],
#g360-avatar-modal[aria-hidden="true"] {
  display:none!important; visibility:hidden!important; pointer-events:none!important;
}

/* GABON360 MOBILE LAYOUT HOTFIX: keep the map/dashboard clear of floating controls. */
@media (max-width: 720px) {
  #g360-ai-relay-status { top: 58px!important; left: 12px!important; right: 12px!important; max-width:none!important; box-sizing:border-box!important; }
  #g360-page-exit-bar { top: 8px!important; left: 8px!important; right: 8px!important; gap: 6px!important; }
  #g360-page-exit-bar button { min-height: 38px!important; padding: 7px 10px!important; font-size: 12px!important; }
  #g360-satellite-open { right: 12px!important; bottom: 82px!important; z-index: 100020!important; }
  #g360-avatar-launch { left: 12px!important; bottom: 82px!important; width: 48px!important; height: 48px!important; z-index: 100021!important; }
  #g360-avatar-home-button { right: 12px!important; bottom: 140px!important; width: 44px!important; height: 44px!important; z-index: 100021!important; }
  #g360-avatar-mic, #g360-avatar-microphone, #g360-mic-button { bottom: 145px!important; left: 12px!important; width: 58px!important; height: 58px!important; z-index: 100022!important; }
  #g360-page-view, #g360-universal, .g360-upage { box-sizing:border-box!important; max-width:100vw!important; }
  #g360-page-view { padding-bottom: 180px!important; }
  #g360-page-view button, .g360-upage button { max-width:100%; }
  #g360-ai-pending-v2 { bottom: 12px!important; max-height: 24dvh!important; }
}
</style>
<script id="g360-final-overlay-repair">
(function(){
  if(window.__G360_FINAL_OVERLAY_REPAIR_V1)return;
  window.__G360_FINAL_OVERLAY_REPAIR_V1=true;
  function setup(){
    /* Close any startup catalogue by known IDs and by visible title/content.
       Earlier injectors create several differently named page drawers. */
    function closeOverlay(el){
      if(!el || el.id==='g360-page-exit-bar' || el.id==='g360-page-back' || el.id==='g360-page-home') return;
      el.setAttribute('aria-hidden','true');
      el.classList.remove('open','active','visible','show','is-open','g360-visible');
      el.classList.add('g360-hidden');
      el.style.setProperty('display','none','important');
      el.style.setProperty('visibility','hidden','important');
      el.style.setProperty('pointer-events','none','important');
    }
    ['g360-universal','g360-v2','g360-pages-modal','g360-cm-modal','g360-avatar-modal','g360-complete-modal',
     'g360-module-drawer','g360-all-pages','g360-all-pages-modal','g360-page-list','g360-functions-panel',
     'g360-functions-modal','g360-pages-panel','g360-module-panel','g360-module-menu','g360-menu-modal'].forEach(function(id){
      closeOverlay(document.getElementById(id));
    });
    /* Root fix: find the actual fixed drawer from its visible heading, then close its drawer ancestor.
       Do not try to hide the heading itself (the previous algorithm did exactly that). */
    function hideDrawerForHeading(needle){
      var nodes=Array.prototype.slice.call(document.querySelectorAll('body *'));
      var heading=null;
      for(var i=0;i<nodes.length;i++){
        var el=nodes[i], txt=(el.innerText||'').trim().toLowerCase();
        if(!txt || txt.length>100 || txt.indexOf(needle)<0) continue;
        var r=el.getBoundingClientRect();
        if(r.width<90 || r.height<10 || r.width>window.innerWidth*1.05 || r.height>window.innerHeight*1.05) continue;
        if(!heading || txt.length<(heading.innerText||'').trim().length) heading=el;
      }
      if(!heading)return false;
      var cur=heading;
      while(cur && cur!==document.body && cur!==document.documentElement){
        var r=cur.getBoundingClientRect(), st=getComputedStyle(cur);
        var positioned=st.position==='fixed'||st.position==='absolute';
        var drawerSized=r.width>=Math.min(240,window.innerWidth*.45) && r.height>=100;
        if(positioned && drawerSized){
          cur.setAttribute('aria-hidden','true');
          cur.classList.remove('open','active','visible','show','is-open','g360-visible');
          cur.classList.add('g360-hidden');
          cur.style.setProperty('display','none','important');
          cur.style.setProperty('visibility','hidden','important');
          cur.style.setProperty('pointer-events','none','important');
          return true;
        }
        cur=cur.parentElement;
      }
      return false;
    }
    hideDrawerForHeading('toutes les pages');
    hideDrawerForHeading('centre des fonctions');
    var panel=document.getElementById('g360-satellite-panel');
    var launcher=document.getElementById('g360-satellite-open');
    if(panel){
      panel.classList.remove('g360-visible');
      panel.classList.add('g360-hidden');
      panel.setAttribute('aria-hidden','true');
    }
    if(launcher){
      launcher.classList.add('g360-visible');
      launcher.setAttribute('aria-expanded','false');
      launcher.onclick=function(){
        if(!panel)return;
        panel.classList.remove('g360-hidden');
        panel.classList.add('g360-visible');
        panel.setAttribute('aria-hidden','false');
        launcher.classList.remove('g360-visible');
        launcher.setAttribute('aria-expanded','true');
      };
    }
    var close=document.getElementById('g360-sat-close');
    if(close && panel && launcher){
      close.onclick=function(){
        panel.classList.remove('g360-visible');
        panel.classList.add('g360-hidden');
        panel.setAttribute('aria-hidden','true');
        launcher.classList.add('g360-visible');
        launcher.setAttribute('aria-expanded','false');
      };
    }
  }
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',setup,{once:true});
  else setup();
  window.addEventListener('load',setup,{once:true});
  window.GABON360_OVERLAY_REPAIR_STATUS={version:'1.0',satellitePanelClosedOnStartup:true,closedOverlaysDoNotBlock:true};
})();
</script>

<!-- GABON360-PAGE-RETURN-HOME-V1 -->
<style>
#g360-page-exit-bar{position:fixed!important;top:env(safe-area-inset-top,0px)!important;left:8px!important;z-index:2147483646!important;display:flex!important;gap:8px!important;pointer-events:auto!important}
#g360-page-exit-bar button{border:1px solid #7da4c7!important;border-radius:12px!important;background:#071522f2!important;color:#fff!important;padding:10px 13px!important;font:600 13px system-ui,sans-serif!important;min-height:42px!important;box-shadow:0 3px 12px #0007!important;pointer-events:auto!important;touch-action:manipulation!important}
#g360-page-exit-bar button:active{transform:scale(.97)}
</style>
<div id="g360-page-exit-bar" aria-label="Navigation de page">
<button type="button" id="g360-page-back" aria-label="Retour à la page précédente">← Retour</button>
<button type="button" id="g360-page-home" aria-label="Retour à l'accueil">⌂ Accueil</button>
</div>
<script id="g360-page-return-home-v1">
(function(){
 if(window.__G360_PAGE_RETURN_HOME_V1)return;window.__G360_PAGE_RETURN_HOME_V1=true;
 var stack=[],last='avatar';
 function callFirst(names,args){for(var i=0;i<names.length;i++){var f=window[names[i]];if(typeof f==='function'){try{f.apply(window,args||[]);return true}catch(e){}}}return false}
 function goHome(){
   stack=[];last='avatar';
   var closed=['g360-pages-modal','g360-universal','g360-cm-modal','g360-avatar-modal','g360-complete-modal'];
   closed.forEach(function(id){var el=document.getElementById(id);if(el){el.setAttribute('aria-hidden','true');el.style.setProperty('display','none','important')}});
   if(callFirst(['GABON360_OPEN_AVATAR_HOME','GABON360_OPEN_MODULE_PAGE','GABON360_NAVIGATE'],['avatar']))return;
   var home=document.querySelector('[data-g360-page="avatar"],#g360-avatar-launch,#g360-avatar-home-button,[data-page="avatar"]');
   if(home&&home.click)home.click();
 }
 function back(){
   if(stack.length){var prev=stack.pop();last=prev;if(callFirst(['GABON360_OPEN_MODULE_PAGE','GABON360_NAVIGATE'],[prev]))return;}
   goHome();
 }
 var backBtn=document.getElementById('g360-page-back'),homeBtn=document.getElementById('g360-page-home');
 if(backBtn)backBtn.addEventListener('click',back);
 if(homeBtn)homeBtn.addEventListener('click',goHome);
 document.addEventListener('click',function(e){
   var b=e.target&&e.target.closest?e.target.closest('button,[role="button"],a'):null;if(!b)return;
   if(b.id==='g360-page-back'||b.id==='g360-page-home')return;
   var label=(b.innerText||b.getAttribute('aria-label')||b.title||'').trim().toLowerCase();
   var map=[['map',/carte|map/],['nav',/navigation|gps terrain/],['sat',/satellite/],['drones',/drone/],['cameras',/cam[eé]ra/],['maritime',/maritime|oc[eé]an/],['alerts',/alerte/],['reports',/rapport/],['stats',/statistique/],['weather',/m[eé]t[eé]o/],['security',/cyber|s[eé]curit[eé]/],['memory',/m[eé]moire/],['avatar',/accueil|avatar|centre national/]];
   for(var i=0;i<map.length;i++){if(map[i][1].test(label)){if(last!==map[i][0])stack.push(last);last=map[i][0];break}}
 },true);
 document.addEventListener('keydown',function(e){if(e.key==='Escape'||e.key==='Backspace'){if(e.target&&/INPUT|TEXTAREA/.test(e.target.tagName))return;back()}});
 function hookAndroidBack(){
   if(window.G360Android&&typeof window.G360Android.setBackHandler==='function'){try{window.G360Android.setBackHandler('g360-page-back');return}catch(e){}}
 }
 hookAndroidBack();
 window.GABON360_PAGE_EXIT_STATUS={backButton:!!backBtn,homeButton:!!homeBtn,version:1};
})();
</script>

'''

def main():
    required = ['GABON360-SATELLITE-PANEL-V1']
    candidates = sorted(Path('android_project').rglob('index.html'), key=lambda p: ('assets' not in p.parts, len(p.parts), str(p)))
    scored=[]
    for p in candidates:
        t=p.read_text(encoding='utf-8',errors='ignore')
        scored.append((sum(x in t for x in required),p,t))
    scored.sort(key=lambda x:(x[0],-len(x[1].parts),str(x[1])),reverse=True)
    if not scored or scored[0][0] < len(required):
        raise SystemExit('OVERLAY-REPAIR FAIL: consolidated index with satellite panel not found')
    _,p,t=scored[0]
    if MARK in t:
        print('OVERLAY-REPAIR already installed:',p); return
    i=t.lower().rfind('</body>')
    if i<0: raise SystemExit('OVERLAY-REPAIR FAIL: </body> missing')
    p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
    print('OVERLAY-REPAIR installed:',p)

if __name__ == '__main__': main()
