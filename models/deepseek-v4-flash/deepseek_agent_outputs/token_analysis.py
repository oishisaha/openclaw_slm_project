import json, os, glob

sessions_dir = os.path.expanduser('~/.openclaw/agents/main/sessions/')
files = glob.glob(sessions_dir + '*.jsonl')

print(f"{'Session':<12} {'Input':>8} {'Output':>7} {'Cache':>8} {'Cost USD':>10}")
print('-' * 55)

for f in sorted(files):
    if 'trajectory' in f:
        continue
    sid = os.path.basename(f)[:8]
    total_in = total_out = total_cache = 0
    has_usage = False
    with open(f) as fh:
        for line in fh:
            try:
                e = json.loads(line)
                if e.get('type') == 'message' and 'usage' in e.get('message', {}):
                    u = e['message']['usage']
                    total_in    += u.get('input', 0)
                    total_out   += u.get('output', 0)
                    total_cache += u.get('cacheRead', 0)
                    has_usage = True
            except:
                pass
    if has_usage:
        cost = (total_in/1e6)*0.09 + (total_out/1e6)*0.18 + (total_cache/1e6)*0.0036
        print(f'{sid:<12} {total_in:>8,} {total_out:>7,} {total_cache:>8,} {cost:>10.5f}')
