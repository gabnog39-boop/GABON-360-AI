#!/usr/bin/env python3
from pathlib import Path

MARKER = "GABON360-AVATAR-HOME-V1"

JS = r"""
<script id="gabon360-avatar-home-v1">
(() => {
  const MARKER = "GABON360-AVATAR-HOME-V1";
  const ORDER = ["avatar","map","nav","sat","drones","cameras","maritime","forests","alerts","reports","stats","weather","sources","security","memory"];
  window.GABON360_PAGE_ORDER = ORDER.slice();

  function pageIds() {
    return Array.isArray(window.GABON360_MODULE_PAGES) ? window.GABON360_MODULE_PAGES : [];
  }

  function open(id) {
    try {
      if (id === "avatar") {
        if (typeof window.GABON360_OPEN_MODULE_PAGE === "function") {
          window.GABON360_OPEN_MODULE_PAGE("avatar");
          return true;
        }
        if (typeof window.GABON360_OPEN_FUNCTION_PAGE === "function") {
          window.GABON360_OPEN_FUNCTION_PAGE("avatar");
          return true;
        }
      }
      if (typeof window.GABON360_OPEN_MODULE_PAGE === "function") {
        window.GABON360_OPEN_MODULE_PAGE(id);
        return true;
      }
      if (typeof window.GABON360_OPEN_FUNCTION_PAGE === "function") {
        window.GABON360_OPEN_FUNCTION_PAGE(id);
        return true;
      }
    } catch (_) {}
    return false;
  }

  window.GABON360_OPEN_AVATAR_HOME = () => {
    window.GABON360_CURRENT_HOME = "avatar";
    window.GABON360_CURRENT_PAGE = "avatar";
    return open("avatar");
  };

  const previousNav = window.GABON360_PAGE_NAVIGATION || {};
  window.GABON360_PAGE_NAVIGATION = {
    order: ORDER.slice(),
    current: () => window.GABON360_CURRENT_PAGE || "avatar",
    go: (id) => {
      const target = ORDER.includes(id) ? id : "avatar";
      window.GABON360_CURRENT_PAGE = target;
      return open(target);
    },
    next: () => {
      const cur = ORDER.indexOf(window.GABON360_CURRENT_PAGE || "avatar");
      const i = cur < 0 ? 0 : Math.min(cur + 1, ORDER.length - 1);
      window.GABON360_CURRENT_PAGE = ORDER[i];
      return open(ORDER[i]);
    },
    previous: () => {
      const cur = ORDER.indexOf(window.GABON360_CURRENT_PAGE || "avatar");
      const i = cur <= 0 ? 0 : cur - 1;
      window.GABON360_CURRENT_PAGE = ORDER[i];
      return open(ORDER[i]);
    }
  };
  window.GABON360_PAGE_NEXT = () => window.GABON360_PAGE_NAVIGATION.next();
  window.GABON360_PAGE_PREVIOUS = () => window.GABON360_PAGE_NAVIGATION.previous();

  const oldCommand = window.GABON360_HANDLE_COMMAND;
  window.GABON360_HANDLE_COMMAND = function(text) {
    const t = String(text || "").toLowerCase().trim();
    if (/^(accueil|home|retour accueil|page principale|ouvre l.?accueil|ouvre avatar|avatar)$/.test(t)) {
      return window.GABON360_OPEN_AVATAR_HOME();
    }
    if (typeof oldCommand === "function") return oldCommand.apply(this, arguments);
    return false;
  };

  function addHomeButton() {
    if (document.getElementById("g360-avatar-home-button")) return;
    const b = document.createElement("button");
    b.id = "g360-avatar-home-button";
    b.type = "button";
    b.textContent = "🤖";
    b.title = "Accueil — Avatar IA";
    b.setAttribute("aria-label", "Accueil Avatar IA");
    Object.assign(b.style, {
      position:"fixed", right:"14px", bottom:"14px", zIndex:"2147483646",
      width:"54px", height:"54px", borderRadius:"50%", border:"1px solid rgba(255,255,255,.35)",
      background:"rgba(8,20,35,.92)", color:"#fff", fontSize:"25px",
      boxShadow:"0 6px 24px rgba(0,0,0,.35)"
    });
    b.addEventListener("click", () => window.GABON360_OPEN_AVATAR_HOME());
    document.body.appendChild(b);
  }

  function setInitialHome() {
    window.GABON360_CURRENT_HOME = "avatar";
    if (!window.GABON360_CURRENT_PAGE) window.GABON360_CURRENT_PAGE = "avatar";
    addHomeButton();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", setInitialHome);
  else setInitialHome();

  window.dispatchEvent(new CustomEvent("gabon360:avatar-home-ready", {
    detail:{marker:MARKER, order:ORDER.slice(), home:"avatar"}
  }));
})();
</script>
"""

def main():
    roots = sorted(Path("android_project").rglob("index.html"), key=lambda p: len(p.parts))
    if not roots:
        raise SystemExit("index.html introuvable")
    p = roots[0]
    s = p.read_text(encoding="utf-8", errors="ignore")
    if MARKER in s:
        print("AVATAR-HOME: déjà présent")
        return
    pos = s.lower().rfind("</body>")
    if pos < 0:
        raise SystemExit("</body> introuvable")
    s = s[:pos] + JS + "\n" + s[pos:]
    p.write_text(s, encoding="utf-8")
    print(f"AVATAR-HOME: injecté dans {p}")

if __name__ == "__main__":
    main()
