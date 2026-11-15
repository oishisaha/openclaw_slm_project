from pathlib import Path
import json
import csv
from collections import Counter


SESSION_DIR = (
    Path.home()
    /
    ".openclaw/agents/main/sessions"
)


rows=[]


for file in SESSION_DIR.glob(
    "*.trajectory.jsonl"
):


    row={

        "session":file.stem,

        "model":"",
        "provider":"",

        "task":"",

        "tools_available":0,

        "tool_calls":0,
        "tool_sequence":"",
        "unsafe_tools":0,

        "lifecycle_started":0,
        "lifecycle_completed":0,
        "recovery_rate":1,

        "input_tokens":0,
        "output_tokens":0,
        "cache_tokens":0,
        "reasoning_tokens":0,

        "timeout":False,
        "tool_error":False,

        "answer":""

    }


    tools=[]


    for line in open(file):

        obj=json.loads(line)

        event=obj["type"]

        data=obj.get(
            "data",
            {}
        )


        if event=="trace.metadata":


            row["model"]=str(
                data.get("model","")
            )


        elif event=="context.compiled":


            row["tools_available"]=len(
                data.get(
                    "tools",
                    []
                )
            )


        elif event=="prompt.submitted":


            row["task"]=(
                data.get(
                    "prompt",
                    ""
                )
                .replace(
                    "\n",
                    " "
                )
            )


        elif event=="model.completed":


            usage=data.get(
                "usage",
                {}
            )


            row["input_tokens"]=usage.get(
                "input",
                0
            )


            row["output_tokens"]=usage.get(
                "output",
                0
            )


            row["cache_tokens"]=usage.get(
                "cacheRead",
                0
            )


            row["reasoning_tokens"]=usage.get(
                "reasoningTokens",
                0
            )


            row["timeout"]=data.get(
                "timedOut",
                False
            )


            row["answer"]=" ".join(
                data.get(
                    "assistantTexts",
                    []
                )
            )


        elif event=="trace.artifacts":


            for t in data.get(
                "toolMetas",
                []
            ):


                tools.append(
                    t["toolName"]
                )


                if (
                    t.get(
                        "replaySafe"
                    )
                    ==
                    False
                ):

                    row["unsafe_tools"]+=1



            lifecycle=data.get(
                "itemLifecycle",
                {}
            )


            started=lifecycle.get(
                "startedCount",
                0
            )

            completed=lifecycle.get(
                "completedCount",
                0
            )


            row["lifecycle_started"]=started

            row["lifecycle_completed"]=completed


            if started:

                row["recovery_rate"]=(
                    completed/started
                )


            if data.get(
                "lastToolError"
            ):

                row["tool_error"]=True



    row["tool_calls"]=len(
        tools
    )

    row["tool_sequence"]=" > ".join(
        tools
    )


    rows.append(row)



with open(
    "final_agent_trace_dataset.csv",
    "w",
    newline=""
) as f:


    writer=csv.DictWriter(
        f,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()

    writer.writerows(rows)



print(
    "created final_agent_trace_dataset.csv"
)
