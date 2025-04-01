import praw
import boto3
import json
import time

reddit = praw.Reddit(
    client_id="aBcDeFgHiJkLmN",  # Replace with your Client ID
    client_secret="xYz12345_aBcDeFgHiJkLmN",  # Replace with your Client Secret
    user_agent="aws:RedditSentimentAnalysis:v1.0 by /u/yourusername"  # Replace with your User Agent
)
firehose = boto3.client('firehose')

subreddit = reddit.subreddit('artificial')
for comment in subreddit.stream.comments(skip_existing=True):
    data = {'id': comment.id, 'text': comment.body, 'created_utc': comment.created_utc}
    print(data['text'])
    firehose.put_record(
        DeliveryStreamName='RedditStream',
        Record={'Data': json.dumps(data) + '\n'}
    )
    time.sleep(1)