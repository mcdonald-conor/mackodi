# tasks.md — Family Launcher Skin (Add-on-first, Nexus)

## Goal
Create a clean, fast, dark Kodi skin acting as a launcher:
Home tiles: Movies, TV Shows, Sport, YouTube, Settings.
Add-on-first: tiles open the chosen add-ons directly.
Target: Kodi Nexus 20.x (Firestick-class performance).

Primary/backup add-ons:
- Movies + TV: Primary = Fen Light AM, Backup = Umbrella
- Sport: Primary = Mad Titan Sports, Backup = The Loop
- YouTube: official YouTube addon

## Hard requirements
- Dark theme, minimal animation, no widgets, no heavy background rotations
- Large tiles and labels (family TV distance)
- Always “back” returns to Home
- Friendly missing-addon messages (no Kodi error spam)
- Optional “Admin mode” for Conor

---

## Task 1 — Fork Estuary into a new lightweight skin
- Copy skin.estuary → skin.family.launcher
- Update addon.xml:
  - id: skin.family.launcher
  - name: Family Launcher
  - version: 1.0.0
- Replace icon/fanart with minimal dark assets.

Acceptance:
- Skin selectable and stable on Kodi Nexus.

---

## Task 2 — Home screen: simple tile menu
Home shows 5 tiles:
1) Movies
2) TV Shows
3) Sport
4) YouTube
5) Settings

- Implement in 1080i/Home.xml (or Estuary equivalent).
- Remove widgets, “recently added”, recommendations, extra menus.

Acceptance:
- Home loads instantly; navigation is snappy.

---

## Task 3 — Add-on-first wiring with primary + backup and long-press behavior
### Default add-on IDs / plugin roots
(These must be editable in Skin Settings because IDs can vary.)

Movies/TV:
- Primary: plugin.video.fenlight  (Fen Light AM)  [confirmed by zip name]  :contentReference[oaicite:4]{index=4}
- Backup: plugin.video.umbrella   (Umbrella)      [treat as configurable] :contentReference[oaicite:5]{index=5}

Sport:
- Primary: (default guess) plugin.video.madtitansports  [configurable; repo is Magnetic] :contentReference[oaicite:6]{index=6}
- Backup: (default guess) plugin.video.theloop          [configurable; Loop repo] :contentReference[oaicite:7]{index=7}

YouTube:
- plugin.video.youtube

### Click actions
- Normal click:
  - Movies → open primary Movies add-on root
  - TV → open primary TV add-on root
  - Sport → open primary Sport add-on root
- Long-press / context click (if supported by Estuary base):
  - Movies long-press → open backup (Umbrella)
  - TV long-press → open backup (Umbrella)
  - Sport long-press → open backup (The Loop)

Implementation approach:
- Use Kodi built-ins with a “safe runner” pattern:
  - Prefer: ActivateWindow(Videos,plugin://<addonid>/,return)
  - Fallback: RunAddon(<addonid>)
- Before calling, check addon exists with:
  - System.HasAddon(<addonid>)
- If missing:
  - Dialog.OK("Not installed", "This section isn’t installed yet.", "Enable Admin mode to install it.")

Acceptance:
- Normal click opens the primary add-on.
- Long-press opens the backup add-on.
- Missing add-on shows friendly dialog.

---

## Task 4 — Skin Settings page (so Conor can tweak IDs without editing files)
Create 1080i/SkinSettings.xml:
- Toggle: Admin mode (on/off)
- Text setting: Movies addon id (default plugin.video.fenlight)
- Text setting: Movies backup addon id (default plugin.video.umbrella)
- Text setting: TV addon id (default plugin.video.fenlight)
- Text setting: TV backup addon id (default plugin.video.umbrella)
- Text setting: Sport addon id (default plugin.video.madtitansports)
- Text setting: Sport backup addon id (default plugin.video.theloop)
- Toggle: Splash enabled (on/off)

Store as skin strings:
- Skin.String(movies_addon_primary)
- Skin.String(movies_addon_backup)
- Skin.String(tv_addon_primary)
- Skin.String(tv_addon_backup)
- Skin.String(sport_addon_primary)
- Skin.String(sport_addon_backup)

Acceptance:
- Changing IDs works immediately after OK / reload skin.

---

## Task 5 — Admin screen (family can’t get lost)
Add an “Admin” entry that is ONLY visible when Admin mode is ON.
Admin screen provides:
- Add-ons browser (ActivateWindow(AddonBrowser))
- File manager (ActivateWindow(FileManager))
- System settings (ActivateWindow(Settings))
- Skin settings shortcut
- OPTIONAL helper: “Show installed video add-ons list”
  - Implement via a simple dialog that displays installed video addon IDs
  - If too hard in pure skin XML, provide a button that opens Add-ons > My add-ons > Video add-ons.

Acceptance:
- Family never sees Admin unless enabled.
- Conor can install/repair add-ons easily.

---

## Task 6 — Dark theme polish (minimal + modern)
- Reduce textures, remove noisy gradients.
- Clear focus state (subtle accent border or glow).
- Large fonts; clean icons.

Acceptance:
- Looks modern, consistent, and readable.

---

## Task 7 — Custom splash logo (family crest)
Implement a simple “fake splash” on startup:
- Dark background + centered family crest image.
- 1–2s delay then Home.
- Toggleable in Skin Settings.

Implementation:
- Add a Startup window XML (e.g., 1080i/Startup.xml).
- Use minimal autoexec.py (optional) to ActivateWindow(splash) then Home.
- Put crest in skin media: media/family_crest.png

Acceptance:
- Crest shows on boot, then tiles.
- No boot loops; if disabled, boot goes straight Home.

---

## Task 8 — Packaging
Deliver:
- skin folder: skin.family.launcher/
- install zip: skin.family.launcher-1.0.0.zip
- README:
  - how to install
  - how to set addon IDs
  - how to enable Admin mode
  - how to add/replace crest image

QA:
- Firestick: cold boot, open tiles fast, back returns home, no errors.

