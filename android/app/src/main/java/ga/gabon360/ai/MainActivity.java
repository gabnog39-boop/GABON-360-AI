package ga.gabon360.ai;

import android.Manifest;
import android.app.Activity;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.webkit.GeolocationPermissions;
import android.webkit.JavascriptInterface;
import android.webkit.PermissionRequest;
import android.webkit.WebChromeClient;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebResourceRequest;
import android.view.ViewGroup;
import android.widget.FrameLayout;
import android.graphics.Color;
import android.net.Uri;
import android.os.Build;

import org.json.JSONObject;

public class MainActivity extends Activity {
    private static final int PERMISSION_REQUEST = 360;
    private static final String TRUSTED_HOST =
        "gabon-360-ai-git-test-avatar-central-gabnog39-7241.vercel.app";

    private WebView webView;
    private LocationManager locationManager;
    private LocationListener locationListener;
    private boolean gpsRunning = false;

    private boolean hasLocationPermission() {
        return checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) == PackageManager.PERMISSION_GRANTED
            || checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) == PackageManager.PERMISSION_GRANTED;
    }

    private boolean isTrustedUrl(String url) {
        try {
            Uri uri = Uri.parse(url);
            return "https".equalsIgnoreCase(uri.getScheme())
                && TRUSTED_HOST.equalsIgnoreCase(uri.getHost());
        } catch (Exception ignored) {
            return false;
        }
    }

    private void sendStatus(boolean ok, String message) {
        if (webView == null) return;
        try {
            JSONObject detail = new JSONObject();
            detail.put("ok", ok);
            detail.put("message", message);
            String script = "window.dispatchEvent(new CustomEvent('g360:gps-status',{detail:"
                + detail.toString() + "}));";
            runOnUiThread(() -> webView.evaluateJavascript(script, null));
        } catch (Exception ignored) { }
    }

    private void sendLocation(Location location) {
        if (webView == null || location == null) return;
        try {
            JSONObject detail = new JSONObject();
            detail.put("lat", location.getLatitude());
            detail.put("lon", location.getLongitude());
            detail.put("accuracy", location.hasAccuracy() ? location.getAccuracy() : JSONObject.NULL);
            detail.put("speed", location.hasSpeed() ? location.getSpeed() : 0);
            detail.put("altitude", location.hasAltitude() ? location.getAltitude() : JSONObject.NULL);
            detail.put("time", location.getTime());
            String script = "window.dispatchEvent(new CustomEvent('g360:gps-fix',{detail:"
                + detail.toString() + "}));";
            runOnUiThread(() -> webView.evaluateJavascript(script, null));
        } catch (Exception ignored) { }
    }

    private void stopGps() {
        gpsRunning = false;
        if (locationManager != null && locationListener != null) {
            try { locationManager.removeUpdates(locationListener); }
            catch (SecurityException ignored) { }
        }
        sendStatus(true, "Suivi GPS arrêté");
    }

    private void startGps() {
        runOnUiThread(() -> {
            if (!hasLocationPermission()) {
                sendStatus(false, "Autorisation de localisation nécessaire. Autorise le GPS dans Android.");
                requestLocationPermission();
                return;
            }
            try {
                if (locationManager == null) {
                    locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
                }
                if (locationManager == null || !locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
                    sendStatus(false, "GPS désactivé. Active la localisation du téléphone.");
                    return;
                }
                if (locationListener == null) {
                    locationListener = new LocationListener() {
                        @Override public void onLocationChanged(Location location) {
                            sendLocation(location);
                            sendStatus(true, "Position GPS réelle reçue");
                        }
                        @Override public void onProviderEnabled(String provider) {
                            sendStatus(true, "GPS activé");
                        }
                        @Override public void onProviderDisabled(String provider) {
                            sendStatus(false, "GPS désactivé");
                        }
                        @Override public void onStatusChanged(String provider, int status, Bundle extras) { }
                    };
                }
                locationManager.removeUpdates(locationListener);
                locationManager.requestLocationUpdates(
                    LocationManager.GPS_PROVIDER, 1000L, 2.0f, locationListener
                );
                gpsRunning = true;
                Location last = locationManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
                if (last != null) sendLocation(last);
                sendStatus(true, "Recherche de la position GPS satellite…");
            } catch (SecurityException error) {
                sendStatus(false, "Permission GPS refusée par Android.");
            } catch (Exception error) {
                sendStatus(false, "Impossible de démarrer le GPS : " + error.getMessage());
            }
        });
    }

    private void requestLocationPermission() {
        if (Build.VERSION.SDK_INT >= 23 && !hasLocationPermission()) {
            requestPermissions(new String[] {
                Manifest.permission.ACCESS_FINE_LOCATION,
                Manifest.permission.ACCESS_COARSE_LOCATION
            }, PERMISSION_REQUEST);
        }
    }

    private final class AndroidGpsBridge {
        @JavascriptInterface
        public void start() { startGps(); }

        @JavascriptInterface
        public void stop() { runOnUiThread(() -> stopGps()); }

        @JavascriptInterface
        public boolean isAvailable() { return hasLocationPermission(); }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setStatusBarColor(Color.rgb(5, 11, 20));
        getWindow().setNavigationBarColor(Color.rgb(5, 11, 20));

        locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        FrameLayout root = new FrameLayout(this);
        root.setLayoutParams(new FrameLayout.LayoutParams(
            ViewGroup.LayoutParams.MATCH_PARENT,
            ViewGroup.LayoutParams.MATCH_PARENT
        ));

        webView = new WebView(this);
        webView.setBackgroundColor(Color.rgb(5, 11, 20));
        WebSettings settings = webView.getSettings();
        settings.setJavaScriptEnabled(true);
        settings.setDomStorageEnabled(true);
        settings.setDatabaseEnabled(true);
        settings.setGeolocationEnabled(true);
        settings.setMediaPlaybackRequiresUserGesture(false);
        settings.setAllowFileAccess(false);
        settings.setSupportZoom(true);

        webView.setWebViewClient(new WebViewClient() {
            @Override
            public void onPageStarted(WebView view, String url, android.graphics.Bitmap favicon) {
                if (isTrustedUrl(url)) {
                    view.addJavascriptInterface(new AndroidGpsBridge(), "AndroidGPS");
                } else {
                    view.removeJavascriptInterface("AndroidGPS");
                    stopGps();
                }
                super.onPageStarted(view, url, favicon);
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return !isTrustedUrl(request.getUrl().toString());
            }

            @SuppressWarnings("deprecation")
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, String url) {
                return !isTrustedUrl(url);
            }
        });

        webView.setWebChromeClient(new WebChromeClient() {
            @Override
            public void onGeolocationPermissionsShowPrompt(
                String origin, GeolocationPermissions.Callback callback
            ) {
                callback.invoke(origin, hasLocationPermission(), false);
            }

            @Override
            public void onPermissionRequest(PermissionRequest request) {
                runOnUiThread(() -> {
                    boolean audio = false;
                    for (String resource : request.getResources()) {
                        if (PermissionRequest.RESOURCE_AUDIO_CAPTURE.equals(resource)) audio = true;
                    }
                    if (audio && checkSelfPermission(Manifest.permission.RECORD_AUDIO)
                        == PackageManager.PERMISSION_GRANTED) {
                        request.grant(request.getResources());
                    } else {
                        request.deny();
                    }
                });
            }
        });

        root.addView(webView);
        setContentView(root);

        String[] permissions = new String[] {
            Manifest.permission.RECORD_AUDIO,
            Manifest.permission.ACCESS_FINE_LOCATION,
            Manifest.permission.ACCESS_COARSE_LOCATION
        };
        boolean needsRequest = false;
        for (String permission : permissions) {
            if (checkSelfPermission(permission) != PackageManager.PERMISSION_GRANTED) {
                needsRequest = true;
                break;
            }
        }
        if (needsRequest) requestPermissions(permissions, PERMISSION_REQUEST);

        if (savedInstanceState == null) {
            webView.loadUrl("https://" + TRUSTED_HOST + "/");
        } else {
            webView.restoreState(savedInstanceState);
        }
    }

    @Override
    public void onRequestPermissionsResult(
        int requestCode, String[] permissions, int[] grantResults
    ) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_REQUEST) {
            if (hasLocationPermission()) {
                sendStatus(true, "Autorisation GPS accordée. Tu peux démarrer le suivi.");
            } else {
                sendStatus(false, "Autorisation GPS refusée. Le suivi GPS reste désactivé.");
            }
        }
    }

    @Override
    public void onBackPressed() {
        if (webView != null && webView.canGoBack()) webView.goBack();
        else super.onBackPressed();
    }

    @Override
    protected void onPause() {
        super.onPause();
        // Le suivi est volontairement arrêté en arrière-plan dans cette première version.
        // Un service de premier plan dédié sera nécessaire pour le suivi écran éteint.
        stopGps();
    }

    @Override
    protected void onSaveInstanceState(Bundle outState) {
        if (webView != null) webView.saveState(outState);
        super.onSaveInstanceState(outState);
    }

    @Override
    protected void onDestroy() {
        stopGps();
        if (webView != null) {
            webView.removeJavascriptInterface("AndroidGPS");
            webView.destroy();
            webView = null;
        }
        super.onDestroy();
    }
}