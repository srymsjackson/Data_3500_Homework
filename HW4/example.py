# This is so I can understand how to loop through this bc I'm super duper confused

prices = [10, 12, 11, 13, 15, 14, 16, 17, 18, 20]  # example list

for i in range(len(prices) - 4):
    five_day_avg = sum(prices[i:i+5]) / 5
    print(f"Day {i+5} average: {five_day_avg:.2f}")

for i in range(len(prices) - 4):
    five_day_avg = sum(prices[i:i+5]) / 5
    current_price = prices[i + 4]


# CHATGPT CAME UP W/ THIS EXAMPLE FYI