import json, os, glob

sessions_dir = os.path.expanduser('~/.openclaw/agents/main/sessions/')
files = glob.glob(sessions_dir + '*.jsonl')

print(f"{'Session':<12} {'Timestamp':<30} {'First message':<50}")
print('-' * 90)

for f in sorted(files):
    if 'trajectory' in f:
        continue
    sid = os.path.basename(f)[:8]
    timestamp = ''
    first_msg = ''
    with open(f) as fh:
        for line in fh:
            try:
                e = json.loads(line)
                if not timestamp and e.get('timestamp'):
                    timestamp = e['timestamp']
                if e.get('type') == 'message':
                    msg = e.get('message', {})
                    if msg.get('role') == 'user':
                        content = msg.get('content', '')
                        if isinstance(content, str):
                            first_msg = content[:60].replace('\n', ' ')
                        elif isinstance(content, list):
                            for c in content:
                                if isinstance(c, dict) and c.get('type') == 'text':
                                    first_msg = c.get('text', '')[:60].replace('\n', ' ')
                                    break
                        if first_msg:
                            break
            except:
                pass
    if timestamp:
        print(f'{sid:<12} {timestamp:<30} {first_msg:<50}')
