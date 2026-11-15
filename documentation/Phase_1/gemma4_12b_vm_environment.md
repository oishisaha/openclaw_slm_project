# Gemma4 12B — OpenClaw VM Environment Documentation

Reference doc for the VM / OpenClaw / model-serving stack this model runs in. Gemma4 12B is now the fixed target for this project — no further model exploration, only optimization work against this environment going forward.

Last updated: 2026-08-07

## Host Environment

- **Host machine:** Dell laptop, Windows
- **Virtualization:** Oracle VirtualBox 7.2.8
- **Model serving:** Ollama runs **on the Windows host directly** (not inside the VM) — listens on `0.0.0.0:11434`
- **GPU:** Host-side Ollama inference. VirtualBox's lack of NVIDIA GPU passthrough on Windows hosts is a non-issue here specifically *because* Ollama runs on the host rather than inside the guest — this setup avoids the CPU-only fallback that would occur if Ollama ran inside the VM instead.

### Known host-side gotcha: Ollama tray auto-relaunch

The Ollama system tray app auto-relaunches as a background service even after a manual `ollama serve` is killed, and re-grabs port 11434 before a fresh `ollama serve` can bind it:

```
Error: listen tcp 0.0.0.0:11434: bind: Only one usage of each socket address (protocol/network address/port) is normally permitted.
```

Fix: right-click the Ollama tray icon → **Quit Ollama** explicitly before running `ollama serve` manually. Only one of "tray-managed service" or "manual serve" can hold the port at a time.

### Persistent context length

Ollama's default context window (~2048 tokens) silently truncates long agent system prompts. Set `OLLAMA_CONTEXT_LENGTH` as a **persistent system environment variable** (not just in the terminal session that launches `ollama serve`), so it survives tray-relaunches and host restarts:

```powershell
[System.Environment]::SetEnvironmentVariable('OLLAMA_CONTEXT_LENGTH', '131072', 'User')
```

Then restart `ollama serve` fresh to pick it up. Verify via `ollama show gemma4:12b --modelfile` (run on host), or from inside the VM if the host CLI isn't accessible:

```bash
curl -s http://10.0.2.2:11434/api/show -d '{"name":"gemma4:12b"}' | grep -i num_ctx
```

## VM Infrastructure

- **Guest OS:** Ubuntu 24.04.3 LTS
- **VM name/hostname:** `openclaw`
- **Provenance:** Cloned from the qwen3.5-9b-via-Ollama VM (same SSH/networking conventions preserved by design)
- **SSH access** (from host PowerShell):

```powershell
ssh -p 2222 vboxuser@127.0.0.1
```

Password: `<redacted>`

- **Networking:** VirtualBox NAT mode, port-forwarded 2222→22
  - Guest's own IP (`enp0s3`): `10.0.2.15` (DHCP-assigned by VirtualBox's internal NAT DHCP — may differ across clones/reboots, doesn't affect any workflow since nothing addresses the VM by this IP)
  - **Host reachable from guest at:** `10.0.2.2` — VirtualBox's fixed NAT gateway alias, identical across all NAT-mode VMs regardless of cloning
  - Ollama endpoint from inside the VM: `http://10.0.2.2:11434`
- **Clone hygiene:** confirm "generate new MAC address for all network adapters" was selected on clone/import, to avoid MAC conflicts if two VMs are ever running simultaneously on the same NAT network
- **System state at last login:** 96 pending updates (38 security), ESM Apps available but not enabled, system restart flagged as required — not yet addressed, low priority unless something breaks

## OpenClaw Setup

- **Version:** 2026.7.1-2 (agentic AI runtime)
- **Gateway:** managed as a systemd user service, `openclaw-gateway.service`, listening on port `18789`
  - Restart after any config change: `systemctl --user restart openclaw-gateway.service` (the service silently respawns with stale in-memory config otherwise)
- **Launch command** (avoids silent local-embedded fallback):

```bash
openclaw tui --url ws://127.0.0.1:18789 --token $(openclaw config get gateway.auth.token)
```

- **Agent:** `main`
- **Active model config:** `ollama/gemma4:12b`
- **Auth token:** must be set as a literal hex string via `openclaw config set gateway.auth.token`, not an env-var SecretRef — systemd doesn't inherit shell environment

### Agent config files (held constant across all models for comparability)

`IDENTITY.md`, `SOUL.md`, `USER.md`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md` — these define the agent's behavior and are the primary levers for the optimization work ahead.

### Workspace path

The agent's actual writable workspace is `/home/vboxuser/.openclaw/workspace` — **not** `/workspace` (that path returns `EACCES: permission denied, mkdir '/workspace'` when the model attempts to write there directly; a recurring early-turn stumble worth being aware of if optimizing prompt guidance for file-write paths).

### Session log location

```
~/.openclaw/agents/main/sessions/<uuid>.jsonl              # raw log — reliable source for full tool-call code, every turn
~/.openclaw/agents/main/sessions/<uuid>.trajectory.jsonl   # trajectory/usage log
```

### Critical known issue — TUI display ID mismatch

OpenClaw's `tui-XXXX` display ID shown in the TUI header **does not reliably match the actual `.jsonl` filename on disk.** This was confirmed repeatedly across nearly every test in this model's evaluation (H10, H11, Test4, the H06/Test7 duplicate-run investigations, and all 10 Hallucination-suite sessions) — never trust the TUI-printed UUID for post-hoc log extraction. Always verify via content-matching:

```bash
grep -l "<distinctive phrase from the prompt>" ~/.openclaw/agents/main/sessions/*.jsonl | grep -v trajectory
```

When multiple sessions match the same phrase (duplicate/retry runs, or cross-model prompt reuse), disambiguate by checking the `"model":"..."` tag and timestamp (`stat -c '%y' <file>`) against the model and expected run time.

### Do NOT do

- Don't search `openclaw.sqlite` / `openclaw-agent.sqlite` — session content isn't there, only auth/memory/orchestration metadata.
- Don't rely on `messagesSnapshot` inside `.trajectory.jsonl` for code — it stops populating after the first few turns. The raw `.jsonl` sibling file is the reliable source.
- Don't search by the "tui-XXXX" ID shown in the app footer — that's a display label, not the filename (see above).

## Extraction Tooling

Three scripts, all living in `~` (home directory) on the VM — **must be co-located and run from `~`**, not a subdirectory (running from e.g. `~/.openclaw/` causes silent "file not found" errors since paths are relative):

- `extract_toolcalls.py <session_id> <output.json>` — pulls every tool call in order from the raw `.jsonl`
- `extract_usage.py <session_id> <output.json>` — pulls per-turn token usage from `.trajectory.jsonl`
- `build_summaries.py <extracts_dir> <metadata.json> <output_dir> --test-set ... --model ... --prefix ...` — second-stage script that builds per-test summary JSON plus a rollup audit summary from the two extraction scripts' output

These are not pre-installed on fresh VM clones — they had to be recreated via `nano` after the Gemma4 12B clone, since files don't automatically carry over from the base OVA/snapshot.

## Terminal / Workflow Gotchas

- **PowerShell SSH terminal mangles multi-line pastes.** Pasting a script directly at the bare `$` prompt in a plain PowerShell→SSH session causes every line to be interpreted as if typed and Enter-pressed individually — this drops loop bodies, mangles heredocs, and can hang the SSH connection entirely. Fix: open `nano <filename>` first, confirm the nano UI is visible, *then* paste — or use VS Code's Remote-SSH integrated terminal, which handles bracketed paste correctly.
- **`bash script.sh` runs in a subshell that does not inherit interactive-shell variables.** Re-declaring a `declare -A SESSIONS=(...)` array at the prompt has no effect on a script's own hardcoded array. Fixes must be made to the script file itself.
- **Working directory affects both script execution and file creation via `nano`.** A file created via `nano` while `cd`'d into `~/.openclaw` lands there, not in `~`, causing "no such file" errors when later invoked assuming it's in `~`.

## Model-Specific Behavioral Notes (relevant to optimization)

Empirical findings from the Housing / Open-Ended / Capability / Hallucination evaluation batches, worth keeping in mind for prompt/SOUL.md tuning:

- **"Type F" failure pattern — uncommitted read, fabricated computation.** Multiple sessions (H04, H07, Test1, Dirty Data, H-T1, H-T4) show **zero `exec` tool calls** — just a single `read` — yet still produce confident, detailed numeric answers. Strong evidence the model sometimes estimates/fabricates statistics by eyeballing a raw file dump rather than running verifiable code. This is the single highest-priority behavior to target in optimization — e.g. via SOUL.md guidance requiring `exec`-verified computation before any numeric claim.
- **Silent proxy substitution without asking.** On the Hallucination suite, the model repeatedly substitutes a plausible-but-wrong column (e.g. `prefarea` for "neighbourhood safety" or "household income") without flagging the substitution or asking first (H-T1, H-T3, H-T6, and partially H-T7/H-T9). Two sessions (H-T2, H-T9-partial) correctly identified a genuinely absent capability and asked/refused appropriately — worth understanding what differentiated those from the failures.
- **Format non-compliance is a separate axis from correctness.** The model twice (H02, H09) computed correct values but omitted the required `@tag[value]` brackets — worth checking if tightening output-format instructions in the agent prompt reduces this without hurting task completion.
- **Non-deterministic retry behavior.** Identical prompts sometimes produce genuinely different outcomes across runs — a Type E retry-loop spiral (Test4 attempt 2, 21 near-identical `exec` calls, empty final output) followed by a clean success on attempt 3, and separately two fully clean duplicate runs of the same ML-build prompt (Test7) with identical results. Determinism/retry behavior may be worth constraining via temperature or retry-limit settings if OpenClaw exposes them.
