from pathlib import Path
import json
import csv


SESSION_DIR = (
    Path.home()
    / ".openclaw/agents/main/sessions"
)


rows = []


for file in SESSION_DIR.glob(
    "*.trajectory.jsonl"
):

    row = {

        "session": file.stem,

        "task": "",

        "model": "",

        "tools_available": 0,

        "tool_calls": 0,

        "tool_sequence": "",

        "files_created": "",

        "input_tokens": 0,

        "output_tokens": 0,

        "reasoning_tokens": 0,

        "lifecycle_started": 0,

        "lifecycle_completed": 0,

        "recovery_rate": 1,

        "tool_error": False

    }


    tools = []

    files = []


    for line in open(file):

        obj = json.loads(line)


        event = obj.get(
            "type",
            ""
        )


        data = obj.get(
            "data",
            {}
        )


        # -------------------------
        # model metadata
        # -------------------------

        if event == "trace.metadata":

            row["model"] = str(
                data.get(
                    "model",
                    ""
                )
            )


        # -------------------------
        # available tools
        # -------------------------

        elif event == "context.compiled":

            row["tools_available"] = len(
                data.get(
                    "tools",
                    []
                )
            )


        # -------------------------
        # user task
        # -------------------------

        elif event == "prompt.submitted":

            row["task"] = (
                data.get(
                    "prompt",
                    ""
                )
                .replace(
                    "\n",
                    " "
                )
            )


        # -------------------------
        # token usage
        # -------------------------

        elif event == "model.completed":

            usage = data.get(
                "usage",
                {}
            )


            row["input_tokens"] = usage.get(
                "input",
                0
            )


            row["output_tokens"] = usage.get(
                "output",
                0
            )


            row["reasoning_tokens"] = usage.get(
                "reasoningTokens",
                0
            )


        # -------------------------
        # tool behaviour
        # -------------------------

        elif event == "trace.artifacts":


            for t in data.get(
                "toolMetas",
                []
            ):


                tool_name = t.get(
                    "toolName",
                    ""
                )


                tools.append(
                    tool_name
                )


                meta = t.get(
                    "meta",
                    ""
                )


                # capture generated artifacts

                if (
                    ".png" in meta
                    or ".pptx" in meta
                    or ".py" in meta
                    or ".html" in meta
                    or tool_name == "write"
                ):

                    files.append(
                        meta
                    )


            lifecycle = data.get(
                "itemLifecycle",
                {}
            )


            started = lifecycle.get(
                "startedCount",
                0
            )


            completed = lifecycle.get(
                "completedCount",
                0
            )


            row["lifecycle_started"] = started

            row["lifecycle_completed"] = completed


            if started:

                row["recovery_rate"] = (
                    completed / started
                )


            if data.get(
                "lastToolError"
            ):

                row["tool_error"] = True



    # ----------------------------------
    # KEEP ONLY HOUSING ANALYSIS TESTS
    # ----------------------------------

    task_lower = row[
        "task"
    ].lower()


    if (

        "housing" in task_lower

        or "house" in task_lower

        or "price" in task_lower

        or "furnishing" in task_lower

        or "visualization" in task_lower

        or "visualisation" in task_lower

        or "machine learning" in task_lower

        or "regression model" in task_lower

        or "predict" in task_lower

        or "executive" in task_lower

        or "slide" in task_lower

        or "powerpoint" in task_lower

        or "presentation" in task_lower

    ):


        row["tool_calls"] = len(
            tools
        )


        row["tool_sequence"] = (
            " > ".join(
                tools
            )
        )


        row["files_created"] = (
            " | ".join(
                files
            )
        )


        rows.append(
            row
        )


# -------------------------
# write final CSV
# -------------------------


with open(
    "housing_agent_eval.csv",
    "w",
    newline=""
) as f:


    writer = csv.DictWriter(
        f,
        fieldnames=rows[0].keys()
    )


    writer.writeheader()


    writer.writerows(
        rows
    )


print(
    "Housing sessions extracted:",
    len(rows)
)


print(
    "Created: housing_agent_eval.csv"
)
