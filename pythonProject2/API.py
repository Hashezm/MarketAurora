from fastapi import FastAPI
from fastapi import Request

import tensorflow as tf
from tensorflow.keras.layers import TextVectorization
from newsapi import NewsApiClient
from datetime import datetime, timedelta
from config import getAPI
import re
from nltk.corpus import stopwords
from slowapi import Limiter
from slowapi.util import get_remote_address

model = tf.keras.models.load_model('model-best')  # load best model trained in the jupyter notebook

app = FastAPI()  # initialize FastAPI application

print(model.summary())


def preprocess(text):
    text = text.lower()

    # remove punctuations and numbers
    text = re.sub('[^a-zA-Z]', ' ', text)

    text = re.sub(r"\s+[a-zA-Z]\s+", ' ', text)  # when we remove apostrophe, is it replaced by a white space

    # remove all single characters and replace it by a space
    text = re.sub(r'\s+', ' ', text)

    # remove stopwords
    stop_words = stopwords.words('english')
    pattern = re.compile(r'\b(' + r'|'.join(stop_words) + r')\b\s*')

    text = pattern.sub('', text)
    return text


def processArticles(articles):
    processed_list = []
    for article in articles['articles']:
        # Get title, description, and URL
        title = article.get('title', '')
        description = article.get('description', '')
        url = article.get('url', '')

        # Further make sure title and description are strings
        if not isinstance(title, str):
            title = ''
        if not isinstance(description, str):
            description = ''

        # Preprocess title and description
        title_and_description = preprocess(title + ' ' + description)

        # Append the processed data as a dictionary
        processed_list.append({
            "title": title,
            "description": description,
            "url": url,
            "content": title_and_description
        })

    return processed_list


def getArticles(input):
    # Initialize the client with your API key
    api_key = getAPI()
    newsapi = NewsApiClient(api_key=api_key)

    # Get today's date in the format YYYY-MM-DD
    yesterday = (datetime.today() - timedelta(10)).strftime('%Y-%m-%d')
    today = datetime.today().strftime('%Y-%m-%d')

    # Fetch articles related to the input query
    articles = newsapi.get_everything(
        q=input,
        from_param=yesterday,
        to=today,
        language='en',
        sort_by='relevancy'
    )

    return processArticles(articles)


def run_model(inp):
    # Get the list of processed articles
    articles = getArticles(inp)

    if not articles:
        return {"message": "Empty! No recent news available here."}

    # Initialize the output dictionary
    output = {"articles": []}

    # Sentiment labels corresponding to the model's output classes
    sentiment_labels = ["Negative", "Neutral", "Positive"]

    # Predict sentiment for each article
    for article in articles:
        title = article["title"]
        description = article["description"]
        url = article["url"]
        content = article["content"]

        # Predict sentiment using the model
        predictions = model.predict([content])

        # Get the predicted class
        predicted_class = tf.argmax(predictions, axis=1).numpy()[0]

        # Map the predicted class to the corresponding sentiment label
        predicted_sentiment = sentiment_labels[predicted_class]

        # Add the article information to the output list
        output["articles"].append({
            "title": title,
            "description": description,
            "url": url,
            "sentiment": predicted_sentiment.lower()  # Use lowercase for consistency with JSON standards
        })

    return output


limiter = Limiter(key_func=get_remote_address) # limiter based on user ip


@app.get("/analyze/")
@limiter.limit("5/minute")  # use limiter to allow each ip 5 per minute
async def analyze_topic(request: Request, topic: str):
    # run with the provided topic
    result = run_model(topic)
    return result
