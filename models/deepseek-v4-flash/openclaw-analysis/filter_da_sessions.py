import pandas as pd


df=pd.read_csv(
    "final_agent_trace_dataset.csv"
)


da=df[
    df.task
    .fillna("")
    .str.contains(
        "insurance|vaccination|csv|data/",
        case=False
    )
]


da.to_csv(
    "dabench_agent_eval.csv",
    index=False
)


print(
    "DA sessions:",
    len(da)
)


print(
    da[
        [
        "task",
        "tool_calls",
        "input_tokens",
        "recovery_rate",
        "tool_error"
        ]
    ]
)
