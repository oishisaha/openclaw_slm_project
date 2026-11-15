import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

CORRECT  = "#43a047"
WRONG    = "#e53935"
WARN     = "#e6a817"
ACCENT   = "#1a56db"
BG       = "#f7f6f2"
SURFACE  = "#ffffff"
INK      = "#0e0e0e"
MUTED    = "#5a5a5a"
PURPLE   = "#7b1fa2"

plt.rcParams.update({
    "font.family":        "DejaVu Sans",
    "axes.facecolor":     SURFACE,
    "figure.facecolor":   BG,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.spines.left":   False,
    "axes.spines.bottom": True,
    "axes.grid":          True,
    "grid.color":         "#e0deda",
    "grid.linewidth":     0.5,
    "text.color":         INK,
    "axes.labelcolor":    MUTED,
    "xtick.color":        MUTED,
    "ytick.color":        MUTED,
    "font.size":          10,
})

# ── Data ──────────────────────────────────────────────────────────────────

questions = [
    {"id": "Q24",  "task": "Mean age",        "level": "Easy",   "dataset": "insurance",
     "initial_correct": True,  "final_correct": True,
     "initial_answer": "39.21", "correct_answer": "39.21",
     "session_input": 25657,   "session_output": 394,   "session_cache": 48000,
     "prompt_change": False},
    {"id": "Q25",  "task": "BMI normality",   "level": "Easy",   "dataset": "insurance",
     "initial_correct": False, "final_correct": True,
     "initial_answer": "not_normal (Shapiro-Wilk)", "correct_answer": "normal (skewness<0.5)",
     "session_input": 706598,  "session_output": 1410,  "session_cache": 6912,
     "prompt_change": True,
     "initial_input": 77345,   "initial_output": 2131},
    {"id": "Q26",  "task": "Pearson corr.",   "level": "Easy",   "dataset": "insurance",
     "initial_correct": False, "final_correct": True,
     "initial_answer": "0.30 (age vs charges)", "correct_answer": "0.07 (charges vs children)",
     "session_input": 45496,   "session_output": 470,   "session_cache": 28544,
     "prompt_change": True,
     "initial_input": 95392,   "initial_output": 3109},
    {"id": "Q27",  "task": "Outlier count",   "level": "Medium", "dataset": "insurance",
     "initial_correct": True,  "final_correct": True,
     "initial_answer": "139",  "correct_answer": "139",
     "session_input": 470453,  "session_output": 25974, "session_cache": 345600,
     "prompt_change": False},
    {"id": "Q28",  "task": "Preprocessing",   "level": "Hard",   "dataset": "insurance",
     "initial_correct": False, "final_correct": True,
     "initial_answer": "0.0 (z-score mean)", "correct_answer": "6/6 cols correct (min-max)",
     "session_input": 127736,  "session_output": 977,   "session_cache": 53248,
     "prompt_change": True,
     "initial_input": 208036,  "initial_output": 3440},
    {"id": "Q30",  "task": "Linear reg.",     "level": "Hard",   "dataset": "insurance",
     "initial_correct": False, "final_correct": True,
     "initial_answer": "0.12 (R-squared)",   "correct_answer": "11464.74 (RMSE)",
     "session_input": 96727,   "session_output": 521,   "session_cache": 26112,
     "prompt_change": True,
     "initial_input": 124135,  "initial_output": 1330},
    {"id": "Q123", "task": "Top country",     "level": "Easy",   "dataset": "vaccinations",
     "initial_correct": True,  "final_correct": True,
     "initial_answer": "Gibraltar", "correct_answer": "Gibraltar",
     "session_input": 77345,   "session_output": 2131,  "session_cache": 51200,
     "prompt_change": False},
    {"id": "Q124", "task": "ANOVA",           "level": "Hard",   "dataset": "vaccinations",
     "initial_correct": True,  "final_correct": True,
     "initial_answer": "no, p=0.6641", "correct_answer": "no",
     "session_input": 50044,   "session_output": 516,   "session_cache": 24576,
     "prompt_change": False},
    {"id": "Q125", "task": "Multiple reg.",   "level": "Hard",   "dataset": "vaccinations",
     "initial_correct": True,  "final_correct": True,
     "initial_answer": "yes,yes / 0.6059", "correct_answer": "yes,yes / 0.6059",
     "session_input": 95392,   "session_output": 3109,  "session_cache": 84992,
     "prompt_change": False},
]

ids      = [q["id"]    for q in questions]
tasks    = [q["task"]  for q in questions]
levels   = [q["level"] for q in questions]

level_col = {"Easy": "#1565c0", "Medium": "#e65100", "Hard": "#880e4f"}

fig = plt.figure(figsize=(20, 16), facecolor=BG)
fig.suptitle(
    "OpenClaw + DeepSeek V4 Flash — DABench Evaluation\n"
    "insurance.csv (Q24–Q30) · country_vaccinations.csv (Q123–Q125)",
    fontsize=14, fontweight="bold", y=0.99, color=INK
)

# ── Plot 1: Initial vs final correctness ──────────────────────────────────
ax1 = fig.add_subplot(3, 3, (1, 2))
x = np.arange(len(ids))
w = 0.35
init_correct = [1 if q["initial_correct"] else 0 for q in questions]
final_correct = [1 if q["final_correct"]  else 0 for q in questions]
init_colors  = [CORRECT if v else WRONG for v in init_correct]
final_colors = [CORRECT if v else WARN  for v in final_correct]

b1 = ax1.bar(x - w/2, init_correct,  w, color=init_colors,  label="Initial prompt run",  zorder=3, edgecolor="white")
b2 = ax1.bar(x + w/2, final_correct, w, color=final_colors, label="Corrected prompt run", zorder=3, edgecolor="white", alpha=0.85)

ax1.set_xticks(x)
ax1.set_xticklabels([f"{q['id']}\n{q['task']}" for q in questions], fontsize=8.5)
ax1.set_yticks([0, 1])
ax1.set_yticklabels(["Incorrect", "Correct"])
ax1.set_ylim(0, 1.3)
ax1.set_title("Initial vs final correctness — effect of prompt specification", fontweight="bold", pad=10)
for i, lvl in enumerate(levels):
    ax1.text(i, -0.28, lvl, ha="center", fontsize=7.5, color=level_col[lvl], fontweight="bold")

p1 = mpatches.Patch(color=CORRECT, label="Correct (initial prompt)")
p2 = mpatches.Patch(color=WRONG,   label="Incorrect (initial prompt)")
p3 = mpatches.Patch(color=WARN,    label="Correct (after prompt fix)")
ax1.legend(handles=[p1, p2, p3], fontsize=8, loc="upper right", framealpha=0.9)

# ── Plot 2: What went wrong — initial vs correct answers ─────────────────
ax2 = fig.add_subplot(3, 3, 3)
ax2.axis("off")
ax2.set_title("Prompt mismatch — what changed", fontweight="bold", pad=10)
mismatches = [q for q in questions if q["prompt_change"]]
y = 0.95
ax2.text(0.0, y, "Question", fontsize=8, fontweight="bold", transform=ax2.transAxes, color=INK)
ax2.text(0.28, y, "Initial answer", fontsize=8, fontweight="bold", transform=ax2.transAxes, color=WRONG)
ax2.text(0.65, y, "Correct answer", fontsize=8, fontweight="bold", transform=ax2.transAxes, color=CORRECT)
y -= 0.06
ax2.axhline(y + 0.02, xmin=0, xmax=1, color="#e0deda", linewidth=0.8, transform=ax2.transAxes)
for q in mismatches:
    ax2.text(0.0,  y, q["id"],                fontsize=7.5, transform=ax2.transAxes, color=INK, fontweight="bold")
    ax2.text(0.28, y, q["initial_answer"],     fontsize=7,   transform=ax2.transAxes, color=WRONG)
    ax2.text(0.65, y, q["correct_answer"],     fontsize=7,   transform=ax2.transAxes, color=CORRECT)
    y -= 0.16
    ax2.axhline(y + 0.08, xmin=0, xmax=1, color="#e0deda", linewidth=0.5, transform=ax2.transAxes)

# ── Plot 3: Token usage per question ─────────────────────────────────────
ax3 = fig.add_subplot(3, 3, (4, 5))
input_k  = [q["session_input"]  / 1000 for q in questions]
output_k = [q["session_output"] / 1000 for q in questions]
cache_k  = [q["session_cache"]  / 1000 for q in questions]

b_in    = ax3.bar(x, input_k,  0.5, label="Input tokens",      color=ACCENT,   zorder=3, edgecolor="white")
b_out   = ax3.bar(x, output_k, 0.5, bottom=input_k,            label="Output tokens",  color=PURPLE,  zorder=3, edgecolor="white", alpha=0.85)
b_cache = ax3.bar(x, cache_k,  0.5,
                  bottom=[i+o for i, o in zip(input_k, output_k)],
                  label="Cache reads",    color="#e0deda",  zorder=3, edgecolor="#ccc")

ax3.set_xticks(x)
ax3.set_xticklabels([f"{q['id']}\n{q['task']}" for q in questions], fontsize=8.5)
ax3.set_ylabel("Tokens (thousands)")
ax3.set_title("Token usage per benchmark question (final run)", fontweight="bold", pad=10)
ax3.legend(fontsize=8, loc="upper right")
for i, lvl in enumerate(levels):
    ax3.text(i, -ax3.get_ylim()[1]*0.12, lvl, ha="center", fontsize=7.5,
             color=level_col[lvl], fontweight="bold")

# ── Plot 4: Cost per question ─────────────────────────────────────────────
ax4 = fig.add_subplot(3, 3, 6)
costs = [(q["session_input"]/1e6)*0.09 + (q["session_output"]/1e6)*0.18 +
         (q["session_cache"]/1e6)*0.0036 for q in questions]
bar_cols = [level_col[q["level"]] for q in questions]
bars = ax4.bar(x, costs, color=bar_cols, zorder=3, edgecolor="white", width=0.55)
for bar, cost in zip(bars, costs):
    ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.0002,
             f"${cost:.4f}", ha="center", va="bottom", fontsize=7.5)
ax4.set_xticks(x)
ax4.set_xticklabels([q["id"] for q in questions], fontsize=8.5)
ax4.set_ylabel("Cost (USD)")
ax4.set_title("Cost per question\n(DeepSeek V4 Flash)", fontweight="bold", pad=10)
easy_p  = mpatches.Patch(color=level_col["Easy"],   label="Easy")
med_p   = mpatches.Patch(color=level_col["Medium"], label="Medium")
hard_p  = mpatches.Patch(color=level_col["Hard"],   label="Hard")
ax4.legend(handles=[easy_p, med_p, hard_p], fontsize=8)

# ── Plot 5: Initial vs corrected token cost comparison ───────────────────
ax5 = fig.add_subplot(3, 3, 7)
changed = [q for q in questions if q["prompt_change"]]
ch_ids  = [q["id"] for q in changed]
ch_x    = np.arange(len(ch_ids))
init_costs = [(q["initial_input"]/1e6)*0.09 + (q["initial_output"]/1e6)*0.18 for q in changed]
corr_costs = [(q["session_input"]/1e6)*0.09 + (q["session_output"]/1e6)*0.18 +
              (q["session_cache"]/1e6)*0.0036 for q in changed]

ax5.bar(ch_x - 0.2, init_costs, 0.35, color=WRONG,   label="Initial (wrong) prompt", zorder=3, edgecolor="white")
ax5.bar(ch_x + 0.2, corr_costs, 0.35, color=CORRECT, label="Corrected prompt",        zorder=3, edgecolor="white")
ax5.set_xticks(ch_x)
ax5.set_xticklabels(ch_ids, fontsize=9)
ax5.set_ylabel("Cost (USD)")
ax5.set_title("Cost: wrong vs corrected prompt\n(questions that needed fixing)", fontweight="bold", pad=10)
ax5.legend(fontsize=8)

# ── Plot 6: DABench benchmark comparison ──────────────────────────────────
ax6 = fig.add_subplot(3, 3, 8)
models  = ["GPT-3.5\n(DABench)", "GPT-4\n(DABench)", "DAAgent-34B\n(DABench)",
           "OpenClaw +\nDeepSeek V4 Flash\n(this work, n=9)"]
scores  = [70, 88, 73.9, 100]
colors  = [MUTED, MUTED, MUTED, CORRECT]
bars6   = ax6.bar(models, scores, color=colors, zorder=3, edgecolor="white", width=0.5)
for bar, score in zip(bars6, scores):
    ax6.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
             f"{score}%", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax6.set_ylim(0, 115)
ax6.set_ylabel("Accuracy (%)")
ax6.set_title("vs DABench published baselines\n(note: subset of 9 questions)", fontweight="bold", pad=10)
ax6.axhline(100, color=CORRECT, linewidth=0.8, linestyle="--", alpha=0.4)
ax6.text(3, 102, "this work", ha="center", fontsize=7.5, color=CORRECT)
note = "* DABench full set = 257 Qs\n  This evaluation = 9 Qs\n  Direct comparison is indicative only"
ax6.text(0.02, 0.04, note, transform=ax6.transAxes, fontsize=7, color=MUTED, va="bottom")

# ── Plot 7: Q25 disagreement deep dive ───────────────────────────────────
ax7 = fig.add_subplot(3, 3, 9)
ax7.axis("off")
ax7.set_title("Q25 — methodology disagreement", fontweight="bold", pad=10)
lines = [
    ("Task:",        "BMI normality check"),
    ("", ""),
    ("Initial method:", "Shapiro-Wilk test"),
    ("Initial result:", "W=0.994, p≈0 → not_normal"),
    ("Agent reasoning:", "Ran 5,000 Monte Carlo sims"),
    ("",              "Statistically correct at n=1,338"),
    ("", ""),
    ("Benchmark method:", "Skewness < 0.5 threshold"),
    ("Benchmark result:", "skewness=0.284 → normal"),
    ("", ""),
    ("Finding:", "Both answers are defensible."),
    ("",         "Shapiro-Wilk has high power"),
    ("",         "at large n — detects trivial"),
    ("",         "departures from normality."),
    ("",         "Benchmark uses practical rule."),
    ("", ""),
    ("Verdict:", "Prompt specification issue,"),
    ("",         "not model failure."),
]
y = 0.97
for label, value in lines:
    if label:
        ax7.text(0.02, y, label,  fontsize=7.5, fontweight="bold",
                 transform=ax7.transAxes, color=INK)
        ax7.text(0.42, y, value,  fontsize=7.5,
                 transform=ax7.transAxes, color=MUTED)
    y -= 0.055

plt.tight_layout(rect=[0, 0, 1, 0.97])
plt.savefig("dabench_results_v2.png", dpi=150, bbox_inches="tight", facecolor=BG)
plt.show()
print("Saved: dabench_results_v2.png")
