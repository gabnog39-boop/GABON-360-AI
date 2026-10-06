#!/usr/bin/env python3
"""Integrate Google Play Billing into the consolidated Android project.

Adds BillingClient and a small WebView bridge. Product IDs are deliberately
configuration-driven; the Play Console product must exist before real purchases
can be completed. Purchase verification remains server-side.
"""
from __future__ import annotations
import re
from pathlib import Path

MARKER = "GABON360_PAYMENT_BILLING_V1"
DEPENDENCY = 'implementation "com.android.billingclient:billing:9.1.0"'

BRIDGE_TEMPLATE = r'''package {package};

import android.app.Activity;
import android.webkit.JavascriptInterface;
import android.webkit.WebView;
import com.android.billingclient.api.*;
import java.util.List;

public final class PaymentBillingBridge implements PurchasesUpdatedListener {
    private final Activity activity;
    private final WebView webView;
    private BillingClient billingClient;

    public PaymentBillingBridge(Activity activity, WebView webView) {
        this.activity = activity;
        this.webView = webView;
        billingClient = BillingClient.newBuilder(activity)
                .setListener(this)
                .enablePendingPurchases()
                .build();
        billingClient.startConnection(new BillingClientStateListener() {
            @Override public void onBillingSetupFinished(BillingResult result) {
                emit("ready", result.getResponseCode() == BillingClient.BillingResponseCode.OK, result.getDebugMessage());
            }
            @Override public void onBillingServiceDisconnected() { emit("disconnected", false, "Google Play Billing indisponible"); }
        });
    }

    @JavascriptInterface
    public void buy(String productId) {
        if (productId == null || productId.trim().isEmpty()) { emit("error", false, "Product ID manquant"); return; }
        if (!billingClient.isReady()) { emit("error", false, "Google Play Billing n'est pas prêt"); return; }
        QueryProductDetailsParams params = QueryProductDetailsParams.newBuilder()
                .setProductList(List.of(QueryProductDetailsParams.Product.newBuilder()
                        .setProductId(productId)
                        .setProductType(BillingClient.ProductType.SUBS)
                        .build()))
                .build();
        billingClient.queryProductDetailsAsync(params, (result, details) -> {
            if (result.getResponseCode() != BillingClient.BillingResponseCode.OK || details == null || details.isEmpty()) {
                emit("error", false, "Abonnement introuvable dans Google Play : " + result.getDebugMessage()); return;
            }
            ProductDetails pd = details.get(0);
            if (pd.getSubscriptionOfferDetails() == null || pd.getSubscriptionOfferDetails().isEmpty()) {
                emit("error", false, "Aucune offre d'abonnement configurée"); return;
            }
            String offer = pd.getSubscriptionOfferDetails().get(0).getOfferToken();
            BillingFlowParams flow = BillingFlowParams.newBuilder()
                    .setProductDetailsParamsList(List.of(BillingFlowParams.ProductDetailsParams.newBuilder()
                            .setProductDetails(pd).setOfferToken(offer).build()))
                    .build();
            activity.runOnUiThread(() -> billingClient.launchBillingFlow(activity, flow));
        });
    }

    @Override public void onPurchasesUpdated(BillingResult result, List<Purchase> purchases) {
        if (result.getResponseCode() != BillingClient.BillingResponseCode.OK || purchases == null) {
            emit("purchase", false, result.getDebugMessage()); return;
        }
        for (Purchase p : purchases) {
            String token = p.getPurchaseToken();
            String product = p.getProducts().isEmpty() ? "" : p.getProducts().get(0);
            boolean purchased = p.getPurchaseState() == Purchase.PurchaseState.PURCHASED;
            emit("purchase", purchased, product + "|" + token);
        }
    }

    private void emit(String type, boolean ok, String message) {
        String safe = message == null ? "" : message.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ");
        activity.runOnUiThread(() -> webView.evaluateJavascript(
                "window.GABON360BillingResult && window.GABON360BillingResult('" + type + "'," + ok + ",'" + safe + "')", null));
    }
}
'''

UI = r'''<!-- GABON360_PAYMENT_BILLING_V1 -->
<style>
#g360-pay{position:fixed;top:70px;right:14px;z-index:100003;background:#0b1a2a;color:#eef6ff;border:1px solid #31506d;border-radius:12px;padding:9px;box-shadow:0 10px 30px #0008;font:12px system-ui,sans-serif}
#g360-pay button{border:1px solid #29425a;background:#15324b;color:#fff;border-radius:8px;padding:8px 10px;cursor:pointer}
#g360-pay .state{margin:4px 0 7px}.g360-pay-ok{color:#8df0b1}.g360-pay-wait{color:#ffd48a}
</style>
<div id="g360-pay"><div><b>💳 Accès GABON 360 AI</b></div><div id="g360-pay-state" class="state g360-pay-wait">Vérification de l'abonnement…</div><button id="g360-pay-buy">S'abonner / payer</button></div>
<script>
(function(){
 const state=document.getElementById('g360-pay-state');
 const productId='gabon360_monthly';
 window.GABON360BillingResult=function(type,ok,msg){
   if(type==='ready') state.textContent=ok?'Google Play prêt — abonnement requis':'Google Play indisponible';
   else if(type==='purchase') state.textContent=ok?'Achat reçu — vérification serveur obligatoire':'Achat non confirmé';
   else if(type==='error') state.textContent=msg||'Erreur paiement';
   state.className='state '+(ok?'g360-pay-ok':'g360-pay-wait');
   if(type==='purchase'&&ok){
     window.dispatchEvent(new CustomEvent('gabon360:payment-token',{detail:{productId:productId,raw:msg}}));
   }
 };
 document.getElementById('g360-pay-buy').onclick=function(){
   if(window.GABON360Billing&&window.GABON360Billing.buy){window.GABON360Billing.buy(productId);}
   else state.textContent='Google Play Billing n’est pas encore relié à l’écran Android.';
 };
})();
</script>
'''

def find_module_gradle():
    for p in sorted(Path('android_project').rglob('build.gradle*')):
        try: t=p.read_text(encoding='utf-8')
        except Exception: continue
        if 'com.android.application' in t: return p,t
    raise SystemExit('Module Android application introuvable')

def find_namespace(gradle_text):
    m=re.search(r'namespace\s*[= ]\s*["\']([^"\']+)["\']',gradle_text)
    if m:return m.group(1)
    m=re.search(r'applicationId\s*[= ]\s*["\']([^"\']+)["\']',gradle_text)
    if m:return m.group(1)
    raise SystemExit('Namespace/applicationId introuvable')

def inject_activity(package):
    candidates=list(Path('android_project').rglob('*.java'))+list(Path('android_project').rglob('*.kt'))
    for p in candidates:
        try:t=p.read_text(encoding='utf-8')
        except Exception:continue
        if 'WebView' not in t or 'setContentView' not in t or 'GABON360Billing' in t:continue
        if p.suffix=='.java':
            vm=re.search(r'WebView\s+(\w+)\s*(?:=|;)',t)
            if not vm:continue
            v=vm.group(1)
            needle='setContentView('
            pos=t.find(needle)
            if pos<0:continue
            end=t.find('\n',pos)
            if end<0:end=len(t)
            line='\n        '+v+'.addJavascriptInterface(new PaymentBillingBridge(this, '+v+'), "GABON360Billing");'
            t=t[:end]+line+t[end:]
            if 'import android.webkit.WebView;' not in t:
                t=t.replace('package '+package+';','package '+package+';\n\nimport android.webkit.WebView;',1)
            p.write_text(t,encoding='utf-8');return p
        else:
            vm=re.search(r'(?:lateinit\s+var|var|val)\s+(\w+)\s*:\s*WebView',t)
            if not vm:continue
            v=vm.group(1); pos=t.find('setContentView(')
            if pos<0:continue
            end=t.find('\n',pos)
            if end<0:end=len(t)
            line=f'\n        {v}.addJavascriptInterface(PaymentBillingBridge(this, {v}), "GABON360Billing")'
            t=t[:end]+line+t[end:];p.write_text(t,encoding='utf-8');return p
    return None

def main():
    gradle,txt=find_module_gradle()
    if DEPENDENCY not in txt:
        anchor='dependencies {'
        i=txt.find(anchor)
        if i<0: raise SystemExit('Bloc dependencies introuvable')
        e=i+len(anchor)
        txt=txt[:e]+'\n    '+DEPENDENCY+txt[e:]
        gradle.write_text(txt,encoding='utf-8')
    package=find_namespace(txt)
    src=Path('android_project')
    pkgdir=src/next((p for p in src.rglob('java') if p.is_dir()),Path('app/src/main/java'))
    for _ in []: pass
    roots=[p for p in src.rglob('java') if p.is_dir()]
    root=roots[0] if roots else src/'app/src/main/java'
    target=root/Path(package.replace('.','/'))
    target.mkdir(parents=True,exist_ok=True)
    bridge=target/'PaymentBillingBridge.java'
    if not bridge.exists(): bridge.write_text(BRIDGE_TEMPLATE.format(package=package),encoding='utf-8')
    activity=inject_activity(package)
    if activity is None: print('WARNING: WebView Activity not automatically wired; BillingClient and bridge were installed.')
    else: print('wired:',activity)
    for p in sorted(src.rglob('index.html')):
        t=p.read_text(encoding='utf-8')
        if 'GABON360_PAYMENT_BILLING_V1' not in t:
            i=t.lower().rfind('</body>')
            if i>=0:p.write_text(t[:i]+UI+'\n'+t[i:],encoding='utf-8');print('payment UI:',p);break
    print('payment billing integration complete')

if __name__=='__main__':main()
