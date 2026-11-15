from pathlib import Path
import json
from collections import Counter, defaultdict


SESSION_DIR = Path.home() / ".openclaw/agents/main/sessions"


files = list(
    SESSION_DIR.glob("*.trajectory.jsonl")
)

print(f"Found {len(files)} trajectory files")


event_types = Counter()
keys = Counter()


for file in files:

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            try:
                obj=json.loads(line)

            except Exception:
                continue

            for k in obj.keys():
                keys[k]+=1

            if "type" in obj:
                event_types[obj["type"]] +=1



print("\n=== EVENT TYPES ===")

for k,v in event_types.most_common():
    print(k,v)



print("\n=== TOP JSON KEYS ===")

for k,v in keys.most_common():
    print(k,v)
