import datetime
import warnings
import matplotlib as plt
from matplotlib.pyplot import close, contour
import yfinance as yf
from psaw import PushshiftAPI
from tickers import ticker_set
from full_company_name import full_name_dictionary
import praw
from tqdm import tqdm
warnings.filterwarnings("ignore")

class wsbv2:
    def __init__(self,limit,section): #section="top" or "hot"
        self.stock_dictionary = {}
        self.sorted_stocks = {}
        self.chars = set('0123456789(),./;"-_&* ')
        self.limit = limit
        self.section = section

        self.reddit = praw.Reddit(
            client_id="DMH2AzCy2dMNnyK9Zl9AyA",
            client_secret="4uG5A4m2VPEiBS3s3XZwr06yrJ2EcA",
            user_agent="windows10:com.example.myredditapp:v1.0.0 (by u/kingheavyd)",
            ratelimit_seconds=600,
            timeout = 600,
        )

    def has_numbers(self,inputString):
        return any(char.isdigit() for char in inputString)

    def valid_stock(self,inputString):
        if inputString.upper() in ticker_set:
            return True
        return False

    def get_change(self,current, previous):
        return ((current - previous) / previous) * 100.0

    def filler_word_filter(self,str):
        if len(str) > 5:
            return True
        if self.has_numbers(str):
            return True
        return False

    def get_month_change(self,ticker):
        ticker_yahoo = yf.Ticker(ticker)
        try:
            data = ticker_yahoo.history(period="30d")[['Close']]
            month_change = ((data.iloc[-1]['Close'] - data.iloc[0]['Close']) / data.iloc[0]['Close']) * 100
        except:
            month_change = 0
        return month_change

    def get_stock_price(self,ticker):
        ticker_yahoo = yf.Ticker(ticker)
        try:
            data = ticker_yahoo.history(period="1d")[['Close']]
            close_price = data.iloc[-1]['Close']
        except:
            close_price = 0
        return close_price

    def read_posts(self):
        if(self.section=="top"):
            print("Getting stock mentions from TOP posts...")
            for submission in self.reddit.subreddit("wallstreetbets").top(limit=self.limit,):
                split_title = submission.title.split()
                self.read_one_title(split_title)
        else: # hot
            print("Getting stock mentions from HOT posts...")
            for submission in self.reddit.subreddit("wallstreetbets").hot(limit=self.limit):
                split_title = submission.title.split()
                self.read_one_title(split_title)
                i+=1

        self.sorted_stocks = sorted(self.stock_dictionary.items(),key=lambda x: x[1], reverse=True)

    def read_one_title(self,split_title):
        for word in split_title:
            if(self.valid_stock(word)): # read ticker mentions
                self.stock_dictionary[word.upper()] = 1 + self.stock_dictionary.get(word.upper(),0)
            else:   # check if its full companies name as well
                if(word in full_name_dictionary):
                    ticker = full_name_dictionary[word]
                    self.stock_dictionary[ticker.upper()] = 1 + self.stock_dictionary.get(ticker.upper(),0)
