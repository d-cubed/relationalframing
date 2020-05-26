import boto3
import json

session = boto3.Session(profile_name='default')

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

text = "It is raining today in Seattle"

print('Calling DetectSentiment')
print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
s = comprehend.detect_sentiment(Text="you are stupid and ugly", LanguageCode='en')


aws_rating = s['Sentiment']
aws_positive = s['SentimentScore']['Positive']
aws_negative = s['SentimentScore']['Negative']
aws_neutral =  s['SentimentScore']['Neutral']
aws_mixed = s['SentimentScore']['Mixed']

print("AWS rating: %s positive: %s negative %s neutral: %s mixed: %s"% (aws_rating, aws_positive, aws_negative, aws_neutral, aws_mixed ))

print('End of DetectSentiment\n')

