"""Rebuild the dataset and samples.

    python3 scripts/generate_samples.py

From scripts/facts_source.py: data/facts.csv, data/facts.json, data/matrix.csv,
data/plans.csv, docs/comparison.md and data/cost-at-volume.csv (cli/cost.py at
100, 250, 500, 1,000, 2,500 and 5,000 pages a month).
Also writes samples/worked-examples/: the fictional statements used on the
ZeraBooks bank pages, as CSV with a sidecar of printed balances. They add up.
"""
import csv
import json
import os
import sys
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
sys.path.insert(0, os.path.join(ROOT, "cli"))
from facts_source import FACTS, PLANS  # noqa: E402

EXAMPLES = {
    "citi-two-accounts-2026-06": {
        "bank": "Citi", "business": "Harbor Lane Studio (fictional)", "page": "https://www.zerabooks.com/citi-bank-statement-to-excel",
        "accounts": {
            "Checking ...6630": ("7412.90", [("06/02/26", "MOBILE DEPOSIT", "2300.00"), ("06/09/26", "ACH PAYROLL GUSTO", "-3118.44"),
                                             ("06/12/26", "ONLINE TRANSFER TO SAVINGS ...6648 Reference # 7731", "-1000.00"),
                                             ("06/20/26", "STRIPE TRANSFER", "1650.00"), ("06/30/26", "MONTHLY SERVICE FEE", "-15.00")], "7229.46"),
            "Savings ...6648": ("12000.00", [("06/12/26", "ONLINE TRANSFER FROM CHECKING ...6630 Reference # 7731", "1000.00"),
                                             ("06/30/26", "INTEREST PAID", "4.12")], "13004.12")}},
    "us-bank-dec-to-jan": {
        "bank": "U.S. Bank", "business": "Pinecrest Auto Detailing (fictional)", "page": "https://www.zerabooks.com/us-bank-statement-to-excel",
        "accounts": {"Silver Business Checking ...2219": ("3845.10", [
            ("2025-12-29", "MOBILE CHECK DEPOSIT", "1200.00"), ("2026-01-09", "SQUARE INC DEPOSIT", "2764.35"),
            ("2025-12-27", "CARD 0412 AUTOZONE", "-312.48"), ("2026-01-05", "CARD 0412 SHELL OIL", "-61.20"),
            ("2026-01-14", "CARD 7781 AMAZON MKTPLACE", "-145.90"), ("2026-01-02", "ELECTRONIC WITHDRAWAL RENT", "-286.00"),
            ("2026-01-21", "MAINTENANCE FEE", "-10.00")], "6993.87")}},
    "td-bank-check-gap-2026-09": {
        "bank": "TD Bank", "business": "Seaside Bakery LLC (fictional)", "page": "https://www.zerabooks.com/td-bank-statement-to-excel",
        "accounts": {"Business checking ...8834": ("10240.55", [
            ("09/03", "DEPOSIT", "1875.00"), ("09/08", "ELECTRONIC DEPOSIT SQUARE", "4312.60"), ("09/22", "ELECTRONIC DEPOSIT SQUARE", "3980.15"),
            ("09/11", "CHECK 2041", "-1200.00"), ("09/18", "CHECK 2043*", "-860.00"), ("09/15", "ELECTRONIC PMT SYSCO", "-642.18"),
            ("09/25", "ELECTRONIC PMT PAYROLL", "-5410.92"), ("09/30", "SERVICE CHARGE", "-25.00")], "12270.20")}},
    "pnc-starts-overdrawn-2026-06": {
        "bank": "PNC", "business": "Mill Creek Hauling LLC (fictional)", "page": "https://www.zerabooks.com/pnc-bank-statement-to-excel",
        "accounts": {"Business Checking ...7740": ("-612.40", [
            ("06/02", "ACH ADDITION CUSTOMER PAYMENT", "2480.00"), ("06/03", "SERVICE CHARGE", "-36.00"),
            ("06/05", "3214 DEBIT CARD PURCHASE PILOT", "-418.22"), ("06/10", "ACH DEDUCTION TRUCK LOAN", "-1150.00"),
            ("06/16", "ACH ADDITION CUSTOMER PAYMENT", "2915.50"), ("06/19", "3214 DEBIT CARD PURCHASE LOVES", "-397.06")], "2781.82")}},
    "amex-three-card-members-2026-10": {
        "bank": "American Express", "business": "Lakeview Events Co. (fictional)", "page": "https://www.zerabooks.com/american-express-statement-to-excel",
        "card": True,
        "accounts": {"Business card (owed)": ("6240.18", [
            ("09/20/26", "PAYMENT RECEIVED - THANK YOU", "-6240.18"), ("09/28/26", "ORTIZ: CREDIT EVENT RENTALS", "-85.00"),
            ("09/18/26", "LEE: DELTA AIR LINES", "642.80"), ("10/02/26", "LEE: MARRIOTT", "118.45"),
            ("09/25/26", "ORTIZ: PARTY RENTAL CO", "1250.00"), ("10/08/26", "ORTIZ: COSTCO", "212.37"),
            ("10/11/26", "PATEL: ADOBE", "486.20")], "2624.82")}},
}


def main():
    fields = list(csv.DictReader(open(os.path.join(ROOT, "data", "fields.csv"), encoding="utf-8")))
    tools = list(csv.DictReader(open(os.path.join(ROOT, "data", "tools.csv"), encoding="utf-8")))
    rows = [{"tool_id": t, "field": f, "value": v, "source_url": u, "checked": c, "note": n} for t, f, v, u, c, n in FACTS]
    with open(os.path.join(ROOT, "data", "facts.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["tool_id", "field", "value", "source_url", "checked", "note"], lineterminator="\r\n")
        w.writeheader()
        w.writerows(rows)
    json.dump({"dataset": "Bank statement converter comparison", "publisher": "ZeraBooks (Zera Books Inc.)",
               "note": "ZeraBooks makes one of the tools listed. Every fact was read on the vendor's own page on its checked date.",
               "tools": tools, "fields": fields, "facts": rows}, open(os.path.join(ROOT, "data", "facts.json"), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
    by = {(r["tool_id"], r["field"]): r for r in rows}
    with open(os.path.join(ROOT, "data", "matrix.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["tool"] + [f["field"] for f in fields])
        for t in tools:
            w.writerow([t["tool"]] + [by.get((t["tool_id"], f["field"]), {}).get("value", "") for f in fields])
    with open(os.path.join(ROOT, "data", "plans.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["tool_id", "plan", "unit", "allowance", "monthly_usd", "annual_billing_monthly_usd", "source_url", "checked"])
        w.writerows([[p[0], p[1], p[2], p[3], p[4] or "", p[5] or "", p[6], p[7]] for p in PLANS])
    md = ["# Bank statement converter comparison", "",
          "Generated from `data/facts.csv`. Every cell links to the vendor page it was read on, with the date. A blank cell means the vendor's page didn't say. ZeraBooks makes one of these tools.", ""]
    for f in fields:
        md += [f"## {f['label']}", "", f"_{f['what_it_records']}_", "", "| Tool | Value | Source |", "|---|---|---|"]
        for t in tools:
            r = by.get((t["tool_id"], f["field"]))
            if r:
                val = r["value"].replace("|", "/") + (f" ({r['note']})" if r["note"] else "")
                md.append(f"| {t['tool']} | {val} | [{r['checked']}]({r['source_url']}) |")
            else:
                md.append(f"| {t['tool']} | | |")
        md.append("")
    open(os.path.join(ROOT, "docs", "comparison.md"), "w", encoding="utf-8").write("\n".join(md))
    import cost
    with open(os.path.join(ROOT, "data", "cost-at-volume.csv"), "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, lineterminator="\r\n")
        w.writerow(["pages_per_month", "statements_per_month", "organizations", "billing", "tool", "plan", "monthly_cost_usd", "cost_per_page_usd", "note"])
        # A firm's month: about 4 pages a statement and 2 statements per client organization.
        for pages in (100, 250, 500, 1000, 2500, 5000):
            stmts = max(1, pages // 4)
            orgs = max(1, stmts // 2)
            for billing in ("monthly", "annual"):
                for r in cost.estimate(pages, stmts, orgs, billing):
                    w.writerow([pages, stmts, orgs, billing, r["tool"], r["plan"], r["monthly"], r["per_page"], r["note"]])
    os.makedirs(os.path.join(ROOT, "samples", "worked-examples"), exist_ok=True)
    for name, ex in EXAMPLES.items():
        with open(os.path.join(ROOT, "samples", "worked-examples", name + ".csv"), "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, lineterminator="\r\n")
            w.writerow(["Account", "Date", "Description", "Amount"])
            for acct, (_, lines, _) in ex["accounts"].items():
                for d, desc, amt in lines:
                    w.writerow([acct, d, desc, amt])
        side = {"bank": ex["bank"], "business": ex["business"], "zerabooks_page": ex["page"], "card_statement": bool(ex.get("card")),
                "accounts": {a: {"opening": o, "closing": c} for a, (o, _, c) in ex["accounts"].items()}, "fictional": True,
                "amount_sign": "Bank: money in positive. Card: charges positive (they raise the balance owed), payments and credits negative."}
        json.dump(side, open(os.path.join(ROOT, "samples", "worked-examples", name + ".balances.json"), "w", encoding="utf-8"), indent=2)
    print(f"{len(rows)} facts, {len(PLANS)} plans, {len(EXAMPLES)} worked examples")


if __name__ == "__main__":
    main()
