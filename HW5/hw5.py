import json

def meanReversionStrategy(prices):
    print("\nMean Reversion Strategy:")
    print("-" * 40)
    
    position = None  # Track if we're holding stock
    first_buy = None
    total_profit = 0.0
    
    # Calculate moving average for each price point
    for i in range(5, len(prices)):  # Start at 5 to have enough data for average
        # Calculate average of last 5 prices (5-day moving average)
        avg = sum(prices[i-5:i]) / 5
        current_price = prices[i]
        
        # Mean reversion logic
        if current_price < avg * 0.98 and position is None:
            # Buy signal
            print("buying at:       " + str(current_price))
            position = current_price
            if first_buy is None:
                first_buy = current_price
                
        elif current_price > avg * 1.02 and position is not None:
            # Sell signal
            print("selling at:      " + str(current_price))
            trade_profit = current_price - position
            print("trade profit:    " + str(round(trade_profit, 2)))
            total_profit += trade_profit
            position = None
    
    # If still holding at end, note it
    if position is not None:
        print("Still holding from: " + str(position))
    
    # Calculate returns
    print("-" * 23)
    print("Total profit:    " + str(round(total_profit, 2)))
    print("First buy:       " + str(first_buy))
    
    if first_buy and first_buy > 0:
        percent_return = (total_profit / first_buy) * 100
        print("Percent return:  " + str(round(percent_return, 2)) + "%")
    else:
        percent_return = 0.0
    
    return round(total_profit, 2), round(percent_return, 2)


def simpleMovingAverageStrategy(prices):
    """
    Implements a simple moving average trading strategy.
    Buys when price goes above moving average, sells when it goes below.
    Returns profit and percentage returns.
    """
    print("\nSimple Moving Average Strategy:")
    print("-" * 40)
    
    position = None  # Track if we're holding stock
    first_buy = None
    total_profit = 0.0
    
    # Calculate moving average for each price point
    for i in range(5, len(prices)):  # Start at 5 to have enough data for average
        # Calculate average of last 5 prices (5-day moving average)
        avg = sum(prices[i-5:i]) / 5
        current_price = prices[i]
        
        # Simple moving average logic
        if current_price > avg and position is None:
            # Buy signal
            print("buying at:       " + str(current_price))
            position = current_price
            if first_buy is None:
                first_buy = current_price
                
        elif current_price < avg and position is not None:
            # Sell signal
            print("selling at:      " + str(current_price))
            trade_profit = current_price - position
            print("trade profit:    " + str(round(trade_profit, 2)))
            total_profit += trade_profit
            position = None
    
    # If still holding at end, note it
    if position is not None:
        print("Still holding from: " + str(position))
    
    # Calculate returns
    print("-" * 23)
    print("Total profit:    " + str(round(total_profit, 2)))
    print("First buy:       " + str(first_buy))
    
    if first_buy and first_buy > 0:
        percent_return = (total_profit / first_buy) * 100
        print("Percent return:  " + str(round(percent_return, 2)) + "%")
    else:
        percent_return = 0.0
    
    return round(total_profit, 2), round(percent_return, 2)


def saveResults(results):
 
    with open("HW5/results.json", "w") as file:
        json.dump(results, file, indent=4)
    print("\nResults saved to results.json")


# Finally the main thing

if __name__ == "__main__":
    # Stock Tickers
    tickers = ["AAPL", "ADBE", "AMC", "AXP", "DASH", "GOOG", "MCD", "RDDT", "WMT", "XOM"]
    # Dictionary
    results = {}
    
    # looping through each ticker here
    for ticker in tickers:
        print("\n" + "="*50)
        print("Processing " + ticker)
        print("="*50)
        
        # let's looooad the prices from file
        file_path = "HW5/stock_files/" + ticker + ".txt"
        with open(file_path, "r") as file:
            lines = file.readlines()
            prices = [round(float(line.strip()), 2) for line in lines]
        
        # Store them prices in results.json
        results[ticker + "_prices"] = prices
        
        # Run SMA function
        sma_profit, sma_returns = simpleMovingAverageStrategy(prices)
        results[ticker + "_sma_profit"] = sma_profit
        results[ticker + "_sma_returns"] = sma_returns
        
        # Run the MRS function
        mr_profit, mr_returns = meanReversionStrategy(prices)
        results[ticker + "_mr_profit"] = mr_profit
        results[ticker + "_mr_returns"] = mr_returns

    # Save all the results to that json file
    saveResults(results)
    
    # summary
    print("\n" + "="*50)
    print("SUMMARY")
    print("="*50)
    for ticker in tickers:
        if ticker + "_sma_profit" in results:
            print("\n" + ticker + ":")
            print("  SMA Profit: $" + str(results[ticker + "_sma_profit"]))
            print("  SMA Returns: " + str(results[ticker + "_sma_returns"]) + "%")
            print("  MR Profit: $" + str(results[ticker + "_mr_profit"]))
            print("  MR Returns: " + str(results[ticker + "_mr_returns"]) + "%")