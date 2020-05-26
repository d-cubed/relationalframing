#! /usr/bin/python3

import pandas as pd
import io
import matplotlib.pyplot as plt
import sys
import re
import json

print ("You are currently running %s" % (sys.argv[0]))

if len(sys.argv) < 2:
    print("You should supply the name of a CSV that should be converted to a CSV")
    sys.exit()
else:
    filename = sys.argv[1]
    csv = pd.read_csv(filename)

cols = {'text_blob_rating', 'flair_rating', 'aws_rating'}
pd.melt(csv, id_vars =['text'], value_vars =cols)

