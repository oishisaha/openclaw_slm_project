import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

# ======================================================
# THEME
# ======================================================

CORRECT = "#43a047"
WRONG = "#e53935"
WARN = "#e6a817"
BLUE = "#1565c0"
ORANGE = "#e65100"
RED = "#880e4f"
GREY = "#777777"
BG = "#f7f6f2"
SURFACE = "white"
INK = "#111111"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "figure.facecolor": BG,
    "axes.facecolor": SURFACE,
    "axes.spines.top": False,
    "axes.spines.right": False,
    "axes.grid": True,
    "grid.alpha": 0.25,
})


# ======================================================
# DATA
# ======================================================

questions = [
    ("Q24", "Mean age", "Easy", True, True, 25657, 394, 48000, False),
    ("Q25", "BMI normality", "Easy", False, True, 706598, 1410, 6912, True),
    ("Q26", "Correlation", "Easy", False, True, 45496, 470, 28544, True),
    ("Q27", "Outlier count", "Medium", True, True, 470453, 25974, 345600, False),
    ("Q28", "Preprocess", "Hard", False, True, 127736, 977, 53248, True),
    ("Q30", "Regression", "Hard", False, True, 96727, 521, 26112, True),
    ("Q123", "Country", "Easy", True, True, 77345, 2131, 51200, False),
    ("Q124", "ANOVA", "Hard", True, True, 50044, 516, 24576, False),
    ("Q125", "Multi reg", "Hard", True, True, 95392, 3109, 84992, False),
]

ids = [q[0] for q in questions]

level_map = {"Easy": 1, "Medium": 2, "Hard": 3}
level_colors = {"Easy": BLUE, "Medium": ORANGE, "Hard": RED}


fig = plt.figure(figsize=(20, 15))
fig.suptitle(
    "OpenClaw + DeepSeek V4 Flash — DABench Evaluation Analysis\n"
    "Accuracy Recovery · Prompt Failures · Cost Behaviour",
    fontsize=16,
    weight="bold",
)


# ======================================================
# 1. BEFORE / AFTER OUTCOME MATRIX
# ======================================================

ax1 = fig.add_subplot(2, 3, 1)

matrix = np.array([
    [1 if q[3] else 0 for q in questions],
    [1 if q[4] else 0 for q in questions],
])

ax1.imshow(matrix, aspect="auto", cmap="Greens")

for y in range(2):
    for x in range(len(ids)):
        text = "✓" if matrix[y, x] else "✗"
        color = "white" if matrix[y, x] else "#333333"
        ax1.text(x, y, text, ha="center", va="center", fontsize=18, color=color, weight="bold")

ax1.set_xticks(range(len(ids)))
ax1.set_xticklabels(ids, fontsize=9)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(["Initial Prompt", "Fixed Prompt"], fontsize=9)
ax1.set_title("Before / After Outcome Matrix", weight="bold", pad=10)
ax1.text(0.5, -0.12, "Prompt refinement recovered 4/4 failures → final accuracy 100%", transform=ax1.transAxes, ha="center", fontsize=9, color=GREY)


# ======================================================
# 2. FAILURE DIAGNOSIS FLOW CARDS
# ======================================================

ax2 = fig.add_subplot(2, 3, 2)
ax2.axis("off")
ax2.set_title("Failure Diagnosis: Specification Mismatch", weight="bold", pad=10)

cards = [
    ("Q25", "Shapiro-Wilk\n→\nSkewness rule"),
    ("Q26", "Wrong variables\n(age vs charges)"),
    ("Q28", "Z-score\n→\nMin-max scaling"),
    ("Q30", "R² metric\n→\nRMSE metric"),
]

y = 0.9
for q, msg in cards:
    ax2.text(0.05, y, f"{q}\n{msg}\n↓\nFixed Prompt ✓", bbox=dict(boxstyle="round", fc="#f2f2f2", ec="#dddddd"), fontsize=9)
    y -= 0.23


# ======================================================
# 3. TOKEN PARETO
# ======================================================

ax3 = fig.add_subplot(2, 3, 3)

tokens = np.array([q[5] + q[6] + q[7] for q in questions])
order = np.argsort(tokens)[::-1]
sorted_ids = np.array(ids)[order]
sorted_tokens = tokens[order]
percent = sorted_tokens / sorted_tokens.sum() * 100

ax3.bar(sorted_ids, percent, color=BLUE, alpha=0.9)
for i, v in enumerate(percent):
    ax3.text(i, v + 1.0, f"{v:.0f}%", ha="center", fontsize=8)
ax3.set_ylabel("% of total tokens")
ax3.set_title("Token Usage Concentration", weight="bold", pad=10)
ax3.text(0.02, 0.95, "2 questions account for ~70% of compute", transform=ax3.transAxes, fontsize=8, color=GREY)


# ======================================================
# 4. COST VS DIFFICULTY SCATTER
# ======================================================

ax4 = fig.add_subplot(2, 3, 4)

costs = []
for q in questions:
    c = (q[5] / 1e6) * 0.09 + (q[6] / 1e6) * 0.18 + (q[7] / 1e6) * 0.0036
    costs.append(c)

for q, c in zip(questions, costs):
    ax4.scatter(level_map[q[2]], c, s=(q[5] + q[6]) / 3000, color=level_colors[q[2]], alpha=0.8)
    ax4.text(level_map[q[2]], c, q[0], fontsize=8)

ax4.set_xticks([1, 2, 3])
ax4.set_xticklabels(["Easy", "Medium", "Hard"])
ax4.set_ylabel("Cost ($)")
ax4.set_title("Cost vs Difficulty Mismatch", weight="bold", pad=10)
ax4.text(0.02, 0.95, "Benchmark difficulty does not explain compute cost", transform=ax4.transAxes, fontsize=8, color=GREY)


# ======================================================
# 5. COST SLOPE CHART
# ======================================================

ax5 = fig.add_subplot(2, 3, 5)

changes = {
    "Q25": (0.007, 0.064),
    "Q26": (0.009, 0.004),
    "Q28": (0.020, 0.012),
    "Q30": (0.012, 0.009),
}

for q, (a, b) in changes.items():
    ax5.plot([0, 1], [a, b], marker="o", color=BLUE, linewidth=1.5)
    ax5.text(-0.08, a, q, fontsize=8)

ax5.set_xticks([0, 1])
ax5.set_xticklabels(["Initial\nWrong Prompt", "Corrected\nPrompt"])
ax5.set_ylabel("Cost ($)")
ax5.set_title("Prompt Quality Changes Cost Behaviour", weight="bold", pad=10)
ax5.text(0.02, 0.95, "Prompt fixes can increase or decrease cost", transform=ax5.transAxes, fontsize=8, color=GREY)


# ======================================================
# 6. Q25 METHOD COMPARISON
# ======================================================

ax6 = fig.add_subplot(2, 3, 6)
ax6.axis("off")
ax6.set_title("Q25: Statistical Method Disagreement", weight="bold", pad=10)

text = """
AGENT METHOD
Shapiro-Wilk Test
W = 0.994
p ≈ 0
Result: NOT NORMAL

BENCHMARK METHOD
Skewness Rule
skew = 0.284 < 0.5
Result: NORMAL

Verdict:
Prompt specification mismatch,
not reasoning failure
"""

ax6.text(0.05, 0.05, text, fontsize=10, bbox=dict(boxstyle="round", fc="#f2f2f2", ec="#dddddd"))


plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig("/home/oishika/dabench_results_v4.png", dpi=300, bbox_inches="tight", facecolor=BG)
plt.show()
print("Saved: /home/oishika/dabench_results_v4.png")
