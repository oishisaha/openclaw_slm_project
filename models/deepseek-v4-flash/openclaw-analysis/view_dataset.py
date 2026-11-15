import pandas as pd


df = pd.read_csv(
    "final_agent_trace_dataset.csv"
)


cols=[
    "session",
    "task",
    "tool_calls",
    "tool_sequence",
    "input_tokens",
    "output_tokens",
    "recovery_rate",
    "tool_error"
]


print(
    df[cols]
    .head(20)
    .to_string()
)
