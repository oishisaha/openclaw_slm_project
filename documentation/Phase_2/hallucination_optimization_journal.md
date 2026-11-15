---
title: Hallucination / Dirty-Data Suite - Optimization Journal
author: Oishika Saha
date: 2026-08-25
version: 1.0
---

<br>

## If Viewing this on VS-Code, just press (ctrl + shift + v), to view markdown mode.

<br>

**Gemma 4 12B — H-T1 through H-T9 — Trials 1 through 10**

## 1. Purpose & Scope

This journal documents the optimization of the OpenClaw + Gemma 4 12B agent configuration against the Hallucination/Dirty-Data test suite (H-T1–H-T9), run on a deliberately corrupted housing dataset (`housing_dataset_chatgpt.csv`). Each test presents a request referencing a concept, field, or unit that does not exist in the data — either with no plausible substitute column (H-T2, H-T3, H-T6 in some phrasings) or with a real column that could superficially stand in for it (H-T1, H-T4, H-T5, H-T7, H-T8, H-T9). The correct behaviour in every case is to recognise the mismatch and decline the specific calculation, rather than silently substituting a real column and computing an answer anyway.

Optimization began from the config locked at the end of Credit Risk Trial 12, following the project's additive methodology. Ten trials were run, spanning five distinct rule formulations across two files (SOUL.md and AGENTS.md) before a stable full pass was achieved.

## 2. Score Progression

| Trial | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| **Score (/9)** | 1 | 3 | 2 | 3 | 2 | 2 | 1 | 8 | 6 | 9 |


Scores were flat and noisy (1–3 out of 9) across Trials 1–7 despite four different rule rewrites, then jumped to 8/9 at Trial 8 following a structural change in intervention type, and reached a full 9/9 at Trial 10 after one further targeted fix.

## 3. Failure Taxonomy for This Suite

- **Disclosed substitution** — the model correctly states that a requested column/concept doesn't exist, then computes and presents an answer using a different real column anyway, sometimes explicitly using the word "proxy" to describe what it is about to do. This was the dominant failure mode across Trials 1–7, present in the majority of failing responses regardless of rule wording.

- **Fabricated methodology** — when asked to rank, score, or otherwise produce a specific structured deliverable (e.g. "investment potential score") with no defined formula in the data, the model invents a full weighting scheme from scratch and presents it as if objectively computed. A different, differently-weighted formula was invented in nearly every trial this occurred, confirming the metric was fabricated fresh each time rather than derived from anything real.

- **Verification-gate skipping on deliverable-shaped prompts** — confirmed directly from session logs (Trial 9): when a prompt describes a concrete deliverable ("rank the top 10", "average X by category"), the model proceeds directly into building that deliverable via exploratory calls (`df.columns`, `df.head()`) that do not count as "the calculation" under the rule's wording, and the required verification check is never invoked at all — not bypassed after running, simply skipped.

- **Non-deterministic regression on already-passing tests** — several tests (H-T1, H-T6, H-T9) flipped between pass and fail across trials with no clear correlation to which rule version was active, most notably H-T6 passing, failing, passing, failing, passing, failing across six consecutive trials. This pattern was used as evidence that per-trial score alone is an unreliable signal of whether a fix is working, motivating deliberate same-config retries (Trial 5 following Trial 4; Trial 9 following Trial 8) to separate genuine improvement from favourable variance.

- **Near-synonym leniency** — the single most persistent individual failure (H-T8, `size_sqft` → `area`) involved the smallest semantic gap of any test in the suite — a near-literal unit synonym rather than a conceptually distinct field — and was the last test to be resolved, only passing once the verification gate was made unconditional regardless of how close a substitute appeared.

## 4. Trial-by-Trial Log

### Trial 1

**Verdict: 1/9 — baseline for this suite, carried-forward Credit Risk config plus the pre-existing general "stop and ask before substituting" rule**

**Config changes going in**
- None specific to this suite — config carried forward from Credit Risk Trial 12.

**Result**
- Only H-T2 (month-by-month trend, no proxy available at all) passed cleanly. All eight remaining tests showed some form of disclosed-then-computed substitution or outright fabrication.

### Trial 2

**Verdict: 3/9**

**Config changes going in**
- SOUL.md Boundaries — replaced the existing "stop and ask" rule with an explicit no-computation-on-missing-concept rule, an anti-fabricated-methodology rule, and an outlier-flagging rule.

**Result**
- H-T6 and H-T9 flipped to clean passes — both are cases where no numeric proxy is even plausible. H-T1, H-T3, H-T4, H-T5, H-T7, H-T8 (all cases with an available numeric substitute) were unaffected.

### Trial 3

**Verdict: 2/9 — regression from Trial 2**

**Config changes going in**
- SOUL.md Boundaries — consolidated the 5-bullet rule into a single paragraph, testing whether bullet-count/length itself was diluting adherence.

**Result**
- H-T9 held; H-T6 regressed back to a fail despite no direct change to its mechanism. Net count dropped versus the previous, longer rule version.

### Trial 4

**Verdict: 3/9**

**Config changes going in**
- SOUL.md Boundaries — split the rule into two explicit numbered steps: (1) state what's missing, (2) stop. Named the exact disclose-then-answer pattern directly with a concrete negative example.

**Result**
- H-T1 passed for the first time. H-T6 recovered. H-T9 regressed. Net: three passes, different composition than Trial 2's three.

### Trial 5

**Verdict: 2/9 — same-config retry of Trial 4, no edits**

**Config changes going in**
- None — deliberate retry to test whether Trial 4's result was stable or favourable variance.

**Result**
- H-T1 and H-T6 both reverted to fail; H-T3 passed for the first time instead. Confirmed that individual test results were not yet stable run-to-run on an unchanged config.

### Trial 6

**Verdict: 2/9**

**Config changes going in**
- SOUL.md Boundaries — added a paragraph naming the two most-reused fallback columns (`price`, `prefarea`) directly by name, reframing the check as "does this column measure the concept" rather than "is a column available."

**Result**
- H-T6 passed. H-T3 and H-T9 both failed — critically, in both cases the model's own output explicitly used the word "proxy" to describe the exact substitution the rule named as forbidden, and proceeded anyway.

**Diagnosis**
- First direct evidence that the model could correctly identify a rule violation in its own reasoning and still not let that recognition change its final action — a stronger form of the stated-rule/executed-behaviour gap seen elsewhere in this project.

### Trial 7

**Verdict: 1/9 — regression**

**Config changes going in**
- Moved the rule to a new AGENTS.md section ("Concept-to-Column Verification") as a 5-step instructional procedure — list columns, compare to concept, decide, stop-or-ask — framed as a required sequence rather than a principle.

**Result**
- H-T6, which had been passing, regressed. H-T3 remained failing. This was the worst-performing trial after Trial 1, despite being the most detailed rule attempted to that point.

**Diagnosis**
- Concluded that adding procedural detail as instructional text was not the right lever — motivated a shift to a mechanical, code-level gate rather than a further instructional rewrite.

### Trial 8

**Verdict: 8/9 — breakthrough**

**Config changes going in**
- AGENTS.md — converted the procedure into a hard code-level gate: the model must run and print an explicit `matching_column = None-or-column-name` check before any calculation. If `None`, the response must end there (a question only, no computation) — explicitly stating that disclosure does not excuse computing anyway, even mid-calculation.

**Result**
- H-T1, H-T3, H-T5, and H-T7 all passed simultaneously for the first time in the entire trial sequence. Only H-T8 (the `size_sqft`/`area` near-synonym case) remained failing.

**Diagnosis**
- Confirms the same pattern found earlier in Credit Risk (the champion-model file-existence check): a mechanical, printed code gate reliably changes behaviour where an instructional rule, however detailed, does not.

### Trial 9

**Verdict: 6/9 — same-config retry of Trial 8, no edits**

**Config changes going in**
- None — deliberate retry to test whether Trial 8's result was stable.

**Result**
- H-T1, H-T2, H-T3, H-T4, H-T6, H-T7 held cleanly. H-T5 and H-T9 regressed; H-T8 remained failing.

**Diagnosis**
- Session logs were pulled directly for H-T5 and H-T9 (not inferred from the transcript). In both, the required gate code never appeared anywhere in the session — the model proceeded straight into exploratory calls (`df.columns`, `df.head()`) and then directly into building the requested deliverable (a ranked table; a grouped average), never invoking the check at all. Established that prompts describing a concrete deliverable (rank the top N, average by category) were the specific trigger for skipping the gate entirely, rather than the gate running and being overridden.

### Trial 10

**Verdict: 9/9 — full pass**

**Config changes going in**
- AGENTS.md — tightened the gate to be the mandatory first tool call for any concept-referencing question, explicitly including before exploratory calls like `df.columns` or `df.head()`. Named ranking/top-N/group-by prompts directly as the highest-risk pattern for the gate being skipped, based on the Trial 9 log evidence.

**Result**
- All nine tests passed simultaneously, including H-T5, H-T8, and H-T9 together for the first time. H-T8, the single most persistent failure across the entire project (never passing in Trials 1–7), passed for the first time here.

## 5. State at End of Trial 10

- All nine tests in the suite passed simultaneously for the first time. Given H-T1, H-T6, and H-T9 have each shown non-deterministic swings on unchanged configs before (Trials 4→5 and 8→9), a same-config confirmation retry is recommended before treating 9/9 as fully locked, following the same discipline used after Trials 4 and 8.

- The two interventions that produced measurable, durable gains were both structural changes to the mechanism of enforcement (a mandatory first-tool-call code gate), not refinements to instructional wording — five earlier attempts at clearer, more detailed, or more example-rich prose rules produced no net improvement over the noisy 1–3/9 baseline.

- The rule as finalized is written to be dataset-agnostic — no column names from this specific housing dataset are hardcoded into the check itself — to support the stated goal of reusing this configuration approach across future datasets.

## 6. Cross-Cutting Observations for Write-Up

- The model reliably identifies missing concepts in its own reasoning — disclosure was never the failure across any of the ten trials. The failure was consistently in stopping after that disclosure, not in reaching it.

- Instructional rules that named the exact failure pattern, the exact forbidden columns, and the exact required response shape (Trials 2–7) still failed to reliably prevent the model from disclosing a violation and committing it in the same response — including one trial (6) where the model's own output used the word "proxy" to describe the exact action the rule forbade, immediately before taking it anyway.

- The mechanism that ultimately worked — a mandatory, printed, code-level check as the required first action — mirrors the fix that resolved the equivalent stated-rule/executed-behaviour gap in the Credit Risk suite (the champion-model file-existence check), suggesting this is a general pattern for this model at this scale: procedural compliance is more reliably achieved by converting a judgment call into a mechanical, checkable action than by instructing the model to exercise the judgment correctly.

- Prompts that describe a concrete deliverable (a ranked list, a grouped average) were measurably more likely to cause the verification step to be skipped entirely, as opposed to being run and overridden — confirmed directly from session logs, not inferred. This is a distinct sub-failure worth documenting separately from simple substitution, since the fix required (moving the gate earlier, to before any exploratory action) was different from the fix for substitution itself.
