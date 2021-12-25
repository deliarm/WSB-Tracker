import datetime
import re
import warnings
import time
import seaborn
import matplotlib as plt
import yfinance as yf
from psaw import PushshiftAPI
import config
import psycopg2
import psycopg2.extras


year = 2021
month = 12
day = 22
iterations = 8000  # 10k seems to be a good benchmark
top = 20


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def valid_stock(inputString):
    chars = set('.,()#%^*!@?<>/\-+&')
    if any((c in chars) for c in inputString):
        return False
    else:
        return True


def get_change(current, previous):
    return ((current - previous) / previous) * 100.0


warnings.filterwarnings("ignore")
stock_dictionary = {}
print("\nFetching data from "+str(year)+"-"+str(month)+"-"+str(day) + "...\n")


api = PushshiftAPI()
date = int(datetime.datetime(year, month, day).timestamp())

# generator
submissions = list(api.search_submissions(after=date,
                                          subreddit='wallstreetbets',
                                          filter=['url', 'author',
                                                  'title', 'subreddit'],
                                          limit=iterations))
for i in submissions:
    print(i)
    words = i.title.split()
    cashtag = list(
        set(filter(lambda word: word.lower().startswith('$'), words)))
    for tag in cashtag:
        # print(tag)   # optional print statment to see raw data
        if (len(tag) >= 2 and len(tag) <= 5):
            if (has_numbers(tag) == False):
                if(valid_stock(tag) == True):
                    if(tag.upper() in stock_dictionary.keys()):
                        stock_dictionary[tag.upper()] += 1
                    else:
                        stock_dictionary[tag.upper()] = 1

# sort and get only top amount declared
sorted_stocks = sorted(stock_dictionary.items(),
                       key=lambda x: x[1], reverse=True)[:top]
print("\n Sorted Data: ")
# print stocks and times mentioned
for stock, count in sorted_stocks:
    print(stock, " \t: ", count)
print("\n")


# display stock data:
print("Stock \t Volume \t Mentions")
for stock, count in sorted_stocks:
    try:
        temp = yf.Ticker(stock[1:])
        day_volume = (temp.info["volume"])
        print(str(stock[1:]) + "\t" + str(day_volume)+" \t   "+str(count))
    except:
        print("Stock info not available for "+str(stock[1:]))
print("\n")
