# Mackodi v1.0.0 – Firestick Lite Kodi Build (Convention over Configuration)

## Objective

Build **Mackodi**, a minimal, performance-first Kodi configuration and installer designed for **Amazon Firestick Lite**, using **convention over configuration**.

Mackodi should:
- Be fast and stable on low-RAM hardware
- Be “dad-proof” (predictable UI, no tweaking required)
- Focus on Movies / TV as primary use
- Include YouTube as a first-class citizen (no need to exit Kodi)
- Support occasional UK football (sports) use
- Avoid heavy skins, widgets, and maintenance gimmicks
- Be reproducible, versioned, and remotely installable via repo/installer
- Be add-on-first (Home items open add-ons, not Library views)

This is not a flashy Kodi build — it is an engineered baseline.

---

## Target Environment

- **Device:** Amazon Firestick Lite (primary target)
- **Future:** Must scale cleanly to Firestick 4K / 4K Max later
- **Kodi Version:** Kodi 21.x (Omega)
- **Development Platform:** macOS (golden master build)
- **Distribution:** GitHub Pages–hosted Kodi repo + installer

---

## Design Principles (Non-Negotiable)

- Convention over configuration
- Performance > visuals
- Estuary base or a lightweight Family Launcher skin (no heavy skins)
- No animated widgets
- No background services unless essential
- Minimal addon surface area
- One obvious way to do things
- Stability beats freshness

---

## Mackodi Home Menu Contract (Fixed API)

The following home menu must exist and remain stable:

Home
├── Movies
├── TV Shows
├── YouTube
├── Sports
├── Search
├── Downloads
└── Settings


Rules:
- No sub-menus on Home
- No widget rows
- No hidden sections
- All navigation reachable in ≤2 clicks
- Items open add-ons directly (not Library views)

---

## Addon Strategy

### Core Streaming (Real Debrid)

> Configure once, auto-play by default, no source selection dialogs.

Primary:
- Fen Light

Secondary (fallback only):
- Umbrella

Rules:
- Max 2 streaming addons
- Auto-play enabled
- Source selection disabled
- Default resolution capped appropriately for Firestick Lite
- Large torrent packs disabled
- Real Debrid pre-configured

---

### YouTube

- Official YouTube addon
- API keys configured
- Account signed in during golden master setup
- Exposed directly on Home menu
- No requirement to exit Kodi to Fire TV UI

---

### Sports (UK Football)

- One sports addon only (e.g. Mad Titan Sports or equivalent)
- Lives under Home → Sports
- Treated as “best effort”, not guaranteed
- No IPTV clutter unless explicitly required

---

### Utilities (Minimal)

Allowed:
- a4kSubtitles (or equivalent)
- Real Debrid resolver
- Trakt (optional; not mandatory)

Explicitly excluded:
- Cleaners
- Maintenance tools
- Cache wipers
- Log uploaders
- Skin helpers
- “Performance boost” addons

---

## Kodi Core Configuration

### Skin & UI
- Skin: Estuary base or Family Launcher (if implemented)
- RSS feed disabled
- Unused home sections removed
- No background animations

### Playback
- Adjust display refresh rate: On start/stop
- Hardware acceleration enabled
- Resume playback enabled

### Services
Disable unless required:
- UPnP
- Zeroconf
- AirPlay
- Remote control services

---

## Family Launcher Skin (Omega) Workstream

Goal: a clean, dark, add-on-first launcher skin with large tiles for family use.

### Scope
- Fork Estuary into `skin.family.launcher` (lightweight only)
- Home tiles: Movies, TV Shows, Sport, YouTube, Settings
- Add-on-first navigation (no Library dependency)
- Optional Admin mode for maintenance tasks

### Add-on wiring (configurable IDs)
- Movies/TV primary: `plugin.video.fenlight`
- Movies/TV backup: `plugin.video.umbrella`
- Sport primary: `plugin.video.madtitansports`
- Sport backup: `plugin.video.theloop`
- YouTube: `plugin.video.youtube`

### Behavior
- Normal click opens primary add-on root
- Long-press opens backup add-on (if supported)
- Missing add-on shows friendly dialog (no error spam)

### Skin settings (editable in UI)
- Admin mode toggle
- Text settings for add-on IDs (primary/backup per section)
- Splash toggle

### Admin screen (only visible when Admin mode is ON)
- Add-ons browser
- File manager
- System settings
- Skin settings shortcut

### Visual requirements
- Dark theme, minimal animation, no widgets
- Large tiles and labels (TV distance)
- Clear focus state

### Splash (optional)
- Simple splash window with crest image
- 1–2s delay then Home
- Toggleable in Skin Settings

Acceptance:
- Skin selectable and stable on Kodi Omega
- Home loads instantly; navigation is snappy
- Tiles open primary add-ons; long-press opens backup
- Missing add-ons show friendly dialog
- Admin mode hides maintenance options by default

---

## Performance Configuration

Create and ship an `advancedsettings.xml` tuned for Firestick Lite:

Goals:
- Conservative memory usage
- Avoid aggressive caching
- Smooth Real Debrid playback
- No assumptions of high RAM or fast storage

Treat this file as a first-class Mackodi artefact, not optional tuning.

---

## Build Workflow (Golden Master)

1. Install fresh Kodi on macOS
2. Apply all Mackodi Kodi settings
3. If using Family Launcher, install and set the skin
4. Install and configure all addons
5. Authenticate Real Debrid and YouTube
6. Configure addon defaults (auto-play, limits, etc.)
7. Build and test full UX:
   - Cold start
   - Search → play
   - Resume playback
   - YouTube navigation
8. Freeze configuration
9. Export **minimal userdata only**

Exclude:
- Personal libraries
- Databases
- Logs
- Thumbnails cache

---

## Packaging Strategy

### Versioning
- Name: Mackodi
- Version: `v1.0.0`
- Codename: “Lite Baseline”
- Semantic versioning required
- No auto-updates without intent

### Distribution Options
Implement one:

**Option A (Preferred):**
- Lightweight “Mackodi Installer” addon
- Copies userdata + settings into place
- Prompts for restart
- No wizard UI bloat

**Option B:**
- Traditional wizard-style installer
- Only if Option A is not viable

---

## Repository Structure (Target)

mackodi/
├── repo/
│ └── repositorcy.makodi.zip
├── installer/
│ └── plugin.progracm.makodi.installer
├── skin/
│ └── skin.family.launcher/
├── skin-zips/
│ └── skin.family.launcher-1.0.0.zip
├── userdata/
│ ├── advancedsettings.xml
│ ├── guisettings.xml
│ └── favourites.xml
├── build.json
├── README.md
└── CHANGELOG.md


---

## README Requirements

The README must:
- Explain Mackodi philosophy
- List what is included and excluded
- Provide 5-step install instructions for non-technical users
- State supported devices
- State update philosophy (“stable, not constant updates”)

---

## Non-Goals (Explicit)

Mackodi v1.0.0 will NOT:
- Compete with flashy Kodi builds
- Support 20+ addons
- Include heavy/complex skins or widget frameworks
- Include maintenance scripts
- Auto-update everything
- Require weekly rebuilds

---

## Success Criteria

Mackodi v1.0.0 is complete when:
- Runs smoothly on Firestick Lite
- A non-technical user can install it remotely
- Movies / TV / YouTube are one click away and open add-ons directly
- Sports works when needed without clutter
- No part of the UI feels slow or confusing
- Updates are intentional, not reactive

---

## Stretch Goals (Post-v1)

- Firestick 4K / 4K Max profile variant
- Optional Trakt-enabled build
- Optional IPTV-focused variant
- Rollback support (v1.0.x → v1.0.y)
- Automated repo publishing via CI
