file = open("HW5/stock_files/AAPL.csv")
lines = file.readlines()
prices = (round(float(line), 2) for line in lines)

print(file)