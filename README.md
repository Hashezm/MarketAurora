# MarketAurora
### Project Overview

MarketAurora is a cloud-hosted, end-to-end machine learning solution designed to provide users with daily insights into financial markets and equities. The project automatically gathers and processes financial news articles, analyzes their sentiment using a CNN model, and makes this information accessible through an API and a web interface. Its key features include a sentiment analysis model, automated ETL pipeline, FastAPI service, and a user-friendly interface for querying and filtering market data.

### Screenshots and descriptions:
As we can see below, MarketAurora has a very pleasant layout. In this sample search,"bitcoin" was the query and it returned results based on financial articles from today.
![image](https://github.com/user-attachments/assets/5fdc83eb-325d-4148-8189-a439fba90dca)


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
git clone https://github.com/Hashezm/MarketAurora.git
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
### 6. Connect Amazon Credentials
- Ensure your machine is configured with AWS credentials using the AWS CLI:
```bash
aws configure
```
### 7. Update S3 Bucket in app.py
```python
# app.py
BUCKET_NAME = 'your_s3_bucket_name_here'
```
### 8. Install Dependences
```python
pip install -r requirements.txt
#make sure to install dependencies for each file individually if this doesn't cover the requirements
```
### 9. Containerize FastAPI (Optional)
- If you want to containerize the FastAPI app:
```bash
docker build -t marketaurora-fastapi .
docker run -p 8000:8000 marketaurora-fastapi
```
### 10. Run the ETL Pipeline
- Start the Airflow scheduler and webserver:
```bash
airflow scheduler
airflow webserver
```
- I recommend to monitor the ETL process in the Airflow UI, lots of companies could lead to resource problems.

### additional settings:
-  There is the option to change parameters of airflow runtimes for each task
-  There is the option to change the limiter for the FastAPI API.py to allow more requests.

### FastAPI documentation:
![image](https://github.com/user-attachments/assets/58a8efc4-0341-4018-99fe-7a9c37e10de2)
![image](https://github.com/user-attachments/assets/b7eb0a7b-defb-4c71-ab42-10b3a685cc60)


### Contributing

We welcome contributions to MarketAurora! If you would like to contribute, please follow these guidelines:

- **Submit Issues**: Use the [GitHub Issues](https://github.com/Hashezm/MarketAurora/issues) to report bugs or request features.
- **Pull Requests**: Fork the repository, create a new branch for your feature or bugfix, and submit a pull request. Please ensure your code follows the project’s coding standards.
- **Coding Standards**: Follow PEP 8 for Python code. Include clear and concise comments and documentation for your code.

### License

This project is licensed under the MIT License. For more details, see the [LICENSE](https://github.com/Hashezm/MarketAurora/blob/main/LICENSE) file in the repository.

