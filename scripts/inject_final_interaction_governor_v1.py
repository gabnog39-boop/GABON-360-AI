#!/usr/bin/env python3
from pathlib import Path

MARK = "GABON360-FINAL-INTERACTION-GOVERNOR-V1"

PAYLOAD = r'''<!-- GABON360-FINAL-INTERACTION-GOVERNOR-V1 -->
<style>
/* Gouverneur final : une seule fenêtre interactive à la fois. */
#g360-avatar-launch,#g360-universal-launch,#g360-v2-launch,#g360-avatar-home-button{
  pointer-events:auto!important;
  touch-action:manipulation!important;
}
#g360-avatar-launch{z-index:2147483640!important}
#g360-universal-launch,#g360-v2-launch{z-index:2147483639!important}
#g360-avatar-modal,#g360-universal,#g360-v2,#g360-pages-modal{
  touch-action:pan-y!important;
}
</style>
<script id="g360-final-interaction-governor">
(function(){
  if(window.__G360_FINAL_INTERACTION_GOVERNOR_V1)return;
  window.__G360_FINAL_INTERACTION_GOVERNOR_V1=true;

  var modalIds=['g360-avatar-modal','g360-universal','g360-v2','g360-pages-modal'];

  function el(id){return document.getElementById(id);}
  function hide(id){
    var e=el(id);
    if(!e)return;
    e.style.setProperty('display','none','important');
    e.setAttribute('aria-hidden','true');
  }
  function show(id,display){
    var e=el(id);
    if(!e)return false;
    e.style.setProperty('display',display||'block','important');
    e.setAttribute('aria-hidden','false');
    e.style.setProperty('pointer-events','auto','important');
    return true;
  }
  function closeAll(except){
    modalIds.forEach(function(id){if(id!==except)hide(id);});
  }
  window.GABON360_CLOSE_ALL_PANELS=function(except){closeAll(except||null);};

  /* L'Avatar est la vraie page d'accueil : on ouvre son lanceur central,
     pas la simple liste de fonctions "Avatar". */
  window.GABON360_OPEN_AVATAR_HOME=function(){
    closeAll('g360-avatar-modal');
    var b=el('g360-avatar-launch');
    if(b){b.click();return true;}
    var m=el('g360-avatar-modal');
    if(m)return show('g360-avatar-modal','flex');
    return false;
  };

  function openModule(id){
    closeAll(null);
    if(id==='avatar')return window.GABON360_OPEN_AVATAR_HOME();
    if(typeof window.GABON360_OPEN_MODULE_PAGE==='function'){
      return window.GABON360_OPEN_MODULE_PAGE(id);
    }
    return false;
  }

  var ORDER=['avatar','map','nav','sat','drones','cameras','maritime','forests','alerts','reports','stats','weather','sources','security','memory'];
  window.GABON360_PAGE_ORDER=ORDER.slice();
  var current=window.GABON360_CURRENT_PAGE||'avatar';

  window.GABON360_PAGE_NAVIGATION={
    order:ORDER.slice(),
    current:function(){return current;},
    go:function(id){
      if(ORDER.indexOf(id)<0)id='avatar';
      current=id;window.GABON360_CURRENT_PAGE=id;
      return openModule(id);
    },
    next:function(){
      var i=ORDER.indexOf(current);if(i<0)i=0;
      if(i<ORDER.length-1){current=ORDER[i+1];window.GABON360_CURRENT_PAGE=current;return openModule(current);}
      return true;
    },
    previous:function(){
      var i=ORDER.indexOf(current);if(i<0)i=0;
      if(i>0){current=ORDER[i-1];window.GABON360_CURRENT_PAGE=current;return openModule(current);}
      return openModule('avatar');
    }
  };
  window.GABON360_PAGE_NEXT=function(){return window.GABON360_PAGE_NAVIGATION.next();};
  window.GABON360_PAGE_PREVIOUS=function(){return window.GABON360_PAGE_NAVIGATION.previous();};

  /* Rebranche les boutons principaux afin qu'ils ne restent jamais derrière
     une ancienne fenêtre. */
  function wire(){
    var a=el('g360-avatar-launch');
    if(a&&!a.__g360Governor){
      a.__g360Governor=true;
      a.addEventListener('click',function(){closeAll('g360-avatar-modal');},true);
    }
    var u=el('g360-universal-launch');
    if(u&&!u.__g360Governor){
      u.__g360Governor=true;
      u.addEventListener('click',function(){closeAll('g360-universal');},true);
    }
    var v=el('g360-v2-launch');
    if(v&&!v.__g360Governor){
      v.__g360Governor=true;
      v.addEventListener('click',function(){closeAll('g360-v2');},true);
    }
    var h=el('g360-avatar-home-button');
    if(h&&!h.__g360Governor){
      h.__g360Governor=true;
      h.addEventListener('click',function(e){e.preventDefault();window.GABON360_OPEN_AVATAR_HOME();},true);
    }
  }

  /* Les boutons internes ferment les autres surfaces avant d'ouvrir la leur. */
  document.addEventListener('click',function(e){
    var b=e.target&&e.target.closest?e.target.closest('button,a,[role="button"]'):null;
    if(!b)return;
    if(b.id==='g360-avatar-launch'||b.id==='g360-avatar-home-button')return;
    if(b.id==='g360-universal-launch'||b.id==='g360-v2-launch')return;
    var label=(b.innerText||b.textContent||'').replace(/\s+/g,' ').trim().toLowerCase();
    if(label==='fermer' || label==='✕' || label==='x')return;
    if(/page suivante|page précédente|page precedente|page suivante/.test(label))return;
  },true);

  /* Commandes Avatar pour navigation horizontale. */
  var old=window.GABON360_HANDLE_COMMAND;
  window.GABON360_HANDLE_COMMAND=function(raw){
    var q=String(raw||'').toLowerCase().trim();
    if(/^(accueil|home|page principale|ouvre avatar|avatar)$/.test(q))
      return window.GABON360_OPEN_AVATAR_HOME();
    if(/page suivante|ouvre la page suivante|fais défiler vers la gauche|glisse vers la gauche/.test(q))
      return window.GABON360_PAGE_NEXT();
    if(/page précédente|page precedente|ouvre la page précédente|fais défiler vers la droite|glisse vers la droite/.test(q))
      return window.GABON360_PAGE_PREVIOUS();
    return typeof old==='function'?old.apply(this,arguments):false;
  };

  wire();
  if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',wire);
  [300,800,1500,3000].forEach(function(ms){setTimeout(wire,ms);});

  /* Au démarrage : Avatar uniquement. */
  setTimeout(function(){
    closeAll(null);
    window.GABON360_CURRENT_PAGE='avatar';
    wire();
    /* L'avatar est réellement la page principale : ouvrir son interface centrale. */
    try{ window.GABON360_OPEN_AVATAR_HOME(); }catch(e){}
  },350);

  window.GABON360_FINAL_INTERACTION_GOVERNOR={version:'1.0',home:'avatar',singlePanel:true,horizontalNavigation:true};
})();
</script>
'''

def main():
    roots=sorted(Path('android_project').rglob('index.html'),key=lambda p:(len(p.parts),str(p)))
    if not roots: raise SystemExit('index.html introuvable')
    required=['GABON360-UNIVERSAL-MODULE-PAGES-V1','GABON360-AVATAR-HOME-V1']
    candidates=[]
    for p in roots:
        t=p.read_text(encoding='utf-8',errors='ignore')
        score=sum(x in t for x in required)
        candidates.append((score,p,t))
    score,p,t=max(candidates,key=lambda x:(x[0],-len(x[1].parts),str(x[1])))
    if score<len(required): raise SystemExit('Aucun index.html consolidé trouvé')
    if MARK in t:
        print('already:',p); return
    i=t.lower().rfind('</body>')
    if i<0: raise SystemExit('</body> introuvable')
    p.write_text(t[:i]+PAYLOAD+'\n'+t[i:],encoding='utf-8')
    print('installed:',p)

if __name__=='__main__': main()
