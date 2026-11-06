#!/usr/bin/env python3
"""What a month of statements costs on each converter, from published prices.

    python3 cli/cost.py --pages 600
    python3 cli/cost.py --pages 600 --statements 150 --organizations 40 --billing annual
    python3 cli/cost.py --pages 600 --csv

Tools sell in different units, so give what you know:
  --pages          statement pages a month (default needed)
  --statements     account statements a month (MoneyThumb's unit; default pages / 4)
  --organizations  client organizations (Hubdoc's unit; default 1)
  --billing        monthly or annual
Prices and plans are in data/plans.csv with their source and date. Where a
volume is past a tool's published plans, or a price isn't published, it
says so instead of guessing.

Part of https://github.com/ZeraBooks/bank-statement-converter-comparison
(ZeraBooks, https://www.zerabooks.com/bank-statement-converter).
"""
import argparse
import csv
import os
import sys
from decimal import ROUND_HALF_UP, Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))


def plans():
    from facts_source import PLANS
    return PLANS


def money(x):
    return f"{Decimal(x).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP):.2f}"


def smallest(rows, need, annual):
    ok = [p for p in rows if p[3] >= need and (p[5] if annual else p[4])]
    return min(ok, key=lambda p: p[3]) if ok else None


def estimate(pages, statements=None, organizations=None, billing="monthly"):
    statements = statements or max(1, pages // 4)
    organizations = organizations or 1
    annual = billing == "annual"
    P = plans()
    out = []

    def add(tool, plan, monthly, note=""):
        per = money(Decimal(monthly) / pages) if monthly not in (None, "") else ""
        out.append({"tool": tool, "plan": plan, "monthly": money(monthly) if monthly not in (None, "") else "", "per_page": per, "note": note})

    for tool, label in (("zerabooks", "ZeraBooks"), ("docuclipper", "DocuClipper")):
        rows = [p for p in P if p[0] == tool]
        p = smallest(rows, pages, annual)
        if p:
            add(label, p[1], p[5] if annual else p[4], "includes the ZeraBooks General Ledger" if tool == "zerabooks" else "")
        else:
            add(label, "", None, "past the largest published plan")
    rows = [p for p in P if p[0] == "autoentry"]
    credits = pages * 3
    p = smallest(rows, credits, False)
    add("AutoEntry", f"{p[1]} ({credits} credits)" if p else "", p[4] if p else None,
        "3 credits a page; monthly prices only" if p else f"{credits} credits is past the largest published plan (2,500)")
    if annual:
        rows = [p for p in P if p[0] == "moneythumb" and p[2] == "conversions_per_year"]
        p = smallest(rows, statements * 12, True)
        add("MoneyThumb", f"{p[1]} ({statements * 12} statements a year)" if p else "", p[5] if p else None,
            "priced per account statement, not per page" if p else "past the largest published yearly plan (800)")
    else:
        rows = [p for p in P if p[0] == "moneythumb" and p[2] == "conversions"]
        p = smallest(rows, statements, False)
        add("MoneyThumb", f"{p[1]} ({statements} statements)" if p else "", p[4] if p else None,
            "priced per account statement, not per page" if p else "past the largest published monthly plan (60)")
    add("Hubdoc", f"{organizations} organization{'s' if organizations != 1 else ''} x $12", Decimal("12") * organizations,
        "per organization; included in Xero Starter, Standard and Premium; statements up to 100 pages, Canada and U.S.")
    add("Dext", "Business plan + $0.32 a page", Decimal("25.21") + Decimal("0.32") * pages,
        "pay-as-you-go rate; a 50-document bundle is $13 a month; larger bundles aren't on the price page")
    add("Nanonets", "", None, "no per-page or per-statement price published")
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Monthly cost of statement conversion on each tool, from published prices.")
    ap.add_argument("--pages", type=int, required=True)
    ap.add_argument("--statements", type=int)
    ap.add_argument("--organizations", type=int)
    ap.add_argument("--billing", choices=["monthly", "annual"], default="monthly")
    ap.add_argument("--csv", action="store_true")
    a = ap.parse_args(argv)
    if a.pages <= 0:
        print("--pages must be more than 0", file=sys.stderr)
        return 2
    rows = estimate(a.pages, a.statements, a.organizations, a.billing)
    if a.csv:
        w = csv.DictWriter(sys.stdout, fieldnames=["tool", "plan", "monthly", "per_page", "note"], lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
        return 0
    s = a.statements or max(1, a.pages // 4)
    o = a.organizations or 1
    print(f"{a.pages} pages, {s} statements, {o} organization{'s' if o != 1 else ''} a month, {a.billing} billing (USD)\n")
    print(f"{'Tool':12} {'A month':>10} {'Per page':>9}  Plan / note")
    for r in rows:
        m = f"${r['monthly']}" if r["monthly"] else "n/a"
        pp = f"${r['per_page']}" if r["per_page"] else ""
        print(f"{r['tool']:12} {m:>10} {pp:>9}  {r['plan']}{'; ' if r['plan'] and r['note'] else ''}{r['note']}")
    print("\nPrices from data/plans.csv (vendor pages, dated). Check them before you decide.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
