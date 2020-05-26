#!/home/willard/anaconda3/bin/python
#https://atomar94.github.io/playing-with-reddit-using-python-praw-and-pandas/

import praw
import pandas as pd
from datetime import datetime
from importlib import reload


reddit = praw.Reddit(client_id = "JrC02mT2XjAnAw",
                     client_secret = "ocxsQHcTQgrNvYyxhbUUl3sBJSk",
                     user_agent = "reddit researcher made by /u/gnudon",
                     username='gnudon', 
                     password='2b2late')

def get_yyyy_mm_dd_from_utc(dt):
    date = datetime.utcfromtimestamp(dt)
    return str(date.year) + "-" + str(date.month) + "-" + str(date.day)
 

subreddit = reddit.subreddit('autism')
 
 
top_subreddit = subreddit.top(limit=998)
 
topics_dict = { "title":[], "score":[], "id":[], "url":[], \
                "comms_num": [], "created": [],  "body":[], "z_comments":[]}
 
 
for submission in top_subreddit:
     
    # https://www.reddit.com/r/redditdev/comments/46g9ao/using_praw_to_call_reddit_api_need_help/
    topics_dict["title"].append(submission.title)
    topics_dict["score"].append(submission.score)
    topics_dict["id"].append(submission.id)
    topics_dict["url"].append(submission.url)
    topics_dict["comms_num"].append(submission.num_comments)
    topics_dict["created"].append(get_yyyy_mm_dd_from_utc(submission.created))
    topics_dict["body"].append(submission.selftext)
     
    
   
    all_comments = submission.comments.list()
    print (all_comments)

#r = praw.Reddit('just a test - /u/gnudon')
#r.login('gnudon', '2b2late', disable_warning=True)

#http://api.intelligentonlinetools.com/diy/reddit/

"""comments = []
for submission in r.subreddit("askreddit").hot(limit=25):
  submission.comments.replace_more(limit=32)
  comments.append(submission.comments.list())
"""
#submission = r.get_submission(submission_id='5q9ppf')      # UNIQUE ID FOR THE THREAD GOES HERE - GET FROM THE URL
#submission.replace_more_comments(limit=None, threshold=0)  # all comments, not just first page
