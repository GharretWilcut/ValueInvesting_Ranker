import csv
from stock_class import Stock

def file_read(file):
    file = open(file)
    type(file)

    csvreader = csv.reader(file)
    header = []
    header = next(csvreader)
    header
    rows = []
    for row in csvreader:
        stock = Stock(row[0])
        rows.append(stock)
    return rows