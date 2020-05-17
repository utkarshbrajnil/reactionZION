# To mine the required data from Reddit

import praw
import pandas as pd

reddit = praw.Reddit(client_id='O819Gp7QK8_o5A', client_secret='4pC2Pu3eTJWxdSKfKscZYQOh2-o', user_agent='Reddit WebScraping')


def top_posts(topic):
    posts=[]
    f_subreddit = reddit.subreddit(topic)
    for post in f_subreddit.hot(limit=100):
        posts.append([post.title, post.score, post.id, post.num_comments])
    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'num_comments'])
    posts.sort_values(by=['score','num_comments'], inplace=True, ascending=False)
    posts.set_index('title',inplace=True)
    return posts




def to_id_list(posts):
    id_list= posts["id"].tolist()
    return id_list


def mine_comments(id_list):
    comments=[]
    for i in id_list:
        submission = reddit.submission(id=i)
        submission.comments.replace_more(limit=None)
        for comment in submission.comments.list():
            comments.append([submission.title,submission.score,submission.upvote_ratio,comment.body,comment.score,comment.created_utc])
    comments=pd.DataFrame(comments,columns=['title','s_score','upvote_ratio','comments','c_score','c_date'])
    comments['c_date'] = pd.to_datetime(comments['c_date'],unit='s')
    comments.sort_values(by=['c_date','s_score','c_score'], inplace=True, ascending=False)
    comments.set_index('title',inplace=True)
    return comments


def f_csv(comments):
    f=comments.to_csv('comments.csv',index=True)
    return f






#def join_frames(posts,comments):
#        posts.append([post.title, post.score, post.id, post.subreddit, post.url, post.num_comments, post.selftext, post.created])
#    posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created'])

#        comments.append([submission.title,comment.subreddit,comment.submission,comment.body,comment.score,submission.upvote_ratio])
#   comments=pd.DataFrame(comments,columns=['title','subreddit','submission','comments','score','upvote_ratio'])
