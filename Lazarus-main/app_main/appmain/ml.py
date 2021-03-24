import numpy as np
import pandas as pd
import pickle
import appmain
# from nltk.tokenize import word_tokenize
# from nltk.corpus import stopwords
# from nltk.stem import SnowballStemmer
# from sklearn.ensemble import AdaBoostClassifier
# import nltk
# from sklearn.feature_extraction.text import CountVectorizer


#preprocessing=pickle.load(open('/home/abhash/Documents/lazarus/app_main/appmain/preprocessing.pkl','rb'))
# classifier=pickle.load(open('/home/abhash/Documents/lazarus/app_main/appmain/ada.pkl','rb'))
# vectorizer=pickle.load(open('/home/abhash/Documents/lazarus/app_main/appmain/vec.pkl','rb'))



def pr(tweet):
   print(tweet)

# from vaderSentiment import SentimentIntensityAnalyzer
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
def predict(tweet):
   analyzer = SentimentIntensityAnalyzer()
   vs = analyzer.polarity_scores(tweet)
   return vs
   # print("{:-<65} {}".format(tweet, str(vs)))























# def predict(tweet):
#    twee=format_text(tweet)
#    li_tw=list(twee)
#    tkn=tknize_and_stop(li_tw)
#    stm=stem(tkn)

#    #clean_data=preprocessing.transform(twee)
#    vector=vectorizer.transform(stm)
#    result=classifier.predict(vector)
#    return result[0]


# def format_text(tw):
#   #Remove @ tags
#   comp_df=tw
#   # remove all the punctuation
#   comp_df = comp_df.replace(r'(@\w*)','')

#   #Remove URL
#   comp_df=comp_df.replace(r"http\S+", "")

#   #Remove # tag and the following words
#   comp_df= comp_df.replace(r'#\w+',"")

#   #Remove all non-character
#   comp_df= comp_df.replace(r"[^a-zA-Z ]","")

#   # Remove extra space
#   comp_df= comp_df.replace(r'( +)'," ")
#   comp_df= comp_df.strip()

#   # Change to lowercase
#   comp_df= comp_df.lower()

#   return comp_df

# # tokenizing and stop word removal

# def tknize_and_stop(tweet):
#   tok_li=[]
#   stop=set(stopwords.words('english'))
#   for i in tweet:
#     li=word_tokenize(i)
#     stop_rem=[i for i in li if i not in stop]
#     sen=" ".join(stop_rem)
#     tok_li.append(sen)
  
#   return tok_li


# # Stemmer
# def stem(tweet):
#   ss=SnowballStemmer('english')
#   stem_sen=[]
#   for i in tweet:
#     sentence=''
#     wrds=i.split(' ')
#     for i in wrds:
#       w=ss.stem(i)
#       w=w.lower()
#       sentence+=w
#       sentence+=' '
#     stem_sen.append(sentence)  
#   return stem_sen  


