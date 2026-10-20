# STATE — quick load

**Full detail:** `00-context-handoff.md` (authoritative). This file is the cheat sheet.

## Deliverable (current)
`index.html` — single self-contained file, two tabs:
1. **The report** (14 sections) — narrative + RICE + metric + business + prototype notes
2. **Prototype** — clickable, real SmartLead shell, Today vs Proposed mode, live run-log, memory drawer, undo

No external assets; safe in the sandboxed preview and as a standalone emailed file.

## Report structure (as built — client's outline, verbatim)
Cover (Akshay & Iknoor / Oct 2026 / Ashish Pathak / PM — Smart Assistant)
01 The Wall · 02 Our Users (Operator + Novice) · 03 The Product Today · 04 The Core Problem (5 symptoms
+ deprioritised STT) · 05 Prioritization (RICE 36/32/30/20/14) · 06 Strategic Clarity (3 principles,
4 refusals) · 07 The Wedge Moment (comparison table + flow + terminal card) · 08 6-Month Roadmap
(3 phases) · 09 Success Metrics · 10 Business & Pricing (competitor table) · 11 Validation Plan
(5 assumptions) · 12 UI Prototype Direction (3 screens) · 13 Closing

## Editing layer
- **✎ Edit** in top bar (or ⌘/Ctrl+E) makes `#reportRoot` contenteditable — click any text, type.
- Autosaves to `localStorage` key `sa_report_edits_v1`; restores on reload ("Your earlier edits were restored").
- **⤓ Save .html** downloads a clean copy: editor UI stripped, edits baked in, read-only.
- **⎙ PDF** → print stylesheet (also the way to get a PDF out of a sandboxed preview).
- **Reset all edits** — two-step confirm (native confirm() is blocked in sandboxed iframes).
- Prototype tab is intentionally NOT editable — the report is. Reload note: exported copy always
  opens on The report; the Prototype tab is still intact inside it.

## Signals — where they live (implicit, never lectured)
1. Problem framing → 04, in user voice + cost per pain
2. Strategic clarity → 08 (3 principles + "what it is not" table)
3. Scope discipline → 09 (cut lists, exit criteria) + 06 (interleave argument)
4. Wedge insight → 07 (beat-by-beat 90s; "the Undo is the feeling")
5. Success metric → 10 (executed-task rate, 0→20→35, guardrails, falsification test)
6. Business mindset → 11 (meter not gate, memory as non-exportable moat, positioning, brand risk)
7. The surprise → 12 (silent failures / guide = negative value)

## Decisions the report defends (don't dilute)
- Brief's "adoption problem" framing is a **category error** → argued in 05, earns the pushback credit.
- STT ranked 5th on purpose; **annoyance ≠ cost** — explicit, deliberate disagreement with own list.
- Memory ranks 3rd on RICE, ships 2nd — **interaction effects overrule the formula, said out loud**.
- Account-context loss scored 18 @ 0.4 confidence → **week-1 investigation, not a roadmap line**.
- Proactivity scores 0 on RICE → named as a framework limitation, not hidden.

## Figma export (added)
`build_figma.py` is the single source of truth: one spec -> three outputs, so the Figma
file and the clickable prototype never drift.
- `figma/*.svg` - 5 frames at 1280x800; drag into Figma, text stays editable
- `figma-plugin/` - manifest + code.js; builds named frames, SA/ colour styles, real text layers
- `figma/index.html` - contact sheet, all 5 frames side by side (inline SVG, offline safe)
- `smart-assistant-figma-frames.zip` - everything above, for download
- `figma/README.md` - import steps + colour tokens
- `png/*.png` - 1x (1280x800) and `@2x` (2560x1600) renders, Chromium-accurate
- `png/00-all-frames.png` - captioned contact sheet, all 5 frames
- `PROJECT-README.md` - package guide: how to open, edit, import into Figma, regenerate
Regenerate: `python3 build_figma.py`

## Whole-project download
`/home/user/smartlead-smart-assistant-project.zip` - the entire folder (report, prototype,
PNGs, SVGs, plugin, builder, docs). Nested zips were removed from inside it to avoid duplication.

## Asset status
| File | Status |
|---|---|
| `00-context-handoff.md` | authored context, verbatim |
| `index.html` | built, browser-tested (Chromium) |
| deck outline | not built |
| Loom script | not built |
| PDF export | not built — print CSS exists, browser Print → PDF works |

## Next-step menu
(a) deck outline from this report · (b) Loom script · (c) skeptical-founder pressure test ·
(d) tighten any section · (e) PDF / docx export
