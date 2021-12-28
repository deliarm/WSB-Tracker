import matplotlib.pyplot as plt
import numpy as np
import WallStreetBets as wsb


top_mentions = wsb.get_common_stocks()

print(f"{'Ticker' :<12} {'Mentions' :<12} {'Price' :<12} {'Monthly Change(%)' :<12}")
for stock, count in top_mentions:
    current_price = round(wsb.get_stock_price(stock),2)
    month_change = round(wsb.get_month_change(stock),2)
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
