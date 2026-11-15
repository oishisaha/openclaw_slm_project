"""
DABench Evaluation — Final Visualisation
OpenClaw + DeepSeek V4 Flash
Run: python3 dabench_viz_final.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patches as patches
import matplotlib.gridspec as gridspec
import numpy as np

C_GREEN  = "#43a047"
C_RED    = "#e53935"
C_AMBER  = "#e6a817"
C_BLUE   = "#1a56db"
C_GRAY   = "#9e9e9e"
C_BG     = "#f7f6f2"
C_SURF   = "#ffffff"
C_INK    = "#0e0e0e"
C_MUTED  = "#5a5a5a"
C_RULE   = "#e0deda"
LVL_COL  = {"Easy": "#1565c0", "Medium": "#e65100", "Hard": "#880e4f"}

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "axes.facecolor":     C_SURF,
    "figure.facecolor":   C_BG,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   False,
    "axes.spines.bottom": False,
    "axes.grid":          False,
    "text.color":         C_INK,
    "font.size":          10,
})

questions = [
    {"id":"Q24",  "task":"Mean Age",      "level":"Easy",   "initial":True,  "tokens": 25657, "cost":0.0026, "init_cost":0.0026},
    {"id":"Q25",  "task":"BMI Normality", "level":"Easy",   "initial":False, "tokens":706598, "cost":0.0639, "init_cost":0.0085},
    {"id":"Q26",  "task":"Correlation",   "level":"Easy",   "initial":False, "tokens": 45496, "cost":0.0043, "init_cost":0.0095},
    {"id":"Q27",  "task":"Outlier Count", "level":"Medium", "initial":True,  "tokens":470453, "cost":0.0483, "init_cost":0.0483},
    {"id":"Q28",  "task":"Preprocessing", "level":"Hard",   "initial":False, "tokens":127736, "cost":0.0119, "init_cost":0.0197},
    {"id":"Q30",  "task":"Regression",    "level":"Hard",   "initial":False, "tokens": 96727, "cost":0.0089, "init_cost":0.0114},
    {"id":"Q123", "task":"Top Country",   "level":"Easy",   "initial":True,  "tokens": 77345, "cost":0.0075, "init_cost":0.0075},
    {"id":"Q124", "task":"ANOVA",         "level":"Hard",   "initial":True,  "tokens": 50044, "cost":0.0047, "init_cost":0.0047},
    {"id":"Q125", "task":"Multiple Reg.", "level":"Hard",   "initial":True,  "tokens": 95392, "cost":0.0095, "init_cost":0.0095},
]

mismatches = [
    {"id":"Q25", "task":"BMI Normality",
     "initial": "not_normal\n(Shapiro-Wilk test)",
     "correct": "normal\n(skewness < 0.5)"},
    {"id":"Q26", "task":"Correlation",
     "initial": "0.30\n(age vs charges)",
     "correct": "0.07\n(charges vs children)"},
    {"id":"Q28", "task":"Preprocessing",
     "initial": "0.0\n(z-score mean)",
     "correct": "0.3956\n(min-max mean)"},
    {"id":"Q30", "task":"Regression",
     "initial": "0.12\n(R-squared)",
     "correct": "11464.74\n(RMSE)"},
]

fig = plt.figure(figsize=(20, 14), facecolor=C_BG)
fig.suptitle(
    "OpenClaw + DeepSeek V4 Flash — DABench Evaluation Analysis\n"
    "Accuracy Recovery  ·  Prompt Failures  ·  Cost Behaviour",
    fontsize=14, fontweight="bold", y=0.99, color=C_INK
)

gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.44, wspace=0.32)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT 1: Before / After outcome matrix
# ─────────────────────────────────────────────────────────────────────────────
ax1 = fig.add_subplot(gs[0, 0])
ax1.set_title("Before / After Outcome Matrix",
              fontweight="bold", pad=10, fontsize=11)

n_q = len(questions)
rows_labels = ["Initial\nPrompt", "Fixed\nPrompt"]

for ri, row_label in enumerate(rows_labels):
    for ci, q in enumerate(questions):
        if ri == 0:
            correct = q["initial"]
        else:
            correct = True
        color = C_GREEN if correct else "#c62828"
        ax1.add_patch(plt.Rectangle(
            (ci - 0.45, ri - 0.45), 0.90, 0.90,
            facecolor=color, edgecolor="white",
            linewidth=2, zorder=2
        ))
        sym = "✓" if correct else "✗"
        ax1.text(ci, ri, sym, ha="center", va="center",
                 fontsize=14, fontweight="bold",
                 color="white", zorder=3)

ax1.set_xlim(-0.6, n_q - 0.4)
ax1.set_ylim(-0.6, 1.6)
ax1.set_xticks(range(n_q))
ax1.set_xticklabels(
    [f"{q['id']}  {q['task']}" for q in questions],
    fontsize=7.5, rotation=35, ha="right", rotation_mode="anchor"
)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(rows_labels, fontsize=9)
ax1.tick_params(length=0)

for ci, q in enumerate(questions):
    lvl = q["level"]
    ax1.text(ci, -0.72, lvl, ha="center", fontsize=7,
             color=LVL_COL[lvl], fontweight="bold")

ax1.text(0.5, -0.30,
         "Prompt refinement recovered 4/4 failures → final accuracy 100%",
         ha="center", va="top", fontsize=8.5,
         fontweight="bold", color=C_AMBER,
         transform=ax1.transAxes)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT 2: Prompt mismatch — red/green two-column table
# ─────────────────────────────────────────────────────────────────────────────
ax2 = fig.add_subplot(gs[0, 1])
ax2.axis("off")
ax2.set_title("Failure Diagnosis: Specification Mismatch",
              fontweight="bold", pad=10, fontsize=11)

col_x = [0.03, 0.35, 0.68]
ax2.text(col_x[0], 0.97, "Question",
         fontsize=8.5, fontweight="bold", color=C_MUTED,
         transform=ax2.transAxes, va="top")
ax2.text(col_x[1], 0.97, "Initial Answer",
         fontsize=8.5, fontweight="bold", color=C_RED,
         transform=ax2.transAxes, va="top")
ax2.text(col_x[2], 0.97, "Correct Answer",
         fontsize=8.5, fontweight="bold", color=C_GREEN,
         transform=ax2.transAxes, va="top")

ax2.axhline(0.93, xmin=0.01, xmax=0.99, color=C_RULE,
            linewidth=1.2)

row_h = 0.20
ry = 0.88
for m in mismatches:
    ax2.add_patch(plt.Rectangle(
        (0.01, ry - row_h + 0.01), 0.98, row_h - 0.01,
        transform=ax2.transAxes,
        facecolor="#fafaf8", edgecolor=C_RULE,
        linewidth=0.5, zorder=0
    ))
    ax2.text(col_x[0], ry - 0.02,
             f"{m['id']}\n{m['task']}",
             fontsize=8, fontweight="bold",
             color=C_INK, transform=ax2.transAxes, va="top")
    ax2.text(col_x[1], ry - 0.02, m["initial"],
             fontsize=8, color=C_RED,
             transform=ax2.transAxes, va="top")
    ax2.text(col_x[2], ry - 0.02, m["correct"],
             fontsize=8, color=C_GREEN,
             transform=ax2.transAxes, va="top")
    ry -= row_h

ax2.text(0.5, 0.01,
         "Model reasoned correctly — task specification was misaligned",
         ha="center", va="bottom", fontsize=8.5,
         fontweight="bold", color=C_BLUE,
         transform=ax2.transAxes)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT 3: Token usage concentration
# ─────────────────────────────────────────────────────────────────────────────
ax3 = fig.add_subplot(gs[0, 2])
ax3.set_title("Token Usage Concentration",
              fontweight="bold", pad=10, fontsize=11)

total_tokens = sum(q["tokens"] for q in questions)
sorted_qs    = sorted(questions, key=lambda q: q["tokens"], reverse=True)
pcts  = [q["tokens"] / total_tokens * 100 for q in sorted_qs]
ids   = [q["id"] for q in sorted_qs]
cols  = [LVL_COL[q["level"]] for q in sorted_qs]

bars = ax3.bar(range(len(sorted_qs)), pcts, color=cols,
               edgecolor="white", linewidth=0.8, zorder=3)
for i, (bar, pct) in enumerate(zip(bars, pcts)):
    ax3.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + 0.4,
             f"{pct:.0f}%", ha="center", va="bottom",
             fontsize=8, fontweight="bold")

ax3.set_xticks(range(len(sorted_qs)))
ax3.set_xticklabels(ids, fontsize=9)
ax3.set_ylabel("% of total tokens", fontsize=9)
ax3.spines["left"].set_visible(True)
ax3.spines["left"].set_color(C_RULE)
ax3.spines["bottom"].set_visible(True)
ax3.spines["bottom"].set_color(C_RULE)
ax3.grid(axis="y", color=C_RULE, linewidth=0.5)

top2_pct = sorted_qs[0]["tokens"]/total_tokens*100 + sorted_qs[1]["tokens"]/total_tokens*100
ax3.text(0.5, 0.96,
         f"2 questions account for ~{top2_pct:.0f}% of compute",
         ha="center", va="top", fontsize=8.5,
         fontweight="bold", color=C_AMBER,
         transform=ax3.transAxes)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT 4: Cost vs Difficulty scatter
# ─────────────────────────────────────────────────────────────────────────────
ax4 = fig.add_subplot(gs[1, 0])
ax4.set_title("Cost vs Difficulty Mismatch",
              fontweight="bold", pad=10, fontsize=11)

lvl_x  = {"Easy": 0, "Medium": 1, "Hard": 2}
jitter = {"Q24":-0.18, "Q25": 0.00, "Q26": 0.18,
           "Q27": 0.00,
           "Q28":-0.18, "Q30": 0.00, "Q123": 0.18,
           "Q124":-0.12, "Q125": 0.12}

label_offsets = {
    "Q24": (-0.01, -0.004, "right"),
    "Q25": ( 0.00,  0.003, "center"),
    "Q26": ( 0.01, -0.004, "left"),
    "Q27": ( 0.00,  0.003, "center"),
    "Q28": (-0.01,  0.003, "right"),
    "Q30": ( 0.00, -0.004, "center"),
    "Q123":( 0.01,  0.003, "left"),
    "Q124":(-0.01, -0.004, "right"),
    "Q125":( 0.01,  0.003, "left"),
}

for q in questions:
    x   = lvl_x[q["level"]] + jitter.get(q["id"], 0)
    col = LVL_COL[q["level"]]
    ax4.scatter(x, q["cost"], s=130, color=col,
                zorder=4, edgecolors="white", linewidth=0.9)
    lox, loy, lha = label_offsets.get(q["id"], (0, 0.002, "center"))
    ax4.text(x + lox, q["cost"] + loy, q["id"],
             ha=lha, va="bottom" if loy > 0 else "top",
             fontsize=7.5, color=col, fontweight="bold")

ax4.set_xticks([0, 1, 2])
ax4.set_xticklabels(["Easy", "Medium", "Hard"], fontsize=10)
ax4.set_ylabel("Cost ($)", fontsize=9)
ax4.set_xlim(-0.5, 2.5)
ax4.set_ylim(-0.005, max(q["cost"] for q in questions) * 1.30)
ax4.spines["bottom"].set_visible(True)
ax4.spines["bottom"].set_color(C_RULE)
ax4.spines["left"].set_visible(True)
ax4.spines["left"].set_color(C_RULE)
ax4.grid(axis="y", color=C_RULE, linewidth=0.5)

q25 = next(q for q in questions if q["id"] == "Q25")
ax4.annotate(
    "Easy label,\nhighest cost\n(5k Monte Carlo sims)",
    xy=(lvl_x["Easy"] + jitter["Q25"], q25["cost"]),
    xytext=(0.7, q25["cost"] - 0.016),
    fontsize=7, color=LVL_COL["Easy"],
    arrowprops=dict(arrowstyle="->", color=LVL_COL["Easy"], lw=0.9)
)

ax4.text(0.5, -0.15,
         "Benchmark difficulty does not explain compute cost",
         ha="center", va="bottom", fontsize=8.5,
         fontweight="bold", color=C_BLUE,
         transform=ax4.transAxes)

for lv, col in LVL_COL.items():
    ax4.scatter([], [], color=col, label=lv, s=80)
ax4.legend(fontsize=8, loc="upper right", framealpha=0.9)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT 5: Prompt quality changes cost behaviour (slope chart)
# ─────────────────────────────────────────────────────────────────────────────
ax5 = fig.add_subplot(gs[1, 1])
ax5.set_title("Prompt Quality Changes Cost Behaviour",
              fontweight="bold", pad=10, fontsize=11)

needs_fix = [q for q in questions if not q["initial"]]
x_pos = [0, 1]
ax5.set_xlim(-0.3, 1.3)
ax5.set_ylim(-0.005, max(q["cost"] for q in questions) * 1.25)
ax5.set_xticks([0, 1])
ax5.set_xticklabels(["Initial\nWrong Prompt", "Corrected\nPrompt"], fontsize=10)
ax5.set_ylabel("Cost ($)", fontsize=9)
ax5.spines["bottom"].set_visible(True)
ax5.spines["bottom"].set_color(C_RULE)
ax5.spines["left"].set_visible(True)
ax5.spines["left"].set_color(C_RULE)
ax5.grid(axis="y", color=C_RULE, linewidth=0.5)

for q in needs_fix:
    col   = LVL_COL[q["level"]]
    y0    = q["init_cost"]
    y1    = q["cost"]
    arrow_col = C_RED if y1 > y0 else C_GREEN
    ax5.plot([0, 1], [y0, y1], color=col,
             linewidth=1.8, alpha=0.85, zorder=3)
    ax5.scatter([0], [y0], color=col, s=70, zorder=4, edgecolors="white")
    ax5.scatter([1], [y1], color=col, s=70, zorder=4, edgecolors="white")
    offset = 0.0015 if y1 > y0 else -0.0025
    ax5.text(1.02, y1 + offset, q["id"],
             fontsize=7.5, color=col, fontweight="bold", va="center")

ax5.text(0.5, 0.96,
         "Prompt fixes can increase or decrease cost",
         ha="center", va="top", fontsize=8,
         color=C_MUTED, transform=ax5.transAxes)

# ─────────────────────────────────────────────────────────────────────────────
# PLOT 6: Q25 Statistical Method Disagreement
# ─────────────────────────────────────────────────────────────────────────────
ax6 = fig.add_subplot(gs[1, 2])
ax6.axis("off")
ax6.set_title("Q25: Statistical Method Disagreement",
              fontweight="bold", pad=10, fontsize=11)

# Two method boxes side by side
box_w, box_h = 0.42, 0.52
ax6.add_patch(patches.FancyBboxPatch(
    (0.02, 0.40), box_w, box_h,
    boxstyle="round,pad=0.02",
    transform=ax6.transAxes,
    facecolor="#fce4ec", edgecolor=C_RED, linewidth=1.3
))
ax6.add_patch(patches.FancyBboxPatch(
    (0.56, 0.40), box_w, box_h,
    boxstyle="round,pad=0.02",
    transform=ax6.transAxes,
    facecolor="#e8f5e9", edgecolor=C_GREEN, linewidth=1.3
))

ax6.text(0.23, 0.90, "AGENT METHOD",
         ha="center", va="top", fontsize=8.5,
         fontweight="bold", color=C_RED,
         transform=ax6.transAxes)
ax6.text(0.77, 0.90, "BENCHMARK METHOD",
         ha="center", va="top", fontsize=8.5,
         fontweight="bold", color=C_GREEN,
         transform=ax6.transAxes)

agent_lines = [
    "Shapiro-Wilk Test",
    "W = 0.994",
    "p ≈ 0",
    "Ran 5,000 Monte Carlo sims",
    "Result: NOT NORMAL",
]
bench_lines = [
    "Skewness Rule",
    "skew = 0.284",
    "< 0.5",
    "Practical DA heuristic",
    "Result: NORMAL",
]

ay, by = 0.83, 0.83
for al, bl in zip(agent_lines, bench_lines):
    ax6.text(0.23, ay, al, ha="center", va="top",
             fontsize=7.8, color=C_RED,
             transform=ax6.transAxes)
    ax6.text(0.77, by, bl, ha="center", va="top",
             fontsize=7.8, color=C_GREEN,
             transform=ax6.transAxes)
    ay -= 0.087
    by -= 0.087

ax6.text(0.5, 0.56, "VS",
         ha="center", va="center", fontsize=13,
         fontweight="bold", color=C_MUTED,
         transform=ax6.transAxes)

# Verdict box
ax6.add_patch(patches.FancyBboxPatch(
    (0.03, 0.02), 0.94, 0.34,
    boxstyle="round,pad=0.02",
    transform=ax6.transAxes,
    facecolor=C_BG, edgecolor=C_BLUE, linewidth=1.3
))
ax6.text(0.5, 0.34,
         "Both answers are statistically defensible",
         ha="center", va="top", fontsize=8.5,
         fontweight="bold", color=C_BLUE,
         transform=ax6.transAxes)
ax6.text(0.5, 0.24,
         "At n=1,338, Shapiro-Wilk detects trivial departures\n"
         "from normality. Benchmark uses a practical DA heuristic.\n"
         "This is a prompt specification issue,\nnot a reasoning failure.",
         ha="center", va="top", fontsize=7.2,
         color=C_MUTED, transform=ax6.transAxes)

plt.savefig("/home/oishika/dabench_results_final.png", dpi=150,
            bbox_inches="tight", facecolor=C_BG)
plt.show()
print("Saved: /home/oishika/dabench_results_final.png")
