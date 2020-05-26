# -*- coding: utf-8 -*-

from flair.models import TextClassifier
from flair.data import Sentence
import pandas
import sys
import re
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#todo split by sentence; graph by author
#great article on dist plots in python

if len(sys.argv) < 2:
    print("You should supply the name of a CSV to analyze for sentiment")
    sys.exit()
else:
    filetoread = sys.argv[1]
    df = pandas.read_csv(filetoread, names=['text'])

classifier = TextClassifier.load('en-sentiment')

for i in range(3):
    print("************************************")
print ("You are currently running %s" % (sys.argv[0]))
print("This program uses text classification. \nIt needs to load some flair models first.")
print("There will be messages from pytorch and flair.")
for i in range(3):
    print("************************************")

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

df['valence'] = df['text'].apply(get_valence)

#print(df['valence'].dtypes)
#print_col_from_df(df,1)


#plt.hist(df['valence'])
plt.hist(df['valence'], color = 'blue', edgecolor = 'black')
plt.show()

"""
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
