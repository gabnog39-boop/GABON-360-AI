#!/usr/bin/env python3
from pathlib import Path
MARK='<!-- GABON360-AVATAR-HOME-FIX-V2 -->'
PAYLOAD=r'''<!-- GABON360-AVATAR-HOME-FIX-V2 -->
<style>
/* L'avatar central doit être visible sur l'accueil, sans dépendre du menu IA. */
#g360-avatar-launch{display:block!important;visibility:visible!important;opacity:1!important;position:fixed!important;left:12px!important;right:auto!important;bottom:154px!important;width:82px!important;height:82px!important;z-index:2147483000!important}
#g360-avatar-launch img{display:block!important;visibility:visible!important;opacity:1!important;width:100%!important;height:100%!important;object-fit:cover!important}
#g360-avatar-home-dock{display:flex;position:fixed;left:12px;bottom:154px;width:82px;height:82px;z-index:2147482999;pointer-events:none;align-items:center;justify-content:center}
#g360-avatar-home-dock.g360-home-hidden{display:none!important}
#g360-avatar-home-dock button{pointer-events:auto;width:82px;height:82px;border-radius:50%;overflow:hidden;padding:0;border:2px solid #35e6a0;background:#061522;box-shadow:0 0 24px #1de59a66}
#g360-avatar-home-dock img{width:100%;height:100%;object-fit:cover;display:block}
#g360-avatar-home-label{position:absolute;left:0;top:86px;white-space:nowrap;background:#061522ee;border:1px solid #35e6a066;border-radius:8px;padding:4px 7px;color:#dff;font:11px system-ui,sans-serif}
@media(max-width:420px){#g360-avatar-launch{width:76px!important;height:76px!important;bottom:154px!important;left:10px!important}#g360-avatar-home-dock{width:76px;height:76px;left:10px;bottom:154px}}
</style>
<script>
(function(){
 function install(){
   var src=document.getElementById('g360-avatar-launch');
   if(!src)return false;
   src.style.setProperty('display','block','important');
   src.style.setProperty('visibility','visible','important');
   src.style.setProperty('opacity','1','important');
   src.style.setProperty('z-index','2147483000','important');
   /* The avatar itself remains the original embedded image. No replacement image is generated. */
   if(!document.getElementById('g360-avatar-home-dock')){
     var dock=document.createElement('div'); dock.id='g360-avatar-home-dock';
     var b=document.createElement('button'); b.type='button'; b.setAttribute('aria-label','Ouvrir l IA centrale');
     var im=src.querySelector('img');
     if(im){var copy=im.cloneNode(true); b.appendChild(copy);}
     else{b.textContent='🤖';}
     var label=document.createElement('span');label.id='g360-avatar-home-label';label.textContent='IA centrale';
     b.addEventListener('click',function(){src.click();}); dock.appendChild(b);dock.appendChild(label);document.body.appendChild(dock);
   }
   return true;
 }
 if(!install()){
   var n=0,t=setInterval(function(){n++;if(install()||n>30)clearInterval(t)},200);
 }
 window.GABON360_AVATAR_HOME={version:'2.0',visible:true};
})();
</script>
'''
def main():
    candidates=sorted(Path('android_project').rglob('index.html'),key=lambda p:len(p.parts))
    if not candidates: raise SystemExit('No index.html found')
    for p in candidates:
        text=p.read_text(encoding='utf-8')
        if MARK in text: print('already:',p); return
        i=text.lower().rfind('</body>')
        if i<0: continue
        p.write_text(text[:i]+PAYLOAD+'\n'+text[i:],encoding='utf-8')
        print('injected:',p); return
    raise SystemExit('No suitable index.html found')
if __name__=='__main__': main()
