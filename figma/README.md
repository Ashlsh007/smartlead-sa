# Figma design file — Smart Assistant prototype

Five frames, built from `build_figma.py` so the design and the clickable HTML prototype
never drift apart. 1280 × 800, Inter, SmartLead palette.

| Frame | What it proves |
|---|---|
| `01-composer--drop-zone.svg` | A file is a first-class object in the composer |
| `02-live-run-log-in-progress.svg` | Execution shown step by step — done / active / pending |
| `03-live-run-log-terminal-state.svg` | Terminal proof: counts, skipped rows, Undo next to the result |
| `04-memory-panel.svg` | Memory visible, editable, scoped to one client workspace |
| `05-today-the-guide-response-before.svg` | The "here are the steps" answer, for the before/after comparison |

## Option A — drag and drop (fastest)
Open Figma → drag any `.svg` from this folder onto the canvas.
Text arrives as **editable Figma text layers**, shapes as real rectangles/vectors,
and every layer keeps its name (`Run-log / step / done`, `Button / undo`, `Memory card / ICP`…).

## Option B — rebuild as native layers with the plugin (best fidelity)
1. Figma → **Plugins → Development → Import plugin from manifest…**
2. Select `figma-plugin/manifest.json`
3. Run **Smart Assistant — Prototype Builder**

It creates a page called *Smart Assistant — Prototype* with five named, auto-laid-out
frames spaced 80px apart, plus colour styles under **SA/** (`SA/indigo`, `SA/purple`,
`SA/lav`, `SA/ok`, `SA/danger` …) so fills can be swapped globally.

## Notes
- Everything is static — for interaction, use `index.html` (the clickable prototype) and
  mirror the states into Figma prototype links.
- Colours: `#1b1b6b` shell · `#6c5ce7` action · `#efecff` active nav · `#fff8e1` warning.
- Regenerate after any change: `python3 build_figma.py`
