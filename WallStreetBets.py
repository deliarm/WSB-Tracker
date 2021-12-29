import datetime
import warnings
import matplotlib as plt
from matplotlib.pyplot import close
import yfinance as yf
from psaw import PushshiftAPI
from tickers import ticker_set
from full_company_name import full_name_dictionary
warnings.filterwarnings("ignore")

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
def get_common_stocks(year,month,day,iterations,top):
    print("\nFetching data from "+str(year) +
          "-"+str(month)+"-"+str(day) + "...\n")

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
    return sorted_stocks


def get_month_change(ticker,prev_date,current_date):
    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history(start=prev_date, end=current_date)[['Close']]
    month_change = ((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100
    return month_change


def get_stock_price(ticker,prev_date,current_date):
    ticker_yahoo = yf.Ticker(ticker)
    data = ticker_yahoo.history(start=prev_date, end=current_date)[['Close']]
    close_price = data.iloc[-1]['Close']
    return close_price
