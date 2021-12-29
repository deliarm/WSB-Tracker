import matplotlib.pyplot as plt
import numpy as np
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
prev_date = "{}-{}-{}".format(year, month-1, day)
if(month==1):
    prev_date = "{}-{}-{}".format(year-1, 12, day)

iterations = int(sys.argv[2])  # 10k seems to be a good benchmark
top = int(sys.argv[3])

top_mentions = wsb.get_common_stocks(year,month,day,iterations,top)

print(f"{'Ticker' :<12} {'Mentions' :<12} {'Price' :<12} {'Monthly Change(%)' :<12}")
for stock, count in top_mentions:
    current_price = round(wsb.get_stock_price(stock,prev_date,current_date),2)
    month_change = round(wsb.get_month_change(stock,prev_date,current_date),2)
    print("{:<12} {:<12} {:<12} {:<12}".format(stock,count,current_price,month_change))

# plt.rcdefaults()
# fig, ax = plt.subplots()

# # Example data
# people = ('Tom', 'Dick', 'Harry', 'Slim', 'Jim')
# y_pos = np.arange(len(people))
# performance = 3 + 10 * np.random.rand(len(people))
# error = np.random.rand(len(people))

# ax.barh(y_pos, performance, xerr=error, align='center')
# ax.set_ylabel("Ticker")
# ax.invert_yaxis()  # labels read top-to-bottom
# ax.set_xlabel('Performance')
# ax.set_title('How fast do you want to go today?')

# plt.show()
