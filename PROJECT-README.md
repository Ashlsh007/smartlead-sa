# Smart Assistant — From Guide to Execution Layer

Complete project package: the written report, the clickable prototype, the Figma-ready
design frames, and the generator that keeps them in sync.

Prepared for **Akshay & Iknoor, SmartLead AI** · **Ashish Pathak** · October 2026

---

## Start here

**`index.html`** — open this first. Everything is in it.

- **The report** tab: all 13 sections, in the final order (The Wall → Closing)
- **Prototype** tab: the clickable prototype in the real SmartLead shell

It is fully self-contained. No internet, no build step, no dependencies — double-click it
and it runs. You can email it as a single attachment.

### Editing the report
Three buttons in the top bar:

| Button | What it does |
|---|---|
| **✎ Edit** (⌘/Ctrl + E) | Click any text in the report and rewrite it. Autosaves to your browser. |
| **⤓ Save .html** (⌘/Ctrl + S) | Downloads a clean copy with your edits baked in and the editing UI removed. |
| **⎙ PDF** | Opens the print dialog — use "Save as PDF" for a shareable file. |

**Reset all edits** in the yellow edit bar wipes your changes and restores the original.

Note: edits live in the browser's local storage (per browser, per machine). When you're
happy with a version, use **Save .html** to make it permanent.

### Driving the prototype
- Switch **Today / Proposed** in the chat header to see the same request answered both ways
- Click **📎** or the *Import a lead list* chip to run the full import
- Expand any step in the run-log, then press **Undo Import**
- Click **✦ Memory** for the workspace-scoped memory drawer
- Try all four chips: import · create campaign · check deliverability · set up an agent

---

## What's in the package

```
smartlead-sa/
├── index.html                    ← THE DELIVERABLE: report + clickable prototype
├── PROJECT-README.md             ← this file
├── 00-context-handoff.md         ← original brief, observations and locked decisions
├── STATE.md                      ← working brief: what's built, what isn't
│
├── png/                          ← every frame as an image
│   ├── 00-all-frames.png         ← captioned contact sheet, all 5
│   ├── 01-05 *.png               ← 1280 × 800
│   └── 01-05 *@2x.png            ← 2560 × 1600 (slides, retina, print)
│
├── figma/                        ← drag-and-drop Figma frames
│   ├── 01-composer--drop-zone.svg
│   ├── 02-live-run-log-in-progress.svg
│   ├── 03-live-run-log-terminal-state.svg
│   ├── 04-memory-panel.svg
│   ├── 05-today-the-guide-response-before.svg
│   ├── index.html                ← contact sheet with the SVGs inlined
│   └── README.md                 ← Figma import instructions
│
├── figma-plugin/                 ← rebuild the frames as native Figma layers
│   ├── manifest.json
│   └── code.js
│
└── build_figma.py                ← the single source of truth for the design frames
```

### The five design frames

| # | Frame | What it proves |
|---|---|---|
| 01 | Composer & drop zone | A file is a first-class object — the composer invites work, not questions |
| 02 | Run-log, in progress | Execution as evidence: ✓ done · ● active · ○ pending |
| 03 | Run-log, terminal state | Proof, not a promise — Undo sits next to the result |
| 04 | Memory panel | Visible, editable, deletable — scoped to one client workspace |
| 05 | Today — the guide response | The same request, answered with instructions. 0 account changes. |

**For the deck:** frame 03 next to frame 05 is the most persuasive pairing — the product
doing the work, beside the product explaining the work.

---

## Getting the frames into Figma

**Option A — drag and drop.** Open Figma and drag any `.svg` from `figma/` onto the canvas.
Text arrives as editable text layers, shapes as real rectangles and vectors, layer names intact.

**Option B — the plugin (best fidelity).** In Figma:
**Plugins → Development → Import plugin from manifest…** → select `figma-plugin/manifest.json`
→ run **Smart Assistant — Prototype Builder**.

It builds a page with five named frames and colour styles under `SA/`
(`SA/indigo`, `SA/purple`, `SA/lav`, `SA/ok`, `SA/danger`) for global recolouring.

---

## Regenerating after a change

The SVG frames, the plugin and the contact sheet are all generated from one Python file:

```bash
cd smartlead-sa
python3 build_figma.py
```

Change a number or a colour once in `build_figma.py` and every output updates together —
no drift between the report, the prototype and the Figma file.

The PNG renders were produced by opening each SVG in headless Chromium at 2× and
screenshotting at 2560 × 1600 (ImageMagick renders these SVGs inaccurately — it drops the
checkmarks and breaks the fonts). If you regenerate the SVGs, re-shoot the PNGs rather
than converting with ImageMagick.

---

## Design tokens

| Token | Hex | Use |
|---|---|---|
| Shell | `#1b1b6b` | Top bar, scope badge |
| Action | `#6c5ce7` | Primary buttons, active states, send |
| Active nav | `#efecff` | Selected nav item background |
| Track | `#f7f5ff` | Chips, secondary surfaces |
| Warning | `#fff8e1` | Caution panels, edit bar |
| Success | `#0e9d5c` | Completed steps, terminal state |
| Danger | `#d92d20` | Undo, destructive affordances |
| Ink | `#14142b` | Primary text |

Typeface: **Inter** (system fallback stack in the HTML). 1280 × 800 frames.

---

## One caveat

The prototype is a faithful mid-fidelity simulation — every state change is simulated in
the page, and nothing is sent anywhere. It is built to make the argument legible, not to
be wired to a real API.
