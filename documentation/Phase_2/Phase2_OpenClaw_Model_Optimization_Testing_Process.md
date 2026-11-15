---
title: OpenClaw Model Optimization — Testing Process
author: Oishika Saha
date: 2026-08-25
version: 1.0
---

<br>

## If Viewing this on VS-Code, just press (ctrl + shift + v), to view markdown mode.

<br>

# This Guide contains 1 component,

A full walkthrough of the Phase 2 configuration-optimization process — how the selected model (Gemma 4 12B) was iteratively tuned via SOUL.md/AGENTS.md prompt engineering, from trial setup through to locking a passing config and moving to the next benchmark suite.

Chapters:
- Chapter 1: Why / When to use this
- Chapter 2: The optimization methodology
- Chapter 3: Setting up a trial
- Chapter 4: Running a trial session
- Chapter 5: Extracting and auditing trial logs
- Chapter 6: Diagnosing a failure
- Chapter 7: Recording trial results in the optimization workbook
- Chapter 8: Locking a fix and advancing
- Chapter 9: Troubleshooting

<br><br><br><br><br><br>

# **Chapter 1** Why / When to use this

Use this guide any time a new optimization trial is run against Gemma 4 12B (or, in principle, any model carried into Phase 2) inside OpenClaw. It documents the trial-and-fix loop end-to-end so every trial is repeatable, auditable, and comparable to the ones before and after it — a fix is only real if it can be shown to hold across consecutive trials, not just the one it was written for.

> The research question this process supports: once a model has been selected via Phase 1's benchmark sweep, how much of the remaining gap to frontier performance can be closed through configuration alone — no fine-tuning, no hyperparameter tuning — and where does configuration-only optimization hit a hard ceiling?

This is a different exercise from Phase 1. Phase 1 (see `Phase1_OpenClaw_Model_Evaluation_Testing_Process.md`) ran every candidate model through an *identical, unmodified* config to compare them fairly. Phase 2 deliberately does the opposite for a single selected model: the config is changed between every trial, and the whole point is to track what changed and why.

<br><br><br><br><br><br>

# **Chapter 2** The optimization methodology

### 2.1 Additive-only

Rules are only ever **added** or **modifed** to SOUL.md/AGENTS.md — never removed, never rewritten from scratch mid-sequence. Once a suite's config passes, that config is the floor for every suite tested afterward. This is what makes the trial log meaningful as a record: a regression can always be traced to either (a) a specific new rule interacting badly with old ones, or (b) the model failing to hold a fix that no config change touched — both of which are findings worth keeping, not just noise.

### 2.2 One suite at a time, trial-by-trial

Optimization proceeds suite by suite (Calc_Tests → Open-Ended → Capability → Credit Risk → Hallucination, or whichever order that phase's run followed — confirm actual sequence against the trial logs for each suite, since the order isn't fixed by this guide). Within a suite:

1. Run a trial against the current config.
2. Diagnose what failed and why (Chapter 6).
3. Make the smallest targeted config change that addresses the root cause — not a broad rewrite.
4. Re-run and confirm the fix held, ideally across more than one trial, before treating it as locked.

### 2.3 Trials are not all equal weight

Some trials exist purely to confirm a previous fix held (e.g. "no new config — testing whether last trial's crash was resolved"); others introduce new config. Both are logged the same way — a clean confirmation trial is exactly as valuable as one that introduces a fix, since a fix that hasn't been re-tested isn't yet trustworthy (see Chapter 6.3 on regressions).

### 2.4 Ground truth is independently reproduced, not trusted at face value

Before a trial's numeric output is judged PASS/FAIL, the ground truth it's being compared against should itself be independently reproduced from the raw data/source methodology wherever practical. This is what separates "the model's code has a bug" from "the ground truth needs scrutiny" — conflating the two burns trials chasing a fix for a problem that doesn't exist in the model.

### 2.5 A trial can be halted mid-suite

A suite's optimization sequence can be deliberately halted before every question is resolved (e.g. to move on to a different suite under time constraints). When this happens, document the halt explicitly: what's locked/stable, what's still open, and why the halt point was chosen — don't let an unfinished suite quietly read as "done."

<br><br><br><br><br><br>

# **Chapter 3** Setting up a trial

### 3.1 Confirm the starting config

Before Trial 1 of a new suite, confirm exactly what config is being carried forward from the previous suite's locked state. Note this explicitly in the trial log even when the answer is "none — carried forward unchanged," since that's itself part of the audit trail.

### 3.2 Make the config edit

Edit SOUL.md / AGENTS.md directly. Keep each edit as narrow as the diagnosed root cause allows — a single wrong method name, a single missing rule, a single advisory-to-hard-assert upgrade. Broad rewrites make it impossible to isolate which change caused which effect in the next trial.

### 3.3 Restart the gateway — every time

```bash
systemctl --user restart openclaw-gateway.service
```

or

```bash
openclaw gateway restart
```

**This is required after every single config edit.** The service does not pick up in-place file changes on its own — running a trial against a config that was edited but never applied is a wasted trial that will look like a mysterious non-fix in the log.

### 3.4 Clear workspace contamination

Check for and remove leftover `.py` scripts, PNGs, and other output files from the previous trial before starting a fresh session. Workspace contamination (a fresh session silently reading or reusing stale code/output from a prior trial) has recurred more than once in this project even after being cleared — it isn't a one-time setup step, it's a per-trial check.

<br><br><br><br><br><br>

# **Chapter 4** Running a trial session

### 4.1 Send prompts word-for-word

Same rule as Phase 1: copy each prompt exactly from the source prompt document, no edits or paraphrasing, so trial-to-trial and model-to-model results stay comparable.

### 4.2 One-shot vs multi-turn, unchanged from Phase 1

Suites keep the same testing method they used in Phase 1 (one session per question for Housing/Hallucination; one continuous multi-turn session for Credit Risk) — Phase 2 optimizes the config, not the testing method.

### 4.3 Note the session ID immediately

Capture the session ID the moment the trial finishes, before starting the next one:

```bash
ls -lat ~/.openclaw/agents/main/sessions/*.jsonl | grep -v trajectory | head -3
```

Do not rely on the "tui-XXXX" ID shown in the app footer — it is a display label and does not reliably match the actual `.jsonl` filename on disk. If a session ID is ever in doubt, confirm by content match rather than assuming:

```bash
grep -l "<unique string from this trial>" ~/.openclaw/agents/main/sessions/*.jsonl
```

<br><br><br><br><br><br>

# **Chapter 5** Extracting and auditing trial logs

Reuses the same two extraction scripts from Phase 1 (`extract_toolcalls.py`, `extract_usage.py`) — see `openclaw_code_audit_guide.md` for the full step-by-step. A few things specific to trial auditing in Phase 2:

### 5.1 Extract every trial, not just the ones that look interesting

A clean-looking trial can still hide a silent issue (e.g. silent post-error fabrication, or a fix that "worked" only because of a lucky retrain). Extract and skim the toolcalls even for trials whose final answer looked fine.

### 5.2 Rule out infrastructure before attributing a failure to the model

Before concluding a trial's failure is a genuine capability or config gap, rule out:
- **Context truncation** — confirm `OLLAMA_CONTEXT_LENGTH`/`num_ctx` was actually set for this session; the ~2048-token default silently truncates a long system prompt without any visible error.
- **Resource contention** — a crash at a low token count (well under the context ceiling) is not context exhaustion; it's more likely CPU/GPU contention between Ollama's own inference and whatever the model's code is running (e.g. a CatBoost fit on the same host).
- **Logging cutoffs** — a usage log that stops partway through a session is a runtime logging artifact, not a sign the trial itself failed.

### 5.3 Verify a fix landed in the code, not just in the model's stated intent

The clearest failure mode surfaced in Phase 2 optimization is the model *describing* a rule correctly in its own reasoning/prose while never actually executing the code that would satisfy it. Confirming a fix "worked" requires checking the tool-call code itself (was the required script actually run? was the file actually checked for/loaded?), not just checking that the final numeric answer happened to be close.

<br><br><br><br><br><br>

# **Chapter 6** Diagnosing a failure

### 6.1 Start from the project's failure taxonomy

Every trial failure should be classified against the existing Type A/D/E/F/G taxonomy first. If a failure doesn't fit any existing type cleanly, that's a signal to consider adding a new taxonomy entry (6.2) rather than force-fitting it.

### 6.2 Failure patterns identified during Phase 2 optimization

These surfaced across trials and are documented as reusable diagnostic categories, not one-off notes:

- **Third-party API hallucination** — the model invents a plausible-sounding but nonexistent library method/parameter name. Distinct from a Type F "no genuine computation" failure because the model *does* attempt real computation — the bug is in library-call correctness, not in whether it computed at all.
- **Silent post-error fabrication** — an exec call raises an exception, and instead of surfacing that failure, the model reports a plausible-looking numeric answer anyway.
- **Cross-question value contamination** — a numeric answer for one question exactly matches a different question's answer, most plausibly from the model reusing a recently-seen value in its own context instead of recomputing fresh.
- **Workspace script contamination** — a fresh trial session reads or reuses stale code/output left over from a previous trial.
- **Stated-rule / executed-behavior gap** — the model can accurately describe a rule it's supposed to follow while never actually executing the code that would satisfy it. This is the single clearest argument for hard code-level assertions over advisory wording (see 6.4).
- **Background-process abandonment** — a long-running exec call is polled once, not re-polled to completion, and abandoned in favor of launching a duplicate run.
- **Best-iteration vs. final-iteration confusion** — with `use_best_model=True` (or equivalent), a prediction method reflects the best checkpoint, not the final one; computing "final" metrics from it silently returns the wrong values.

### 6.3 A fix holding once is not a fix holding

A config change that produces a correct result in the trial it was introduced can still regress in a later trial with **no intervening config change**. Treat 1 clean trial as provisional; treat 3+ consecutive clean trials as the bar for calling something locked/stable.

### 6.4 When advisory wording keeps failing, escalate to a hard assertion

If a behavioral instruction (verify X, check Y before proceeding) fails to hold across multiple trials despite being clearly stated, the next escalation is a hard code-level gate — e.g. an `assert` that must pass in code before results can be reported — rather than restating the instruction more emphatically. Advisory wording depends on the model choosing to follow it every time; an assertion fails loudly and can't be silently skipped.

<br><br><br><br><br><br>

# **Chapter 7** Recording trial results in the optimization workbook

All Phase 2 trial results accumulate in `openclaw_model_optimization.xlsx`. For each suite being optimized, record per trial:

- Trial number (including sub-trials, e.g. "10.5", used for a same-config re-run)
- Config changes going in (or "none — carried forward")
- Verdict (a short headline judgment, e.g. "fixes landed — new bug surfaced")
- What happened (question-by-question observations, not just the aggregate score)
- Root cause identified (or "not yet isolated" — don't leave this blank if a cause is suspected but unconfirmed)

Trial-level narrative detail (the "what happened" / "root cause" write-up) is generally kept in a per-suite optimization journal (e.g. `credit_risk_optimization_journal.md`) rather than crammed into workbook cells — the workbook holds the structured, comparable fields; the journal holds the reasoning trail. Cross-reference between them by trial number.

<br><br><br><br><br><br>

# **Chapter 8** Locking a fix and advancing

A suite is ready to close out and hand its config forward as the floor for the next suite when:

1. Every question in the suite has either an exact/near-exact match against independently-reproduced ground truth, or is documented as a standing, known limitation (not silently dropped).
2. Core metrics have been confirmed stable across at least 2–3 consecutive trials with no intervening config change.
3. Any remaining open issues are written up explicitly — what's broken, the best current root-cause hypothesis, and what a stronger fix would look like — even if that fix wasn't tested before the halt.

At halt, write a short "state at halt" section (locked/stable vs. known open issues) so the next suite's Trial 1 config-carry-forward decision (Chapter 3.1) has something concrete to reference.

<br><br><br><br><br><br>

# **Chapter 9** Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Config edit doesn't seem to change model behavior at all | Gateway wasn't restarted after the edit | `systemctl --user restart openclaw-gateway.service`, then re-run the trial |
| A fix that worked for 3+ trials suddenly regresses with no config change | Model-level inconsistency, not a config problem | Log it as a regression rather than assuming the earlier trials were flukes; don't re-edit the config in response to a single regressed trial |
| Two identical/duplicate prompts in the same session return different answers | The model is not reusing a prior result (e.g. re-training a model instead of loading saved predictions) | Check whether the required "load, don't retrain" instruction is advisory only — escalate to a hard assertion/required script (6.4) |
| A numeric answer looks plausible but is wrong | Possible silent post-error fabrication | Check the raw tool-call log for an exception immediately before the answer was produced, don't just re-verify the final number |
| Trial crashes at a low token count, well under context ceiling | Not context exhaustion — likely resource contention (e.g. CPU-only model fit competing with Ollama's own inference on the same host) | Document as an infrastructure-level caveat; don't treat as a prompting/config target |
| The model states a rule correctly but the trial log shows it wasn't followed | Stated-rule / executed-behavior gap (6.2) | Escalate the rule to a hard code-level assertion rather than restating it |
| Workspace has stale files from a prior trial | Contamination wasn't cleared before this trial started | Clear the workspace (3.4) and re-run; note that this may need to happen more than once across a long sequence |
