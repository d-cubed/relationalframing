#!/usr/bin/python3
# -*- coding: utf-8 -*-
from flair.models import TextClassifier
from flair.data import Sentence
import pandas
import sys
import re
import boto3
import os
from textblob import TextBlob
import json

if len(sys.argv) < 2:
    print("You should supply the name of a CSV to analyze for sentiment")
    sys.exit()
else:
    files = []
    for i in range(1, len(sys.argv)):
        print("Adding %s to list of csvs" % str(sys.argv[i]))
        files.append(str(sys.argv[i]))

dfs = []
for file in files:
    df = pandas.read_csv(file, names=['text'])
    df['filename'] = os.path.basename(file).split('.')[0]
    dfs.append(df)
   # dfs.append(pandas.read_csv(file, names=['text']))

print("Added %s CSVs for processing"%(str(len(sys.argv)-1)))
print("This program generates new CSVs with sentiment values")
print("This program does not create graphics")


def threelines():
    for i in range(3):
        print("************************************")

def print_intro():
    threelines()
    print("You are currently running %s" % (sys.argv[0]))
    print("This program uses text classification. \nIt needs to load some flair models first.")
    print("There will be messages from pytorch and flair.")
    threelines()

def print_text_from_df(df):
    for index, row in df.iterrows():
        print(index, row['text'])

def print_col_from_df(df, col):
    if col > len(df.columns):
        print("There are only %s columns"%len(df.columns))
    else:
        print("printing col %s" % col)
        for index, row in df.iterrows():
            print(index, row[col])


def get_flair(text):
    #this is for flair
    try:
        sentence = Sentence(text)
        classifier.predict(sentence)
        thevalence = re.findall(r'\d+\.*\d*', str(sentence.labels[0]))
        thevalence = float(thevalence[0])
        therating = sentence.get_label_names()[0]
        return  [therating, thevalence]

    except Exception:
        print("An exception occurred. Text was not passed to get_valence")
        return 'n/a'

def get_aws_scores(text):
    s = comprehend.detect_sentiment(Text=text, LanguageCode='en')
    aws_rating = s['Sentiment']
    aws_positive = s['SentimentScore']['Positive']
    aws_negative = s['SentimentScore']['Negative']
    aws_neutral = s['SentimentScore']['Neutral']
    aws_mixed = s['SentimentScore']['Mixed']
    aws_scores = [aws_rating, aws_positive, aws_negative, aws_neutral, aws_mixed]
    return aws_scores

def split_to_flair_rating(score):
    return score[0]
def split_to_flair_valence(score):
    return score[1]
def split_to_aws_rating(score):
    return score[0]
def split_to_aws_positive(score):
    return score[1]
def split_to_aws_negative(score):
    return score[2]
def split_to_aws_neutral(score):
    return score[3]
def split_to_aws_mixed(score):
    return score[4]


def get_textblob_polarity(text):
    tb = TextBlob(text)
    return tb.sentiment.polarity

def get_textblob_rating(textblobpolarity):
    if (textblobpolarity < -0.05):
        return 'NEGATIVE'
    elif (textblobpolarity > 0.05):
        return 'POSITIVE'
    else:
        return 'NEUTRAL'

def save_to_csv(filename, df):
    csvfile = 'data/sentiments_' + filename + '.csv'
    print("saving CSV %s "% csvfile)
    df.to_csv(csvfile, index=False)

def clean_and_save(df):
    filename = df.at[1, 'filename']
    cleandf = df[['filename', 'text','text_blob_rating','text_blob_polarity']].copy()
    #ignore warning or use .copy()
    #https://www.dataquest.io/blog/settingwithcopywarning/
    cleandf['flair_rating'] = df['flair_scores'].apply(split_to_flair_rating)
    cleandf['flair_valence'] = df['flair_scores'].apply(split_to_flair_valence)
    cleandf['aws_rating'] = df['aws_scores'].apply(split_to_aws_rating)
    cleandf['aws_positive'] = df['aws_scores'].apply(split_to_aws_positive)
    cleandf['aws_negative'] = df['aws_scores'].apply(split_to_aws_negative)
    cleandf['aws_neutral'] = df['aws_scores'].apply(split_to_aws_neutral)
    cleandf['aws_mixed'] = df['aws_scores'].apply(split_to_aws_mixed)

    save_to_csv(filename, cleandf)

print_intro()

#flair
classifier = TextClassifier.load('en-sentiment')

#AWS
session = boto3.Session(profile_name='default')
comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

num=0
for df in dfs:
    threelines()
    print("Preparing valence for df %d - this may take a second"%num)
    df['flair_scores'] = df['text'].apply(get_flair)
    df['aws_scores'] = df['text'].apply(get_aws_scores)
    df['text_blob_polarity'] = df['text'].apply(get_textblob_polarity)
    df['text_blob_rating'] = df['text_blob_polarity'].apply(get_textblob_rating)
    num+=1

for df in dfs:
    clean_and_save(df)

"""
for df in dfs:
    threelines()
    print_col_from_df(df,2)
"""
