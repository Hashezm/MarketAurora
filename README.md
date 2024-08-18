﻿# MarketAurora

# MarketAurora Setup Guide

Welcome to the MarketAurora project! This guide will help you set up and run the project on your machine.

## Prerequisites

Before you begin, make sure you have the following:

- Python 3.8 or higher installed on your machine.
- An AWS account with access to S3.
- An API key from [NewsAPI](https://newsapi.org/).
- Docker installed (optional, for containerizing the FastAPI application).

## Setup Instructions

### 1. Clone the Repository

Clone the MarketAurora repository to your local machine:

```bash
git clone https://github.com/yourusername/marketaurora.git
cd marketaurora
```
### 2. Get Your NewsAPI Key
- Sign up at NewsAPI and get your API key.
- Open the config.py file located in the root of the project and add your API key:
```python
# config.py
NEWSAPI_KEY = 'your_newsapi_key_here'
```
### 3. Host Your FastAPI API
- Open the app.py file in the pythonProject2 directory.
- Set up your FastAPI by hosting it locally or on a cloud service.
- After hosting, update the API URL in the app.py:
```python
# app.py
API_URL = 'http://your-hosted-api-url.com'
```
### 4. Create an Amazon S3 Bucket
- Log in to AWS and create a new S3 bucket. Note the bucket name as it will be used in subsequent steps.

### 5. Configure ETL Pipeline
- Open etl-dag.py:
-   Add your NewsAPI key:
```python
# etl-dag.py
NEWSAPI_KEY = 'your_newsapi_key_here'
```
-   Add companies to refresh daily:
```python
# etl-dag.py
COMPANIES = ['apple', 'microsoft', 'amazon']  # Add the companies you're interested in
```
-   Update the S3 bucket name:
```python
# etl-dag.py
BUCKET_NAME = 'your_s3_bucket_name_here'
```
### 6. 
