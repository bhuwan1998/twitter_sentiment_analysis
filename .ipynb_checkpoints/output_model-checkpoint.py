import numpy as np
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from re import sub

from tabulate import tabulate
from tqdm import trange
import random
import multiprocessing
from sklearn.cluster import KMeans


from time import time
from unidecode import unidecode
from gensim.models import Word2Vec
from collections import defaultdict
from gensim.models import KeyedVectors
from gensim.test.utils import get_tmpfile
from gensim.models.phrases import Phrases, Phraser
from cleantext import clean


stop_word = set(stopwords.words("english"))


def read_csv(file_path):
    return pd.read_csv(file_path)


def remove_emoji_from_tweet(text):
    x = clean(x, no_emoji=True)
    return x


def clean_text(text):
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
    text = text.split()
    word_list = [w for w in text if w not in stop_words]
    return word_list


# Manual Cleaning of DF
tweets = read_csv("elonmust_2021-11-26.csv")
tweets = tweets.drop(columns="Unnamed: 0")
tweets = tweets.Text.apply(remove_emoji_from_tweet)

tweets['World_List'] = tweets.Text.apply(clean_text)

phrases = Phrases(tweets.Word_List, min_count=1, progress_per=50000)

bigram = Phraser(phrases)

sentences = bigram[tweets.Word_List]
# Generate Model
w2v_model = Word2Vec(min_count=3,
                     window=4,
                     sample=1e-5,
                     alpha=0.03,
                     min_alpha=0.0007,
                     negative=20,
                     workers=multiprocessing.cpu_count()-1)

w2v_model.vector_size = 300

# Check time required to train
start = time()

w2v_model.build_vocab(sentences, progress_per=50000)

w2v_model.train(sentences, total_examples=w2v_model.corpus_count,
                epochs=30, report_delay=1)

# Print time to train model in terminal
print("Time to train the model: {} mins".format(
    round((time() - start) / 60, 2)))

w2v_model.init_sims(replace=True)

temp = tweets.Word_List
# using pandas series properties and applying a bigram on word list
temp.apply(lambda x: ' '.join(bigram[x]))

# print statements
print(temp)
print(" ")
# ---------

# using the model directly within the script itself
word_vectors = w2v_model.wv
model = KMeans(n_clusters=2, max_iter=1000, random_state=True,
               n_init=50).fit(X=word_vectors.vectors)
positive_cluster_center = model.cluster_centers_[0]
negative_cluster_center = model.cluster_centers_[1]

# Print 2 cluster centers
print(model.cluster_centers_)
print("")

# check words which are similar
print(word_vectors.similar_by_vector(
    model.cluster_centers_[0], topn=10, restrict_vocab=None))
print("")

# index_to_key - new function
words = pd.DataFrame(list(word_vectors.index_to_key))
words.columns = ["words"]
words["words"] = words.words.apply(lambda x: word_vectors[f'{x}'])
# reshaping from (100,0) to (1,100) - as we have 100 features - one row of 100 columns in each row of the DF
#   1 [1,100]
#   2 [1,100]
words["cluster"] = words.vectors.apply(
    lambda x: model.predict(np.array(x).reshape(1, -1)))

words.cluster = words.cluster.apply(lambda x: x[0])
# if you print this - you will get which cluster center is the word assigned to

words['cluster_value'] = [1 if i == 0 else -1 for i in words.cluster]
# TODO normalise these
words['closeness_score'] = words.apply(
    lambda x: 1/(model.transform([x.vectors]).min()), axis=1)
words['sentiment_coeff'] = words.closeness_score * words.cluster_value

# TODO After normalising decide which values are considered to be neutral, positive or negative
