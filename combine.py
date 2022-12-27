import numpy as np 
import pandas as pd
import os 
from os import listdir 

cwd = os.getcwd()

files = listdir(f'{cwd}/tweets/')

tweets = []

for f in files: 
    tweets.append(pd.read_csv(f"{cwd}/tweets/{f}"))


tweet_concat = pd.concat(tweets, ignore_index=True)

tweet_concat.to_csv("tweets.csv")