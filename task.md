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

This is not a flashy Kodi build — it is an engineered baseline.

---

## Target Environment

- **Device:** Amazon Firestick Lite (primary target)
- **Future:** Must scale cleanly to Firestick 4K / 4K Max later
- **Kodi Version:** Kodi 20.x (Nexus) OR 21.x (Omega) — choose one and standardise
- **Development Platform:** macOS (golden master build)
- **Distribution:** GitHub Pages–hosted Kodi repo + installer

---

## Design Principles (Non-Negotiable)

- Convention over configuration
- Performance > visuals
- Estuary skin only (no custom skins in v1)
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
- Skin: Estuary
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
3. Install and configure all addons
4. Authenticate Real Debrid and YouTube
5. Configure addon defaults (auto-play, limits, etc.)
6. Build and test full UX:
   - Cold start
   - Search → play
   - Resume playback
   - YouTube navigation
7. Freeze configuration
8. Export **minimal userdata only**

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
- Include custom skins
- Include maintenance scripts
- Auto-update everything
- Require weekly rebuilds

---

## Success Criteria

Mackodi v1.0.0 is complete when:
- Runs smoothly on Firestick Lite
- A non-technical user can install it remotely
- Movies / TV / YouTube are one click away
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
