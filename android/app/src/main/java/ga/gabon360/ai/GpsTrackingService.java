package ga.gabon360.ai;

import android.Manifest;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Build;
import android.os.Bundle;
import android.os.IBinder;

import androidx.core.app.NotificationCompat;

public class GpsTrackingService extends Service {
    public static final String ACTION_LOCATION = "ga.gabon360.ai.ACTION_GPS_LOCATION";
    private static final String CHANNEL_ID = "g360_field_gps";
    private static final int NOTIFICATION_ID = 3601;
    private LocationManager locationManager;
    private LocationListener listener;

    @Override
    public void onCreate() {
        super.onCreate();
        createNotificationChannel();
        startForeground(NOTIFICATION_ID, buildNotification("En attente de la première position GPS…"));
    }

    private void createNotificationChannel() {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                CHANNEL_ID, "Suivi GPS des patrouilles", NotificationManager.IMPORTANCE_LOW
            );
            channel.setDescription("Indique que le GPS de patrouille GABON 360 AI est actif.");
            NotificationManager manager = getSystemService(NotificationManager.class);
            if (manager != null) manager.createNotificationChannel(channel);
        }
    }

    private Notification buildNotification(String message) {
        Intent openApp = new Intent(this, MainActivity.class);
        PendingIntent pending = PendingIntent.getActivity(
            this, 3601, openApp,
            PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE
        );
        return new NotificationCompat.Builder(this, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.ic_menu_mylocation)
            .setContentTitle("GABON 360 AI — Patrouille GPS")
            .setContentText(message)
            .setContentIntent(pending)
            .setOngoing(true)
            .setOnlyAlertOnce(true)
            .setCategory(NotificationCompat.CATEGORY_SERVICE)
            .build();
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (checkSelfPermission(Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED
            && checkSelfPermission(Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            stopSelf();
            return START_NOT_STICKY;
        }
        try {
            locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
            if (locationManager == null || !locationManager.isProviderEnabled(LocationManager.GPS_PROVIDER)) {
                stopSelf();
                return START_NOT_STICKY;
            }
            if (listener == null) {
                listener = new LocationListener() {
                    @Override public void onLocationChanged(Location location) {
                        Intent update = new Intent(ACTION_LOCATION);
                        update.setPackage(getPackageName());
                        update.putExtra("location", location);
                        sendBroadcast(update);
                        NotificationManager manager = getSystemService(NotificationManager.class);
                        if (manager != null) manager.notify(NOTIFICATION_ID,
                            buildNotification("Position reçue — précision "
                                + (location.hasAccuracy() ? Math.round(location.getAccuracy()) + " m" : "inconnue")));
                    }
                    @Override public void onProviderEnabled(String provider) { }
                    @Override public void onProviderDisabled(String provider) { stopSelf(); }
                    @Override public void onStatusChanged(String provider, int status, Bundle extras) { }
                };
            }
            locationManager.removeUpdates(listener);
            locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000L, 2.0f, listener);
        } catch (SecurityException error) {
            stopSelf();
            return START_NOT_STICKY;
        } catch (Exception error) {
            stopSelf();
            return START_NOT_STICKY;
        }
        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        if (locationManager != null && listener != null) {
            try { locationManager.removeUpdates(listener); }
            catch (SecurityException ignored) { }
        }
        stopForeground(true);
        super.onDestroy();
    }

    @Override
    public IBinder onBind(Intent intent) { return null; }
}
