#!/usr/bin/env python3
"""
Extract per-turn token usage from an OpenClaw session's trajectory log.

Usage:
    python3 extract_usage.py <session_id> <output_name>

Reads from:
    ~/.openclaw/agents/main/sessions/<session_id>.trajectory.jsonl

Note: some models/sessions stop logging usage after a certain point (a
runtime logging cutoff, not a sign anything failed). This script writes
whatever is present per turn, including turns with no usage data.
"""
import json
import os
import sys

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    session_id, out_path = sys.argv[1], sys.argv[2]
    traj_path = os.path.expanduser(f"~/.openclaw/agents/main/sessions/{session_id}.trajectory.jsonl")

    if not os.path.exists(traj_path):
        print(f"ERROR: not found: {traj_path}")
        sys.exit(1)

    out = []
    with open(traj_path) as f:
        for line in f:
            d = json.loads(line)
            if d.get("type") == "model.completed":
                u = d["data"].get("usage", {})
                out.append({"ts": d.get("ts"), "seq": d.get("seq"), **u})

    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)

    n_with_usage = sum(1 for t in out if "total" in t)
    print(f"Wrote {len(out)} turns to {out_path} ({n_with_usage} with usage data, {len(out)-n_with_usage} without)")

if __name__ == "__main__":
    main()
