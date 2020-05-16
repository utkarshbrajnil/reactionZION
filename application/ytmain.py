
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

import datetime as dt
from application.yt_advsearch import search_vidid,allvidcom
from apiclient.discovery import build
from rfc3339 import rfc3339

import datetime as dt
import pandas as pd
from twitterscraper import query_tweets

import json
import sqlite3
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from unidecode import unidecode
import time
from threading import Lock, Timer
import pandas as pd

import regex as re
from collections import Counter
import string
import pickle
import itertools
#from textblob import TextBlob


def twload(ipstr):
    ytload(ipstr)
    analyzer = SentimentIntensityAnalyzer()

    conn = sqlite3.connect('data/alldata.db', isolation_level=None, check_same_thread=False)
    c = conn.cursor()

    def create_table():
        try:
            c.execute("PRAGMA journal_mode=wal")
            c.execute("PRAGMA wal_checkpoint=TRUNCATE")

            c.execute("CREATE TABLE IF NOT EXISTS twsentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, screen name TEXT, timestamp TIMESTAMP, text TEXT, likes INTEGER, retweets INTEGER, replies INTEGER)")

        except Exception as e:
            print(str(e))

    create_table()

    two_months = dt.timedelta(days=60)
    end_date = dt.date.today()
    begin_date = end_date - two_months

    limit = 5000
    lang = "english"

    tweets = query_tweets(ipstr, begindate=begin_date, enddate=end_date ,limit=limit, lang=lang)

    df = pd.DataFrame(t._dict_ for t in tweets)
    df.sort_values(by=['likes','retweets','replies'], inplace=True, ascending=False)
    #removing unwanted columns
    df.drop(df.columns[[3,4,6,8,9,10,11,12,13,17,18,19,20]], axis = 1, inplace = True)
    df = df[df.likes >=0]
    df.set_index('username',inplace=True)

    df.insert(0, 'id', range(0, len(df)))

    f_list=df['text'].to_list()
    for l in f_list:
        if(l=="[removed]" or l=="[deleted]"):
            f_list.append(0)

    negative=0.0
    positive=0.0
    neutral=0.0

    pol=list()

    for l in f_list:
        if(l!=0):
            analysis=TextBlob(l).sentiment
            #print (analysis)
            if(analysis.polarity==0):
                neutral+=1
            elif(analysis.polarity>0):
                positive+=1
            elif(analysis.polarity<0):
                negative+=1
            t=analysis.polarity
            pol.append(t)
        else:
            pol.append(0)
            #l1=l.str.replace(l,nalysis.polarity)
            #df['comments']=l1
    df['sentiment']=pol

    #print(maindf)
    #c.execute('''DROP TABLE IF EXISTS youtube''')
    df.to_sql('twsentiment', conn, if_exists='replace')

def ytload(query):
    analyzer = SentimentIntensityAnalyzer()

    conn = sqlite3.connect('data/alldata.db', isolation_level=None, check_same_thread=False)
    c = conn.cursor()

    def create_table():
        try:

            # http://www.sqlite.org/pragma.html#pragma_journal_mode
            # for us - it allows concurrent write and reads
            c.execute("PRAGMA journal_mode=wal")
            c.execute("PRAGMA wal_checkpoint=TRUNCATE")
            #c.execute("PRAGMA journal_mode=PERSIST")

            # changed unix to INTEGER (it is integer, sqlite can use up to 8-byte long integers)
            c.execute("CREATE TABLE IF NOT EXISTS sentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, comments TEXT, sentiment REAL)")
            # key-value table for random stuff
            #c.execute("CREATE TABLE IF NOT EXISTS misc(key TEXT PRIMARY KEY, value TEXT)")
            # id on index, both as DESC (as you are sorting in DESC order)
            #c.execute("CREATE INDEX id_unix ON sentiment (id DESC, unix DESC)")
            # out full-text search table, i choosed creating data from external (content) table - sentiment
            # instead of directly inserting to that table, as we are saving more data than just text
            # https://sqlite.org/fts5.html - 4.4.2
            #c.execute("CREATE VIRTUAL TABLE sentiment_fts USING fts5(tweet, content=sentiment, content_rowid=id, prefix=1, prefix=2, prefix=3)")
            # that trigger will automagically update out table when row is interted
            # (requires additional triggers on update and delete)
            #c.execute("""
            #    CREATE TRIGGER sentiment_insert AFTER INSERT ON sentiment BEGIN
            #        INSERT INTO sentiment_fts(rowid, tweet) VALUES (new.id, new.tweet);
            #    END
            #""")
        except Exception as e:
            print(str(e))

    create_table()


    days = dt.timedelta(days=2)
    end_date = dt.date.today()
    begin_date = end_date - days
    videoid_list=search_vidid(begin_date, end_date, query)
    maindf = allvidcom(videoid_list)

    maindf.insert(0, 'id', range(0, len(maindf)))

    f_list=maindf['comments'].to_list()
    for l in f_list:
        if(l=="[removed]" or l=="[deleted]"):
            f_list.append(0)

    negative=0.0
    positive=0.0
    neutral=0.0

    pol=list()

    for l in f_list:
        if(l!=0):
            analysis=TextBlob(l).sentiment
            #print (analysis)
            if(analysis.polarity==0):
                neutral+=1
            elif(analysis.polarity>0):
                positive+=1
            elif(analysis.polarity<0):
                negative+=1
            t=analysis.polarity
            pol.append(t)
        else:
            pol.append(0)
            #l1=l.str.replace(l,nalysis.polarity)
            #df['comments']=l1
    maindf['sentiment']=pol

    #print(maindf)
    #c.execute('''DROP TABLE IF EXISTS youtube''')
    maindf.to_sql('sentiment', conn, if_exists='replace') # - writes the pd.df to SQLIte DB


    #dfn=pd.read_sql('select * from sentiment', conn)
    #conn.commit()
    #conn.close()
    #print(dfn)
