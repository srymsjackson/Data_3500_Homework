'''
In this assignment you will write a python program which:

1.  Load the daily stock prices for Tesla (stock ticker TSLA) data from Nasdaq, from todays date through last year at this time.  
2.  Run a mean reversion trading strategy on the data.
3.Output the results of the strategy including the profits (see sample output below).
 

You may be unfamiliar with the stock market, or stock market trading.  That is ok!
You actually have already learned all the python programming you need to accomplish this task.  
And the mean reversion trading strategy itself is fairly simple.  

'''
files = open("HW4/TSLA.txt")
print(files)
lines = files.readlines()

prices = []
for line in lines:
    line = float(line)
    prices.append(line)

for i in range(len(prices) - 4):
    five_day_avg = sum(prices[i:i+5]) / 5

if current_price < five_day_avg * .98:
    for i in prices
