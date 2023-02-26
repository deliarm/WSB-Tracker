import matplotlib.pyplot as plt
import numpy as np
from yfinance import ticker
import WallStreetBetsV2 as wsb
import sys

if(len(sys.argv)!=4):
    print("CORRECT USAGE: [top or hot] [# Of Iterations] [Top X stocks]")
    exit(1)

section = sys.argv[1]
num_iterations = int(sys.argv[2])   # number of posts to read
top = int(sys.argv[3])              # number of top stocks to report

wsb_reader = wsb.wsbv2(limit=num_iterations,section=section)
wsb_reader.read_posts()

print(f"{'Ticker' :<12} {'Mentions' :<12} {'Price' :<12} {'Monthly Change(%)' :<12}")
for stock, count in wsb_reader.sorted_stocks:
    current_price = round(wsb_reader.get_stock_price(stock),2)
    month_change = round(wsb_reader.get_month_change(stock),2)
    print("{:<12} {:<12} {:<12} {:<12}".format(stock,count,current_price,month_change))

tickers = [x[0] for x in wsb_reader.sorted_stocks]
mentions = [x[1] for x in wsb_reader.sorted_stocks]
title = "WallStreetBets Activity"


### GUI
plt.rcdefaults()
fig, ax = plt.subplots(figsize=(12,8))
fig.canvas.set_window_title('WSB Visualized Data')
my_cmap = plt.get_cmap("Set3")

stocks = wsb_reader.sorted_stocks
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