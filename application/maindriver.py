
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob

from application.redditScraping import top_posts,to_id_list,mine_comments

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


def create_connection():
    try:
        conn = sqlite3.connect('data/alldata.db')#, isolation_level=None, check_same_thread=False)
        c = conn.cursor()
    except Exception as e:
        print(str(e))
    return conn

def create_tabletw(conn):
    try:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS twsentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, screen_name TEXT, timedate TIMESTAMP, texts TEXT, likes INTEGER, retweets INTEGER, replies INTEGER, sentiment REAL)")
    except Exception as e:
        print(str(e))

def create_tableyt(conn):
    try:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS ytsentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, unix INTEGER, comments TEXT, sentiment REAL)")
    except Exception as e:
        print(str(e))

def create_tablerd(conn):
    try:
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS rdsentiment(id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, s_score INTEGER, upvote_ratio REAL, comments TEXT, c_score INTEGER , c_date TIMESTAMP, sentiment REAL)")
    except Exception as e:
        print(str(e))


def analyse_sentiment(df , term):
    f_list=df[term].to_list()
    for l in f_list:
        if(l=="[removed]" or l=="[deleted]"):
            f_list.append(0)

    pol=list()
    for l in f_list:
        if(l!=0):
            analysis=TextBlob(l).sentiment
            t=analysis.polarity
            pol.append(t)
        else:
            pol.append(0)
    df['sentiment']=pol
    df=df[df.sentiment != 0]
    return df

def rdload(topic):

    conn=create_connection()
    c = conn.cursor()
    create_tablerd(conn)

    df1=top_posts(topic)
    list1=to_id_list(df1)
    rddf=mine_comments(list1)

    rddf.insert(0, 'id', range(0, len(rddf)))

    rddf=analyse_sentiment(rddf,"comments")
    #print(rddf['sentiment'])
    rddf.to_sql('rdsentiment', conn, if_exists='replace') # - writes the pd.df to SQLIte DB


def ytload(query):

    conn=create_connection()
    c = conn.cursor()
    create_tableyt(conn)



    days = dt.timedelta(days=2)
    end_date = dt.date.today()
    begin_date = end_date - days
    videoid_list=search_vidid(begin_date, end_date, query)
    ytdf = allvidcom(videoid_list)

    ytdf.insert(0, 'id', range(0, len(ytdf)))

    ytdf=analyse_sentiment(ytdf,"comments")

    ytdf.to_sql('ytsentiment', conn, if_exists='replace') # - writes the pd.df to SQLIte DB



def twload(ipstr):
    ytload(ipstr)
    conn=create_connection()
    create_tabletw(conn)

    two_months = dt.timedelta(days=60)
    end_date = dt.date.today()
    begin_date = end_date - two_months

    limit = 500
    lang = "english"

    tweets = query_tweets(ipstr, begindate=begin_date, enddate=end_date ,limit=limit, lang=lang)

    df = pd.DataFrame(t.__dict__ for t in tweets)
    df.sort_values(by=['likes','retweets','replies'], inplace=True, ascending=False)
    #removing unwanted columns
    df.drop(df.columns[[3,4,6,8,9,10,11,12,13,17,18,19,20]], axis = 1, inplace = True)
    df = df[df.likes >=0]
    df.set_index('username',inplace=True)

    df.insert(0, 'id', range(0, len(df)))

    df=analyse_sentiment(df,"text")
    #print(df['sentiment'])

    df.to_sql('twsentiment', conn, if_exists='replace')

    #rdload(ipstr)
