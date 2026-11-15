from pathlib import Path
import json
import re


SESSION_DIR=Path.home()/".openclaw/agents/main/sessions"


keywords=[

"error",
"failed",
"retry",
"fix",
"incorrect",
"mistake",
"try again",
"issue",
"bug",
"recalculate",
"verify"

]


for file in SESSION_DIR.glob("*.trajectory.jsonl"):

    hits=[]

    for line in open(file):

        text=line.lower()


        for word in keywords:

            if word in text:
                hits.append(word)


    if hits:

        print(
            file.name,
            set(hits)
        )
