import contextlib
import csv
import datetime as dt
import glob
import io
import json
import os
import sys
import unittest
from decimal import Decimal

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "cli"))
import check_dataset as cd  # noqa: E402
import cost  # noqa: E402


def by_tool(rows):
    return {r["tool"]: r for r in rows}


class Dataset(unittest.TestCase):
    def test_clean_on_release_date(self):
        issues, s = cd.check(dt.date(2026, 11, 5))
        self.assertEqual([i for i in issues if i[1] == "error"], [])
        self.assertEqual(s["tools"], 7)

    def test_zerabooks_rows_stay_true(self):
        z = {f["field"]: f["value"] for f in csv.DictReader(open(os.path.join(ROOT, "data", "facts.csv"))) if f["tool_id"] == "zerabooks"}
        self.assertIn("500 pages", z["file_limits"])
        self.assertIn("card at checkout", z["free_trial"])
        self.assertIn("No direct connection", z["accounting_integration"])
        text = " ".join(z.values()).lower()
        for banned in ("unlimited", "soc 2", "sync", "free plan", "bank feed"):
            self.assertNotIn(banned, text)

    def test_every_tool_has_pricing_and_balance_proof_or_blank(self):
        facts = list(csv.DictReader(open(os.path.join(ROOT, "data", "facts.csv"))))
        for t in {f["tool_id"] for f in facts}:
            self.assertIn("pricing", {f["field"] for f in facts if f["tool_id"] == t}, t)


class Cost(unittest.TestCase):
    def test_published_worked_numbers(self):
        r = by_tool(cost.estimate(1000, billing="annual"))
        self.assertEqual(r["ZeraBooks"]["monthly"], "79.00")
        self.assertEqual(r["DocuClipper"]["monthly"], "153.30")
        r = by_tool(cost.estimate(1000, billing="monthly"))
        self.assertEqual(r["ZeraBooks"]["monthly"], "149.00")
        self.assertEqual(r["DocuClipper"]["monthly"], "219.00")

    def test_autoentry_plan_by_volume(self):
        # Same as the ZeraBooks AutoEntry page: 150 -> Platinum, 500 -> Diamond, 800 -> Sapphire
        for pages, plan, price in ((150, "Platinum", "103.00"), (500, "Diamond", "298.00"), (800, "Sapphire", "469.00")):
            r = by_tool(cost.estimate(pages))["AutoEntry"]
            self.assertTrue(r["plan"].startswith(plan), r)
            self.assertEqual(r["monthly"], price)
        self.assertEqual(by_tool(cost.estimate(900))["AutoEntry"]["monthly"], "")

    def test_moneythumb_counts_statements_not_pages(self):
        r = by_tool(cost.estimate(400, statements=50))["MoneyThumb"]
        self.assertEqual(r["monthly"], "99.95")
        self.assertEqual(by_tool(cost.estimate(400, statements=61))["MoneyThumb"]["monthly"], "")

    def test_nanonets_never_guessed(self):
        self.assertEqual(by_tool(cost.estimate(300))["Nanonets"]["monthly"], "")

    def test_cli(self):
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(cost.main(["--pages", "600"]), 0)
            self.assertEqual(cost.main(["--pages", "600", "--csv", "--billing", "annual"]), 0)


class WorkedExamples(unittest.TestCase):
    def test_every_example_ties(self):
        files = sorted(glob.glob(os.path.join(ROOT, "samples", "worked-examples", "*.csv")))
        self.assertEqual(len(files), 5)
        for f in files:
            side = json.load(open(f.replace(".csv", ".balances.json")))
            rows = list(csv.DictReader(open(f)))
            for acct, b in side["accounts"].items():
                total = sum(Decimal(r["Amount"]) for r in rows if r["Account"] == acct)
                self.assertEqual(Decimal(b["opening"]) + total, Decimal(b["closing"]), (f, acct))


if __name__ == "__main__":
    unittest.main()
