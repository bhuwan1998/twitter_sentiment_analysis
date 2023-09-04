<<<<<<< HEAD
# Twitter Sentiment Analyis

## Finding a correlation between Tesla Stock and Elon Musk's Tweets (Started Januray 2023 - Ended August 2023)

### Data Retrieval

- Tweets were retrieved with open source third party scraper which no longer works as twitter/X has blocked all third party scrapers.
=======
# Twitter Sentiment Analyis 
## Finding a correlation between Tesla Stock and Elon Musk's Tweets 
### Data Retrieval 
- Tweets were retrieved with open source third party scraper which no longer works as twitter/X has blocked all third party scrapers. 
>>>>>>> 3da12c37b0e447221938e02eddeb52e7cce24c97
- Tesla Stock Data was retrieved using yahoo finance python library.
- All the data was simply combined into a single dataframe before pre-processing tweets and normalising data for stock.

### Data Processing Brief

- Before proceeding with prediction we need to test if the two are related in anyway possible. The tweets were clean using standardised techniques with reference to hugging face Roberta Model especially trained for tweets.
- After cleaning data compound scores were calculated by using the weights as seen in the sentiment_analysis.ipynb (Python Notebook). Using the compound scores and the changes between consecutive values we are able to make out changes in sentiment with ajusted close price.
- Both the dataframes were averaged per day to be able to find a correlation between the two when merged.
- It is evident that there were two major shortcomings in this project. Lack of data and restrictions of obtaining tweets recently was a major road-block in order to get the latest tweets and gather more information. As stock data is still easily available to be used easily.

### Sentiment Value Processing

- Roberta Based model trained on tweets was used from [Hugging Face](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest). The model was used to find the neutral, positive and negative values for each tweet after cleaning.
- After getting these values weights were applied to each negative:-2, positive:+2 and neutral: 1 to find the compound value. Which was then normalised between 0 and 1.
- Similarly the stock data once averaged per day was normalised.

### Sentiment vs Stock Timeseries and Findings

- When both datasets were averaged for each day and merged it was found on the timeseries that there were few similarities visually but when statistically the changes in sentiment and returns were observed, the correlation showed a mere 0.27 value which is way lower than 0.5 which would give us some kind of indication that the tweet sentiment affects the stock value.
- Therefore, in conclusion tweet sentiment of Elon Musks tweets from November 2021 till November 2022 had no affect on the Tesla stock returns.

### Resources

1. [Hugging Face Twitter Roberta Link](https://huggingface.co/cardiffnlp/twitter-roberta-base-sentiment-latest)
2. [Plotly Graphing Libraries](https://plotly.com/graphing-libraries/)
3. [Sentiment Analysis Guide](https://algotrading101.com/learn/sentiment-analysis-python-guide/)
4. [Snacrape - Social Media Scrapping Github Project](https://github.com/JustAnotherArchivist/snscrape)
5. [Yahoo Finance Tesla Stock Page](https://au.finance.yahoo.com/quote/TSLA?p=TSLA)
