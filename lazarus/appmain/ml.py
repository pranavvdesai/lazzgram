import numpy as np
import pandas as pd
import pickle
import appmain

def pr(tweet):
   print(tweet)

# from vaderSentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def predict(tweet):
   analyzer = SentimentIntensityAnalyzer()
   vs = analyzer.polarity_scores(tweet)
   return vs







