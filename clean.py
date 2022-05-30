"""
Functions for text cleaning of raw transcript

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

from collections import Counter

from sklearn.feature_extraction import text 
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.decomposition import TruncatedSVD
from sklearn.cluster import KMeans
from sklearn.pipeline import make_pipeline

from sklearn.decomposition import NMF
from sklearn.preprocessing import normalize

from wordcloud import WordCloud
import gensim
from gensim import matutils, models
import scipy.sparse

import re
import string

import nltk
from nltk import pos_tag
from tokenizer import split_into_sentences
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import sent_tokenize , word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import LancasterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

# Preparation for topic modeling
# Handle words to remove
add_stop_words = ['like','youre','ive','im','really','id','just','dont','didnt','thi','wa',
                  'say','know','make','people',"today","way","day","time","year",'tonight']

boring_words = ['say','like','just','dont','don','im','it','ve','re','we',
                'live','youll','youve','things','thing','youre','right','really','lot',
                'make','know','people','way','day',
                'little', 'maybe','men',"americans","america",
                'kind','heart', "american","president","united","states"         
                ]

gist_file = open("gist_stopwords.txt", "r")
content = gist_file.read()
stop_words = content.split(",")+boring_words+add_stop_words

# pos Lemmatisation：
lemmatizer = WordNetLemmatizer()
def lemmatize_all(sent):
    words=[]
    for word, tag in pos_tag(word_tokenize(sent)):
        if tag.startswith('NN'):
            words.append(lemmatizer.lemmatize(word, pos='n'))
        elif tag.startswith('VB'):
            words.append(lemmatizer.lemmatize(word, pos='v'))
        elif tag.startswith('JJ'):
            words.append(lemmatizer.lemmatize(word, pos='a'))
        elif tag.startswith('R'):
            words.append(lemmatizer.lemmatize(word, pos='r'))
        else:
            words.append(word)
    return words
     
def decode(word):
    return (word.encode('utf8').decode('unicode_escape'))

# remove  words 
def remove_words(doc):
    sentence_lists=[]
    sentences = sent_tokenize(doc)
    for sent in sentences:
        # lemma with POS tag
        stem_sentence= lemmatize_all(sent)
        # symbol
        filtered_tokens = [decode(w.lower()) for w in stem_sentence if re.search('^[a-zA-Z]+$', w)]
        # stopwords
        nostop_tokens= [w for w in filtered_tokens if w not in stop_words and 4<len(w)<20]          
        sentence_lists.append(" ".join(nostop_tokens))
    return " ".join(sentence_lists)


def select_length(text):
    word_lists= [w for w in word_tokenize(text) if w not in stop_words and 4<len(w)<20]          
    return " ".join(word_lists)
    
# def clean_text(text):   
#     text = re.sub('\[.*?\]','',text)
#     text = re.sub('[%s]' % re.escape(string.punctuation),'',text)
#     text = re.sub('\w*\d\w*','',text)
#     text = re.sub('[-]','',text)
#     text = re.sub('[–’“”…]','',text)
#     text = re.sub('\xa0','',text)
#     text = re.sub('\n','',text)
#     text = re.sub('\r','',text)
#     return text

def clean_text(transcripts):
    transcripts = transcripts.lower()
    transcripts = re.sub('\((.*?\))', '', transcripts)
    transcripts = re.sub('\[.*?\]', '', transcripts)
    transcripts = re.sub('[%s]' % re.escape(string.punctuation), '', transcripts)
    transcripts = re.sub('\w*\d\w*', '', transcripts)
    return transcripts


# def remove_unpunc(text):   
#     text = re.sub('\[*\]','',text)
#     text = re.sub('\'s*','',text)
#     text = re.sub('\w*\d\w*','',text)
#     text = re.sub('[-]','',text)
#     text = re.sub('[–’“”…]','',text)
#     text = re.sub('\xa0','',text)
#     text = re.sub('\n','',text)
#     text = re.sub('\r','',text)
#     return text

def clean(df,column_name):
    """
    Given the df and column_name
    (remove names, basic clean, lemmatization) and return the df.
    """
    #df[column_name] = df[column_name].apply(lambda x: remove_special_characters(x)) 
    df["clean"] = df[column_name]
    df["clean"] = df["clean"].apply(lambda x: remove_words(x))
    df["clean"] = df["clean"].apply(lambda x: clean_text(x))
    df["clean"] = df["clean"].apply(lambda x: select_length(x)) 
    return df

#-----------------------------------------------------------------------------------------
# choose only the noun and verbs

def lemmatize_nv(sent):
    words=[]
    for word, tag in pos_tag(word_tokenize(sent)):
        if tag.startswith('NN'):
            words.append(lemmatizer.lemmatize(word, pos='n'))
        elif tag.startswith('VB'):
            words.append(lemmatizer.lemmatize(word, pos='v'))
        else:
            words.append(" ")
    return words

def get_nv(doc):
    sentence_lists=[]
    sentences = sent_tokenize(doc)
    for sent in sentences:
        # lemma with POS tag
        stem_sentence= lemmatize_nv(sent)
        # symbol
        filtered_tokens = [w.lower()  for w in stem_sentence if re.search('[a-zA-Z]', w)]
        # stopwords
        nostop_tokens= [w for w in filtered_tokens if w not in stop_words and 4<len(w)<20]          
        sentence_lists.append(" ".join(nostop_tokens))
    return " ".join(sentence_lists)


def clean_text(text):   
    text = re.sub('\[.*?\]','',text)
    text = re.sub('[%s]' % re.escape(string.punctuation),'',text)
    text = re.sub('\w*\d\w*','',text)
    text = re.sub('[-]','',text)
    text = re.sub('[–’“”…]','',text)
    text = re.sub('\xa0','',text)
    text = re.sub('\n','',text)
    text = re.sub('\r','',text)
    return text

def clean_nv(df,column_name):
    df["n-v"] = df[column_name]
    df["n-v"] =  df["n-v"].apply(get_nv)
    df["n-v"] = df["n-v"].apply(lambda x: clean_text(x))
    return df
