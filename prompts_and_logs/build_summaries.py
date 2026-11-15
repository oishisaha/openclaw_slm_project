#!/usr/bin/env python3
"""
build_summaries.py — turn raw OpenClaw extraction files into a
per-question "audit folder" of summary JSON (time taken, token usage,
tool-call breakdown, verdict, notes), plus one combined rollup file.

This is a SEPARATE, second-stage script — it does not replace or modify
extract_toolcalls.py / extract_usage.py. Run those first (per
openclaw_code_audit_guide.md), then run this on their output.

Usage:
    python3 build_summaries.py <extracts_dir> <metadata_json> <output_dir> \
        --test-set "Name of this test set" \
        --model "ollama/qwen3.5:9b" \
        --deployment "Local (host-laptop Ollama via VirtualBox NAT, 10.0.2.2:11434)" \
        --date "2026-08-04" \
        --prefix "qwen3.5-9b"

Example:
    python3 build_summaries.py \
        ./qwen3.5-9b_extracts \
        ./openended_metadata.json \
        ./qwen3.5-9b_openended_audit \
        --test-set "Open-Ended DA Tests (Tests 1-5)" \
        --model "ollama/qwen3.5:9b" \
        --prefix "qwen3.5-9b"

INPUT 1 — extracts_dir:
    A folder containing pairs of files named:
        <prefix>_<test_id>_toolcalls.json
        <prefix>_<test_id>_token_usage.json
    exactly as produced by extract_toolcalls.py / extract_usage.py.
    test_id can be anything (H01, T1, Test1, CR01, PD01, ...) — it's
    auto-discovered from the filenames, no need to edit this script per
    test set.

INPUT 2 — metadata_json:
    A JSON file mapping each test_id to the human-judgment fields that
    can't be computed automatically:
        {
          "H01": {
            "title": "H01 — Mean Price (Easy)",
            "prompt": "The file data/housing_dataset.csv contains...",
            "ground_truth": "@mean_price[4766729.25]",       (optional)
            "model_output": "...",                            (optional)
            "verdict": "PASS",                                (required)
            "notes": ["note 1", "note 2"]                     (optional)
          },
          "H02": { ... }
        }
    Only "title", "verdict" are required per entry; the rest are
    optional and will just be omitted from the summary if absent.
    See metadata_template.json for a blank starting point.

OUTPUT (written to output_dir):
    <prefix>_<test_id>_summary.json   — one per test_id
    <prefix>_<test_set-slug>_audit_summary.json  — combined rollup with
        aggregate totals (tool calls, tokens, time, verdict counts)

Notes on computed fields:
    time_taken_seconds — delta between the first and last tool-call
        timestamp in that test's toolcalls.json. This is elapsed
        tool-calling wall-clock time, not total model "thinking" time,
        and not the same as the token_usage log's own timestamp (which
        is typically a single cumulative entry per session, not one per
        turn, so it can't be used for elapsed-time calculation the same
        way).
    token_usage — taken directly from the first entry in that test's
        token_usage.json. If a session logs multiple usage entries
        (e.g. a genuinely multi-turn session), only the first is used;
        rerun with --sum-usage to sum all entries instead.
"""
import argparse
import datetime
import json
import os
import re
import sys
from collections import Counter
from glob import glob


def parse_args():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("extracts_dir", help="Folder containing *_toolcalls.json / *_token_usage.json pairs")
    p.add_argument("metadata_json", help="JSON file with title/prompt/ground_truth/verdict/notes per test_id")
    p.add_argument("output_dir", help="Folder to write summary JSON files into (created if missing)")
    p.add_argument("--test-set", required=True, help="Human-readable name of this test set, e.g. 'Open-Ended DA Tests (Tests 1-5)'")
    p.add_argument("--model", required=True, help="Model identifier, e.g. 'ollama/qwen3.5:9b'")
    p.add_argument("--deployment", default="", help="Deployment description, e.g. 'Local (host-laptop Ollama via VirtualBox NAT, 10.0.2.2:11434)'")
    p.add_argument("--date", default=datetime.date.today().isoformat(), help="Date of the test run (default: today)")
    p.add_argument("--prefix", required=True, help="Filename prefix used in extraction files, e.g. 'qwen3.5-9b'")
    p.add_argument("--sum-usage", action="store_true", help="Sum all token_usage entries instead of taking only the first")
    p.add_argument("--copy-raw", action="store_true", help="Also copy the raw toolcalls/token_usage files into output_dir/raw_extracts/")
    return p.parse_args()


def discover_test_ids(extracts_dir, prefix):
    pattern = os.path.join(extracts_dir, f"{prefix}_*_toolcalls.json")
    ids = []
    for path in sorted(glob(pattern)):
        fname = os.path.basename(path)
        m = re.match(rf"^{re.escape(prefix)}_(.+)_toolcalls\.json$", fname)
        if m:
            ids.append(m.group(1))
    return ids


def elapsed_seconds(toolcalls):
    if not toolcalls:
        return 0.0
    fmt = "%Y-%m-%dT%H:%M:%S.%fZ"
    try:
        t0 = datetime.datetime.strptime(toolcalls[0]["timestamp"], fmt)
        t1 = datetime.datetime.strptime(toolcalls[-1]["timestamp"], fmt)
        return round((t1 - t0).total_seconds(), 3)
    except (KeyError, ValueError, TypeError):
        return None


def human_time(seconds):
    if seconds is None:
        return "unknown"
    return f"{seconds/60:.1f} min" if seconds >= 60 else f"{seconds:.1f} sec"


def verdict_bucket(v):
    """First word of the verdict string, used to group the aggregate verdict_counts."""
    if not v:
        return "UNSPECIFIED"
    return v.split()[0].rstrip(":—-").upper()


def main():
    args = parse_args()

    if not os.path.isdir(args.extracts_dir):
        sys.exit(f"ERROR: extracts_dir not found: {args.extracts_dir}")
    if not os.path.isfile(args.metadata_json):
        sys.exit(f"ERROR: metadata_json not found: {args.metadata_json}")

    with open(args.metadata_json) as f:
        metadata = json.load(f)

    test_ids = discover_test_ids(args.extracts_dir, args.prefix)
    if not test_ids:
        sys.exit(f"ERROR: no '{args.prefix}_*_toolcalls.json' files found in {args.extracts_dir}")

    missing_meta = [t for t in test_ids if t not in metadata]
    if missing_meta:
        print(f"WARNING: no metadata entry for: {', '.join(missing_meta)} — these will use minimal placeholder fields.")

    os.makedirs(args.output_dir, exist_ok=True)
    if args.copy_raw:
        raw_dir = os.path.join(args.output_dir, "raw_extracts")
        os.makedirs(raw_dir, exist_ok=True)

    all_summaries = []

    for tid in test_ids:
        tc_path = os.path.join(args.extracts_dir, f"{args.prefix}_{tid}_toolcalls.json")
        us_path = os.path.join(args.extracts_dir, f"{args.prefix}_{tid}_token_usage.json")

        with open(tc_path) as f:
            toolcalls = json.load(f)

        usage_entries = []
        if os.path.isfile(us_path):
            with open(us_path) as f:
                usage_entries = json.load(f)

        if args.sum_usage and usage_entries:
            usage = {
                "input": sum(u.get("input", 0) or 0 for u in usage_entries),
                "output": sum(u.get("output", 0) or 0 for u in usage_entries),
                "total": sum(u.get("total", 0) or 0 for u in usage_entries),
                "turns_logged": len(usage_entries),
            }
        elif usage_entries:
            usage = {
                "input": usage_entries[0].get("input"),
                "output": usage_entries[0].get("output"),
                "total": usage_entries[0].get("total"),
                "turns_logged": len(usage_entries),
            }
        else:
            usage = {"input": None, "output": None, "total": None, "turns_logged": 0}

        counts = dict(Counter(c.get("tool", "unknown") for c in toolcalls))
        et = elapsed_seconds(toolcalls)
        meta = metadata.get(tid, {})

        summary = {
            "test_id": tid,
            "title": meta.get("title", tid),
            "prompt": meta.get("prompt"),
            "session_id": meta.get("session_id"),
            "model": args.model,
            "ground_truth": meta.get("ground_truth"),
            "model_output": meta.get("model_output"),
            "time_taken_seconds": et,
            "time_taken_human": human_time(et),
            "token_usage": usage,
            "tool_calls": {"total": len(toolcalls), "breakdown": counts},
            "verdict": meta.get("verdict", "UNSPECIFIED"),
            "notes": meta.get("notes", []),
        }
        # drop null-valued optional keys for a cleaner file
        summary = {k: v for k, v in summary.items() if v is not None}
        all_summaries.append(summary)

        out_path = os.path.join(args.output_dir, f"{args.prefix}_{tid}_summary.json")
        with open(out_path, "w") as f:
            json.dump(summary, f, indent=2)

        if args.copy_raw:
            import shutil
            shutil.copy(tc_path, raw_dir)
            if os.path.isfile(us_path):
                shutil.copy(us_path, raw_dir)

    slug = re.sub(r"[^a-z0-9]+", "_", args.test_set.lower()).strip("_")
    rollup = {
        "model": args.model,
        "deployment": args.deployment,
        "test_set": args.test_set,
        "date": args.date,
        "tests": all_summaries,
        "aggregate": {
            "total_tool_calls": sum(s["tool_calls"]["total"] for s in all_summaries),
            "total_tokens": sum((s["token_usage"].get("total") or 0) for s in all_summaries),
            "total_time_seconds": round(sum((s.get("time_taken_seconds") or 0) for s in all_summaries), 3),
            "verdict_counts": dict(Counter(verdict_bucket(s.get("verdict")) for s in all_summaries)),
        },
    }
    rollup_path = os.path.join(args.output_dir, f"{args.prefix}_{slug}_audit_summary.json")
    with open(rollup_path, "w") as f:
        json.dump(rollup, f, indent=2)

    print(f"Wrote {len(all_summaries)} per-test summaries + 1 rollup to {args.output_dir}/")
    print(f"Aggregate: {rollup['aggregate']}")


if __name__ == "__main__":
    main()
