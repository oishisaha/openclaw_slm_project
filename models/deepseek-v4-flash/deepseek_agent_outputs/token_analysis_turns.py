import json, os, glob

sessions_dir = os.path.expanduser('~/.openclaw/agents/main/sessions/')
traj_files = sorted(glob.glob(sessions_dir + '*.trajectory.jsonl'))

print(f"Found {len(traj_files)} trajectory files")
print()

for f in traj_files:
    sid = os.path.basename(f)[:8]
    turns = []
    with open(f) as fh:
        for line in fh:
            try:
                e = json.loads(line)
                if e.get('type') == 'model.completed':
                    d = e.get('data', {})
                    usage = d.get('usage', {})
                    # also grab what the model actually output
                    texts = d.get('assistantTexts', [])
                    tool_calls = d.get('toolCalls', [])
                    turns.append({
                        'input':        usage.get('inputTokens', 0),
                        'output':       usage.get('outputTokens', 0),
                        'reasoning':    usage.get('reasoningTokens', 0),
                        'cache_read':   usage.get('cacheReadTokens', 0),
                        'cache_write':  usage.get('cacheWriteTokens', 0),
                        'text_chars':   sum(len(t) for t in texts),
                        'tool_calls':   len(tool_calls),
                        'tool_names':   [tc.get('name','?') for tc in tool_calls],
                    })
            except:
                pass

    if not turns:
        continue

    print(f"=== {sid} ({len(turns)} turns) ===")
    print(f"  {'Turn':<5} {'Input':>8} {'Output':>7} {'Reason':>7} {'CacheR':>8} {'Tools':>6} {'Tool names'}")
    print(f"  {'-'*70}")
    for i, t in enumerate(turns):
        tools = ','.join(t['tool_names']) if t['tool_names'] else '-'
        print(f"  {i+1:<5} {t['input']:>8,} {t['output']:>7,} {t['reasoning']:>7,} {t['cache_read']:>8,} {t['tool_calls']:>6} {tools}")

    # session totals
    total_in  = sum(t['input'] for t in turns)
    total_out = sum(t['output'] for t in turns)
    total_rea = sum(t['reasoning'] for t in turns)
    total_cr  = sum(t['cache_read'] for t in turns)
    print(f"  {'TOTAL':<5} {total_in:>8,} {total_out:>7,} {total_rea:>7,} {total_cr:>8,}")
    print()
