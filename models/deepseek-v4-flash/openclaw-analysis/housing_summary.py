import pandas as pd


df = pd.read_csv(
    "housing_agent_eval.csv"
)


print("="*50)

print(
    "HOUSING AGENT EVALUATION"
)

print("="*50)


print(
    "\nSessions:"
)

print(
    len(df)
)


print(
    "\nAverage tool calls:"
)

print(
    df.tool_calls.mean()
)


print(
    "\nMax tool calls:"
)

print(
    df.tool_calls.max()
)


print(
    "\nAverage tools available:"
)

print(
    df.tools_available.mean()
)


print(
    "\nAverage input tokens:"
)

print(
    round(
        df.input_tokens.mean()
    )
)


print(
    "\nRecovery rate:"
)

print(
    df.recovery_rate.mean()
)


print(
    "\nTool errors:"
)

print(
    df.tool_error.sum()
)


all_tools=[]


for seq in df.tool_sequence.dropna():

    for tool in seq.split(" > "):

        if tool:

            all_tools.append(tool)


print(
    "\nTool frequency:"
)


print(
    pd.Series(
        all_tools
    )
    .value_counts()
)
