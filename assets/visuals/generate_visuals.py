#!/usr/bin/env python3
"""Generate the Context Engineering diagram set as clean, branded SVGs.

Style: white canvas, navy (#0B1F4A) primary boxes with white text,
light blue (#E0F2FE) secondary boxes with navy text, cyan (#0891B2)
arrows, amber (#F59E0B) accent for warnings/gates. Every chart's
numbers are the measured outputs of the lesson it illustrates,
cited in the subtitle. Run: python3 generate_visuals.py
"""
import os

OUT = os.path.dirname(os.path.abspath(__file__))
NAVY = "#0B1F4A"
LIGHT = "#E0F2FE"
CYAN = "#0891B2"
AMBER = "#F59E0B"
GREY = "#475569"
FONT = "Segoe UI, Helvetica, Arial, sans-serif"


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


class SVG:
    def __init__(self, w, h, title, subtitle):
        self.w, self.h = w, h
        self.parts = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">',
            f'<rect width="{w}" height="{h}" fill="#FFFFFF"/>',
            f'<text x="40" y="52" font-family="{FONT}" font-size="30" font-weight="700" fill="{NAVY}">{esc(title)}</text>',
            f'<text x="40" y="82" font-family="{FONT}" font-size="17" fill="{GREY}">{esc(subtitle)}</text>',
            f'<rect x="40" y="98" width="90" height="5" fill="{CYAN}"/>',
        ]

    def box(self, x, y, w, h, text, fill=NAVY, color="#FFFFFF", size=16, bold=False):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}"/>')
        weight = "700" if bold else "400"
        lines = text.split("\n")
        for i, line in enumerate(lines):
            ly = y + h / 2 + (i - (len(lines) - 1) / 2) * (size + 4) + size * 0.35
            self.parts.append(f'<text x="{x + w / 2}" y="{ly:.0f}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" fill="{color}" text-anchor="middle">{esc(line)}</text>')

    def arrow(self, x1, y1, x2, y2, color=CYAN):
        self.parts.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="3"/>')
        self.parts.append(f'<polygon points="{x2},{y2} {x2 - 10},{y2 - 6} {x2 - 10},{y2 + 6}" fill="{color}"/>')

    def label(self, x, y, text, size=15, color=GREY, anchor="start"):
        self.parts.append(f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" fill="{color}" text-anchor="{anchor}">{esc(text)}</text>')

    def bar(self, x, y, w, h, frac, color=CYAN):
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#E2E8F0"/>')
        self.parts.append(f'<rect x="{x}" y="{y}" width="{w * frac:.0f}" height="{h}" fill="{color}"/>')

    def save(self, name):
        self.parts.append("</svg>")
        with open(os.path.join(OUT, name), "w") as f:
            f.write("\n".join(self.parts))
        print("wrote", name)


def course_map():
    s = SVG(1180, 560, "Context Engineering: the course map",
            "Ten modules, one window: measure it, budget it, then write, select, compress, order, remember, and gate it.")
    mods = [("0 Foundations", "00-02"), ("1 The budget", "03-05"),
            ("2 Writing", "06-09"), ("3 Selecting", "10-13"),
            ("4 Compressing", "14-17"), ("5 Ordering", "18-20"),
            ("6 Memory", "21-23"), ("7 Tools", "24-25"),
            ("8 Cost", "26-27"), ("9 Capstone", "28-31")]
    for i, (name, rng) in enumerate(mods):
        x = 40 + (i % 5) * 224
        y = 150 + (i // 5) * 170
        s.box(x, y, 190, 110, f"{name}\nLessons {rng}", fill=NAVY if i in (0, 9) else LIGHT,
              color="#FFFFFF" if i in (0, 9) else NAVY, bold=True)
        if i % 5 != 4:
            s.arrow(x + 192, y + 55, x + 220, y + 55)
    s.label(40, 520, "Every lesson runs offline on the standard library, and every number in it is measured by its own code.", size=16)
    s.save("course-map.svg")


def window_anatomy():
    s = SVG(1180, 520, "Anatomy of one assembled context",
            "Measured in Lesson 01: 668 approx tokens for a Fernhill support turn. Retrieval is 56 percent of what the model reads.")
    parts = [("retrieval", 374, CYAN), ("history", 156, NAVY),
             ("system", 50, AMBER), ("tools", 41, GREY),
             ("user", 30, LIGHT), ("memory", 17, LIGHT)]
    y = 150
    for name, tokens, color in parts:
        s.label(40, y + 22, f"{name}", size=17, color=NAVY)
        s.bar(190, y, 800, 26, tokens / 374, color)
        s.label(1010, y + 22, f"{tokens} tokens", size=17, color=NAVY)
        y += 52
    s.label(40, 490, "The component teams write most carefully (the system prompt) is 7.5 percent of the window.", size=16)
    s.save("window-anatomy.svg")


def u_curve():
    s = SVG(1180, 520, "Lost in the middle, measured (Lesson 05)",
            "Stand-in recall of the same facts at each of 10 positions. Edges 1.0, middle 0.65, on the course's labelled stand-in rule.")
    vals = [1.0, 1.0, 1.0, 0.975, 0.7, 0.65, 0.925, 1.0, 1.0, 1.0]
    base_y, top_y = 440, 150
    for i, v in enumerate(vals):
        x = 90 + i * 108
        h = (base_y - top_y) * v
        s.parts.append(f'<rect x="{x}" y="{base_y - h:.0f}" width="70" height="{h:.0f}" fill="{AMBER if v < 0.9 else CYAN}"/>')
        s.label(x + 35, base_y - h - 12, f"{v}", size=15, color=NAVY, anchor="middle")
        s.label(x + 35, base_y + 28, f"{i + 1}", size=15, color=GREY, anchor="middle")
    s.label(90, base_y + 58, "Position of the fact-bearing document in a fixed 10 document context", size=15)
    s.save("u-curve.svg")


def four_ops():
    s = SVG(1180, 470, "The four operations (LangChain taxonomy, 2025)",
            "Write, select, compress, isolate: the course devotes a module block to each, and the capstone composes all four.")
    ops = [("WRITE", "Save context outside\nthe window\nLessons 06-09, 21-22"),
           ("SELECT", "Pull in what the\nstep needs\nLessons 10-13"),
           ("COMPRESS", "Keep only the tokens\nthat carry facts\nLessons 14-17"),
           ("ISOLATE", "Split work across\nclean windows\nLesson 23")]
    for i, (name, body) in enumerate(ops):
        x = 40 + i * 284
        s.box(x, 150, 250, 170, f"{name}\n{body}", fill=LIGHT, color=NAVY)
        if i < 3:
            s.arrow(x + 252, 235, x + 280, 235)
    s.label(40, 400, "Anthropic's framing adds the goal: the smallest set of high-signal tokens that maximises the desired outcome.", size=16)
    s.save("four-operations.svg")


def budget_ledger():
    s = SVG(1180, 500, "The standard budget breaks at turn 30 (Lesson 03)",
            "4,000 token window, 500 reserved for the answer. History is the only component that grows every turn.")
    rows = [("system", 350, 350), ("tools", 450, 450), ("memory", 300, 300),
            ("retrieval", 1600, 1600), ("history", 800, 1354)]
    y = 150
    for name, allowance, actual in rows:
        s.label(40, y + 22, name, size=17, color=NAVY)
        s.bar(190, y, 700, 26, min(1.0, actual / 1600), AMBER if actual > allowance else CYAN)
        s.label(910, y + 22, f"{actual} of {allowance}", size=17, color=NAVY)
        y += 52
    s.label(40, 460, "After 48 scripted turns the ledger totals 4,054 tokens: over budget by 54, with no error raised anywhere.", size=16)
    s.save("budget-ledger.svg")


def compaction():
    s = SVG(1180, 500, "Three ways to survive a long conversation (Lesson 16)",
            "Tokens and surviving facts for the 24 turn fixture conversation. Truncation is cheapest and forgets; notes cost more and forget nothing measured.")
    rows = [("keep everything", 677, "probes 5/5, pinned 5/5", CYAN),
            ("truncate to last 8 turns", 267, "probes 3/5, pinned 5/5", AMBER),
            ("rolling notes + pins", 528, "probes 5/5, pinned 5/5", NAVY)]
    y = 160
    for name, tokens, surv, color in rows:
        s.label(40, y + 6, name, size=18, color=NAVY)
        s.bar(40, y + 18, 700, 24, tokens / 677, color)
        s.label(770, y + 38, f"{tokens} tokens, {surv}", size=17, color=NAVY)
        y += 100
    s.save("compaction-strategies.svg")


def pipeline():
    s = SVG(1180, 470, "The capstone pipeline (Lessons 29-31)",
            "Gates fixed before the build. As built: 4 of 5 gates (precision 0.1326 vs 0.15). Hardened with a relevance floor: 5 of 5, 572 mean tokens.")
    steps = [("Structured\nrules", "Lesson 06"), ("TF-IDF select\nunder budget", "Lesson 11"),
             ("Relevance\nfloor 0.25", "Lesson 31 fix"), ("Fixed layout\nquestion last", "Lessons 18-20"),
             ("Gate check\n5 gates", "Lesson 29")]
    for i, (name, src) in enumerate(steps):
        x = 40 + i * 224
        fill = AMBER if i == 4 else (LIGHT if i == 2 else NAVY)
        color = NAVY if i in (2, 4) else "#FFFFFF"
        s.box(x, 160, 190, 120, f"{name}\n{src}", fill=fill, color=color)
        if i < 4:
            s.arrow(x + 192, 220, x + 220, 220)
    s.label(40, 360, "Baseline (wall prompt, preload everything): recall 0.8781 at 2,292 tokens. The pipeline: recall 1.0 at 572.", size=17, color=NAVY)
    s.label(40, 400, "Both the failure and the fix stay in Lesson 31's output. That is what the gates are for.", size=16)
    s.save("capstone-pipeline.svg")


if __name__ == "__main__":
    course_map()
    window_anatomy()
    u_curve()
    four_ops()
    budget_ledger()
    compaction()
    pipeline()
