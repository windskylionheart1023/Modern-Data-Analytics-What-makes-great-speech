"""
Generating Word Cloud
"""

import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

from wordcloud import WordCloud
from sklearn.feature_extraction import text 
from sklearn.feature_extraction.text import CountVectorizer

add_stop_words = ['like','youre','ive','im','really','id','ve','just','dont','didnt','thi','wa',
                  'say','know','make','people',"today","way","day","time","year",'tonight']

boring_words = ['say','like','just','dont','don','im',
                'live','youll','youve','things','thing','youre','right','really','lot',
                'make','know','people','way','day',
                'little', 'maybe','men',"americans","america"
                'kind','heart', "american","president","united","states"         
                ]

gist_file = open("gist_stopwords.txt", "r")
content = gist_file.read()
stop_words = content.split(",")+boring_words+add_stop_words

def show_word_cloud(df, column_name, add_stop_words, collocation_threshold = 30):
    """
    Input: df, column_name (Ex:speech_clean_2.transcript)
    Output: show Word Cloud of first 16 speeches
    
    """
    # Reset the output dimensions
    plt.rcParams['figure.figsize'] = [30, 10]

    stop_words = text.ENGLISH_STOP_WORDS.union(add_stop_words)
    wc = WordCloud(stopwords=stop_words, background_color="white", colormap="Dark2",
                       max_font_size=150, random_state=42,
                       collocation_threshold = collocation_threshold)

    for index, speech in enumerate(df[column_name].iloc[:6]):
        wc.generate(speech)
        plt.subplot(2, 3, index+1)
        plt.imshow(wc, interpolation="bilinear")
        plt.axis("off")
        plt.title("Topic"+str(index+1),fontweight='normal') 
        
    plt.show()



