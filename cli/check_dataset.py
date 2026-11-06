#!/usr/bin/env python3
"""Check the dataset's rules: every fact sourced to the vendor's own page,
dated, one per cell, and the generated files in step.

    python3 cli/check_dataset.py
    python3 cli/check_dataset.py --as-of 2027-02-01     # list facts older than 90 days on that date
    python3 cli/check_dataset.py --json

Exit 0 = no errors, 1 = errors.

Part of https://github.com/ZeraBooks/bank-statement-converter-comparison
(ZeraBooks, https://www.zerabooks.com/bank-statement-converter).
"""
import argparse
import csv
import datetime as dt
import json
import os
import re
import sys
from urllib.parse import urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STALE_DAYS = 90


def load(name):
    return list(csv.DictReader(open(os.path.join(ROOT, "data", name), encoding="utf-8")))


def domain(u):
    h = urlparse(u).hostname or ""
    parts = h.split(".")
    return ".".join(parts[-2:])


def check(as_of):
    issues = []
    tools = {t["tool_id"]: t for t in load("tools.csv")}
    fields = {f["field"] for f in load("fields.csv")}
    facts = load("facts.csv")
    seen = set()
    for n, f in enumerate(facts, start=2):
        where = f"facts.csv line {n} ({f['tool_id']}/{f['field']})"
        if f["tool_id"] not in tools or f["field"] not in fields:
            issues.append(("DS-001", "error", where, "unknown tool or field"))
            continue
        u = f["source_url"]
        if not u.startswith("https://"):
            issues.append(("DS-002", "error", where, f"source '{u}' is not an https URL"))
        elif domain(u) != domain(tools[f["tool_id"]]["website"]):
            issues.append(("DS-002", "error", where, f"source {u} isn't on the vendor's own site ({tools[f['tool_id']]['website']})"))
        try:
            d = dt.date.fromisoformat(f["checked"])
            if d > as_of:
                issues.append(("DS-003", "error", where, f"checked date {d} is after {as_of}"))
            elif (as_of - d).days > STALE_DAYS:
                issues.append(("DS-006", "warning", where, f"checked {d}, {(as_of - d).days} days before {as_of}: re-check it"))
        except ValueError:
            issues.append(("DS-003", "error", where, f"checked date '{f['checked']}' is not YYYY-MM-DD"))
        if not f["value"].strip():
            issues.append(("DS-004", "error", where, "empty value: leave the fact out instead"))
        key = (f["tool_id"], f["field"])
        if key in seen:
            issues.append(("DS-005", "error", where, "a second fact for the same tool and field"))
        seen.add(key)
        if f["field"] == "price_per_page_usd" and not re.match(r"^\d+\.\d+", f["value"]):
            issues.append(("DS-007", "error", where, f"'{f['value']}' doesn't start with a number"))
    # Generated files in step with facts.csv
    j = json.load(open(os.path.join(ROOT, "data", "facts.json"), encoding="utf-8"))
    if j["facts"] != facts:
        issues.append(("DS-008", "error", "facts.json", "doesn't match facts.csv; run scripts/generate_samples.py"))
    by = {(f["tool_id"], f["field"]): f["value"] for f in facts}
    name_to_id = {t["tool"]: k for k, t in tools.items()}
    for r in load("matrix.csv"):
        tid = name_to_id.get(r["tool"])
        for fld in fields:
            if r.get(fld, "") != by.get((tid, fld), ""):
                issues.append(("DS-008", "error", "matrix.csv", f"{r['tool']}/{fld} doesn't match facts.csv; run scripts/generate_samples.py"))
    for p in load("plans.csv"):
        if domain(p["source_url"]) != domain(tools[p["tool_id"]]["website"]):
            issues.append(("DS-002", "error", f"plans.csv {p['tool_id']} {p['plan']}", "source isn't on the vendor's own site"))
    return issues, {"tools": len(tools), "fields": len(fields), "facts": len(facts), "cells": len(tools) * len(fields)}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--as-of", type=dt.date.fromisoformat, default=dt.date.today())
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    issues, summary = check(a.as_of)
    errors = [i for i in issues if i[1] == "error"]
    if a.json:
        print(json.dumps({"ok": not errors, "summary": summary, "issues": [dict(zip(("rule", "severity", "where", "message"), i)) for i in issues]}, indent=2))
    else:
        for i in issues:
            print(f"{i[1].upper():7} {i[0]} {i[2]}: {i[3]}")
        print(f"{summary['facts']} facts for {summary['tools']} tools x {summary['fields']} fields ({summary['cells'] - summary['facts']} cells left blank). "
              + ("OK" if not errors else f"{len(errors)} error(s)"))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
