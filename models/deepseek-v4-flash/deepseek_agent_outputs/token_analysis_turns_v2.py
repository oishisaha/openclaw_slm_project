import json, os, glob

sessions_dir = os.path.expanduser('~/.openclaw/agents/main/sessions/')
traj_files = sorted(glob.glob(sessions_dir + '*.trajectory.jsonl'))

print(f"Found {len(traj_files)} trajectory files")
print()

all_sessions = []

for f in traj_files:
    sid = os.path.basename(f)[:8]
    turns = []

    with open(f) as fh:
        for line in fh:
            try:
                e = json.loads(line)
                if e.get('type') == 'model.completed':
                    d = e.get('data', {})
                    u = d.get('usage', {})
                    lcu = d.get('promptCache', {}).get('lastCallUsage', {})
                    texts = d.get('assistantTexts', [])
                    timed_out = d.get('timedOut', False)
                    model = e.get('modelId', '?')

                    # cumulative usage (total so far in session)
                    cum_in     = u.get('input', 0)
                    cum_out    = u.get('output', 0)
                    cum_cache  = u.get('cacheRead', 0)
                    cum_reason = u.get('reasoningTokens', 0)

                    # per-call usage (just this turn)
                    call_in    = lcu.get('input', 0)
                    call_out   = lcu.get('output', 0)
                    call_cache = lcu.get('cacheRead', 0)
                    call_write = lcu.get('cacheWrite', 0)

                    # what the model actually said
                    text_len = sum(len(t) for t in texts)
                    n_texts  = len(texts)

                    turns.append({
                        'cum_in': cum_in, 'cum_out': cum_out,
                        'cum_cache': cum_cache, 'cum_reason': cum_reason,
                        'call_in': call_in, 'call_out': call_out,
                        'call_cache': call_cache, 'call_write': call_write,
                        'text_len': text_len, 'n_texts': n_texts,
                        'timed_out': timed_out, 'model': model,
                    })
            except:
                pass

    if not turns:
        continue

    all_sessions.append({'sid': sid, 'turns': turns})

    # print turn-by-turn for multi-turn sessions
    if len(turns) > 1:
        print(f"=== {sid} ({len(turns)} turns) model={turns[0]['model']} ===")
        print(f"  {'Turn':<5} {'CallIn':>8} {'CallOut':>8} {'CacheR':>8} {'CacheW':>7} {'Reason':>7} {'TextLen':>8} {'Texts':>6}")
        print(f"  {'-'*75}")
        for i, t in enumerate(turns):
            print(f"  {i+1:<5} {t['call_in']:>8,} {t['call_out']:>8,} {t['call_cache']:>8,} {t['call_write']:>7,} {t['cum_reason']:>7,} {t['text_len']:>8,} {t['n_texts']:>6}")
        last = turns[-1]
        print(f"  {'CUM':<5} {last['cum_in']:>8,} {last['cum_out']:>8,} {last['cum_cache']:>8,} {'':>7} {last['cum_reason']:>7,}")
        print()

# ── AGGREGATE ANALYSIS ────────────────────────────────────────────────────────
print("\n" + "="*70)
print("AGGREGATE ANALYSIS — ALL SESSIONS")
print("="*70)

all_turns_flat = [t for s in all_sessions for t in s['turns']]
n_sessions = len(all_sessions)
n_turns    = len(all_turns_flat)

# Use cumulative from last turn of each session for session totals
session_totals = []
for s in all_sessions:
    last = s['turns'][-1]
    session_totals.append({
        'sid': s['sid'],
        'input': last['cum_in'],
        'output': last['cum_out'],
        'cache': last['cum_cache'],
        'reasoning': last['cum_reason'],
        'n_turns': len(s['turns']),
    })

total_input    = sum(s['input']     for s in session_totals)
total_output   = sum(s['output']    for s in session_totals)
total_cache    = sum(s['cache']     for s in session_totals)
total_reasoning= sum(s['reasoning'] for s in session_totals)
total_tokens   = total_input + total_output + total_cache

print(f"\nSessions:          {n_sessions}")
print(f"Total input:       {total_input:>12,} tokens")
print(f"Total output:      {total_output:>12,} tokens")
print(f"Total cache reads: {total_cache:>12,} tokens")
print(f"Total reasoning:   {total_reasoning:>12,} tokens")
print()
print(f"Avg input/session:     {total_input/n_sessions:>10,.0f} tokens")
print(f"Avg output/session:    {total_output/n_sessions:>10,.0f} tokens")
print(f"Avg cache/session:     {total_cache/n_sessions:>10,.0f} tokens")
print(f"Avg reasoning/session: {total_reasoning/n_sessions:>10,.0f} tokens")
print()

# Output breakdown — why is output so low?
print("OUTPUT BREAKDOWN (what drives low output):")
for s in sorted(session_totals, key=lambda x: x['output'], reverse=True)[:10]:
    ratio = s['output']/s['input']*100 if s['input'] > 0 else 0
    print(f"  {s['sid']}  input={s['input']:>8,}  output={s['output']:>7,}  ratio={ratio:.1f}%  turns={s['n_turns']}")

print()

# Cache efficiency
print("CACHE EFFICIENCY:")
for s in sorted(session_totals, key=lambda x: x['cache'], reverse=True)[:5]:
    if s['input'] > 0:
        cache_pct = s['cache']/(s['input']+s['cache'])*100
        print(f"  {s['sid']}  cache={s['cache']:>8,}  ({cache_pct:.0f}% of total context served from cache)")

print()

# Reasoning analysis
print("REASONING TOKENS (thinkLevel:high evidence):")
for s in sorted(session_totals, key=lambda x: x['reasoning'], reverse=True)[:10]:
    print(f"  {s['sid']}  reasoning={s['reasoning']:>7,}  output={s['output']:>7,}  ratio={s['reasoning']/max(s['output'],1):.2f}x output")

print()

# Cost
total_cost = (total_input/1e6)*0.09 + (total_output/1e6)*0.18 + (total_cache/1e6)*0.0036
print(f"TOTAL COST: ${total_cost:.4f}")
print(f"  Input:      ${(total_input/1e6)*0.09:.4f}")
print(f"  Output:     ${(total_output/1e6)*0.18:.4f}")
print(f"  Cache read: ${(total_cache/1e6)*0.0036:.4f}")
