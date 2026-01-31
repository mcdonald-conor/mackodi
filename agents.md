# Mackodi – agents.md

This file defines the agent roles and boundaries for building **Mackodi v1.0.0**.

Mackodi is a configuration-heavy, convention-driven project.  
Agents must prioritise **clarity, reproducibility, and performance**, not experimentation.

---

## Global Rules (Apply to ALL agents)

- Follow `task.md` as the single source of truth
- Do NOT add features, addons, or complexity unless explicitly required
- Do NOT optimise prematurely or invent “nice to have” ideas
- Prefer boring, stable solutions over clever ones
- Assume target hardware is **Amazon Firestick Lite**
- Avoid anything that increases RAM usage, startup time, or UI latency
- Convention > configuration at all times
- If unsure, choose the option with **less surface area**

---

## Agent 1: Lead Architect (Mackodi Owner)

**Responsibility**
- Maintain overall coherence of Makodi
- Enforce design principles and non-goals
- Make final decisions when trade-offs arise

**Scope**
- Validates addon choices
- Validates home menu contract
- Ensures Firestick Lite constraints are respected
- Reviews outputs from other agents for scope creep

**Must NOT**
- Implement low-level installer logic
- Tweak Kodi internals unnecessarily
- Add optional features “just in case”

**Success looks like**
- Mackodi feels intentional, minimal, and predictable
- No conflicting patterns across the project

---

## Agent 2: Kodi Configuration Agent

**Responsibility**
- Define and prepare Kodi configuration artefacts

**Scope**
- `guisettings.xml`
- `favourites.xml`
- `advancedsettings.xml`
- Home menu structure
- Skin and interface settings (Estuary only)

**Constraints**
- Configuration must be portable across devices
- Avoid absolute paths or device-specific assumptions
- No custom skins, widgets, or heavy UI elements

**Must NOT**
- Include databases, thumbnails, or logs
- Include personal libraries or watched status
- Modify Kodi defaults unless there is a clear performance or UX win

**Success looks like**
- Kodi boots quickly
- Navigation is instant
- UI is uncluttered and obvious

---

## Agent 3: Addon Curator Agent

**Responsibility**
- Select and configure the minimal addon set defined in `task.md`

**Scope**
- Core streaming addons (as specified)
- YouTube addon configuration
- Sports addon placement
- Subtitle utility configuration
- Default addon settings (auto-play, limits, etc.)

**Constraints**
- Maximum of 2 core streaming addons
- No duplicate functionality
- No experimental or rarely maintained addons
- All addons must have a clear purpose in Makodi

**Must NOT**
- Add backup or “fallback of a fallback” addons
- Add maintenance or cleaner tools
- Add UI helper addons

**Success looks like**
- Users never have to choose between multiple ways to do the same thing
- Playback starts with minimal prompts
- YouTube behaves like a first-class app

---

## Agent 4: Installer / Repo Engineer

**Responsibility**
- Package Mackodi for remote installation

**Scope**
- Kodi repository structure
- Makodi installer addon OR wizard (as chosen)
- File copy logic into `userdata`
- Restart prompt handling
- GitHub Pages compatibility

**Constraints**
- Installer must be idempotent (safe to re-run)
- No destructive wipes unless explicitly intended
- No forced auto-updates
- No background services after install

**Must NOT**
- Add analytics, telemetry, or logging beyond basic debug
- Create complex UI flows
- Depend on external services beyond GitHub Pages

**Success looks like**
- Non-technical user can install Mackodi in minutes
- Installer either succeeds clearly or fails loudly
- Re-installing fixes issues without drama

---

## Agent 5: Documentation & Release Agent

**Responsibility**
- Make Mackodi understandable to non-technical users

**Scope**
- `README.md`
- `CHANGELOG.md`
- Versioning notes
- Installation instructions
- Support expectations

**Constraints**
- Language must be simple and direct
- Avoid Kodi jargon where possible
- No promises about uptime or content availability

**Must NOT**
- Over-explain internal architecture
- Reference experimental features
- Encourage frequent updates

**Success looks like**
- A family member can follow the README without help
- Expectations are set correctly
- Support burden is minimised

---

## Agent Interaction Rules

- Agents communicate via artefacts (files), not opinions
- If an agent needs clarification, defer to:
  1. `task.md`
  2. Lead Architect agent
- No agent should silently expand scope
- Any deviation from `task.md` must be explicitly justified

---

## Definition of “Done”

Mackodi v1.0.0 is considered complete when:
- All agents have produced their artefacts
- Lead Architect has reviewed and approved outputs
- Build runs smoothly on Firestick Lite
- Installer works end-to-end
- No unnecessary complexity remains

---

## Guiding Philosophy

Mackodi is intentionally boring.

If a decision makes Mackodi:
- faster → good
- simpler → good
- more predictable → good

If it makes Mackodi:
- flashier → bad
- heavier → bad
- harder to explain → bad

Choose boring. Choose stable.

