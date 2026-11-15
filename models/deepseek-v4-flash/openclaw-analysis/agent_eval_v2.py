from pathlib import Path
import json
import csv
from collections import Counter


SESSION_DIR = (
    Path.home()
    / ".openclaw/agents/main/sessions"
)


rows=[]


for file in SESSION_DIR.glob("*.trajectory.jsonl"):


    row={

        "session":file.stem,

        "tools_available":0,

        "tool_calls":0,
        "unique_tools":"",
        "unsafe_tools":0,

        "lifecycle_started":0,
        "lifecycle_completed":0,

        "input_tokens":0,
        "output_tokens":0,
        "cache_tokens":0,
        "reasoning_tokens":0,

        "timeout":False,
        "tool_error":False
    }


    tool_counter=Counter()


    for line in open(file):

        obj=json.loads(line)

        event=obj["type"]

        data=obj.get("data",{})



        if event=="context.compiled":

            row["tools_available"]=len(
                data.get("tools",[])
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



        elif event=="trace.artifacts":


            for tool in data.get(
                "toolMetas",
                []
            ):

                name=tool.get(
                    "toolName"
                )

                tool_counter[name]+=1


                if not tool.get(
                    "replaySafe",
                    True
                ):

                    row["unsafe_tools"]+=1



            lifecycle=data.get(
                "itemLifecycle",
                {}
            )


            row["lifecycle_started"]=(
                lifecycle.get(
                    "startedCount",
                    0
                )
            )


            row["lifecycle_completed"]=(
                lifecycle.get(
                    "completedCount",
                    0
                )
            )


            if data.get(
                "lastToolError"
            ):

                row["tool_error"]=True



    row["tool_calls"]=sum(
        tool_counter.values()
    )


    row["unique_tools"]=";".join(
        tool_counter.keys()
    )


    rows.append(row)



with open(
    "agent_eval_v2.csv",
    "w",
    newline=""
) as f:

    writer=csv.DictWriter(
        f,
        fieldnames=rows[0].keys()
    )

    writer.writeheader()
    writer.writerows(rows)


print("created agent_eval_v2.csv")
