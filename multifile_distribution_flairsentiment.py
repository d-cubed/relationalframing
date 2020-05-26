#!/usr/bin/python3

# -*- coding: utf-8 -*-


from flair.models import TextClassifier
from flair.data import Sentence
import pandas
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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
    dfs.append(pandas.read_csv(file, names=['text']))

print("Added %s CSVs for processing"%(str(len(sys.argv)-1)))


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
        for index, row in df.iterrows():
            print(index, row[col])


def get_valence(text):
    try:
        sentence = Sentence(text)
        classifier.predict(sentence)
        thevalence = re.findall(r'\d+\.*\d*', str(sentence.labels[0]))
        thevalence = float(thevalence[0])
        #print(type(thevalence))
        return  thevalence
    #Surely I missed the builtin method that just returns the value?
    except Exception:
        print("An exception occurred. Text was not passed to get_valence")
        return 'n/a'

def plotone_df(df):
    plt.hist(df['valence'], color='blue', edgecolor='black')
    #plt.tight_layout()
    plt.show()

print_intro()

classifier = TextClassifier.load('en-sentiment')

num=0
for df in dfs:
    threelines()
    print("Preparing valence for df %d - this may take a second"%num)
    #print("Preparing valence for df %s "%str(dfs.index(df)))
    df['valence'] = df['text'].apply(get_valence)
    #df.reset_index(drop=True)
    #plt.hist(df['valence'], color='blue', edgecolor='black')
    # plt.tight_layout()
    #plt.show()
    num+=1

    #plotone_df(df)
    #print(df['valence'].dtypes)
    #print_col_from_df(df,1)
    #plt.hist(df['valence'])

#plotone_df(dfs[0])

"""
fig = plt.figure()
for df in dfs:
    plt.hist(df['valence'], color='blue', edgecolor='black')
plt.show()
"""
#https://stackoverflow.com/questions/6871201/plot-two-histograms-on-single-chart-with-matplotlib

num = 0
bins = np.linspace(-10, 10, 30)

plt.style.use('seaborn-deep')
vals = []
min = 1.0
max = 0.0

for df in dfs:
    vals.append(df['valence'])
    if (df['valence'].min()< min):
        min = df['valence'].min()
    if (df['valence'].max()>max):
        max = df['valence'].max()

#https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
#https://towardsdatascience.com/histograms-and-density-plots-in-python-f6bda88f5ac0
bins = np.linspace(min,max,100)
plt.hist(vals,bins)
plt.show()

plt.legend(loc='upper right')
plt.tight_layout()
plt.show()



print("done")

"""
for df in dfs:
    plotone_df(df)
    
    
for i, binwidth in enumerate([1, 5, 10, 15]):
    # Set up the plot
    ax = plt.subplot(2, 2, i + 1)

    # Draw the plot
    ax.hist(df['valence'], bins=int(180 / binwidth),
            color='blue', edgecolor='black')

    # Title and labels
    ax.set_title('Histogram with Binwidth = %d' % binwidth, size=30)
    ax.set_xlabel('valence', size=22)
    ax.set_ylabel('valence', size=22)

plt.tight_layout()
plt.show()
"""
