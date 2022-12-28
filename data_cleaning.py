import numpy as np 
import pandas as pd 
import re 
from nltk.corpus import stopwords
from re import sub 
from sklearn.cluster import KMeans
from unidecode import unidecode
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser


class clean_tweet: 

    stopwords = set(stopwords.words('english'))
    
    # apply to series in dataframe
    def remove_stop_word(self, text): 
        text = str(text)
        text = text.lower()

        # Clean the text
        text = sub(r"[^A-Za-z0-9^,!?.\/'+]", " ", text)
        text = sub(r"\+", " plus ", text)
        text = sub(r",", " ", text)
        text = sub(r"\.", " ", text)
        text = sub(r"!", " ! ", text)
        text = sub(r"\?", " ? ", text)
        text = sub(r"'", " ", text)
        text = sub(r":", " : ", text)
        text = sub(r"\s{2,}", " ", text)
        text = sub(r"[^\w\s]", "", text) 
        text = text.split()
        word_list = [w for w in text if w not in self.stopwords] 
        return word_list
    
    # @TODO: add more functions later 





# @TODO: Data cleaning
tweets = pd.read_csv('./tweets.csv')

# Read both tsla stock 
tsla_stock = pd.read_csv('./stock_data.csv')

# Ordered by datetime 
tweets = tweets.sort_values(by=['Datetime'])

clean = clean_tweet()

tweets["World_List"] = tweets.Text.apply(clean.remove_stop_word)

phrases = Phrases(tweets.Word_List, min_count=1, progress_per=500000)

bigram = Phraser(phrases)

sentences = bigram[tweets.Word_List]

# Word2Vec Model 






