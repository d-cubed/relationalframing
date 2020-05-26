#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""
Adapted from Ian Hussey 2016 (ian.hussey@ugent.be)
    Originally released under the MIT license.
    Then released under the GPLv3+ license.

Current version:
    All mistakes are mine, don@complexbehavior.io
    Still under the GPLv3+ license
"""
import praw
import csv
import os
import sys
import pickle
import boto3
import json
import scraper_config as secret #python file in working directory

session = boto3.Session(profile_name='default')

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')



if len(sys.argv) < 2:
    print("You should supply the name of one or more reddit submission IDs to scrape from")
    sys.exit()
else:
    threads = []
    for i in range (1,len(sys.argv)):
        print("Adding %s to queue" % str(sys.argv[i]))
        threads.append(str(sys.argv[i]))

#https://atomar94.github.io/playing-with-reddit-using-python-praw-and-pandas/
# Change directory to that of the current script
absolute_path = os.path.abspath(__file__)
directory_name = os.path.dirname(absolute_path)
os.chdir(directory_name)

if(not os.path.isdir("./data/")):
    os.mkdir("./data/")

# Acquire comments via reddit API, load from Scraper_config
r = praw.Reddit(client_id = secret.client_id,
                     client_secret = secret.client_secret,
                     user_agent = secret.user_agent,
                     username=secret.username,
                     password=secret.password)

def save_pickle(filename, submission):
    picklefile = 'data/aws_' + filename + '.pkl'
    output = open(picklefile, 'wb')
    pickle.dump(submission, output, -1)
    output.close()

def get_toplevelcomments(submission):
    top_level_comments = []
    already_done = set()
    commentnumber = 1
    forest_comments = submission.comments
    for comment in forest_comments:
        if comment.body and comment.is_root:
            # if comment.body:
            if comment.id not in already_done:
                already_done.add(comment.id)  # add it to the list of checked comments
                storethisstring = comment.body.replace('\n', ' ').replace('\r', '')
                top_level_comments.append([storethisstring])
                commentnumber += 1
    print("downloaded %s comments" % str(commentnumber - 1))
    return top_level_comments

def save_to_csv(filename, top_level_comments):
    csvfile = 'data/aws_' + filename + '.csv'
    with open(csvfile, "w") as output:
        writer = csv.writer(output)
        writer.writerows(top_level_comments)

def get_submission(thread):
    submission = r.submission(id=thread)
    submission.comments.replace_more(limit=0, threshold=0)
    subreddit_name = submission.subreddit_name_prefixed.split('/')[1]
    filename = subreddit_name + '_' + submission.id
    save_pickle(filename, submission)
    top_level_comments=get_toplevelcomments(submission)
    save_to_csv(filename, top_level_comments)


print("Retrieving %s reddit threads"%(str(len(sys.argv)-1)))
for thread in threads:
    print("Getting %s"%thread)
    get_submission(thread)
