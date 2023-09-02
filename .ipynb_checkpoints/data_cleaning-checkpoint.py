# Imports 
import numpy as np 
import pandas as pd 
import re 
from nltk.corpus import stopwords
from re import sub 
from sklearn.cluster import KMeans
from unidecode import unidecode
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases, Phraser
import multiprocessing
from time import time 



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

tweets["Word_List"] = tweets.Text.apply(clean.remove_stop_word)

phrases = Phrases(tweets.Word_List, min_count=1, progress_per=500000)

bigram = Phraser(phrases)

sentences = bigram[tweets.Word_List]

# Word2Vec Model 
w2v = Word2Vec(min_count=3, window=4, sample=1e-5, alpha=0.03, min_alpha=0.0007, negative=20, workers=multiprocessing.cpu_count()-1)

w2v.vector_size = 300 

# to print the time taken for model to train 
start = time() 

w2v.build_vocab(sentences, progress_per=50000)

w2v.train(sentences, total_examples=w2v.corpus_count, epochs=30, report_delay=1)

print("Time to train the model {} mins".format(round(time() - start)/60, 2))

# Printing the word list 
temp = tweets.Word_List
temp = temp.apply(lambda x: ' '.join(bigram[x])).reset_index(drop=True)
print(temp[0:10])


# Unsupervised learning using w2v values for words and creating clusers for word in w2v vocabulary 
# @TODO: Find sentiment value for each sentence using the words