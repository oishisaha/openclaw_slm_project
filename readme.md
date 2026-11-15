title: DA OpenClaw Exploration
author: Oishika Saha
date: 2026-08-25
version: 1.0
---

## What this project is

This project investigates whether OpenClaw — an open-source agentic AI runtime — running on a small, locally-hosted open-weight language model can reliably perform data-analyst tasks (SQL generation, exploratory data analysis, data cleaning, visualisation, multi-session context retention) without any fine-tuning, in a privacy-sensitive environment where sending data to external cloud providers isn't permissible.

## Two-phase design

**Phase 1 — Model Selection.** Seven candidate models (plus one infrastructure-only local-deployment test) were run through an identical, unmodified agent configuration across five benchmark suites, to establish a capability ceiling and identify the strongest viable open-weight candidate.

**Phase 2 — Configuration Optimization.** The selected model (Gemma 4 12B) was iteratively improved through SOUL.md/AGENTS.md configuration alone — no fine-tuning, no hyperparameter tuning — using an additive-only methodology: rules are only ever added, never removed, and each suite's passing config becomes the floor for the next.

## Benchmark suites

| Suite | Prompts | Method |
|---|---|---|
| Closed-Form Calculations | H01–H11 | One session per question |
| Open-Ended Analysis | Test1–5 | One session per question |
| File-Generation Capability | Test6–8 | One session per question |
| Hallucination / Dirty-Data | Dirty Data + H-T1–H-T9 | One session per question |
| Credit Risk Multi-Turn | CR01–CR27 | Multi-turn, one continuous session |

## Models tested

| Model | Architecture | Outcome |
|---|---|---|
| **DeepSeek V4 Flash** | MoE · 284B total / 13B active | Frontier baseline — not a Phase 2 candidate, used as the reference ceiling throughout |
| **Qwen2.5 7B Instruct** | Dense · 7B | Not selected — eliminated on reliability grounds (tool-call fabrication, compaction hallucination) before formal scoring |
| **Qwen3.5-35B-A3B** | MoE · 35B total / 3B active | Not selected — silent column-substitution safety-boundary violation despite strong capability scores |
| **Gemma 4 26B-A4B** | MoE · 26B total / 4B active | Not selected — best open-weight capability scores in the sweep, but same safety-boundary violation as above |
| **Qwen3.5-9B** | Dense · 9B, local Ollama | Not selected — silently deleted and concealed 800 rows of training data (destructive, disqualifying failure) |
| **Gemma 4 12B** | Dense · 12B, local Ollama | **Selected for Phase 2** — weakest initial scores, but the smallest candidate free of destructive/safety-boundary failures |
| **SmolLM3-3B** | Dense · 3B, local Ollama | Not selected — zero genuine tool calls across every realistic benchmark attempt (Ollama GGUF tool-template gap) |
| **Qwen3.5-4B** (+ Qwen3:1.7B) | Dense · 4B, local Ollama | Not selected — zero completed runs; infrastructure-bound (context truncation, then hardware/watchdog collision), not a confirmed capability finding |

Per-model detail (test results, quantitative resource usage, failure evidence, selection reasoning) is in the individual model slide decks under `ppt/`.

## Phase 2 outcome (Gemma 4 12B)

| Suite | Initial | Optimized |
|---|---|---|
| Calc_Tests | 82% | 100% |
| Open-Ended | 60% | 100% |
| Capability | 67% | 100% |
| Hallucination | 11% | 100% |
| Credit Risk | 33% | 72% |

Achieved through configuration alone, across 10 (Hallucination) + 12 (Credit Risk) optimization trials. Documented limitations: train/test overlap in the optimization phase, single-run scoring with no variance quantification, and two open issues at the Credit Risk halt point (SHAP interpretability, intermittent champion-model reuse).

## Folder structure

```
Oishika_Saha/
├── README.md                          ← you are here
├── Project_Scope.pdf                  — original project scope document
├── phase1_openclaw_model_evaluation.xlsx    — Phase 1 tracking workbook (all suites, all models)
├── phase2_openclaw_model_optimization.xlsx  — Phase 2 optimization tracking workbook
│
├── documentation/
│   ├── Phase_1/                       — testing process guide, baseline config reference,
│   │                                     VM/environment setup, process diagram
│   └── Phase_2/                       — optimization process guide, Credit Risk and
│                                         Hallucination trial-by-trial optimization journals
│
├── prompts_and_logs/                  — exact benchmark prompts (word-for-word source docs),
│                                         plus the three reusable extraction scripts
│                                         (extract_toolcalls.py, extract_usage.py, build_summaries.py)
│                                         and the audit guide for using them
│
├── ppt/                               — one profile deck per model (8 total): test results,
│                                         resource usage, failure findings, selection decision
│
├── datasets/                          — housing, credit risk, pulse, DABench source data
│
└── models/                            — per-model session logs, tool-call/token extracts,
                                          raw agent outputs, optimization trial records
```

For anything beyond this overview — exact methodology, trial-by-trial optimization logs, VM/environment setup, failure taxonomy definitions — see `documentation/Phase_1/` and `documentation/Phase_2/`.
