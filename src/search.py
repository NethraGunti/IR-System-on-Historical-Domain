import sqlite3, re, time, math

import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

docs = {}
result = {}
term = {}

class Docs():
    terms = {}

class Terms():
    def __init__(self):
        self.docfreq = 0
        self.termfreq = 0
        self.idf = 0.
        self.tfidf = 0.


# query: search item
# N: number of documents in the databse
# 
if __name__ == "__main__":
    #commect to database
    
    #take input
    #tokenize and stem it
    #find docs using postional index