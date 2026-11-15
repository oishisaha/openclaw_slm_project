import pandas as pd


df=pd.read_csv(
    "final_agent_trace_dataset.csv"
)


print("="*50)
print("OPENCLAW AGENT EVALUATION SUMMARY")
print("="*50)


print("\nSessions analysed:")
print(len(df))


print("\nAverage available tools:")
print(
    df.tools_available.mean()
)


print("\nAverage tool calls:")
print(
    df.tool_calls.mean()
)


print("\nMax tool calls:")
print(
    df.tool_calls.max()
)


print("\nAverage input tokens:")
print(
    round(
        df.input_tokens.mean()
    )
)


print("\nAverage output tokens:")
print(
    round(
        df.output_tokens.mean()
    )
)


print("\nAverage reasoning tokens:")
print(
    round(
        df.reasoning_tokens.mean()
    )
)


print("\nAverage recovery rate:")
print(
    df.recovery_rate.mean()
)


print("\nSessions with tool errors:")
print(
    df.tool_error.sum()
)


print("\nTimeouts:")
print(
    df.timeout.sum()
)



all_tools=[]


for seq in df.tool_sequence.dropna():

    for tool in seq.split(" > "):

        if tool.strip():

            all_tools.append(tool)


print("\nTool frequency:")
print(
    pd.Series(
        all_tools
    )
    .value_counts()
)
