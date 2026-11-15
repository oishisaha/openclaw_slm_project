from pathlib import Path
import json
from collections import Counter


SESSION_DIR = Path.home() / ".openclaw/agents/main/sessions"


for file in SESSION_DIR.glob("*.trajectory.jsonl"):

    tools=Counter()

    for line in open(file):

        try:
            obj=json.loads(line)
        except:
            continue


        text=json.dumps(obj)


        possible_tools=[
            "exec",
            "read",
            "write",
            "web_fetch",
            "web_search",
            "memory",
            "cron",
            "canvas"
        ]


        for t in possible_tools:

            if t in text:
                tools[t]+=1


    if tools:

        print("\nSESSION:",file.name)

        for tool,count in tools.items():
            print(
                tool,
                count
            )
