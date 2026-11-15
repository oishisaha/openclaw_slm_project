from pathlib import Path
import json
import csv


SESSION_DIR = (
    Path.home()
    / ".openclaw/agents/main/sessions"
)


rows=[]


for file in SESSION_DIR.glob(
    "*.trajectory.jsonl"
):


    prompt=""


    for line in open(file):

        obj=json.loads(line)


        if obj["type"]=="prompt.submitted":

            data=obj["data"]


            messages=data.get(
                "messages",
                []
            )


            for m in messages:

                if (
                    m.get("role")
                    ==
                    "user"
                ):

                    prompt=str(
                        m.get("content")
                    )


    rows.append(
        [
            file.stem,
            prompt[:200]
        ]
    )


with open(
    "session_prompts.csv",
    "w",
    newline=""
) as f:

    writer=csv.writer(f)

    writer.writerow(
        [
            "session",
            "prompt"
        ]
    )

    writer.writerows(rows)


print("created")
