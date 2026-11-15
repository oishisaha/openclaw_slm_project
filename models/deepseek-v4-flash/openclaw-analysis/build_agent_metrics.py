from pathlib import Path
import json
import csv


SESSION_DIR=Path.home()/".openclaw/agents/main/sessions"


rows=[]


for file in SESSION_DIR.glob("*.trajectory.jsonl"):

    turns=0
    tool_calls=0
    corrections=0
    tokens=0


    for line in open(file):

        turns+=1

        text=line.lower()


        if "tool" in text:
            tool_calls+=1


        if any(
            x in text
            for x in [
                "error",
                "retry",
                "fix",
                "mistake",
                "verify"
            ]
        ):
            corrections+=1



    rows.append(
        [
            file.name,
            turns,
            tool_calls,
            corrections
        ]
    )


with open(
    "agent_metrics.csv",
    "w",
    newline=""
) as f:

    writer=csv.writer(f)

    writer.writerow(
        [
            "session",
            "trajectory_events",
            "tool_calls",
            "self_correction_events"
        ]
    )

    writer.writerows(rows)



print("created agent_metrics.csv")
