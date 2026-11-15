#!/usr/bin/env python3
"""
Extract every tool call (exec/write/read/process/canvas/...) from an OpenClaw
session, in order, with full code/arguments and timestamps.

Usage:
    python3 extract_toolcalls.py <session_id> <output_name>

Reads from:
    ~/.openclaw/agents/main/sessions/<session_id>.jsonl
    (the RAW session log — not the .trajectory.jsonl file, which does not
    reliably contain full tool-call code past the first few turns)
"""
import json
import os
import sys

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    session_id, out_path = sys.argv[1], sys.argv[2]
    session_path = os.path.expanduser(f"~/.openclaw/agents/main/sessions/{session_id}.jsonl")

    if not os.path.exists(session_path):
        print(f"ERROR: not found: {session_path}")
        print("Double check the session_id (it's the UUID, not the 'tui-...' display id).")
        sys.exit(1)

    out = []
    with open(session_path) as f:
        for line in f:
            try:
                d = json.loads(line)
            except json.JSONDecodeError:
                continue
            msg = d.get("message")
            if not isinstance(msg, dict) or msg.get("role") != "assistant":
                continue
            content = msg.get("content")
            if not isinstance(content, list):
                continue
            for block in content:
                if block.get("type") == "toolCall":
                    out.append({
                        "timestamp": d.get("timestamp"),
                        "tool": block.get("name"),
                        "arguments": block.get("arguments"),
                    })

    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    print(f"Wrote {len(out)} tool calls to {out_path}")
    from collections import Counter
    counts = Counter(c["tool"] for c in out)
    for tool, n in counts.most_common():
        print(f"  {tool}: {n}")

if __name__ == "__main__":
    main()
