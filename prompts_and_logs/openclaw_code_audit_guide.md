# OpenClaw Session Code Audit — Repeatable Guide

Run this once per model, right after finishing that model's multi-turn test session, before starting the next model's session.

Two files come with this guide — save them once, reuse every time:
- `extract_toolcalls.py` — pulls every tool call (the actual code) from the session
- `extract_usage.py` — pulls per-turn token usage

## Step 0 — Get the session ID while it's still current

The moment you finish testing a model, before opening a new session, run:

```bash
ls -lat ~/.openclaw/agents/main/sessions/*.jsonl | grep -v trajectory | head -3
```

The top result is your session. Copy its filename (minus `.jsonl`) — that's the session ID you'll use below. Set it once per run:

```bash
SESSION_ID=<paste-uuid-here>
MODEL_NAME=<e.g. qwen2.5-14b>   # used to name your output files
```

Do this immediately — once you start the *next* model's session, "most recent" points at the wrong file.

**Optional sanity check**, confirms it's the right session before you extract anything:

```bash
grep -c "wiry_pulse\|pulse.csv" ~/.openclaw/agents/main/sessions/$SESSION_ID.trajectory.jsonl
```

(swap in whatever's unique to your test — dataset name, target column, etc.)

## Step 1 — Extract every tool call

```bash
python3 extract_toolcalls.py $SESSION_ID ${MODEL_NAME}_toolcalls.json
```

Prints a per-tool breakdown (exec/write/read/process/canvas counts) as it runs — a first, quick signal of how the model worked before you even look at the code.

## Step 2 — Extract token usage

```bash
python3 extract_usage.py $SESSION_ID ${MODEL_NAME}_token_usage.json
```

Tells you up front how many turns actually have usage data — some sessions stop logging usage partway through (this happened on the DeepSeek run, from Turn 5 onward). Not an error, just note it when it happens.

## Step 3 — Sanity check before uploading

```bash
wc -l ${MODEL_NAME}_toolcalls.json ${MODEL_NAME}_token_usage.json
```

Rough expectation: a 10-turn session should land somewhere in the 30–60 tool-call range, but this will vary by model — a big deviation either way is itself worth noting (e.g. a model that needed 100+ calls to do the same job, or one that did almost nothing per turn).

## Step 4 — Upload both files to Claude

Upload `${MODEL_NAME}_toolcalls.json` and `${MODEL_NAME}_token_usage.json` in your chat and ask for the code audit document. From these two files alone, Claude can:
- segment the tool calls into turns using the usage-timestamp boundaries
- build the full code audit (every exec/write/read/process/canvas call, in order, verbatim)
- flag which turns are missing usage data, if any

## Things that will vary model to model — expect and note these, don't treat them as bugs

- **Turn boundaries may not land as cleanly.** DeepSeek's turn boundaries lined up neatly with `model.completed` timestamps because it didn't drop usage data until Turn 5. A model that drops usage data earlier (or never logs it at all) will need turn boundaries inferred from tool-call content/timestamps instead — flag this to Claude rather than assuming the same script will "just work."
- **Tool call volume per turn varies a lot.** DeepSeek did 14 calls in Turn 1 alone. A different model might spread work more evenly, or do almost everything in one giant call, or many small ones. This is itself a useful comparison point across models, not noise to average away.
- **Some models may not use `process` (background polling) at all**, if they don't run anything long enough to need it — don't expect the same tool mix every time.

## Do NOT do (mistakes from the first run that cost time)

- Don't search the SQLite databases (`openclaw.sqlite`, `openclaw-agent.sqlite`) — session content isn't there, only auth/memory/orchestration metadata.
- Don't rely on `messagesSnapshot` inside `.trajectory.jsonl` for code — it stops getting populated after a few turns. The raw `.jsonl` sibling file (used by both scripts above) is the reliable source for full tool-call code, every turn.
- Don't search by the "tui-XXXX" ID shown in the app footer — that's a display label, not the filename. Use Step 0's recency-based lookup instead.
