import datetime
import warnings
import matplotlib as plt
import yfinance as yf
from psaw import PushshiftAPI
from tickers import ticker_set
from full_company_name import full_name_dictionary
warnings.filterwarnings("ignore")


year = 2021
month = 8
day = 8
iterations = 10000  # 10k seems to be a good benchmark
top = 50
stock_dictionary = {}


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


def valid_stock(inputString):
    if inputString.upper() in ticker_set:
        return True
    return False


def get_change(current, previous):
    return ((current - previous) / previous) * 100.0


def filler_word_filter(str):
    if len(str) > 5:
        return True
    if has_numbers(str):
        return True
    return False


### BEGIN PROGRAM ###
print("\nFetching data from "+str(year)+"-"+str(month)+"-"+str(day) + "...\n")

api = PushshiftAPI()
date = int(datetime.datetime(year, month, day).timestamp())

# API call for posts
submissions = list(api.search_submissions(after=date,
                                          subreddit='wallstreetbets',
                                          filter=['title'],
                                          limit=iterations))

# iterate through posts and get stock mentions
for i in submissions:
    # print(i)
    words = i.title.split()
    for word in words:
        if(valid_stock(word)):
            if (word.upper() in stock_dictionary):
                stock_dictionary[word.upper()] += 1
            else:
                stock_dictionary[word.upper()] = 1
        else:
            if(word in full_name_dictionary):
                temp = full_name_dictionary[word]
                if(temp.upper() in stock_dictionary):
                    stock_dictionary[temp.upper()] += 1
                else:
                    stock_dictionary[temp.upper()] = 1

# sort and get only top amount declared
sorted_stocks = sorted(stock_dictionary.items(),
                       key=lambda x: x[1], reverse=True)[:top]

print("\n Sorted Data: ")
for stock, count in sorted_stocks:
    print(stock, " \t: ", count)
print("\n")


# display stock data:
# print("Stock \t Volume \t Mentions")
# for stock, count in sorted_stocks:
#     try:
#         temp = yf.Ticker(stock[1:])
#         day_volume = (temp.info["volume"])
#         print(str(stock[1:]) + "\t" + str(day_volume)+" \t   "+str(count))
#     except:
#         print("Stock info not available for "+str(stock[1:]))
# print("\n")
