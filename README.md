# Mackodi

**The "boring" Kodi build for Amazon Firestick Lite.**

Mackodi is a minimal, performance-first configuration designed to be stable, fast, and predictable. It is not flashy. It does not have animated widgets. It just plays movies and TV shows.

## What is Mackodi?

Mackodi is a pre-configured Kodi setup that takes the hassle out of setting up streaming addons. Instead of spending hours installing and configuring multiple addons, you run one installer and get a complete, optimized setup.

**Key Features:**
- **Pre-configured Addons:** Fen Light (primary), Umbrella (backup), YouTube, Mad Titan Sports, and a4kSubtitles
- **Performance Tuned:** Optimized `advancedsettings.xml` for Firestick Lite's 1GB RAM
- **Launcher Skin:** 5 large tiles (Movies, TV Shows, Sport, YouTube, Settings), no widgets
- **Custom Splash Screen:** Uses the Mackodi logo on a plain dark screen
- **Real Debrid Ready:** Pre-configured for premium streaming (you just need to authorize)

## Supported Devices
- **Primary:** Amazon Firestick Lite (1GB RAM)
- **Also Works:** Firestick 4K, Firestick 4K Max, Android TV boxes
- **Kodi Version:** 21.x (Omega) recommended

## Prerequisites

Before installing Mackodi, you need:

1. **A Real-Debrid account** (required for movie/TV streaming) - Sign up at https://real-debrid.com/
2. **Kodi 21 (Omega)** installed on your device
3. **Unknown Sources enabled** in Kodi settings

## Installation Steps

### Step 1: Prepare Your Device
1. On your Firestick/Android device, go to **Settings > My Fire TV > Developer Options**
2. Enable **Apps from Unknown Sources**
3. Install Kodi 21 (Omega) from the Downloader app or Google Play Store

### Step 2: Add the Mackodi Source
1. Open Kodi
2. Go to **Settings (gear icon) > File Manager > Add Source**
3. Click **<None>** and enter: `https://mcdonald-conor.github.io/mackodi/repo`
4. Name it: `.mackodi` (the dot makes it appear at the top)
5. Click **OK**

### Step 3: Install the Mackodi Repository
1. Go to **Add-ons > Install from zip file**
2. If prompted, allow unknown sources
3. Select **.mackodi**
4. Click on **repository.mackodi-1.0.0.zip**
5. Wait for the "Add-on installed" notification

### Step 4: Install the Mackodi Installer
1. Go to **Add-ons > Install from repository**
2. Select **Mackodi Repository**
3. Go to **Program add-ons**
4. Click **Mackodi Installer** and install

### Step 5: Run the Installer
1. Go to **Add-ons > Program add-ons > Mackodi Installer**
2. Click **Run**
3. Click **Yes** to confirm installation
4. Wait for the installation to complete (this downloads and installs all addons)
5. When finished, you'll see "Installation complete - PLEASE FORCE CLOSE KODI NOW"
6. **Force close Kodi** (don't just exit - fully close the app)
7. Reopen Kodi

### Step 6: Authorize Real-Debrid (REQUIRED)
**IMPORTANT:** While Mackodi copies over addon settings, Real-Debrid authorization is device-specific and must be done manually.

**For Fen Light (Primary):**
1. Open Fen Light addon
2. Go to **Tools > Accounts > Real-Debrid > Authorize**
3. Note the code displayed on screen
4. On your phone/computer, go to: `https://real-debrid.com/device`
5. Enter the code
6. Return to Kodi - you should see "Real-Debrid Authorized"

**For Umbrella (Backup):**
1. Open Umbrella addon  
2. Go to **Tools > Settings > Accounts > Real-Debrid**
3. Click **Authorize**
4. Follow the same process as above

**Without Real-Debrid authorization, you won't get any movie or TV show links!**

## Post-Installation Setup

### Family Launcher Skin
The installer applies the Mackodi launcher skin automatically.

If the skin does not load for any reason:
1. Install `skin.mackodi-1.0.0.zip` from the same source
2. Go to **Settings > Interface > Skin** and select **Mackodi**
3. Open **Skin Settings** and set add-on IDs if yours differ

**Splash logo:** The splash uses `media/logo.png` inside the skin folder. Replace it and re-zip if you want a different logo.

### YouTube Setup (Optional)
If you want to use your YouTube account:
1. Go to **Add-ons > Video add-ons > YouTube**
2. Sign in with your Google account when prompted
3. Or use the default settings for no-login YouTube browsing

### Sports Setup
Mad Titan Sports and The Loop are pre-installed for UK football streaming. Just open them from the Sports section on the home menu.

If streams require Real-Debrid authorization, open **ResolveURL** settings and authorize Real-Debrid there as well.

### Subtitles
a4kSubtitles is pre-installed and will automatically search for subtitles when you play content. No configuration needed.

## What's Included

**Movies & TV:**
- Fen Light (primary streaming addon)
- Umbrella (backup streaming addon)
- CocoScrapers (source scrapers)
- a4kSubtitles (subtitle downloader)

**Sports:**
- Mad Titan Sports
- The Loop

**Other:**
- YouTube
- Family Launcher skin
- Custom splash screen
- Performance-tuned advancedsettings.xml
- Pre-configured addon settings (quality limits, auto-play enabled)

## What's NOT Included

- No maintenance tools or "cleaners"
- No widgets or animated menus
- No IPTV (unless using sports addons)
- No 4K support (Firestick Lite can't handle it)

## Troubleshooting

**"No streams available"**
→ You haven't authorized Real-Debrid. See Step 5 above.

**Kodi crashes on startup**
→ You didn't force-close Kodi after installation. Fully close and reopen.

**Addons don't appear**
→ Wait a few minutes after installation for Kodi to index all addons. If still missing, restart Kodi.

**Buffering issues**
→ Check your internet connection. Mackodi is optimized for 1080p streaming. If you're trying to play 4K content, it will likely crash.

## Update Philosophy

Mackodi is designed to be **stable**, not constantly updated. We only release updates when:
- An addon completely stops working
- A critical security issue is found
- Kodi compatibility is broken

Don't expect weekly updates. This build is meant to "just work" for months at a time.

## Support

This is a personal project. Support is limited to:
- Checking the GitHub issues page: https://github.com/mcdonald-conor/mackodi/issues
- Basic troubleshooting questions

**We cannot help with:**
- Real-Debrid account issues (contact Real-Debrid)
- Content availability (we don't control what shows are available)
- Illegal streaming questions

## Disclaimer

Mackodi is a configuration tool for Kodi. We do not host, stream, or distribute any content. All streaming is done through third-party addons and services. You are responsible for complying with your local laws regarding content streaming.

---

**Version:** 1.0.0 "Lite Baseline"  
**Built for:** Amazon Firestick Lite  
**Kodi Version:** 21.x (Omega)
