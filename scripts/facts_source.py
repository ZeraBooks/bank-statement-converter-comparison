"""Facts for the comparison, as read on each vendor's own pages.

Every competitor fact comes from the source comments of ZeraBooks'
comparison pages (lib/marketing/landing/pages/alternatives-*.ts), where
each was read on the vendor's own page on the date given. ZeraBooks facts
come from zerabooks.com and its help center. A fact a page doesn't state is
left out. Edit here, then run scripts/generate_samples.py.
"""

D = "2026-11-05"
ZB = "https://www.zerabooks.com/pricing"
ZB_CONV = "https://www.zerabooks.com/bank-statement-converter"
ZB_UP = "https://www.zerabooks.com/help/convert-documents/upload-documents"
ZB_PROOF = "https://www.zerabooks.com/help/convert-documents/how-convert-proves-a-statement"
ZB_FMT = "https://www.zerabooks.com/help/convert-export/choose-a-download-format"
DEXT_P = "https://www.dext.com/us/pricing/prepare-direct/"
DEXT_B = "https://www.dext.com/us/business/pricing/extraction-pricing?tab=bse"
DEXT_H = "https://help.dext.com/en/articles/455059-how-to-upload-bank-statements-in-dext"
HUB_P = "https://www.hubdoc.com/pricing"
HUB_H = "https://support.hubdoc.com/hc/en-us/articles/16660344358925-Extract-bank-statement-data-CA-US"
NAN = "https://nanonets.com/bank-statement-converter/"
NAN_P = "https://nanonets.com/pricing"
AE_P = "https://www.autoentry.com/pricing"
AE_H = "https://help.autoentry.com/en/articles/1312890-upload-a-bank-statement-to-autoentry"
DC_P = "https://www.docuclipper.com/pricing/"
DC_H = "https://www.docuclipper.com/"
MT_P = "https://www.moneythumb.com/quickbooks-converters-benefits/"
MT_A = "https://www.moneythumb.com/accounting/"
MT_S = "https://www.moneythumb.com/spreadsheet-converters-desktop/"

FACTS = [
    ("zerabooks", "what_it_is", "A bank statement converter that reads PDF bank, card, check and brokerage statements and proves each account against its printed balances. Included with the ZeraBooks General Ledger in one subscription.", ZB_CONV, D, "ZeraBooks publishes this dataset."),
    ("zerabooks", "pricing", "1,000 pages a month: $149 billed monthly, or $79 a month billed annually ($948 a year). 2,500 pages: $249 monthly or $179 billed annually. 5,000 pages: $599 monthly or $449 billed annually.", ZB, D, ""),
    ("zerabooks", "billing_unit", "Pages per month", ZB, D, ""),
    ("zerabooks", "price_per_page_usd", "0.149 monthly or 0.079 billed annually at 1,000 pages; 0.0716 annually at 2,500; 0.0898 annually at 5,000", ZB, D, "Plan price divided by pages, if every page is used."),
    ("zerabooks", "free_trial", "7 days; a card at checkout, nothing charged for 7 days.", ZB, D, ""),
    ("zerabooks", "file_limits", "PDF only, up to 50 MB and 500 pages per file.", ZB_UP, D, ""),
    ("zerabooks", "input_formats", "PDF (digital or scanned)", ZB_UP, D, ""),
    ("zerabooks", "output_formats", "Excel and CSV, in Standard, Money in and out, QuickBooks-ready, Xero-ready, Sage-ready and All details layouts.", ZB_FMT, D, "CSV and Excel only; no .qbo, IIF or OFX files."),
    ("zerabooks", "fields_extracted", "Date, Description, Amount, Money In, Money Out, Balance, Account, Account Last 4, Cardholder, Type, Check Number, Source File.", ZB_FMT, D, ""),
    ("zerabooks", "balance_proof", "Yes. Each account (and each cardholder on card statements) is checked against the opening, running and closing balances the statement prints; it's marked Proven only when it ties to the cent.", ZB_PROOF, D, ""),
    ("zerabooks", "accounting_integration", "Downloads QuickBooks-, Xero- and Sage-ready CSV layouts to import. No direct connection to accounting software.", ZB_FMT, D, ""),
    ("zerabooks", "counting_rules", "Monthly pages reset each month; annual billing gives the year's 12,000 pages upfront.", ZB, D, ""),

    ("dext", "what_it_is", "Bank Statement Extraction, an add-on to Dext's receipts and bills product.", DEXT_P, D, ""),
    ("dext", "pricing", "Business plan $25.21 a month or $302.50 billed annually (250 documents, 5 users). Bank Statement Extraction add-on from $13.00 a month for 50 documents ($0.26 each, $156.00 billed annually), or $0.32 a document pay as you go.", DEXT_B, D, "USD excl. tax."),
    ("dext", "billing_unit", "Documents (every page of a statement counts)", DEXT_H, D, ""),
    ("dext", "price_per_page_usd", "0.26 in the 50-document bundle; 0.32 pay as you go", DEXT_B, D, "Plus the Dext plan."),
    ("dext", "free_trial", "14 days, no card; free credits include 10 sheets of bank statement extraction.", DEXT_P, D, ""),
    ("dext", "file_limits", "One statement for a single account per file; 50 MB, 300 pages; scans at 200 dpi.", DEXT_H, D, ""),
    ("dext", "input_formats", "PDF or TIFF", DEXT_H, D, ""),
    ("dext", "output_formats", "CSV export; original PDF downloadable.", DEXT_H, D, "Statements can't be published to accounting software."),
    ("dext", "turnaround", "Digital PDFs typically minutes; scans up to 24 hours, about 75% within 4 hours.", DEXT_H, D, ""),
    ("dext", "coverage", "Over 500 supported banks.", DEXT_H, D, ""),
    ("dext", "accounting_integration", "Bank statements can't be published to accounting software; synced bank accounts can't be used.", DEXT_H, D, ""),
    ("dext", "counting_rules", "Every page of a processed statement counts, including pages with no transactions, even if deleted. Bundle documents don't roll over. Over the limit, data isn't extracted until the next bill date or an upgrade.", DEXT_H, D, ""),

    ("hubdoc", "what_it_is", "Document capture that extracts data from bank statements, bills, invoices and receipts and syncs to Xero and QuickBooks Online.", HUB_P, D, ""),
    ("hubdoc", "pricing", "$12 a month (USD). Included in Xero Starter, Standard and Premium plans (Early, Growing and Established in the U.S.).", HUB_P, D, ""),
    ("hubdoc", "billing_unit", "Per organization, flat", HUB_P, D, ""),
    ("hubdoc", "free_trial", "30 days, no card.", HUB_P, D, ""),
    ("hubdoc", "file_limits", "PDF, all pages, up to 100 pages and 35 MB; 200 DPI minimum; one statement only; English; up to 40 inches / 2,880 points.", HUB_H, D, ""),
    ("hubdoc", "input_formats", "PDF", HUB_H, D, ""),
    ("hubdoc", "output_formats", "CSV for QuickBooks or Xero; a Xero CSV is split into a zip above 1,000 transactions.", HUB_H, D, ""),
    ("hubdoc", "fields_extracted", "Debit statements: date, description, amount. Credit statements: posted date, transaction date, description, amount.", HUB_H, D, ""),
    ("hubdoc", "balance_proof", "Errors when totals don't match or there's no opening or closing date.", HUB_H, D, ""),
    ("hubdoc", "coverage", "Canada and U.S. only. A supported-bank list (including Chase, Citibank, PNC, TD Bank, U.S. Bank, Wells Fargo, AMEX); for banks not listed, accuracy might vary and extraction is provided \"as is\".", HUB_H, D, ""),
    ("hubdoc", "accounting_integration", "Syncs to Xero and QuickBooks Online.", HUB_P, D, ""),

    ("nanonets", "what_it_is", "A bank statement converter page on Nanonets' AI workflow platform.", NAN, D, ""),
    ("nanonets", "pricing", "Starter free with $50 in credits, then $100 a month for 100 credits (up to 3 users). Growth quoted, Enterprise custom. Block runs $0.02 simple, $0.10 standard AI, $0.30 complex AI.", NAN_P, D, "No per-page or per-statement price published."),
    ("nanonets", "billing_unit", "Prepaid credits", NAN_P, D, ""),
    ("nanonets", "file_limits", "PDF, PNG, JPG up to 50 MB.", NAN, D, ""),
    ("nanonets", "input_formats", "PDF, PNG, JPG", NAN, D, ""),
    ("nanonets", "output_formats", "XLSX, CSV, JSON", NAN, D, ""),
    ("nanonets", "balance_proof", "Not mentioned. The page's FAQ says to review and validate by comparing rows against the original PDF, and links each transaction back to its place on the statement.", NAN, D, ""),
    ("nanonets", "accuracy_claim", "\"99%+ accuracy\", no method published.", NAN, D, ""),
    ("nanonets", "counting_rules", "Credits are prepaid, shared and never expire.", NAN_P, D, ""),

    ("autoentry", "what_it_is", "Data capture for bills, receipts and bank statements, sold in credits.", AE_P, D, ""),
    ("autoentry", "pricing", "A month, USD excl. VAT: Bronze 50 credits $13, Silver 100 $24, Gold 200 $46, Platinum 500 $103, Diamond 1,500 $298, Sapphire 2,500 $469.", AE_P, D, ""),
    ("autoentry", "billing_unit", "Credits; 3 credits per bank statement page", AE_P, D, ""),
    ("autoentry", "free_trial", "25 free trial credits (8 bank statement pages).", AE_P, D, ""),
    ("autoentry", "input_formats", "Scanned paper statements and ePDFs: bank, credit and debit card statements.", AE_H, D, ""),
    ("autoentry", "output_formats", "Excel or CSV download.", AE_H, D, ""),
    ("autoentry", "fields_extracted", "Account number, date, description, debit, credit, balance, cheque number.", AE_H, D, ""),
    ("autoentry", "counting_rules", "3 credits for every page uploaded, including blank pages, summaries and notes. Unused credits roll over 3 months. Rejected statements refunded; duplicates flagged and blocked, but charged unless rejected.", AE_H, D, ""),

    ("docuclipper", "what_it_is", "A bank statement and financial document converter.", DC_P, "2026-10-11", ""),
    ("docuclipper", "pricing", "Month to month: Starter 60 pages $29, Business 640 pages $159, Business 1,000 pages $219, Enterprise 1,800 pages $399; 1,500 pages $299, 3,000 pages $599, 5,000 pages $899. 30% off billed annually (Starter $20.30, Business 640 $111.30, Business 1,000 $153.30, Enterprise 1,800 $279.30 a month).", DC_P, "2026-10-15", ""),
    ("docuclipper", "billing_unit", "Pages per month", DC_P, "2026-10-15", ""),
    ("docuclipper", "price_per_page_usd", "0.48 (Starter) to 0.22 (Business 1,000) month to month; 0.15 at Business 1,000 billed annually", DC_P, "2026-10-15", "Plan price divided by pages, if every page is used."),
    ("docuclipper", "free_trial", "14 days, no card, up to 120 pages.", DC_P, "2026-10-15", ""),
    ("docuclipper", "output_formats", "Excel, CSV, QBO, IIF, OFX, QFX, QIF", DC_P, "2026-10-11", ""),
    ("docuclipper", "balance_proof", "Says it runs reconciliation checks on the output.", DC_P, "2026-10-11", ""),
    ("docuclipper", "accuracy_claim", "\"99.9% field-level accuracy\", no method published.", DC_H, "2026-10-15", ""),
    ("docuclipper", "input_formats", "Digital PDFs and scanned documents.", DC_H, "2026-10-15", ""),
    ("docuclipper", "counting_rules", "Pages don't roll over.", DC_P, "2026-10-11", ""),

    ("moneythumb", "what_it_is", "PDF and bank file converters for QuickBooks, Quicken, Xero and spreadsheets, online and desktop.", MT_P, "2026-10-11", ""),
    ("moneythumb", "pricing", "MoneyThumb Online: $24.95 a month for 5 conversions, $49.95 for 20, $99.95 for 60. Yearly: $199.95 for 60, $399.95 for 240, $799.95 for 800.", MT_P, "2026-10-15", ""),
    ("moneythumb", "billing_unit", "Conversions: one account on one monthly statement, however many pages", MT_P, "2026-10-15", ""),
    ("moneythumb", "input_formats", "PDF, OFX, CSV, QFX, QIF", MT_P, "2026-10-11", ""),
    ("moneythumb", "output_formats", ".qbo (Web Connect) for QuickBooks; QFX for Quicken; XLS or CSV for spreadsheets.", MT_S, "2026-10-11", ""),
    ("moneythumb", "balance_proof", "Automatic reconciliation compares transaction totals with the statement's summary.", MT_A, "2026-10-11", ""),
    ("moneythumb", "counting_rules", "Unused conversions roll over when the subscription renews.", MT_P, "2026-10-15", ""),
]

# Plans used by cli/cost.py. Each: (tool_id, plan, unit, allowance, monthly_usd, annual_monthly_usd or None, source, checked)
PLANS = [
    ("zerabooks", "ZeraBooks 1,000", "pages", 1000, "149.00", "79.00", ZB, D),
    ("zerabooks", "ZeraBooks 2,500", "pages", 2500, "249.00", "179.00", ZB, D),
    ("zerabooks", "ZeraBooks 5,000", "pages", 5000, "599.00", "449.00", ZB, D),
    ("docuclipper", "Starter", "pages", 60, "29.00", "20.30", DC_P, "2026-10-15"),
    ("docuclipper", "Business 640", "pages", 640, "159.00", "111.30", DC_P, "2026-10-15"),
    ("docuclipper", "Business 1,000", "pages", 1000, "219.00", "153.30", DC_P, "2026-10-15"),
    ("docuclipper", "1,500", "pages", 1500, "299.00", "209.30", DC_P, "2026-10-15"),
    ("docuclipper", "Enterprise 1,800", "pages", 1800, "399.00", "279.30", DC_P, "2026-10-15"),
    ("docuclipper", "3,000", "pages", 3000, "599.00", "419.30", DC_P, "2026-10-15"),
    ("docuclipper", "5,000", "pages", 5000, "899.00", "629.30", DC_P, "2026-10-15"),
    ("autoentry", "Bronze", "credits", 50, "13.00", None, AE_P, D),
    ("autoentry", "Silver", "credits", 100, "24.00", None, AE_P, D),
    ("autoentry", "Gold", "credits", 200, "46.00", None, AE_P, D),
    ("autoentry", "Platinum", "credits", 500, "103.00", None, AE_P, D),
    ("autoentry", "Diamond", "credits", 1500, "298.00", None, AE_P, D),
    ("autoentry", "Sapphire", "credits", 2500, "469.00", None, AE_P, D),
    ("moneythumb", "Online 5", "conversions", 5, "24.95", None, MT_P, "2026-10-15"),
    ("moneythumb", "Online 20", "conversions", 20, "49.95", None, MT_P, "2026-10-15"),
    ("moneythumb", "Online 60", "conversions", 60, "99.95", None, MT_P, "2026-10-15"),
    ("moneythumb", "Yearly 60", "conversions_per_year", 60, None, "16.66", MT_P, "2026-10-15"),
    ("moneythumb", "Yearly 240", "conversions_per_year", 240, None, "33.33", MT_P, "2026-10-15"),
    ("moneythumb", "Yearly 800", "conversions_per_year", 800, None, "66.66", MT_P, "2026-10-15"),
    ("hubdoc", "Hubdoc", "organizations", 1, "12.00", None, HUB_P, D),
    ("dext", "Business plan + pay as you go", "pages_payg", 0, "25.21", None, DEXT_B, D),
]
