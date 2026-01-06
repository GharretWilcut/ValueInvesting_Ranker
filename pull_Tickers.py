import pdfplumber
import re 
import csv
pdf_path = '8-HSF-S-P-Eligible-Stocks-93-12-31-25-su3.pdf'
output_csv = 'tickers.csv'

ticker_pattern = re.compile(r"\([^)]+?:([A-Z\.]+)\)")

tickers = set()
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        text = page.extract_text()
        if not text:
            continue

        matches = ticker_pattern.findall(text)
        for ticker in matches:
            tickers.add(ticker)

with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    for ticker in sorted(tickers):
        writer.writerow([ticker])
print(f"Extracted {len(tickers)} unique tickers to {output_csv}")