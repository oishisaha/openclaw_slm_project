from pathlib import Path
import json


file = (
    Path.home()
    / ".openclaw/agents/main/sessions"
    / "3c57b566-362a-4801-8d1d-adf82d3996da.trajectory.jsonl"
)


for line in open(file):

    obj=json.loads(line)

    print("\n====================")
    print(obj["type"])
    print("====================")

    data=obj.get("data",{})

    if isinstance(data,dict):

        print(data.keys())

    else:

        print(type(data))
