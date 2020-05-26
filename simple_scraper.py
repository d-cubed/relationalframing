# -*- coding: utf-8 -*-
"""
Description:
    1. Scrape all comments from a given reddit thread
    2. Extract top level comments
    3. Save to a csv file

Original Author:
    Copyright (c) Ian Hussey 2016 (ian.hussey@ugent.be)
    Originally released under the MIT license.
    Then released under the GPLv3+ license.

Current version:
    All mistakes are mine, don@complexbehavior.io
    Still under the GPLv3+ license
    Adapted for Python 3


Known issues:
    None.


Notes From Ian :
    1. Although the script only uses publiclly available information,
    PRAW's call to the reddit API requires a reddit login (see line 47).
    2. Reddit API limits number of calls (1 per second IIRC).
    For a large thread (e.g., 1000s of comments) script execution time may therefore be c.1 hour.
    3. Because of this bottleneck, the entire data object is written to a pickle before anything is discarded.
    This speeds up testing etc.
    4. Does not extract comment creation date (or other properties), which might be useful.
"""

# Dependencies
import praw
import csv
import os
import sys
import pickle
from importlib import reload


#https://atomar94.github.io/playing-with-reddit-using-python-praw-and-pandas/



# Change directory to that of the current script
absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

if(not os.path.isdir("./data/")):
    os.mkdir("./data/")

# Acquire comments via reddit API
r = praw.Reddit(client_id = "JrC02mT2XjAnAw",
                     client_secret = "ocxsQHcTQgrNvYyxhbUUl3sBJSk",
                     user_agent = "reddit researcher made by /u/gnudon",
                     username='gnudon', 
                     password='2b2late')


#submission = r.submission(id='5q9ppf') ### what is it like
submission = r.submission(id='4e74ch') ### Autistic people of Reddit what do you wish people would understand better about autism?
#submission = r.submission(id='bnffyo') ###bicycles almost got my bike stolen apparently. close call.



## replace more comments also deprecated see:
#https://praw.readthedocs.io/en/latest/code_overview/models/submission.html
submission.comments.replace_more(limit=0, threshold=0)
#comments = submission.comments.list()




subreddit_name=submission.subreddit_name_prefixed.split('/')[1]
filename = subreddit_name + '_' + submission.id
picklefile = 'data/' + filename + '.pkl'

# Save object to pickle
output = open(picklefile, 'wb')
pickle.dump(submission, output, -1)
output.close()

## Load object from pickle
#pkl_file = open('scraped_data.pkl', 'rb')
#submission = pickle.load(pkl_file)
##pprint.pprint(submission)
#pkl_file.close()


top_level_comments = []
already_done = set()
commentnumber = 1
forest_comments = submission.comments
for comment in forest_comments:
    if comment.body and comment.is_root:
    #if comment.body:
        if comment.id not in already_done:
            already_done.add(comment.id)  # add it to the list of checked comments
            #parseablestring = str(commentnumber) + "|" + comment.body.replace('\n',' ').strip()
            storethisstring = comment.body.replace('\n', ' ').replace('\r', '')
            #top_level_comments.append([parseablestring])  # append to list for saving
            top_level_comments.append([storethisstring])
            commentnumber += 1

print("downloaded %s comments"% str(commentnumber-1))
        
# Save comments to disk
#csvfile = 'data/' + filename + '_all_levels.csv'
csvfile = 'data/' + filename + '.csv'
with open(csvfile, "w") as output:
    writer = csv.writer(output)
    writer.writerows(top_level_comments)
