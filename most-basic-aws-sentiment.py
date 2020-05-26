import boto3
import json

session = boto3.Session(profile_name='default')

comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')

text = "It is raining today in Seattle"

print('Calling DetectSentiment')
print(json.dumps(comprehend.detect_sentiment(Text=text, LanguageCode='en'), sort_keys=True, indent=4))
print('End of DetectSentiment\n')

