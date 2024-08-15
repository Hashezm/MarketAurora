from flask import Flask, render_template, request
import requests
from collections import Counter

app = Flask(__name__)

# FastAPI endpoint URL (replace with your actual FastAPI endpoint)
FASTAPI_URL = 'http://127.0.0.1:5000/analyze/'

@app.route('/', methods=['GET', 'POST'])
def home():
    articles = []
    sentiments = []
    filter_sentiment = request.args.get('filter')  # Get the sentiment filter from URL parameters
    if request.method == 'POST':
        topic = request.form.get('topic')
        response = requests.get(FASTAPI_URL, params={'topic': topic})

        if response.status_code == 200:
            articles = response.json().get('articles', [])

        for article in articles:
            sentiments.append(article['sentiment'])

    counts = Counter(sentiments) # count sentiments
    # print(counts['negative'])
    # print(counts['neutral'])
    # print(counts['positive'])
    if filter_sentiment:
        articles = [article for article in articles if article['sentiment'] == filter_sentiment]

    return render_template('home2.html', articles=articles, counts=counts, filter_sentiment=filter_sentiment)

if __name__ == '__main__':
    app.run(port=8050, debug=True)
