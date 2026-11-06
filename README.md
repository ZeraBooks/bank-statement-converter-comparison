# Bank statement converter comparison

Which bank statement converter checks its work, and what does a month of statements cost on each? This dataset compares seven: [ZeraBooks Convert](https://www.zerabooks.com/bank-statement-converter), Dext, Hubdoc, Nanonets, AutoEntry, DocuClipper and MoneyThumb, on file limits, formats, pricing and its unit, price per page, and whether each one says it checks the rows against the statement's printed balances. Every cell was read on the vendor's own page, with the URL and the date. ZeraBooks publishes it and makes one of the tools; its rows follow the same rule.

- One row per fact: [`data/facts.csv`](data/facts.csv), [`data/facts.json`](data/facts.json)
- One row per tool: [`data/matrix.csv`](data/matrix.csv)
- Tables with a source link in every cell: [`docs/comparison.md`](docs/comparison.md)
- Published plans: [`data/plans.csv`](data/plans.csv), and what they cost at volume: [`data/cost-at-volume.csv`](data/cost-at-volume.csv)
- Cost calculator: [`cli/cost.py`](cli/cost.py)
- Bank layouts that trip converters: [`data/bank-statement-layouts.csv`](data/bank-statement-layouts.csv), with worked examples in [`samples/worked-examples/`](samples/worked-examples/)
- Release zip: [latest](https://github.com/ZeraBooks/bank-statement-converter-comparison/releases/latest)

## At a glance

| Tool | Sold by | Per page | File limits | Says it checks printed balances |
|---|---|---|---|---|
| [ZeraBooks Convert](https://www.zerabooks.com/bank-statement-converter) | Pages a month: 1,000 for $149, or $79 billed annually | $0.08 to $0.15 at 1,000 pages | PDF, 50 MB, 500 pages | Yes: opening, running and closing balances, per account and cardholder, to the cent |
| Dext ([vs ZeraBooks](https://www.zerabooks.com/alternatives/dext)) | Documents; every statement page counts; add-on to a Dext plan | $0.26 (bundle) to $0.32 (pay as you go) | PDF or TIFF, 50 MB, 300 pages, one account per file | Not stated |
| Hubdoc ([vs ZeraBooks](https://www.zerabooks.com/alternatives/hubdoc)) | $12 a month per organization, or included in Xero | | PDF, 35 MB, 100 pages, one statement, Canada and U.S. | Errors when totals don't match or there's no opening or closing date |
| Nanonets ([vs ZeraBooks](https://www.zerabooks.com/alternatives/nanonets)) | Prepaid credits | Not published | PDF, PNG, JPG, 50 MB | Not mentioned; says to compare rows against the PDF |
| AutoEntry ([vs ZeraBooks](https://www.zerabooks.com/alternatives/autoentry)) | Credits; 3 per statement page, blank pages included | | Scans and ePDFs | Not stated |
| DocuClipper ([vs ZeraBooks](https://www.zerabooks.com/alternatives/docuclipper)) | Pages a month | $0.15 to $0.48 | Digital and scanned PDFs | Says it runs reconciliation checks |
| MoneyThumb ([vs ZeraBooks](https://www.zerabooks.com/alternatives/moneythumb)) | Conversions: one account on one monthly statement | | PDF, OFX, CSV, QFX, QIF in | Compares transaction totals with the statement's summary |

Dext, Hubdoc, Nanonets and AutoEntry were checked November 5, 2026; DocuClipper and MoneyThumb October 11 and 15, 2026 (each row says which). Per-page figures assume every page in the plan is used.

## What a month costs

Tools sell in different units (pages, credits, documents, statements, organizations), so compare on your own month:

```
$ python3 cli/cost.py --pages 1000 --billing annual
1000 pages, 250 statements, 1 organization a month, annual billing (USD)

Tool            A month  Per page  Plan / note
ZeraBooks        $79.00     $0.08  ZeraBooks 1,000; includes the ZeraBooks General Ledger
DocuClipper     $153.30     $0.15  Business 1,000
AutoEntry           n/a            3000 credits is past the largest published plan (2,500)
MoneyThumb          n/a            past the largest published yearly plan (800)
Hubdoc           $12.00     $0.01  1 organization x $12; per organization; included in Xero Starter, Standard and Premium; statements up to 100 pages, Canada and U.S.
Dext            $345.21     $0.35  Business plan + $0.32 a page; pay-as-you-go rate; a 50-document bundle is $13 a month; larger bundles aren't on the price page
Nanonets            n/a            no per-page or per-statement price published
```

Pass `--statements` (account statements a month, MoneyThumb's unit) and `--organizations` (client companies, Hubdoc's unit) for your real numbers. Where a volume is past a tool's published plans, or the price isn't published, the calculator says so instead of guessing. [`data/cost-at-volume.csv`](data/cost-at-volume.csv) runs it at 100 to 5,000 pages for a typical firm month (4 pages a statement, 2 statements per client).

## Why balance proof is the column that matters

A converter that reads every row and drops one has still produced a clean-looking spreadsheet. The only test that catches it is arithmetic: opening balance plus the rows must equal the closing balance the bank printed. Some tools say they do this, some say to compare rows against the PDF yourself, and some don't say. That's the `balance_proof` field, in each vendor's own words.

[ZeraBooks Convert](https://www.zerabooks.com/bank-statement-converter) checks every account against the opening, running and closing balances on the statement, and only marks it Proven when it ties to the cent. It reads digital and [scanned PDFs](https://www.zerabooks.com/bank-statement-ocr) up to 500 pages, and downloads Excel or CSV, including QuickBooks-, Xero- and Sage-ready layouts. It doesn't write .qbo, IIF or OFX files and doesn't connect to accounting software; DocuClipper and MoneyThumb do write those formats, which matters if that's your import route.

## Bank layouts that trip converters

[`data/bank-statement-layouts.csv`](data/bank-statement-layouts.csv) lists, for five banks, the layout details that break conversions and how ZeraBooks reads them. Each links to its page:

- [Citi statement to Excel](https://www.zerabooks.com/citi-bank-statement-to-excel): combined relationship statements, opening and closing balances printed as lines
- [U.S. Bank statement to Excel](https://www.zerabooks.com/us-bank-statement-to-excel): periods that aren't calendar months, dates with no year, trailing minus
- [TD Bank statement to Excel](https://www.zerabooks.com/td-bank-statement-to-excel): Checks Paid in number order with an asterisk at a gap
- [PNC statement to Excel](https://www.zerabooks.com/pnc-bank-statement-to-excel): overdrawn balances with a trailing minus, fee summary tables
- [American Express statement to Excel](https://www.zerabooks.com/american-express-statement-to-excel): mid-month billing periods, card member sections, foreign spend lines

[`samples/worked-examples/`](samples/worked-examples/) has the fictional statement from each page as CSV with its printed balances, and the tests prove each one ties. More on what OCR gets wrong on statements: [bank statement OCR](https://www.zerabooks.com/bank-statement-ocr).

## Rules the data follows

1. **The vendor's own pages only.** `cli/check_dataset.py` fails any source off the vendor's domain, in the facts and in the plans.
2. **Blank beats a guess.** 36 of 105 cells are blank because the vendor's page doesn't say.
3. **Dated.** Every fact carries the day it was read; anything older than 90 days is flagged for a re-check.
4. **Units kept.** Prices stay in the unit the vendor sells. Per-page figures appear only where the unit is a page.

```bash
python3 cli/check_dataset.py
python3 cli/check_dataset.py --as-of 2027-02-01
```

## Corrections

Prices change. Open an issue or pull request with the vendor page URL. Edit `scripts/facts_source.py`, then `python3 scripts/generate_samples.py` rebuilds every file. Vendors are welcome to correct their own rows.

## Tests

```bash
python3 scripts/generate_samples.py
python3 -m unittest discover -s tests -v
```

## License and citation

Code MIT ([`LICENSE`](LICENSE)). Data, samples and docs CC BY 4.0 ([`LICENSE-SAMPLES`](LICENSE-SAMPLES)). Cite with [`CITATION.cff`](CITATION.cff). `MANIFEST.json` and `checksums.txt` list every file with its SHA-256.

Product names are trademarks of their owners. Short quotations from vendor pages are used for comparison.
