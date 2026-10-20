#!/usr/bin/env python3
"""
Build Figma-importable design files for the Smart Assistant prototype.

One spec -> two outputs:
  figma/screen-*.svg          drag-and-drop into Figma (text becomes editable text layers)
  figma-plugin/code.js        Figma plugin that builds named frames, fills and text styles

Run:  python3 build_figma.py
"""
import json, os, textwrap

W, H = 1280, 800

C = dict(
    indigo="#1b1b6b", indigo2="#26268a", indigo3="#3a3aa8",
    purple="#6c5ce7", purple2="#8b74ee", purple3="#a897f5",
    lav="#efecff", lav2="#f7f5ff", lav3="#e4dfff",
    ink="#14142b", ink2="#494968", ink3="#7c7c99",
    line="#e7e5f2", line2="#f0eef8",
    bg="#fbfaff", white="#ffffff",
    warn="#fff8e1", warnline="#fdefc7", warnink="#7a5a00",
    ok="#0e9d5c", okbg="#e7f7ee",
    danger="#d92d20", dangerbg="#fdecea",
    muted="#a5a2bb", rail="#f7f6fc",
)

frames = []          # list of {name, ops}
ops = []             # scratch per frame

# ---------------------------------------------------------------- primitives
def rect(x, y, w, h, fill=None, r=0, stroke=None, sw=1, name="rect", opacity=1):
    ops.append(dict(t="rect", x=x, y=y, w=w, h=h, fill=fill, r=r,
                    stroke=stroke, sw=sw, name=name, o=opacity))

def circle(cx, cy, r, fill=None, stroke=None, sw=1, name="circle"):
    ops.append(dict(t="circle", cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, sw=sw, name=name))

def text(x, y, lines, size=13, wgt=400, c=None, lh=None, name=None, align="left", w=None, ls=0):
    if isinstance(lines, str):
        lines = [lines]
    lh = lh or round(size * 1.45, 1)
    ops.append(dict(t="text", x=x, y=y, lines=lines, s=size, wgt=wgt, c=c or C["ink"],
                    lh=lh, name=name or (lines[0][:34]), align=align, w=w, ls=ls))

def line(x1, y1, x2, y2, c=None, sw=1, name="divider"):
    ops.append(dict(t="line", x1=x1, y1=y1, x2=x2, y2=y2, c=c or C["line"], sw=sw, name=name))

def path(d, stroke=None, sw=1.6, fill=None, name="icon"):
    ops.append(dict(t="path", d=d, stroke=stroke, sw=sw, fill=fill, name=name))

def check(cx, cy, color=None, s=1.0):
    path(f"M {cx-3.2*s} {cy+0.2*s} L {cx-1.0*s} {cy+2.4*s} L {cx+3.4*s} {cy-2.4*s}",
         stroke=color or C["white"], sw=1.7 * s, name="check")

def spinner(cx, cy, r=4.2):
    path(f"M {cx} {cy-r} A {r} {r} 0 0 1 {cx+r} {cy}", stroke=C["purple"], sw=1.8, name="spinner")


def save(name):
    global ops
    frames.append(dict(name=name, w=W, h=H, ops=ops))
    ops = []

# ---------------------------------------------------------------- shell
NAV = [
    ("Engage", [("Prospect Finder", False), ("Campaigns", False), ("Master Inbox", False), ("Sender Accounts", False)]),
    ("AI Team", [("AI Assistant", True), ("AI Agents", False), ("Automations", False)]),
    ("Recents", [("Import · Q3 Enterprise", False), ("Reply rate drop · Acme", False)]),
    ("Inbox health", [("Sending Servers", False)]),
    ("Pipeline", [("Deals", False)]),
]

def rail():
    rect(0, 56, 56, H - 56, C["white"], name="Icon rail")
    line(56, 56, 56, H, C["line"])
    # icons
    for i, cy in enumerate([84, 124, 164, 204]):
        rect(21, cy - 6, 14, 12, C["lav3"], r=3, name="Rail icon")
    rect(15, 70, 26, 26, C["lav"], r=8, name="Rail icon / active bg")
    rect(23, 78, 10, 10, C["purple"], r=2.5, name="Rail icon / active")
    line(20, 232, 36, 232, C["line"])
    rect(21, 250, 14, 14, None, r=4, stroke=C["muted"], sw=1.4, name="Rail icon / gear")


def nav():
    rect(56, 56, 196, H - 56, "#fdfdff", name="Navigation")
    line(252, 56, 252, H, C["line"])
    y = 74
    for group, items in NAV:
        text(76, y, group.upper(), 9.5, 800, C["muted"], lh=12, ls=1.1, name="Group / " + group)
        y += 20
        for label, active in items:
            if active:
                rect(66, y - 5, 176, 28, C["lav"], r=8, name="Nav item / active bg")
                rect(78, y + 3, 9, 9, C["purple"], r=2, name="Nav icon")
                text(96, y + 2, label, 13, 700, "#3a1fc4", lh=18, name="Nav / " + label)
                y += 30
            else:
                rect(78, y + 4, 8, 8, None, r=2, stroke=C["muted"], sw=1.2, name="Nav icon")
                text(96, y + 2, label, 13, 500, C["ink2"], lh=18, name="Nav / " + label)
                if label == "Automations":
                    rect(206, y + 3, 30, 14, "#eceaf7", r=5, name="Badge / BETA bg")
                    text(210, y + 5, "BETA", 8, 800, "#6f6c8c", lh=10, name="Badge / BETA")
                y += 28
        y += 10


def topbar():
    rect(0, 0, W, 56, C["indigo"], name="Top bar")
    rect(20, 15, 26, 26, C["purple"], r=7, name="Logo mark")
    text(27, 21, "S", 13, 800, C["white"], lh=14, name="Logo / S")
    text(56, 19, "SmartLead", 14.5, 700, C["white"], lh=18, name="Brand")
    text(140, 19.5, "/ Smart Assistant", 13.5, 500, "#c9c3ff", lh=18, name="Brand / section")
    # workspace switcher
    rect(268, 14, 116, 28, "#2b2b8a", r=8, stroke="#4a4ab0", name="Workspace switcher")
    circle(282, 28, 3.5, "#57e39b", name="Status dot")
    text(292, 19.5, "Acme Co", 13, 600, C["white"], lh=17, name="Workspace name")
    text(368, 20.5, "▾", 9, 500, "#bdb8ee", lh=14, name="Workspace chevron")
    # meta
    text(1000, 21, "Trial · 6 days left", 11.5, 500, "#bdb8ee", lh=15, name="Trial label")
    circle(1232, 28, 13, "#4b3ad1", name="Avatar")
    text(1225, 21.5, "PS", 10, 700, C["white"], lh=13, name="Avatar / initials")


def chat_header(width_end=W, mode="Proposed", memory=True):
    rect(252, 56, width_end - 252, 56, C["white"], name="Chat header")
    line(252, 112, width_end, 112, C["line"])
    text(274, 74, "Smart Assistant", 14, 700, C["ink"], lh=18, name="Chat title")
    text(382, 74.5, "/ Acme Co", 12.5, 400, C["ink3"], lh=18, name="Chat subtitle")
    # mode toggle
    tx = width_end - 260
    rect(tx, 70, 148, 28, "#f2f0fa", r=9, stroke=C["line"], name="Mode toggle")
    if mode == "Today":
        rect(tx + 3, 73, 70, 22, "#fdf1ef", r=7, name="Mode / today bg")
        text(tx + 16, 76.5, "Today", 11.5, 700, "#a4271c", lh=15, name="Mode / today")
        text(tx + 88, 76.5, "Proposed", 11.5, 700, "#6f6c8c", lh=15, name="Mode / proposed")
    else:
        rect(tx + 74, 73, 71, 22, C["white"], r=7, stroke=C["line"], name="Mode / proposed bg")
        text(tx + 16, 76.5, "Today", 11.5, 700, "#6f6c8c", lh=15, name="Mode / today")
        text(tx + 86, 76.5, "Proposed", 11.5, 700, C["indigo"], lh=15, name="Mode / proposed")
    if memory:
        rect(tx + 158, 70, 78, 28, C["white"], r=9, stroke=C["line"], name="Button / memory")
        text(tx + 170, 76, "✦ Memory", 11.5, 700, C["ink2"], lh=15, name="Button / memory label")


def chips(items, y, x=276, primary_first=True):
    cx = x
    for i, label in enumerate(items):
        w = 16 + len(label) * 6.4
        if i == 0 and primary_first:
            rect(cx, y, w, 28, C["purple"], r=14, name="Chip / " + label)
            text(cx + 11, y + 7, label, 11.5, 700, C["white"], lh=14, name="Chip label")
        else:
            rect(cx, y, w, 28, C["lav2"], r=14, stroke=C["lav3"], name="Chip / " + label)
            text(cx + 11, y + 7, label, 11.5, 600, "#4222c9", lh=14, name="Chip label")
        cx += w + 8


def composer(y, dropzone=False, right=W):
    line(252, y - 12, right, y - 12, C["line"])
    rect(252, y, right - 252, H - y, C["white"], name="Composer panel")
    iw = right - 276 - 40
    rect(276, y + 10, iw, 44, C["white"], r=13, stroke=C["line"], name="Composer input")
    text(316, y + 22, "Ask SmartAssistant anything… or drop a CSV", 13.5, 400, "#a5a2bb", lh=18, name="Composer placeholder")
    # paperclip
    path(f"M 296 {y+26} l 5 -5 a 3.4 3.4 0 0 1 4.8 4.8 l -6.4 6.4 a 5.4 5.4 0 0 1 -7.6 -7.6 l 6 -6",
         stroke="#8c89a6", sw=1.5, name="Icon / paperclip")
    # mic
    mx = right - 96
    rect(mx, y + 20, 8, 14, None, r=4, stroke="#8c89a6", sw=1.4, name="Icon / mic")
    line(mx + 4, y + 36, mx + 4, y + 40, "#8c89a6", 1.4)
    circle(mx + 26, y + 32, 14, C["purple"], name="Button / send")
    path(f"M {mx+26} {y+26} l 0 12 M {mx+22} {y+30} l 4 -4 l 4 4", stroke=C["white"], sw=1.6, name="Icon / send arrow")
    if dropzone:
        rect(276, y + 62, iw, 86, C["lav2"], r=12, stroke="#c9bbff", sw=1.5, name="Drop zone")
        text(300, y + 78, "Drop a CSV or paste leads", 13.5, 700, "#3a1fc4", lh=18, name="Drop zone title")
        text(300, y + 98, "We'll map the columns, check for duplicates, and show every step before anything is saved.",
             12, 400, "#5b4fa8", lh=16, name="Drop zone body")
        rect(300, y + 118, 118, 24, C["purple"], r=7, name="Button / choose file")
        text(313, y + 123, "Choose a file", 11, 700, C["white"], lh=14, name="Button label")
        rect(426, y + 118, 152, 24, C["white"], r=7, stroke=C["line"], name="Button / paste")
        text(439, y + 123, "Paste from clipboard", 11, 600, C["ink"], lh=14, name="Button label")


def user_bubble(x, y, w, lines, extra=None):
    rect(x, y, w, 22 + len(lines) * 19 + (extra or 0), C["lav"], r=12, stroke=C["lav3"], name="Message / user")
    text(x + 14, y + 11, lines, 13.5, 400, "#2f2a5e", lh=19, name="Message text")
    circle(x + w + 14, y + 14, 13, "#e9e7f5", name="Avatar / user")
    text(x + w + 9, y + 8, "PS", 9.5, 700, "#5b5b78", lh=12, name="Avatar initials")


def user_bubble_file(x, y, w=300, label="Import this list to my Q3 Enterprise campaign."):
    """User message that carries an attachment, drawn as one unit."""
    rect(x, y, w, 100, C["lav"], r=12, stroke=C["lav3"], name="Message / user + file")
    text(x + 14, y + 11, label, 13.5, 400, "#2f2a5e", lh=19, name="Message text")
    rect(x + 14, y + 36, w - 28, 46, C["white"], r=11, stroke=C["line"], name="Attachment card")
    rect(x + 26, y + 45, 30, 28, C["okbg"], r=8, name="Attachment type bg")
    text(x + 31, y + 52, "CSV", 9, 800, C["ok"], lh=12, name="Attachment type")
    text(x + 66, y + 44, "q3_enterprise_leads.csv", 11.5, 700, C["ink"], lh=15, name="Attachment filename")
    text(x + 66, y + 60, "2,847 rows · 11 columns · 240 KB", 10.5, 400, C["ink3"], lh=14, name="Attachment meta")
    circle(x + w + 14, y + 14, 13, "#e9e7f5", name="Avatar / user")
    text(x + w + 9, y + 8, "PS", 9.5, 700, "#5b5b78", lh=12, name="Avatar initials")


def bot_avatar(x, y):
    rect(x, y, 28, 28, C["purple"], r=8, name="Avatar / assistant")
    text(x + 10, y + 7, "✦", 13, 700, C["white"], lh=16, name="Avatar glyph")


def runlog(x, y, w, rh=54, steps=(), done_label="", header="Importing to Q3 Enterprise Campaign", complete=False):
    """steps: list of (state, title, detail) ; state in done/active/pending"""
    total = 34 + len(steps) * rh
    rect(x, y, w, total, C["white"], r=12, stroke=C["line"], name="Run-log")
    rect(x, y, w, 34, "#f6fdf9" if complete else "#faf9ff", r=12, name="Run-log header bg")
    rect(x, y + 20, w, 14, "#f6fdf9" if complete else "#faf9ff", name="Run-log header bg 2")
    line(x, y + 34, x + w, y + 34, C["line"])
    if complete:
        circle(x + 17, y + 17, 6, C["ok"], name="Header glyph")
        check(x + 17, y + 17)
        text(x + 30, y + 10, header, 12.5, 700, C["ink"], lh=16, name="Run-log title")
        text(x + w - 108, y + 10, done_label, 11, 800, C["ok"], lh=16, name="Run-log status")
    else:
        circle(x + 17, y + 17, 3.5, C["purple"], name="Live dot")
        text(x + 30, y + 10, header, 12.5, 700, C["ink"], lh=16, name="Run-log title")
    for i, (state, title, detail) in enumerate(steps):
        ry = y + 34 + i * rh
        if i < len(steps) - 1:
            line(x, ry + rh, x + w, ry + rh, C["line2"])
        if i > 0:
            line(x + 20, ry - 14, x + 20, ry + 6, C["lav3"], 1.4, name="Step connector")
        gx, gy = x + 20, ry + 16
        if state == "done":
            circle(gx, gy, 8, C["ok"], name="Step glyph / done")
            check(gx, gy)
        elif state == "active":
            circle(gx, gy, 8, C["white"], stroke=C["purple"], sw=1.5, name="Step glyph / active")
            spinner(gx, gy)
        else:
            circle(gx, gy, 8, C["white"], stroke="#d6d3e6", sw=1.4, name="Step glyph / pending")
        tcol = C["ink"] if state != "pending" else C["muted"]
        text(gx + 18, ry + 9, title, 12.5, 600 if state != "pending" else 500, tcol, lh=17, name="Step / " + title)
        text(gx + 18, ry + 27, detail, 11.5, 400, C["ink3"], lh=16, name="Step detail")
        text(x + w - 20, ry + 12, "▾", 9, 500, "#b3b0c7", lh=12, name="Step chevron")
    return total


def summary_card(x, y, w, h=120):
    rect(x, y, w, h, "#f8fdfa", r=12, stroke="#cfe9db", name="Terminal summary card")
    circle(x + 20, y + 22, 8, C["ok"], name="Summary glyph")
    check(x + 20, y + 22)
    text(x + 36, y + 13, "2,691 leads imported to Q3 Enterprise Campaign", 13, 700, "#0b6b40", lh=18, name="Summary title")
    text(x + 20, y + 40, [[("b", "2,691"), ("n", " imported")]], 11.5, 400, C["ink2"], lh=16, name="Summary stat")
    text(x + 116, y + 40, [[("b", "156"), ("n", " skipped")]], 11.5, 400, C["ink2"], lh=16, name="Summary stat")
    text(x + 206, y + 40, "89 dup · 42 invalid · 25 missing", 11.5, 400, C["ink3"], lh=16, name="Summary stat")
    text(x + 420, y + 40, "71s", 11.5, 400, C["ink3"], lh=16, name="Summary stat")
    # memory badge
    rect(x + 20, y + 62, 168, 22, C["lav2"], r=11, stroke=C["lav3"], name="Memory badge")
    text(x + 32, y + 66, "✦ Used 3 saved preferences", 10.5, 700, "#4b32c9", lh=14, name="Memory badge label")
    # buttons
    bx = x + 20
    rect(bx, y + 92, 122, 26, C["white"], r=8, stroke="#f6d7d4", name="Button / undo")
    text(bx + 12, y + 97, "↺ Undo Import", 11, 700, C["danger"], lh=15, name="Button label")
    rect(bx + 130, y + 92, 138, 26, C["white"], r=8, stroke=C["line"], name="Button / view skipped")
    text(bx + 142, y + 97, "View Skipped Rows", 11, 700, C["ink"], lh=15, name="Button label")
    rect(bx + 276, y + 92, 122, 26, C["purple"], r=8, name="Button / open campaign")
    text(bx + 288, y + 97, "Open Campaign", 11, 700, C["white"], lh=15, name="Button label")

# ================================================================ SCREEN 1
topbar(); rail(); nav()
chat_header()
text(430, 300, "What are we getting done today?", 17, 700, C["ink"], lh=22, name="Empty state title")
text(372, 328, ["I can work inside Acme Co — import leads, build campaigns, pause sends,",
                "set up agents. I'll show every step and you can undo any of it."],
     12.5, 400, C["ink3"], lh=19, name="Empty state body")
chips(["✦ Import a lead list", "Create a new campaign", "Check deliverability", "Set up a Smart Agent"], 548)
composer(600, dropzone=True)
save("01 · Composer & drop zone")

# ================================================================ SCREEN 2
topbar(); rail(); nav()
chat_header()
user_bubble_file(700, 140)

bot_avatar(276, 268)
rect(316, 262, 700, 302, C["white"], r=12, stroke=C["line"], name="Message / assistant")
text(332, 274, ["Reading q3_enterprise_leads.csv — 2,847 rows, 11 columns.",
                "Mapping columns and checking this workspace first."],
     12.5, 400, C["ink2"], lh=18, name="Assistant text")
runlog(332, 330, 668, rh=46, steps=[
    ("done", "File received", "2,847 rows detected · 11 columns · UTF-8"),
    ("done", "Columns mapped", "Email → email · First Name → first_name · Company → company_name"),
    ("active", "Validated and deduplicated", "2,691 valid so far · 89 duplicates found · 42 invalid · 25 missing"),
    ("pending", "Import to Q3 Enterprise Campaign", "Waiting for validation to finish"),
], done_label="", header="Importing to Q3 Enterprise Campaign")

text(276, 588, "LIVE RUN-LOG — every step is named, timed and checkable.", 10, 800, C["muted"], lh=14, ls=0.8, name="Annotation")
chips(["✦ Import a lead list", "Create a new campaign", "Check deliverability"], 612)
composer(660)
save("02 · Live run-log — in progress")

# ================================================================ SCREEN 3
topbar(); rail(); nav()
chat_header()
user_bubble_file(700, 140)

bot_avatar(276, 268)
rect(316, 262, 700, 402, C["white"], r=12, stroke=C["line"], name="Message / assistant")
text(332, 274, "Reading q3_enterprise_leads.csv — 2,847 rows, 11 columns.", 12.5, 400, C["ink2"], lh=18, name="Assistant text")
runlog(332, 300, 668, rh=46, steps=[
    ("done", "File received", "2,847 rows detected · 11 columns · UTF-8"),
    ("done", "Columns mapped", "Email → email · First Name → first_name · Company → company_name"),
    ("done", "Validated and deduplicated", "2,691 valid · 156 skipped: 89 duplicates, 42 invalid, 25 missing"),
    ("done", "Imported to Q3 Enterprise Campaign", "2,691 leads live · 0 errors"),
], done_label="4 steps · 0 errors", header="Imported in 71s", complete=True)
summary_card(332, 528, 668)

text(276, 676, "TERMINAL STATE — proof, not a promise. Undo sits next to the result.", 10, 800, C["muted"], lh=14, ls=0.8, name="Annotation")
composer(700)
save("03 · Live run-log — terminal state")

# ================================================================ SCREEN 4
topbar(); rail(); nav()
chat_header(width_end=876)
# chat column (narrow)
user_bubble(452, 140, 384, ["Import this list to my Q3 Enterprise campaign."])
bot_avatar(276, 210)
rect(316, 204, 540, 210, C["white"], r=12, stroke=C["line"], name="Message / assistant")
text(332, 216, ["Importing to Q3 Enterprise Campaign. I used what I already know",
                "about this client, so there's nothing to fill in."],
     12.5, 400, C["ink2"], lh=18, name="Assistant text")
rect(332, 268, 196, 24, C["lav2"], r=12, stroke=C["lav3"], name="Memory badge")
text(346, 273, "✦ Used 3 saved preferences", 10.5, 700, "#4b32c9", lh=15, name="Memory badge label")
for i, (lab, val) in enumerate([
        ("Column mapping defaults", "Email → email · Company → company_name"),
        ("ICP filter", "RevOps, 200–2,000 person SaaS, NA + UK"),
        ("Naming convention", "Q3 · Enterprise · US · v1")]):
    ry = 300 + i * 34
    circle(344, ry + 9, 4, C["purple"], name="Preference dot")
    text(362, ry, lab, 11, 700, C["ink"], lh=15, name="Preference label")
    text(524, ry, val, 11, 400, C["ink3"], lh=15, name="Preference value")
chips(["✦ Import a lead list"], 612, x=276)
composer(660, right=876)

# drawer
rect(870, 0, 410, H, "#14142b", opacity=0.28, name="Scrim")
rect(876, 0, 404, H, C["white"], name="Memory drawer")
text(900, 22, "Remembered for this workspace", 15, 700, C["ink"], lh=20, name="Drawer title")
text(900, 44, "Everything the assistant carries between sessions", 11.5, 400, C["ink3"], lh=16, name="Drawer subtitle")
circle(1250, 32, 14, "#f4f3fa", name="Button / close bg")
text(1245, 25, "✕", 11, 500, "#6f6c8c", lh=14, name="Button / close")
rect(900, 70, 356, 24, C["indigo"], r=12, name="Scope badge")
circle(916, 82, 3, "#57e39b", name="Scope dot")
text(926, 75, "Client: Acme Co · workspace 3 of 14", 10.5, 700, C["white"], lh=14, name="Scope badge label")

MEM = [
    ("ICP DEFINITION", "Learned from 14 conversations", ["RevOps & Sales Ops leaders at 200–2,000-person", "SaaS companies in North America and the UK."]),
    ("EMAIL TONE & VOICE", "Learned from 22 conversations", ["Dry and specific. No exclamation marks, no", "\"hope you're well\". Under 90 words."]),
    ("COLUMN MAPPING DEFAULTS", "Learned from 9 imports", ["Company Domain → domain · First Name →", "first_name · Work Email → email"]),
    ("NAMING CONVENTION", "Set by you", ["{Quarter} · {Segment} · {Region} · v{n} —", "always created paused for review."]),
    ("SENDING PREFERENCES", "Learned from 6 campaigns", ["Max 28/day per mailbox, 3 mailboxes rotating,", "warmup on. Never edit a live sequence without asking."]),
]
my = 108
for lab, src, lines in MEM:
    h = 52 + len(lines) * 17
    rect(900, my, 356, h, C["white"], r=11, stroke=C["line"], name="Memory card / " + lab.title())
    text(914, my + 10, lab, 9, 800, C["ink3"], lh=12, ls=0.9, name="Memory label")
    text(914, my + 23, src, 8.5, 700, "#6b5bb8", lh=12, name="Memory source")
    text(914, my + 38, lines, 11.5, 400, C["ink"], lh=17, name="Memory value")
    my += h + 8

rect(876, H - 62, 404, 62, "#fbfaff", name="Drawer footer")
line(876, H - 62, 1280, H - 62, C["line"])
text(900, H - 48, "🔒 Memory is scoped to this workspace only. Nothing leaks across",
     10.5, 400, C["ink3"], lh=15, name="Drawer footer text")
text(900, H - 33, "clients. All memories are visible, editable, and deletable.", 10.5, 400, C["ink3"], lh=15, name="Drawer footer text 2")
save("04 · Memory panel")

# ================================================================ SCREEN 5
topbar(); rail(); nav()
chat_header(mode="Today")
user_bubble_file(700, 140)

bot_avatar(276, 268)
rect(316, 262, 700, 300, C["white"], r=12, stroke=C["line"], name="Message / assistant")
text(332, 274, "Got it. Here's how to import this list:", 12.5, 400, C["ink2"], lh=18, name="Assistant text")
rect(332, 300, 668, 176, "#fffaf9", r=12, stroke="#f0dcd8", name="Guide card")
steps5 = [
    "Go to Campaigns and open Q3 Enterprise.",
    "Open the Leads tab and click Add Leads → Import CSV.",
    "Upload the file, then map your columns to the lead fields.",
    "Choose how to handle duplicates, then confirm the import.",
]
for i, s in enumerate(steps5):
    ry = 312 + i * 26
    text(346, ry, f"{i+1}.", 12, 700, "#4a4a68", lh=16, name="Guide step number")
    text(362, ry, s, 12, 400, "#4a4a68", lh=16, name="Guide step")
text(346, 424, "0 account changes · 6 manual steps", 10.5, 700, "#a4271c", lh=15, name="Guide meta")
text(332, 492, "\"Let me know once it's done and I'll help you spot-check it. I can't read the file from here.\"",
     11.5, 400, C["ink3"], lh=16, name="Assistant caveat")
text(332, 522, "You are where you started, minus the time it took to read this.",
     11.5, 600, C["ink3"], lh=16, name="Annotation text")
chips(["✦ Import a lead list", "Create a new campaign", "Check deliverability"], 612)
composer(660)
save("05 · Today — the guide response (before)")

# ================================================================ emit
OUT = "figma"
os.makedirs(OUT, exist_ok=True)


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
             .replace('"', "&quot;"))


def svg(frame, idx):
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{frame["w"]}" height="{frame["h"]}" '
         f'viewBox="0 0 {frame["w"]} {frame["h"]}" font-family="Inter, -apple-system, Segoe UI, sans-serif">',
         f'<rect width="{frame["w"]}" height="{frame["h"]}" fill="{C["bg"]}"/>']
    for op in frame["ops"]:
        if op["t"] == "rect":
            a = f'<rect x="{op["x"]}" y="{op["y"]}" width="{op["w"]}" height="{op["h"]}"'
            if op["r"]:
                a += f' rx="{op["r"]}"'
            a += f' fill="{op["fill"] or "none"}"'
            if op["stroke"]:
                a += f' stroke="{op["stroke"]}" stroke-width="{op["sw"]}"'
            a += "/>"
            o.append(a)
        elif op["t"] == "circle":
            a = f'<circle cx="{op["cx"]}" cy="{op["cy"]}" r="{op["r"]}" fill="{op["fill"] or "none"}"'
            if op["stroke"]:
                a += f' stroke="{op["stroke"]}" stroke-width="{op["sw"]}"'
            o.append(a + "/>")
        elif op["t"] == "line":
            o.append(f'<line x1="{op["x1"]}" y1="{op["y1"]}" x2="{op["x2"]}" y2="{op["y2"]}" '
                     f'stroke="{op["c"]}" stroke-width="{op["sw"]}"/>')
        elif op["t"] == "path":
            a = f'<path d="{op["d"]}" fill="{op["fill"] or "none"}"'
            if op["stroke"]:
                a += f' stroke="{op["stroke"]}" stroke-width="{op["sw"]}" stroke-linecap="round" stroke-linejoin="round"'
            o.append(a + "/>")
        elif op["t"] == "text":
            base = op["y"] + op["s"] * 0.92
            anchor = {"left": "start", "center": "middle", "right": "end"}[op["align"]]
            ls = f' letter-spacing="{op["ls"]}"' if op.get("ls") else ""
            head = (f'<text x="{op["x"]}" y="{base}" font-size="{op["s"]}" font-weight="{op["wgt"]}" '
                    f'fill="{op["c"]}" text-anchor="{anchor}"{ls}>')
            spans = []
            for i, ln in enumerate(op["lines"]):
                dy = 0 if i == 0 else op["lh"]
                content = ln
                if isinstance(content, list):      # mixed-weight runs
                    content = "".join(
                        f'<tspan font-weight="{1200 if k=="b" else 400}">{esc(v)}</tspan>' for k, v in content)
                else:
                    content = esc(content)
                spans.append(f'<tspan x="{op["x"]}" dy="{dy}">{content}</tspan>')
            o.append(head + "".join(spans) + "</text>")
    o.append("</svg>")
    name = frame["name"].split("·")[1].strip().lower().replace(" ", "-").replace("—", "").replace("--", "-")
    name = "".join(ch for ch in name if ch.isalnum() or ch == "-")
    p = os.path.join(OUT, f'{idx+1:02d}-{name}.svg')
    open(p, "w").write("\n".join(o))
    return p


made = [svg(f, i) for i, f in enumerate(frames)]

# plugin
os.makedirs("figma-plugin", exist_ok=True)
spec = dict(
    colors=C,
    frames=[dict(name=f["name"], w=f["w"], h=f["h"], ops=f["ops"]) for f in frames],
)
open("figma-plugin/spec.json", "w").write(json.dumps(spec, indent=1))
print("frames:", len(frames))
for m in made:
    print(" ", m)


# ---------------------------------------------------------------- figma plugin
WEIGHT = {400: "Regular", 500: "Medium", 600: "Semi Bold", 700: "Bold", 800: "Extra Bold"}


def js_rect(o):
    parts = [f'x:{o["x"]},y:{o["y"]},w:{o["w"]},h:{o["h"]}']
    if o["fill"]:
        parts.append(f'fill:"{o["fill"]}"')
    if o["r"]:
        parts.append(f'r:{o["r"]}')
    if o["stroke"]:
        parts.append(f'stroke:"{o["stroke"]}",sw:{o["sw"]}')
    parts.append(f'name:' + json.dumps(o["name"]))
    if o.get("o", 1) != 1:
        parts.append(f'o:{o["o"]}')
    return "{t:'rect'," + ",".join(parts) + "}"


def js_circle(o):
    parts = [f'cx:{o["cx"]},cy:{o["cy"]},r:{o["r"]}']
    if o["fill"]:
        parts.append(f'fill:"{o["fill"]}"')
    if o["stroke"]:
        parts.append(f'stroke:"{o["stroke"]}",sw:{o["sw"]}')
    parts.append('name:' + json.dumps(o["name"]))
    return "{t:'circle'," + ",".join(parts) + "}"


def js_line(o):
    return ("{t:'line',x1:%s,y1:%s,x2:%s,y2:%s,c:'%s',sw:%s,name:%s}" %
            (o["x1"], o["y1"], o["x2"], o["y2"], o["c"], o["sw"], json.dumps(o["name"])))


def js_path(o):
    parts = [f'd:"{o["d"]}"']
    if o["stroke"]:
        parts.append(f'stroke:"{o["stroke"]}",sw:{o["sw"]}')
    if o["fill"]:
        parts.append(f'fill:"{o["fill"]}"')
    parts.append('name:' + json.dumps(o["name"]))
    return "{t:'path'," + ",".join(parts) + "}"


def js_text(o):
    lines = []
    for ln in o["lines"]:
        if isinstance(ln, list):
            lines.append("".join(v for _k, v in ln))
        else:
            lines.append(ln)
    parts = [f'x:{o["x"]},y:{o["y"]},s:{o["s"]},w:{o["wgt"]},c:"{o["c"]}",lh:{o["lh"]}',
             'name:' + json.dumps(o["name"]),
             'txt:' + json.dumps("\n".join(lines))]
    if o.get("ls"):
        parts.append(f'ls:{o["ls"]}')
    if o.get("align") and o["align"] != "left":
        parts.append(f'align:"{o["align"]}"')
    return "{t:'text'," + ",".join(parts) + "}"


JS_FRAMES = []
for f in frames:
    body = []
    for o in f["ops"]:
        {"rect": js_rect, "circle": js_circle, "line": js_line,
         "path": js_path, "text": js_text}[o["t"]](o)
        body.append({"rect": js_rect, "circle": js_circle, "line": js_line,
                     "path": js_path, "text": js_text}[o["t"]](o))
    JS_FRAMES.append('{name:%s,w:%d,h:%d,ops:[%s]}' % (json.dumps(f["name"]), f["w"], f["h"], ",\n".join(body)))

plugin_code = """/* Smart Assistant — Prototype figma builder
   Generated by build_figma.py. In Figma: Plugins → Development → Import plugin from manifest. */
const PALETTE = %s;
const FRAMES = [%s];
const WEIGHTS = %s;

function rgb(hex){
  const h = hex.replace('#','');
  return {r: parseInt(h.slice(0,2),16)/255, g: parseInt(h.slice(2,4),16)/255, b: parseInt(h.slice(4,6),16)/255};
}
function paint(hex, opacity){
  const p = {type:'SOLID', color: rgb(hex)};
  if(opacity !== undefined && opacity !== 1) p.opacity = opacity;
  return p;
}

(async () => {
  const families = ['Regular','Medium','Semi Bold','Bold','Extra Bold'];
  await Promise.all(families.map(f => figma.loadFontAsync({family:'Inter', style:f})));

  const styles = {};
  for (const [k,v] of Object.entries(PALETTE)) {
    if (typeof v !== 'string' || v[0] !== '#') continue;
    const st = figma.createPaintStyle();
    st.name = 'SA/' + k;
    st.paints = [paint(v)];
    styles[k] = st;
  }

  const page = figma.currentPage;
  page.name = 'Smart Assistant — Prototype';

  let x = 0;
  for (const spec of FRAMES) {
    const frame = figma.createFrame();
    frame.name = spec.name;
    frame.resize(spec.w, spec.h);
    frame.x = x; frame.y = 0;
    x += spec.w + 80;
    frame.fills = [paint('#fbfaff')];
    frame.clipsContent = true;

    for (const op of spec.ops) {
      let node;
      if (op.t === 'rect') {
        node = figma.createRectangle();
        node.name = op.name;
        node.resize(op.w, op.h);
        node.x = op.x; node.y = op.y;
        if (op.r) node.cornerRadius = op.r;
        node.fills = op.fill ? [paint(op.fill)] : [];
        if (op.stroke) { node.strokes = [paint(op.stroke)]; node.strokeWeight = op.sw; }
        if (op.o && op.o !== 1) node.opacity = op.o;
      } else if (op.t === 'circle') {
        node = figma.createEllipse();
        node.name = op.name;
        node.resize(op.r*2, op.r*2);
        node.x = op.cx - op.r; node.y = op.cy - op.r;
        node.fills = op.fill ? [paint(op.fill)] : [];
        if (op.stroke) { node.strokes = [paint(op.stroke)]; node.strokeWeight = op.sw; }
      } else if (op.t === 'line') {
        node = figma.createLine();
        node.name = op.name;
        node.x = Math.min(op.x1, op.x2);
        node.y = Math.min(op.y1, op.y2);
        const horiz = op.y1 === op.y2;
        node.resize(horiz ? Math.abs(op.x2-op.x1) : 0, horiz ? 0 : Math.abs(op.y2-op.y1));
        node.strokes = [paint(op.c)];
        node.strokeWeight = op.sw;
      } else if (op.t === 'path') {
        node = figma.createVector();
        node.name = op.name;
        const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="-8 -8 24 24"><path d="${op.d}" fill="${op.fill || 'none'}" stroke="${op.stroke || 'none'}" stroke-width="${op.sw || 1}" stroke-linecap="round" stroke-linejoin="round"/></svg>`;
        const v = figma.createNodeFromSvg(svg);
        node.remove();
        node = v;
        node.name = op.name;
        frame.appendChild(node);
        node.x = op.x !== undefined ? op.x : 0;
        // vectors keep their own geometry; place by bounding box origin
        node.x = Math.max(0, node.x);
        node.y = Math.max(0, node.y);
        continue;
      } else if (op.t === 'text') {
        node = figma.createText();
        node.name = op.name;
        node.fontName = {family:'Inter', style: WEIGHTS[op.w] || 'Regular'};
        node.fontSize = op.s;
        node.lineHeight = {unit:'PIXELS', value: op.lh};
        node.characters = op.txt;
        node.fills = [paint(op.c)];
        if (op.ls) node.letterSpacing = {unit:'PIXELS', value: op.ls};
        if (op.align === 'right') node.textAlignHorizontal = 'RIGHT';
        if (op.align === 'center') node.textAlignHorizontal = 'CENTER';
        node.textAutoResize = 'WIDTH_AND_HEIGHT';
        frame.appendChild(node);
        node.x = op.align === 'right' ? op.x - node.width : op.x;
        node.y = op.y;
        continue;
      }
      frame.appendChild(node);
    }
  }
  figma.viewport.scrollTo({x: 0, y: 0, zoom: 0.25});
  figma.closePlugin('5 frames built — named layers, SA/ color styles.');
})();
""" % (json.dumps(C, indent=1), ",\n".join(JS_FRAMES), json.dumps(WEIGHT, indent=1))

os.makedirs("figma-plugin", exist_ok=True)
open("figma-plugin/code.js", "w").write(plugin_code)
open("figma-plugin/manifest.json", "w").write(json.dumps({
    "name": "Smart Assistant — Prototype Builder",
    "id": "smartlead-sa-prototype-builder",
    "api": "1.0.0",
    "main": "code.js",
    "editorType": ["figma"],
}, indent=2))

# ---------------------------------------------------------------- inline sheet
inline = ['<!doctype html><html><head><meta charset="utf-8"><title>Smart Assistant — Figma frames</title>',
          '<style>body{margin:0;background:#e9e7f2;font-family:Inter,-apple-system,sans-serif;padding:28px}',
          'h1{font-size:20px;margin:0 0 4px;color:#14142b}p.s{color:#494968;font-size:13px;margin:0 0 22px}',
          '.grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}',
          '.card{background:#fff;border-radius:12px;overflow:hidden;box-shadow:0 6px 22px rgba(20,20,43,.14)}',
          '.cap{font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;color:#7c7c99;padding:9px 12px;border-bottom:1px solid #eceaf5}',
          '.card svg{display:block;width:100%;height:auto}</style></head><body>',
          '<h1>Smart Assistant — 5 frames</h1><p class="s">Drag the SVGs in <code>figma/</code> into Figma, or run the plugin in <code>figma-plugin/</code> to rebuild them as native layers.</p><div class="grid">']
for f, m in zip(frames, made):
    svgmarkup = open(m).read()
    svgmarkup = svgmarkup.replace('<svg ', '<svg preserveAspectRatio="xMidYMid meet" ', 1)
    inline.append('<div class="card"><div class="cap">%s</div>%s</div>' % (esc(f["name"]), svgmarkup))
inline.append('</div></body></html>')
open("figma/index.html", "w").write("\n".join(inline))
print("plugin + sheet written")
