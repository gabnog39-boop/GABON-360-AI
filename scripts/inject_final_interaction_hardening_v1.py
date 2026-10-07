#!/usr/bin/env python3
from pathlib import Path

MARK = "GABON360-FINAL-INTERACTION-HARDENING-V1"

PAYLOAD = r'''<!-- GABON360-FINAL-INTERACTION-HARDENING-V1 -->
<style>
/* Final interaction layer: hidden overlays never capture touches. */
button,a,[role="button"],input,select,textarea{
  touch-action:manipulation!important;
}
#g360-universal[aria-hidden="true"],
#g360-pages-modal[aria-hidden="true"],
#g360-cm-modal[aria-hidden="true"],
#g360-avatar-modal[aria-hidden="true"]{
  pointer-events:none!important;
  visibility:hidden!important;
}
#g360-universal[aria-hidden="false"],
#g360-pages-modal[aria-hidden="false"],
#g360-cm-modal[aria-hidden="false"],
#g360-avatar-modal[aria-hidden="false"]{
  pointer-events:auto!important;
  visibility:visible!important;
}
#g360-universal-launch,
#g360-pages-open,
#g360-modules,
#g360-avatar-launch,
#g360-avatar-home-dock{
  pointer-events:auto!important;
}
</style>
<script>
(function(){
  if(window.__G360_FINAL_INTERACTION_HARDENING_V1)return;
  window.__G360_FINAL_INTERACTION_HARDENING_V1=true;

  var modalIds=['g360-universal','g360-pages-modal','g360-cm-modal','g360-avatar-modal'];

  function isHidden(el){
    if(!el)return true;
    var s=getComputedStyle(el);
    return el.getAttribute('aria-hidden')==='true' ||
      s.display==='none' ||
      s.visibility==='hidden' ||
      s.pointerEvents==='none';
  }

  function harden(){
    modalIds.forEach(function(id){
      var el=document.getElementById(id);
      if(!el)return;
      var hidden=isHidden(el);
      if(hidden){
        el.style.setProperty('pointer-events','none','important');
      }else{
        el.style.setProperty('pointer-events','auto','important');
      }
    });
    document.querySelectorAll('button,a,[role="button"],input,select,textarea').forEach(function(el){
      el.style.setProperty('pointer-events','auto','important');
      el.style.setProperty('touch-action','manipulation','important');
    });
  }

  function closeStartupOverlays(){
    /* The app must open on the Avatar/dashboard, never on a stale modal. */
    ['g360-pages-modal','g360-cm-modal','g360-avatar-modal'].forEach(function(id){
      var el=document.getElementById(id);
      if(!el)return;
      if(id==='g360-avatar-modal'){
        el.style.setProperty('display','none','important');
        el.setAttribute('aria-hidden','true');
      }else if(!el.hasAttribute('data-g360-keep-open')){
        el.style.setProperty('display','none','important');
        el.setAttribute('aria-hidden','true');
      }
    });
  }

  function openModule(id){
    try{
      if(id==='avatar' && window.GABON360_OPEN_AVATAR_HOME){
        window.GABON360_OPEN_AVATAR_HOME(); return true;
      }
      if(window.GABON360_OPEN_MODULE_PAGE){
        window.GABON360_OPEN_MODULE_PAGE(id); return true;
      }
      if(window.GABON360_NAVIGATE){
        window.GABON360_NAVIGATE(id); return true;
      }
    }catch(e){}
    return false;
  }

  function openCenter(){
    if(window.GABON360_OPEN_MODULE_PAGE){
      try{ window.GABON360_OPEN_MODULE_PAGE('avatar'); return true; }catch(e){}
    }
    var b=document.getElementById('g360-pages-open');
    if(b){b.click();return true;}
    return false;
  }

  function routeText(label){
    var q=String(label||'').replace(/\s+/g,' ').trim().toLowerCase();
    if(!q)return false;
    if(q==='carte'||q.indexOf('carte ')===0)return openModule('map');
    if(q==='satellite'||q.indexOf('satellite')===0)return openModule('sat');
    if(q==='gabon'||q.indexOf('gabon')===0){
      if(window.GABON360_OPEN_AVATAR_HOME){try{window.GABON360_OPEN_AVATAR_HOME();return true}catch(e){}}
      return false;
    }
    if(q.indexOf('centre des fonctions')>=0||q==='toutes les pages')return openCenter();
    if(q.indexOf('gps terrain')>=0||q.indexOf('navigation terrain')>=0)return openModule('nav');
    if(q.indexOf('forêt')>=0||q.indexOf('forêts')>=0)return openModule('forests');
    if(q.indexOf('météo')>=0)return openModule('weather');
    if(q.indexOf('alerte')>=0)return openModule('alerts');
    if(q.indexOf('rapport')>=0)return openModule('reports');
    if(q.indexOf('statistique')>=0)return openModule('stats');
    if(q.indexOf('mémoire')>=0)return openModule('memory');
    if(q.indexOf('cybersécurité')>=0)return openModule('security');
    return false;
  }

  document.addEventListener('click',function(e){
    var b=e.target && e.target.closest ? e.target.closest('button,a,[role="button"]') : null;
    if(!b)return;
    if(b.id==='g360-universal-launch' || b.id==='g360-pages-open'){
      e.stopImmediatePropagation();
      openCenter();
      return;
    }
    var label=b.innerText||b.textContent||b.getAttribute('aria-label')||'';
    /* Only take over the known top-level launchers; ordinary module buttons keep their own handlers. */
    var q=String(label).replace(/\s+/g,' ').trim().toLowerCase();
    if(['carte','satellite','gabon','centre des fonctions','toutes les pages','gps terrain'].indexOf(q)>=0){
      e.stopImmediatePropagation();
      routeText(label);
    }
  },true);

  /* Keep hidden layers from becoming transparent touch blockers after other injectors run. */
  var obs=new MutationObserver(function(){harden();});
  function boot(){
    closeStartupOverlays();
    harden();
    if(window.GABON360_OPEN_AVATAR_HOME){
      try{window.GABON360_OPEN_AVATAR_HOME();}catch(e){}
    }
  }
  if(document.body)boot();
  window.addEventListener('load',boot);
  obs.observe(document.documentElement,{subtree:true,attributes:true,attributeFilter:['style','class','aria-hidden']});
  setInterval(harden,1000);

  window.GABON360_FINAL_INTERACTION={
    version:'1.0',
    hiddenOverlaysDoNotBlock:true,
    topLevelLaunchers:true,
    avatarHome:true
  };
})();
</script>
'''

def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:('assets' in p.parts,len(p.parts)))
    if not candidates:
        raise SystemExit('FINAL-INTERACTION FAIL: index.html introuvable')
    for p in candidates:
        text=p.read_text(encoding='utf-8',errors='ignore')
        if MARK in text:
            print('already:',p)
            return
        i=text.lower().rfind('</body>')
        if i<0:
            continue
        p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
        print('installed:',p)
        return
    raise SystemExit('FINAL-INTERACTION FAIL: aucun index.html exploitable')

if __name__=='__main__':
    main()
