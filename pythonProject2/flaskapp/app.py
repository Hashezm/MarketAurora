from flask import Flask, render_template, request
import requests
from collections import Counter
import boto3
import json
import hashlib

app = Flask(__name__)

#need to change this to amazon when container is pushed
FASTAPI_URL = 'http://127.0.0.1:5000/analyze/'

# aws S3 configuration
s3 = boto3.client('s3')
BUCKET_NAME = 'queries-for-marketaurora'


def query_to_key(query):
    """generate a unique key for the S3 file based on the query."""
    return f"{hashlib.md5(query.encode()).hexdigest()}.json"


def get_results_from_s3(query):
    """check if the results exist in S3 and return them if they do"""
    key = query_to_key(query)
    try:
        s3_object = s3.get_object(Bucket=BUCKET_NAME, Key=key)
        return json.loads(s3_object['Body'].read().decode('utf-8'))
    except s3.exceptions.NoSuchKey:
        return None


def save_results_to_s3(query, results):
    """SAVE QUERY RESULTS TO S3."""
    key = query_to_key(query)
    s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(results))


@app.route('/', methods=['GET', 'POST'])
def home():
    articles = []
    sentiments = []
    filter_sentiment = request.args.get('filter')  # get the sentiment filter from URL parameters

    if request.method == 'POST':
        topic = request.form.get('topic')

        # check if results in S3
        existing_results = get_results_from_s3(topic)

        if existing_results:
            articles = existing_results
        else:
            # if not, process the query using FastAPI
            response = requests.get(FASTAPI_URL, params={'topic': topic})
            if response.status_code == 200:
                articles = response.json().get('articles', [])

                # save the new results to S3
                save_results_to_s3(topic, articles)

        for article in articles:
            sentiments.append(article['sentiment'])

    counts = Counter(sentiments)  # count sentiments

    if filter_sentiment:
        articles = [article for article in articles if article['sentiment'] == filter_sentiment]

    return render_template('home2.html', articles=articles, counts=counts, filter_sentiment=filter_sentiment)


if __name__ == '__main__':
    app.run(port=8050, debug=True)
