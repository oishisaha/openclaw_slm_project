import json, os, glob

sessions_dir = os.path.expanduser('~/.openclaw/agents/main/sessions/')
traj_files = sorted(glob.glob(sessions_dir + '*.trajectory.jsonl'))

# Read one complex session and look at full trace.artifacts structure
target = None
for f in traj_files:
    if 'dadb1483' in f:
        target = f
        break

with open(target) as fh:
    for line in fh:
        try:
            e = json.loads(line)
            if e.get('type') == 'trace.artifacts':
                print("=== trace.artifacts ===")
                print(json.dumps(e.get('data', {}), indent=2)[:4000])
                break
        except:
            pass
