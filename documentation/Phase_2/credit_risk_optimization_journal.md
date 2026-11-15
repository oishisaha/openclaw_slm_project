---
title: Credit Risk Test Suite - Optimization Journal
author: Oishika Saha
date: 2026-08-25
version: 1.0
---

<br>

## If Viewing this on VS-Code, just press (ctrl + shift + v), to view markdown mode.

<br>

**Gemma 4 12B — DA Credit Risk Test Suite (CR01–CR27) — Trials 1 through 12**

## 1. Purpose & Scope

This journal documents the section-by-section optimization of the OpenClaw + Gemma 4 12B agent configuration (SOUL.md, AGENTS.md) against the DA Credit Risk multi-turn test suite (CR01–CR27, later re-labeled C01–C18 and V01–V09 in the tracking workbook). It follows the project's locked additive optimization methodology: test a section, fix only what fails, lock the passing config as a floor, advance.

This section of testing was halted after Trial 12 to move to the Hallucination/Dirty Data test set. Trial 12 represents the current best-achieved state and is documented as such, including its known open issue.

## 2. Ground Truth Provenance

Ground truth values for C01–C18 were independently verified against a source report (DBA5106 Group Project 2: "Asymmetric Cost Classification for Credit Risk") and reproduced from scratch against the actual CSV files (`german_train_80.csv`, `german_val_20.csv`, `german_train_pipelineB.csv`, `german_val_pipelineB.csv`) using Python/pandas/scikit-learn/CatBoost, rather than trusted at face value. This independent reproduction was essential — it definitively separated cases where the model's answer was wrong due to a bug in its code from cases where the ground truth itself needed scrutiny.

## 3. Failure Taxonomy Additions From This Testing Round

Several failure patterns surfaced during Credit Risk testing that were not fully captured by the project's existing Type A/D/E/F/G taxonomy. These are documented here as they were identified, in the order discovered:

- **Third-party API hallucination** — the model invents plausible-sounding but nonexistent library method/parameter names (e.g. CatBoost's `loss_function` string, `get_fold_iterations_logloss()`, sklearn's `tree_.n_samples`) rather than the real API. Distinct from Type F because the model does attempt genuine computation — the bug is in library-call correctness, not in whether it computed at all.

- **Silent post-error fabrication** — an exec call raises an exception, and rather than surfacing that failure, the model reports a plausible-looking numeric answer anyway. Confirmed directly for the Decision Tree Gini computation (C06), which used a non-existent `tree_.n_samples` attribute in every attempt across five trials before the true error was diagnosed via independent reproduction.

- **Cross-question value contamination** — a numeric answer for one question exactly matches a different question's answer (different model, different metric), most plausibly explained by the model reusing a recently-seen value from its own context rather than recomputing fresh. Recurred multiple times (C06/C05 val_auc match in Trial 4; C17/C14 threshold+cost match in Trial 8) even after a dedicated rule was added.

- **Workspace script contamination** — accumulated leftover .py scripts and output files from prior trials sitting in the shared workspace, creating a risk that a fresh session reads/reuses stale code or output rather than generating its own. Recurred after being cleared once (Trial 6), needing a second clearing before Trial 11.

- **Stated-rule / executed-behavior gap** — the model can accurately describe a rule it is supposed to follow (e.g. explicitly writing "I should have saved champion_val_probs.npy as per instructions") while never actually executing the code that would satisfy it. Confirmed directly in Trial 12's session log for the champion-model-reuse rule, which was never followed despite being clearly stated in AGENTS.md across four prior trials.

- **Background-process abandonment** — a long-running exec call (e.g. 1000-iteration CatBoost fit) is polled once, not re-polled to completion, and abandoned in favor of launching a duplicate run — repeated ~13 times in a single turn in Trial 2, contributing to a session crash.

- **Best-iteration vs. final-iteration confusion** — with `use_best_model=True` set, `predict_proba()` reflects the best iteration, not the final one; computing "final" metrics via `predict_proba()` + `log_loss()` silently returns best-iteration values instead.

## 4. Trial-by-Trial Log

### Trial 1 — Baseline

**Verdict: Session crashed mid-run — context/resource exhaustion**

**Config changes going in**
- None — carried-forward config from Capability Tests, no Credit Risk-specific edits yet.

**What happened**
- Session split across two `.jsonl` files; the genuine live segment covered only 5 confirmed turns (C17, C18, C21/V04, C22/V05, C25/V08) before crashing on the 6th (C23/V06).
- Token usage exceeded the model's stated 262k context ceiling on 3 of the 5 logged turns (peaks of 316,725 / 276,260 / 284,401), with non-monotonic totals suggesting active context truncation rather than a clean limit-reached stop.
- CR22 (SHAP): model ran `pip install shap` successfully, then never retried the import — fell back to a mislabeled CatBoost-feature-importance bar chart while falsely claiming "unavailable without pip install", directly contradicted by its own prior action in the same session.

**Root cause identified**
- Verbose retry-loop prose (e.g. ~10 near-identical restatements of the same diagnosis on one turn) burning context budget disproportionate to the value produced, compounding across a long multi-turn session.

### Trial 2

**Verdict: Fixes landed for their target bugs — new bug surfaced (background-process abandonment)**

**Config changes going in**
- AGENTS.md — fixed CatBoost `loss_function` naming (correct value is `'Logloss'`, not `'Log_loss'`/`'LogLoss'`).
- AGENTS.md — added rule requiring re-attempt after a corrective action (e.g. pip install) before claiming a capability unavailable.
- AGENTS.md — added Long Session Discipline (concise retries, periodic memory writes) and Background Process Handling (poll same job to completion, don't restart duplicates).

**What happened**
- Every CatBoost call in this session correctly used `loss_function='Logloss'` — zero naming guesses.
- Session stayed well under the context ceiling (crashed at only 44k/262k, 17%) — verbosity fix held.
- New failure: the model ran the same CatBoost training script ~13 times in one turn (C10/C11), each followed by a single process poll on a new session ID rather than re-polling the same one to completion — a background-process abandonment loop, not context exhaustion, caused this crash.

**Root cause identified**
- 1000-iteration CatBoost fit on Pipeline B's categorical data is the slowest model in the suite; the model gave up waiting after one poll and restarted rather than waiting longer.

### Trial 3

**Verdict: No new config — testing whether Trial 2's crash was resolved; new, different bug found**

**Config changes going in**
- None — same config as Trial 2. Session started directly from CR09 rather than CR01.

**What happened**
- No crash this time — confirmed Trial 2's fixes held.
- C09/C11 (CatBoost): train_logloss and val_logloss came back nearly identical to each other (0.3615 / 0.3624) — inconsistent with the expected large train/val gap from a 1000-iteration boosted model.

**Root cause identified**
- Model used non-standard, invented CatBoost method names (`get_fold_iterations_logloss()`, `get_eval_metrics()`, `get_fold_iterations_mse()`) across ~15 near-identical rewrites within a single turn — none of these are real CatBoost API. The correct method, `get_evals_result()`, was never once tried.

### Trial 4

**Verdict: get_evals_result() fix confirmed correct — but a new, distinct false-capability-belief bug found**

**Config changes going in**
- AGENTS.md — added correct CatBoost method name (`get_evals_result()`), replacing guessed alternatives.

**What happened**
- Real accuracy gains: C03 (categorical column count), C06 (Decision Tree gini/auc), C07 (RF Regressor), and C08 (RF Classifier AUC) all moved to exact or near-exact ground-truth matches for the first time.
- C06 val_auc[0.8126] found to be an exact duplicate of C05's val_auc — first confirmed instance of cross-question value contamination.
- C17 min_total_cost[60] exactly matched C12's total_cost[60] from the same trial — second instance of the same pattern.

**Root cause identified**
- The model asserted CatBoost "doesn't have a class_weights parameter" and substituted `scale_pos_weight` instead — a false belief about the library, later independently disproven (class_weights as a list does work and reproduces ground truth almost exactly).

### Trial 5 — Capability Tests carryover, Test8 chart embedding

**Verdict: Not part of Credit Risk sequence — Capability Tests Trial 5 (referenced for continuity)**

**What happened**
- Recorded here only for chronological continuity; substantive Credit Risk work resumes at Trial 6.

### Trial 6

**Verdict: class_weights fix and workspace cleanup did not resolve C09 — genuine execution-time issue found via direct reproduction**

**Config changes going in**
- Workspace cleared of all leftover scripts/PNGs from prior trials.
- SOUL.md — broadened row-count verification rule to explicitly cover column counts too.

**What happened**
- C01 (num_columns) fixed exactly — the broadened verification rule worked.
- C09/C11 CatBoost training call hung/failed after a legitimate self-correction (dropped an invented `iterations_depth=10` parameter), then the log ended entirely with no further tool calls — consistent with a resource-contention stall (CPU-only CatBoost fit competing with Ollama's own inference on the same host) rather than a logic bug.

**Root cause identified**
- C06 (Decision Tree Gini) independently reproduced from the real CSVs and found to require a completely different fix: sklearn's `DecisionTreeClassifier.tree_` has no `n_samples` attribute — the correct attribute is `n_node_samples`. Every prior C06 attempt across every trial used the wrong (nonexistent) attribute name and had been silently erroring the whole time; the model was fabricating a plausible answer after each silent failure.

### Trial 7

**Verdict: C06 fixed cleanly (exact match) — CR10/CR11 consistency test reveals the champion model is not being reused**

**Config changes going in**
- SOUL.md — fixed the `n_node_samples` attribute bug, verified via independent reproduction against real CSVs.
- SOUL.md — added rule: never report a numeric answer if the exec call that produced it raised an error.

**What happened**
- C06 landed on an exact ground-truth match, confirming the attribute fix.
- CR10 and CR11 (identical, deliberately duplicated prompts) returned two different answers from the model — a real consistency failure, and both were wrong relative to ground truth besides.
- Confusion matrix and downstream metrics (C12–C16) badly broken — signature consistent with the champion model being retrained differently, or with incorrect probability extraction, at each reference.

**Root cause identified**
- The model believed CatBoost lacked a `class_weights` parameter and used `scale_pos_weight` as a substitute for some downstream questions but not others within the same session, producing inconsistent underlying models across supposedly-identical champion-model references.

### Trial 8

**Verdict: C10/C11 consistency achieved for the first time — value still wrong; new confusion-matrix arithmetic bug found**

**Config changes going in**
- AGENTS.md — corrected false belief that CatBoost lacks a `class_weights` parameter (independently verified to work); explicit instruction not to substitute `scale_pos_weight`.
- AGENTS.md — added rule requiring the champion model to be trained once and its predictions reused for all downstream questions, rather than retrained from scratch each time.

**What happened**
- CR10 and CR11 (duplicate prompts) returned identical values for the first time — the reuse rule visibly reduced drift.
- Value still incorrect vs. ground truth, with the train/val logloss pattern again too close together.
- C13 confusion matrix: TN+FP+FN+TP summed to 270, not the correct 200 — a new, purely arithmetic bug, independent of model correctness.
- C17 exactly duplicated C14's threshold and cost values — cross-question contamination recurring despite the reuse-model rule.

**Root cause identified**
- With `use_best_model=True`, `predict_proba()` reflects the best iteration, not necessarily the final one; computing "final" logloss via `predict_proba()` + `log_loss()` silently returns the best-iteration value rather than the true final-iteration value that `get_evals_result()` would provide.

### Trial 9

**Verdict: Three targeted fixes shipped — none of the three visibly changed their target behavior**

**Config changes going in**
- SOUL.md — clarified best-iteration vs. final-iteration distinction for `use_best_model=True`; use `get_evals_result()` for true final values.
- SOUL.md — added confusion-matrix sum check (advisory wording: "verify TN+FP+FN+TP equals the total").
- AGENTS.md — added "No Cross-Question Value Reuse" section with explicit instruction to recompute rather than trust matching numbers.

**What happened**
- C09/C11 still train≈val, still far from ground truth.
- C13 confusion matrix still did not sum to 200.
- C18 still exactly duplicated C13's values — the strengthened reuse rule did not prevent it.
- Leaked internal reasoning/formatting tokens appeared directly in the user-facing C09 response.

**Root cause identified**
- Conclusion drawn at this point: individually diagnosed and fixed bugs were not compounding into a working end-to-end champion-model chain when the model was left to reconstruct the approach from memory each time, across a long multi-turn session — motivating the shift to a fully pre-written required script rather than further behavioral guidance.

### Trial 10 — and 10.5

**Verdict: Required-script intervention produced the largest single improvement of the whole series**

**Config changes going in**
- AGENTS.md — replaced behavioral guidance with a required, pre-verified champion-model script (exact CatBoost config, correct final-iteration extraction via `get_evals_result()`) that must be run once and its predictions saved to disk (`champion_val_probs.npy`); all downstream questions instructed to load the saved predictions rather than retraining.

**What happened**
- Trial 10 crashed early (C06) — reverted to the old, broken `tree_.n_samples` attribute despite this being fixed and stable for three straight prior trials, showing a fix can regress without any config change in between.
- Trial 10.5 (same config, re-run): C09/C11 through C18 mostly matched or came very close to ground truth — C13 confusion matrix exact match, C14/C15 exact matches, C18 exact match. The two identical CatBoost prompts (C10/C11) returned identical results for the first time.
- C16 metrics arithmetically inconsistent with their own inputs (accuracy 0.6250 mathematically incompatible with otherwise-correct TP/FN/TN/FP-derived sensitivity/specificity/precision/F1), suggesting the champion-script "load, don't retrain" instruction was not actually followed for this specific question even though the required script's predictions were available.

**Root cause identified**
- The required script closed most of the remaining gap in one trial, but the "load the saved predictions" instruction for downstream questions was still advisory rather than enforced, leaving room for at least one question to diverge.

### Trial 11 — and 11.5

**Verdict: Champion CatBoost values now fully reproducible across trials — confusion matrix still not enforced**

**Config changes going in**
- AGENTS.md — Champion Model section strengthened: must check for `champion_val_probs.npy` on disk before deciding to train vs. load.

**What happened**
- C09/C11 val_auc identical across Trial 10.5 and Trial 11.5 (0.8131 both times) — genuine determinism achieved for the champion model's core metrics, a first for this project.
- C13 confusion matrix still did not sum to 200 in either trial (350 and 300 respectively) — the advisory sum-check rule was not being enforced as executable code.
- C03 (categorical column count) regressed unpredictably across trials (0, 12, 13) despite being untouched by any recent config change.
- Trial 11 crashed again at C09, at only 32k/262k tokens (12%) — ruled out as context exhaustion; pattern consistent with runtime/resource flakiness in the CatBoost fit itself.

**Root cause identified**
- C16's downstream errors traced to the still-unenforced confusion matrix, not a new bug — same root cause as Trial 8/9, now confirmed to persist through two more trials of advisory-only wording.

### Trial 12

**Verdict: Best trial of the entire series — hard assertion fix worked; one remaining bug fully root-caused and confirmed from raw session logs**

**Config changes going in**
- SOUL.md — confusion-matrix check upgraded from advisory language to a hard `assert tn+fp+fn+tp == len(y_val)` that must pass in code before results can be reported.

**What happened**
- C13 confusion matrix: exact ground-truth match (TN119 FP21 FN19 TP41, cost 116) — first exact match ever for this question.
- C14, C15, C18: all exact matches, cascading cleanly from the now-correct C13.
- C09/C11: val_auc[0.8207] — exact match to ground truth, the best CatBoost result of the entire project.
- C16 broke: specificity[1.0000] (implausible — zero false positives at a lowered threshold).

**Root cause identified**
- Session log for C13 contains the model's own comment: "...since they weren't saved in a file by the tool, I will re-run the prediction... In a real flow, I would have saved 'champion_val_probs.npy' as per instructions in the system prompt if I were doing the champion training." This confirms directly, from the raw log rather than inference, that the model understood the required-script rule correctly in plain language but never once executed the training script or the existence check across the entire session — it retrained CatBoost from scratch independently for every one of 8 downstream questions (C09 through C17). Results matched by luck (CatBoost's near-determinism at random_seed=42) for most questions; C16 is where a run-to-run variation in the independent retrain finally produced a visibly wrong answer.
- This is the clearest documented instance of the "stated-rule / executed-behavior gap" pattern (see Section 3) — the model can articulate a rule immediately after violating it, which rules out simple ignorance of the instruction as the cause.

## 5. State at Halt (End of Trial 12)

**Locked / stable**
- C01–C08 (row/column counts, proportions, Ridge, Logistic Regression, Random Forest Regressor/Classifier): stable exact or near-exact matches across 3+ consecutive trials.
- C13, C14, C15, C18 (confusion matrix, threshold sweep, cost reduction, RF reference): exact matches in Trial 12, contingent on the hard-assertion fix.
- C09/C11 (champion CatBoost classifier core metrics): exact match achieved in Trial 12; full determinism across trials confirmed in 10.5/11.5 for the AUC figure specifically.

**Known open issues, not yet resolved**
- C16 (metrics at optimised threshold): breaks intermittently due to the champion model being retrained from scratch rather than loaded from the required saved-predictions file, despite the rule being stated in AGENTS.md across four trials. A stronger fix (mandatory assert on file existence, explicit trigger phrase warning against writing `CatBoostClassifier(...)` in downstream code) was drafted but not yet tested at time of halt.
- C17 (Global SHAP): never resolved across all 12 trials. The shap library import is inconsistently attempted; when it fails or is skipped, the model substitutes CatBoost's raw feature importance and reports it as if it were SHAP, with varying degrees of disclosure. Treated as a standing, documented limitation rather than a target for further config iteration.
- C03 (Pipeline B categorical column count): shows unexplained instability across trials (10, 12, 13, 14, 0 have all been observed) despite no directly related config change — cause not isolated.
- Intermittent crashes at the C09 CatBoost training step recur across multiple trials at low token counts inconsistent with context exhaustion, suggestive of CPU-resource contention between Ollama's own inference and CatBoost's fit on the same host. Documented as an infrastructure-level caveat rather than a prompting target.
- V01–V09 (visualization and executive-deck questions): not attempted in this testing round; the project deliberately narrowed scope to the ML/computation track after Trial 6.

## 6. Cross-Cutting Observations for Write-Up

- Workspace hygiene (clearing leftover scripts between trials) is not something the model does on its own initiative; contamination reoccurred once after being cleared and needed a second manual clearing. This should be documented as a standing operational requirement of the evaluation protocol, not a one-time setup step.
- Several fixes that worked cleanly for 3+ consecutive trials (`n_node_samples`, the Logloss string) still regressed without warning in a later trial with no intervening config change — a caution against treating any single successful trial as proof a fix is permanent.
- The single most effective intervention across the whole series was replacing behavioral instruction with a complete, pre-verified, literal script the model was required to run — a stronger form of the same principle behind the earlier `add_picture()` and Logloss fixes, but applied at the level of an entire multi-step procedure rather than a single API call.
- Even a fully correct, literal script was insufficient on its own to guarantee downstream compliance (the "load, don't retrain" instruction) — indicating a hard, code-level gate (an assertion that fails loudly) is more reliable at this model scale than a written instruction, however clear.
