import matplotlib.pyplot as plt
import numpy as np
from yfinance import ticker
import WallStreetBets as wsb
import sys


if(len(sys.argv) != 4):
    print("Correct Usage: [MM/DD/YYYY] [# Of Iterations] [Top X stocks]")
input = sys.argv[1].split('/')
if(len(input) != 3):
    print("Correct Usage: [MM/DD/YYYY] [# Of Iterations] [Top X stocks]")

month = int(input[0])
day = int(input[1])
year = int(input[2])
current_date = "{}-{}-{}".format(year, month, day)

if(month==1):
    prev_date = "{}-{}-{}".format(year-1, 12, day)
    print
else:
    prev_date = "{}-{}-{}".format(year, month-1, day)

iterations = int(sys.argv[2])  # 10k seems to be a good benchmark
top = int(sys.argv[3])

top_mentions = wsb.get_common_stocks(year,month,day,iterations,top)

print(f"{'Ticker' :<12} {'Mentions' :<12} {'Price' :<12} {'Monthly Change(%)' :<12}")
for stock, count in top_mentions:
    current_price = round(wsb.get_stock_price(stock,prev_date,current_date),2)
    month_change = round(wsb.get_month_change(stock,prev_date,current_date),2)
    print("{:<12} {:<12} {:<12} {:<12}".format(stock,count,current_price,month_change))


tickers = [x[0] for x in top_mentions]
mentions = [x[1] for x in top_mentions]
title = "WallStreetBets Activity For {}".format(current_date)


### GUI
plt.rcdefaults()
fig, ax = plt.subplots(figsize=(12,8))
fig.canvas.set_window_title('WSB Visualized Data')
my_cmap = plt.get_cmap("Set3")

stocks = top_mentions
y_pos = np.arange(len(stocks))
performance = 3 + 10 * np.random.rand(len(stocks))
error = np.random.rand(len(stocks))

ax.barh(tickers, mentions, align='center',color=my_cmap.colors)
ax.set_ylabel("Ticker")
ax.invert_yaxis()
ax.set_xlabel('Times Mentioned')
ax.set_title(title)

rects = ax.patches
labels = [f"{i}" for i in mentions]
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_width() + 1,rect.get_y() + rect.get_height()/2, label, ha="left", va="center")


plt.show()
