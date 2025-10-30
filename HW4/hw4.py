'''
--------------------------------------------------------------------------------------------------------------------------------
1.  Load the daily stock prices for Tesla (stock ticker TSLA) data from Nasdaq, from todays date through last year at this time.  
2.  Run a mean reversion trading strategy on the data.
3.Output the results of the strategy including the profits (see sample output below).
--------------------------------------------------------------------------------------------------------------------------------
'''
files = open("HW4/TSLA.txt")
lines = files.readlines()

# Very important in order to iterate through all these values in the .txt file
prices = []

for line in lines:
    line = float(line)
    prices.append(line)

# These are all declared in order to use for the summary, if/elif loops, etc... 
#
#
# tracking the holding for buying
holding = False
# For tracking the buy/sell price
buy_price = None
sell_price = None
# to present total profit & first buy at the end of the trading period (the summary)
total_profit = 0.0
first_buy = None

for i in range(len(prices) - 4):
    # Declaring the 5 day avg
    five_day_avg = sum(prices[i:i+5]) / 5

    # Declaring the current price to use in the loop fr
    current_price = prices[i + 4]

    # Decided to make this last min for better readability
    buy_threshold = five_day_avg * 0.98 
    sell_threshold = five_day_avg * 1.02

    if (not holding) and current_price < buy_threshold: # refer above for the buy_threshold variable
        buy_price = current_price # (I used ChatGPT to understand why "if holding != false" wasn't working (replaced w/ "not holding"))
        if first_buy is None:
            first_buy = buy_price
        holding = True
        print("buying at:", buy_price)

    elif holding == True and current_price > sell_threshold: # refer above for the sell_threshold variable
        trade_profit = current_price - buy_price
        total_profit += trade_profit
        holding = False
        buy_price = None
        print("selling at:", current_price)
        print("trade profit:", round(trade_profit, 2))

    else: # if the curr.price is between .98 and 1.02, go onto the next value
        continue

# spacer btw
print("-------------------")

# summary:
print("Total Profit:", round(total_profit, 2))
print("First buy:", round(first_buy, 2))

# used to find the percentage return::
print("% Return:", str(round(((total_profit / first_buy) * 100), 2)) + str("%"))