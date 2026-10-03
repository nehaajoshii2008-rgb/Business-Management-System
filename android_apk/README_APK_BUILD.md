# 📱 ISBMS Android APK Creation & Distribution Guide

This guide explains how to generate a standalone **Android APK file (`ISBMS_v1.0.apk`)** that you can send directly to business owners via WhatsApp, Email, or USB drive—allowing them to install it on their Android smartphones without Google Play Store!

---

## ⚡ Method 1: Instant 1-Click APK Generator (Recommended)

1. **Deploy or Run ISBMS Server**:
   Ensure your ISBMS server is live on your network or cloud domain (e.g. `http://192.168.0.137:8000` or `https://your-domain.com`).

2. **Generate APK online**:
   - Go to **[PWABuilder.com](https://www.pwabuilder.com/)** or **[Web2App.com]**.
   - Enter your website URL.
   - Click **Generate Android Package (.apk)**.
   - Download the `ISBMS.apk` file directly to your computer!

3. **Distribute to Clients**:
   - Send the `.apk` file directly via **WhatsApp**, **Google Drive**, or **Email**.
   - On the client's Android phone: Tap the `.apk` file ➔ Select **Install** (Allow "Install from Unknown Sources").

---

## 🛠️ Method 2: Native Android Studio APK Project

We have included a pre-configured native Android wrapper project right inside your repository under `c:/Users/Admin/OneDrive/Documents/ISBMS/android_apk/`:

- [AndroidManifest.xml](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/android_apk/AndroidManifest.xml)
- [MainActivity.java](file:///c:/Users/Admin/OneDrive/Documents/ISBMS/android_apk/MainActivity.java)

### Steps to compile `.apk`:
1. Open **Android Studio**.
2. Select **Open Project** ➔ Choose `c:/Users/Admin/OneDrive/Documents/ISBMS/android_apk`.
3. In `MainActivity.java`, set `APP_URL` to your production server URL.
4. Click **Build** ➔ **Build Bundle(s) / APK(s)** ➔ **Build APK(s)**.
5. Android Studio will output `app-release.apk` in your build folder!

---

## 📲 Method 3: Direct Web PWA App Install (No APK needed)

Android phones allow installing the app directly from Chrome browser:
1. Open Chrome on the Android phone.
2. Go to `http://192.168.0.137:8000`.
3. Tap **⋮ Menu** ➔ **Add to Home Screen**.
4. Chrome creates an APK container on the phone instantly!
