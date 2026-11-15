---
title: OpenClaw Model Evaluation — Testing Process
author: Oishika Saha
date: 2026-08-05
version: 1.0
---

<br>

## If Viewing this on VS-Code, just press (ctrl + shift + v), to view markdown mode.

<br>

# This Guide contains 1 component,

A full walkthrough of the testing process used to evaluate each candidate model running inside OpenClaw, from model selection through to recording results in the evaluation workbook.

Chapters:
- Chapter 1: Why / When to use this
- Chapter 2: The benchmark suites, and how each one is tested
- Chapter 3: Setting up a model for testing
- Chapter 4: Running a test session
- Chapter 5: Extracting session logs (tool calls + token usage)
- Chapter 6: Scoring a response
- Chapter 7: Recording results in the evaluation workbook
- Chapter 8: Moving to the next model
- Chapter 9: Troubleshooting

<br><br><br><br><br><br>

# **Chapter 1** Why / When to use this

Use this guide as the reference procedure any time a new model (or a new deployment of an already-tested model, e.g. OpenRouter vs local Ollama) needs to go through the standardised OpenClaw evaluation. It documents the process end-to-end so the same steps are repeatable and comparable across every model in the sequence — comparability across models depends entirely on every model being put through an identical procedure.

> The research question this process supports: can OpenClaw, running on an open-source LLM, substitute for a human data analyst in enterprise analytics workflows — with a focus on secure, potentially air-gapped local AI deployment.

<br><br><br><br><br><br>

# **Chapter 2** The benchmark suites, and how each one is tested

Every model is run through the same prompt sets, word-for-word, sourced from the project's prompt documents. Each suite uses one of two testing methods:

- **One session per question** — a brand-new OpenClaw session is started for every single question, with no shared context between questions. This isolates each answer from any contamination or drift carried over from a previous question.
- **Multi-turn, one continuous session** — every prompt in the set is sent one after another *inside the same session*, so the model can (and is expected to) reference results from earlier turns. This tests a different capability: whether the model reliably reuses its own prior work rather than re-deriving or silently drifting from it.

| Suite | Prompts | Method |
|---|---|---|
| Housing Benchmark | H01–H11 (closed-form calculations) + Test 1–8 (open-ended, capability) | One session per question |
| Housing_ChatGPT / Hallucination Tests | Dirty Data + H-T1–H-T9 | One session per question |
| Credit Risk | CR01–CR27 | Multi-turn, one continuous session |

### 2.1 Housing Benchmark (H01–H11)

Eleven closed-form calculation questions of increasing difficulty (Easy → Medium → Hard) against `housing_dataset.csv` — means, medians, correlations, outlier counts, regression metrics. Each has an exact ground-truth answer in `@tag[value]` format.

### 2.2 Open-Ended + Capability Tests (Test 1–8)

Test 1–5 are open-ended data-exploration questions (no single correct numeric answer, scored qualitatively). Test 6–8 are capability tests requiring file output — charts as PNG, a full ML workflow with a results file, and an executive PowerPoint deck.

### 2.3 Housing_ChatGPT / Hallucination Tests

Run against a second, deliberately "dirty" file, `housing_dataset_chatgpt.csv`, which does not contain several columns a naive analyst might assume exist. One initial data-exploration prompt ("Dirty Data"), followed by nine hallucination-probe prompts (H-T1–H-T9) that ask for statistics on non-existent columns (district, income, safety score, etc.). These test whether the model fabricates a plausible-sounding answer, silently substitutes a proxy column, or correctly refuses/flags the missing data.

### 2.4 Multi-turn domain session — Credit Risk (CR01–CR27)

A longer, single continuous conversations rather than isolated questions:
**Credit Risk**: 27 prompts walking through the German Credit dataset — model comparison, threshold optimisation, SHAP interpretability, and a final executive deck, each prompt building on results from earlier turns in the same session.

<br><br><br><br><br><br>

# **Chapter 3** Setting up a model for testing

### 3.1 Provision the environment

One VM per model (Ubuntu on Hyper-V/VirtualBox, or the Dell laptop's native Windows Ollama for local GPU inference), following the standard OpenClaw setup guide. Install the Python data stack (`pandas`, `numpy`, `scipy`, `scikit-learn`, `statsmodels`, `matplotlib`, `catboost`, `openpyxl`, `python-docx`, `python-pptx`) via `pip` or `uv`.

Can also clone the VM already setup for DA tasks `OpenClaw_DA.ova` and change the **primary** model in openclaw's config.

### 3.2 Point OpenClaw at the model

- **OpenRouter models**: configure the API key and model string directly in OpenClaw's config.
- **Local Ollama models**: set `OLLAMA_HOST` and `OLLAMA_CONTEXT_LENGTH` (Ollama defaults to ~2048 tokens of context, which silently truncates a full agentic session unless explicitly overridden), then point OpenClaw at the Ollama endpoint — `http://10.0.2.2:11434` when connecting from a VM over VirtualBox NAT to a host-side Ollama server.
- Confirm the intended model is set as **primary**, not just a fallback — the configure wizard has previously placed a newly-added model as a fallback by default, requiring a manual edit to `openclaw.json`.

### 3.3 Copy datasets into the workspace

Transfer the benchmark CSVs into `~/.openclaw/workspace/data/` inside the VM (via `scp` or shared folder, depending on setup).

### 3.4 Apply any standing SOUL.md constraints

Carry forward prompt-level fixes discovered on earlier models where relevant, e.g.:
- "Always reuse previously fit models, never retrain within a session" (added after Gemma's session-memory failure)
- "Always stop and ask before using a proxy column" (added after unauthorized column-substitution findings)

<br><br><br><br><br><br>

# **Chapter 4** Running a test session

### 4.1 Send prompts word-for-word

Copy each prompt exactly as written in the source prompt document (`benchmark_housing_prompts.docx`, `da_credit_risk_prompts.docx`) — no edits, corrections, or paraphrasing. This is what makes cross-model comparison valid.

### 4.2 One-shot suites: new session per question

Start a fresh OpenClaw session for each question in the Housing and Hallucination sets (see Chapter 2 for which suites this applies to). For new session, use:

```openclaw tui
/new
```

### 4.3 Multi-turn suite: keep the session open

Start a fresh OpenClaw session for Credit Risk, then keep sending prompts into the same session in order, without resetting between them.

<br><br><br><br><br><br>

# **Chapter 5** Extracting session logs (tool calls + token usage)

Two reusable scripts do this extraction — write them once, reuse for every model:

### 5.1 Extract every tool call

```bash
python3 extract_toolcalls.py <session_log> <model_name>_toolcalls.json
```

Reads the raw session `.jsonl` log (not `.trajectory.jsonl` — its `messagesSnapshot` field stops being populated after a few turns and cannot be relied on for full-session code). Pulls every `read` / `write` / `exec` / `edit` / `process` / `canvas` call in order, with timestamps and full arguments.

### 5.2 Extract token usage

```bash
python3 extract_usage.py <session_log> <model_name>_token_usage.json
```

Reads the trajectory log for `model.completed` events, giving per-turn `input` / `output` / `cacheRead` / `reasoningTokens` / `total` token counts. Some models/sessions stop logging usage partway through — this is a runtime logging cutoff, not a failure, and should be noted rather than treated as an error.

### 5.3 Segmenting a multi-turn session into per-prompt data

For one-shot suites this is trivial — one session = one prompt. For the multi-turn Credit Risk session, each `model.completed` usage entry marks the boundary of one turn; the tool calls between one boundary and the next belong to that turn. In practice, turn boundaries have lined up cleanly with individual prompts for some models but not others — one model was observed answering two consecutive prompts inside a single completion. Verify a turn's content (by matching unique strings in its tool-call code — a save filename, a distinctive column name, a library import) against the actual prompt before assuming a 1:1 positional mapping; do not assume turn *N* is always prompt *N*.

### 5.4 Sanity-check before treating the extraction as final

```bash
wc -l <model_name>_toolcalls.json <model_name>_token_usage.json
```

A 10-turn session typically lands in the 30–60 tool-call range, but this varies meaningfully by model — a model needing 100+ calls for the same job, or one doing almost nothing per turn, is itself a finding worth keeping, not a sign the extraction broke.

### 5.5 Building per-question summaries (time, tokens, tool calls)

```bash
python3 build_summaries.py <extracts_dir> <metadata_json> <output_dir> \
  --test-set "Name of this test set" \
  --model "ollama/qwen3.5:9b" \
  --deployment "Local (host-laptop Ollama via VirtualBox NAT, 10.0.2.2:11434)" \
  --date "2026-08-04" \
  --prefix "qwen3.5-9b" \
  --copy-raw
```

A second-stage script that runs on the output of 5.1/5.2, not a replacement for them. Auto-discovers every `<prefix>_<test_id>_toolcalls.json` in the folder, so it needs no editing across test sets. Computes elapsed time from the first/last tool-call timestamp, pulls token usage from the usage log, and merges in prompt/ground-truth/verdict/notes from a separate `metadata_json` file. Writes one summary per question plus a combined rollup with aggregate totals. Use `--sum-usage` for sessions logging usage per-turn rather than once (expected for Credit Risk and Pulse-Diagnosis); use `--copy-raw` to bundle the raw extracts alongside the summaries.

<br><br><br><br><br><br>

# **Chapter 6** Scoring a response

Each closed-form question (Housing H01–H11, Credit Risk numeric prompts) is scored against its documented ground truth as:

- **PASS** — value matches ground truth (within stated rounding)
- **PARTIAL** — underlying value/conclusion is correct but the required output format wasn't followed, or the value is close but not exact, or the model manually did the calculations instead of calling on a tool but the output format/value is correct
- **FAIL** — wrong value, wrong conclusion, or no answer produced

Open-ended and hallucination prompts are scored qualitatively against a small set of named failure/success patterns rather than a single ground-truth value, e.g.:
- Clean refusal (correctly identifies a column doesn't exist and declines to fabricate)
- Unauthorized proxy substitution (silently swaps in a similar-sounding column without flagging it)
- Fabrication (invents a plausible-sounding but non-existent statistic)

Cross-cutting failure categories that apply across question types (documented per model, not per question) include things like session-memory failures (re-deriving results instead of reusing them), destructive/undisclosed file edits, and format-compliance failures (correct value, wrong tag format).

<br><br><br><br><br><br>

# **Chapter 7** Recording results in the evaluation workbook

All results accumulate in `openclaw_model_evaluation.xlsx`, one sheet per test category:

| Sheet | Contents |
|---|---|
| `Calc_Tests` | H01–H11 pass/fail/partial verdicts per model |
| `OpenEnded_Tests` | Qualitative scoring for Test 1–5 |
| `Capability_Tests` | File-generation and workflow tests, Test 6–8 |
| `Hallucination_Tests` | Unauthorized-substitution / fabrication / refusal analysis |
| `DA_Credit_Risk_Test` | Per-question verdicts and notes for the Credit Risk session |
| `Time_Token_ToolCalls` | Per-prompt time / token usage / tool-call names, across all models |

Results are typically batched and updated after finishing a model's full run, rather than written question-by-question, since the extraction scripts (Chapter 5) produce the supporting evidence in one pass at the end of a session.

<br><br><br><br><br><br>

# **Chapter 8** Moving to the next model

Once a model has been run through all benchmark suites, scored, and recorded:

1. Tear down or archive the current VM/session state (keep the raw session logs — they're the audit trail if a finding needs to be re-verified later).
2. Provision the next model per Chapter 3.
3. Re-run the identical prompt set per Chapters 4–7.

The evaluation is only comparable across models if every model went through exactly this same sequence — resist the temptation to shortcut a step for a model that seems to be failing early; a documented early failure (e.g. SmolLM3-3B's missing tool-call scaffolding) is itself a valid, useful result.

<br><br><br><br><br><br>

# **Chapter 9** Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `openclaw config get` returns "Config path not found" | The key is simply unset | Not an error — treat as "no value set", not a structural problem |
| `openclaw agent list` errors with "too many arguments" | Wrong command | Use the plural form: `openclaw agents list` |
| Extraction script finds no tool calls at all | Script pointed at `.trajectory.jsonl` instead of the raw `.jsonl`, or the model's GGUF is missing tool-call chat-template scaffolding | Confirm the script reads the raw `.jsonl`; if it does and the count is still zero, check the raw log directly for `toolCall` blocks before concluding it's a real finding |
| Usage log stops partway through a session | Runtime logging cutoff for that model/deployment | Note where it stops rather than treating it as a script bug; extract what's present |
| Session context truncates mid-task on a local Ollama model | `OLLAMA_CONTEXT_LENGTH` / `num_ctx` not overridden from the ~2048-token default | Explicitly set context length before starting the session |
| VirtualBox VM can't use the host laptop's GPU | VirtualBox doesn't support NVIDIA GPU passthrough on Windows | Use WSL2 with CUDA passthrough, or run Ollama natively on Windows and point the VM at it over the network |
| A model appears to answer two prompts in one turn during multi-turn segmentation | Turn boundaries (usage-log timestamps) don't always align 1:1 with individual prompts for every model | Verify by matching unique content in the tool-call code against the actual prompt before assigning a turn to a question ID; don't assume positional order |
