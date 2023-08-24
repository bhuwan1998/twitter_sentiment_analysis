import os 
import pandas as pd 
from os import listdir 
from datetime import date, datetime, timedelta
import snscrape.modules.twitter as sntwitter 
import yfinance as yf


class data_ret(): 

    ## input start and end - datetime objects 
    ## tuples of date range made 
    def date_range(self, start, end):
        delta = end - start 
        days =  [start + timedelta(days=i) for i in range(delta.days+1)]
        return_days = [day.date() for day in days]

        return_list = [] 
        for i in range(len(return_days)): # need to test for both odd or even date ranges 
            if not(return_days[i] == return_days[len(return_days)-1]): 
                return_list.append((return_days[i], return_days[i+1]))

        return return_list # return tuples of date ranges 
    
    ## get tweets 
    ## wrapper to get tweets 
    def get_tweets(self, twitter_user, start, end, max_tweets):
        ## get tweets based on the user
        tweets_list = [] 
        for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'from:{twitter_user} since:{start} until:{end}').get_items()):
            if i > max_tweets: 
                break
            if("@" not in tweet.content):
                tweets_list.append([tweet.date, tweet.id, tweet.content, tweet.user.username])
        
        temp_df = pd.DataFrame(tweets_list, columns=['Datetime', 'Tweet ID', 'Text', 'Username'])
        temp_df.to_csv(f'{twitter_user}_{start}.csv')


class stock_data():

    def get_stock_data(self, stock_name, start, end): 
        data = yf.download(tickers = stock_name, start=start, end=end, interval='1h')
        data.to_csv("stock_data.csv")


## Testing 
## March 25, 2022 - Starting of Elon's Twitter Criticism - Check effect on the stock
new = data_ret()
start_date = datetime(2021, 11, 26)
end_date = datetime(2023, 4, 26) 
date_range = new.date_range(start_date, end_date)

for start, end in date_range: 
    new.get_tweets('elonmusk', start, end, 100)
# new.get_tweets('elonmusk', start_date, end_date, 5000)

# stock = stock_data()

# stock.get_stock_data('TSLA', start_date, end_date)

