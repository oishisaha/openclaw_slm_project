# SmolLM3 (Model 3) — Setup & Debugging Journal

**Date:** 24 July 2026
**VM:** Ubuntu on Hyper-V ("oi-Virtual-Machine" → rebuilt mid-session with more RAM/CPU)
**Model:** `alibayram/smollm3` (Ollama community GGUF of HuggingFaceTB/SmolLM3-3B)
**Goal:** Set up SmolLM3 as the 3rd model in the OpenClaw DA-agent benchmark, matching the DeepSeek/Model 2 methodology.

---

## 1. VM provisioning

- Built a new Ubuntu VM in Hyper-V for SmolLM3, separate from the DeepSeek/phi4-mini VM.
- **Disk too small (12GB).** Grew the Hyper-V virtual disk externally, then had to resize the Linux partition and filesystem internally: `parted /dev/sda resizepart 1 100%` → `resize2fs /dev/sda1`. Root grew from ~12GB to ~50GB.
- **Network dead after resize** (`Temporary failure resolving 'archive.ubuntu.com'`, then `Network is unreachable`). Root cause: the laptop's VPN was on, interfering with the Hyper-V virtual switch. Turning off the VPN fixed it immediately.
- Installed base tooling: `curl`, `git`, `build-essential`, Node.js (needed for OpenClaw's npm install), VS Code.

## 2. Ollama + model setup

- Installed Ollama, pulled `alibayram/smollm3` (1.9GB, 3B params).
- **Default Ollama context window too small for agent use.** Wrapped the model in a custom Modelfile with `PARAMETER num_ctx 65536` → `phi4-mini-agent`-style pattern, built as `smollm3-agent`.
- **OOM crash at `num_ctx 65536`** on the original 8GB VM — `llama-server` killed repeatedly by the kernel OOM killer (confirmed via `dmesg`/`journalctl`). No swap was configured at the time.
  - Added a 4GB swapfile as a safety net.
  - Rebuilt at `num_ctx 32768` instead, which fit comfortably (~6.3GB used) and ran a clean 27s test response.

## 3. Hyper-V memory: chasing 16GB

- Tried to bump the VM to 16GB RAM in Hyper-V settings — failed to start (`Unable to allocate 16384 MB of RAM: Insufficient system resources`).
- Root cause: **the Windows host itself only had ~13.6GB free** at the time (31.6GB total, ~18GB in use by background processes — no single culprit, spread across many small processes).
- Settled for **12GB** VM RAM instead, which started cleanly and left the host headroom. Confirmed via `free -h` (~11GiB total after boot) and `sudo dmidecode -t memory` (8192MB confirmed on the earlier failed attempt, useful for diagnosing the phantom "16GB" that never actually applied).

## 4. OpenClaw install & config

- Installed via `curl -fsSL https://openclaw.ai/install.sh | bash`.
- `openclaw` command not found after install — `npm`'s global bin dir (`~/.npm-global/bin`) wasn't on `$PATH`. Fixed by adding it to `.bashrc`.

### 4a. Wrong model kept getting used
- Repeatedly set `agents.defaults.model.primary` to `smollm3-agent`/`smollm3-tools`, but the TUI kept showing the old model (`phi4-mini`, then later `smollm3-agent` instead of `smollm3-tools`).
- Root causes, found one at a time:
  1. A stale **systemd user service** (`openclaw-gateway.service`) was silently respawning the gateway with old in-memory config on every `pkill`, ignoring config file edits until the service itself was properly restarted (`systemctl --user restart openclaw-gateway.service`).
  2. The **TUI resumes the last session by session ID**, which pins whatever model that session started with — a brand-new config doesn't retroactively change an existing session's model. Fix: kill the stale session file / force a genuinely new session.
  3. Later in the day, the TUI intermittently launched in **"local embedded" mode** instead of connecting to the gateway (`ws://127.0.0.1:18789`), silently ignoring config changes made to the gateway-side file. Traced to `--url` having no explicit default when running fully local-only (no `gateway.remote.url` configured) — bare `openclaw` can ambiguously fall back to `--local`. Fixed by launching explicitly: `openclaw tui --url ws://127.0.0.1:18789 --token $(openclaw config get gateway.auth.token)`.

### 4b. `tools.profile: "minimal"` silently disabled all tool use
- To cut down OpenClaw's per-turn token overhead, set `tools.profile: "minimal"`.
- Did not realise until much later that `minimal` grants the model **exactly one tool** (`session_status`) — no `exec`, no `read`/`write`. This meant early benchmark runs (H01, H02) had **no way to run Python or touch the CSV at all**, and the model's fabricated answers on those runs were a direct consequence of this, not (at that point) a model failure.
- Switched to `tools.profile: "coding"` (includes `group:fs`, `group:runtime`/`exec`, etc.) once found via the official docs (`config-tools.md`).

### 4c. Timeout chasing
- Requests were getting killed at inconsistent points (24s once, ~6m0s–6m10s repeatedly) with `500` errors in the Ollama log (`srv stop: cancel task`) — the requests were being cancelled from the OpenClaw/client side, not crashing server-side.
- Set `models.providers.ollama.timeoutSeconds: 900` (provider-level HTTP timeout) — did not fully resolve it.
- Found and set `agents.defaults.timeoutSeconds: 900` (separate, per-agent-turn timeout) — also did not fully resolve it; failures still landed around ~6 minutes.
- **Root cause never fully identified.** The consistent ~360s cutoff, despite two different timeout settings raised to 900s, was not traced to any config key found in the schema. Working theory: an undocumented/hardcoded gateway-level watchdog, separate from both settings changed. Left unresolved; worked around by reducing overhead instead (see below) rather than continuing to chase it.

### 4d. Reducing prompt overhead
- OpenClaw's own system prompt + tool schemas were adding **~8,000–14,000 tokens** of overhead to every turn before any user content, confirmed directly in Ollama's logs (`task.n_tokens`).
- Disabled unused bundled skills one at a time (`browser-automation`, `canvas`, `diagram-maker`, `clawhub`, then later `healthcheck`, `node-connect`, `node-inspect-debugger`, `notion`, `skill-creator`, `spike`, `taskflow`, `taskflow-inbox-triage`, `weather`, `meme-maker`) — brought overhead down from ~14k to ~8k tokens.
- Found OpenClaw's documented `agents.defaults.experimental.localModelLean: true` flag late in the process — a purpose-built setting for exactly this scenario (drops heavyweight tool categories while keeping `exec` visible). Applied it as the final overhead-reduction step.

## 5. Tool-calling: the model itself has no tool template

- After finally getting a clean run through with the right profile/timeouts, discovered the model was **fabricating answers** on the benchmark prompts (H01/H02): round, suspiciously clean numbers (`1,500,000.00`, `1,200.00`) against ground truth of `4,766,729.25` / `4,600.00`, with a false narrative claiming pandas was used.
- Confirmed via direct extraction (`extract_toolcalls.py`, then a custom `inspect_session.py`) that **zero tool calls occurred** in these sessions.
- Traced to the actual cause: `ollama show smollm3-agent --modelfile` showed the model's `TEMPLATE` was a bare `System/Prompt/Response` ChatML shape with **no tool-injection scaffolding at all** (`{{ if .Tools }}` block).
- Confirmed via web research this is **not a SmolLM3 architecture limitation** — the base model genuinely supports tool calling (HuggingFace model card, reference vLLM deployment with `--tool-call-parser=hermes`). The gap is specific to this Ollama community GGUF: **no official SmolLM3 exists in Ollama's library** (tracked, unresolved GitHub issue `ollama/ollama#11340`), and every available community quant (`alibayram`, `Impulse2000`, `yasserrmd`) ships the plain template — the tool-call chat template appears to not have survived GGUF conversion.

### 5a. Building a custom tool-call template
- Pulled SmolLM3's actual `chat_template.jinja` from HuggingFace to see the real tool-call format (Hermes/Qwen-style: `<tools>...</tools>` schema injection, `<tool_call>{"name":...,"arguments":...}</tool_call>` output).
- Hand-built a custom Ollama Modelfile `TEMPLATE` porting this pattern into Ollama's Go-template syntax, built as `smollm3-tools`.
- **Isolated test succeeded on the first try** — a direct `curl` to `/api/chat` with a simple weather tool returned a correctly parsed `tool_calls` array. Confirmed the custom template genuinely works at the Ollama level.

## 6. Real benchmark attempts still failed — model doesn't reliably use tools

- Re-ran H01 through OpenClaw with `smollm3-tools`, `tools.profile: coding`, correct timeouts, and lean mode. Still fabricated (`@mean_price[1,000,000.00]`, then `[2.45]` on a separate attempt) with no `toolCall` block in the session log.
- Ran the full PD01–PD07 multi-turn pulse-diagnosis session in one go (matching DeepSeek's methodology). **Zero tool calls across all 7 turns.** The model instead generated seven turns of fluent, plausible-looking fake analysis: invented filenames/scripts (`analyze_data.py`, `/path/to/dataset.csv`), a fabricated results report with specific invented accuracy/precision/recall/F1 numbers, and fabricated feature-importance rankings.
- Confirmed independently via token-per-turn extraction: growth was strictly linear (+300–500 tokens/turn, consistent only with conversational accumulation), with **no spike anywhere** consistent with a tool result being injected into context — a second, independent confirmation that no tool calls occurred, without needing to re-inspect the transcript.
- Conclusion: the isolated weather-tool test worked because it's a textbook, heavily-represented tool-calling pattern. On realistic, open-ended data-analysis prompts — even ones with an explicit imperative ("Use Python to calculate...") — the model does not reliably invoke the tool it has been correctly given access to.

## 7. Bootstrap file gap noted, not yet acted on

- Discovered partway through that `IDENTITY.md` / `SOUL.md` / `USER.md` had not been filled in before the SmolLM3 sessions began (same as the DeepSeek baseline requires). Edited them mid-session.
- This creates a **confound**: earlier sessions (H01, H02, PD01–PD07) ran without the SOUL.md anti-fabrication instruction ("never fabricate numbers... always ask before substituting a column") in context. Any future rerun with the updated files would not be directly comparable to today's results without controlling for this.

## 8. Context window question (128k)

- Raised whether the model needed to be bumped to 128k context, based on a token-usage chart from a prior (DeepSeek) experiment showing ~106k avg tokens/session.
- Clarified this is not an OpenClaw hard requirement, but a legitimate empirical concern for long multi-turn sessions specifically.
- Noted SmolLM3's trained native context is 64K (confirmed via the Ollama model page); 128K is only reachable via YaRN extrapolation with a quality cost, and would very likely re-trigger the earlier OOM problems given the VM's actual RAM budget.
- Decided to empirically test whether 65536 context holds up across a realistic multi-turn session (PD01–PD09) rather than pre-emptively pushing to 128k. The PD01–PD07 run (~8k tokens by turn 7) suggests context size was never actually the bottleneck for this model — tool-use reliability was.

## 9. Where this stands

- VM, Ollama, and OpenClaw infrastructure are now correctly configured and stable (12GB RAM, `num_ctx 65536`, `tools.profile: coding`, lean mode, correct gateway launch command).
- A working custom tool-call template was successfully built for this model (a genuine, documentable side-result).
- Despite a fully corrected setup, **SmolLM3-3B via this Ollama deployment path does not reliably perform tool/exec calls on realistic agentic data-analysis prompts**, instead fabricating plausible-looking fake results. This is treated as the final, load-bearing finding for this model in the benchmark comparison.
