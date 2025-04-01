import json
import boto3
import urllib.parse

s3_client = boto3.client('s3')
comprehend = boto3.client('comprehend', region_name='us-east-1')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = urllib.parse.unquote_plus(record['s3']['object']['key'])

        try:
            # Read the raw data from S3
            response = s3_client.get_object(Bucket=bucket, Key=key)
            raw_data = response['Body'].read().decode('utf-8')

            # Parse all comments
            comments = []
            for line in raw_data.splitlines():
                if not line.strip():
                    continue
                comment_data = json.loads(line)
                comments.append(comment_data)

            # Batch process sentiment analysis (max 25 texts per batch)
            processed_records = []
            batch_size = 25
            for i in range(0, len(comments), batch_size):
                batch = comments[i:i + batch_size]
                texts = [comment['text'] for comment in batch if 'text' in comment]
                if not texts:
                    continue

                response = comprehend.batch_detect_sentiment(
                    TextList=texts,
                    LanguageCode='en'
                )

                sentiment_results = response['ResultList']
                error_results = response.get('ErrorList', [])
                if error_results:
                    print(f"Comprehend batch errors: {error_results}")

                text_to_sentiment = {result['Index']: result for result in sentiment_results}
                for j, comment in enumerate(batch):
                    if 'text' not in comment:
                        comment['sentiment'] = 'UNKNOWN'
                        comment['sentiment_score'] = {}
                    else:
                        text_index = j
                        if text_index in text_to_sentiment:
                            sentiment = text_to_sentiment[text_index]
                            comment['sentiment'] = sentiment['Sentiment']
                            comment['sentiment_score'] = sentiment['SentimentScore']
                        else:
                            comment['sentiment'] = 'UNKNOWN'
                            comment['sentiment_score'] = {}
                    processed_records.append(comment)

            # Write processed data to the processed S3 bucket with .json extension
            processed_key = key.replace('raw/', 'processed/')
            if not processed_key.endswith('.json'):
                processed_key += '.json'
            s3_client.put_object(
                Bucket='reddit-sentiment-processed-umesh',
                Key=processed_key,
                Body='\n'.join(json.dumps(record) for record in processed_records) + '\n',
                ContentType='application/json'
            )

            print(f"Processed {key} and wrote to {processed_key}")

        except Exception as e:
            print(f"Error processing {key}: {str(e)}")
            raise e

    return {
        'statusCode': 200,
        'body': json.dumps('Successfully processed S3 event')
    }