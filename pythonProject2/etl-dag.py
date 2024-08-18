from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import boto3
import json
import requests

# initialize the s3 client
s3 = boto3.client('s3')
BUCKET_NAME = 'put-your-bucket-here-dear-user'

# url for our fastapi service
FASTAPI_URL = 'fast-api-url'

# list of companies we'll process every day
COMPANIES = ['apple']

# convert a search query into a filename/key for s3
def query_to_key(query):
    return f"{query}.json"

# clear out all the existing files in the s3 bucket
def clear_s3_bucket():
    objects_to_delete = s3.list_objects_v2(Bucket=BUCKET_NAME).get('Contents', [])
    if objects_to_delete:
        delete_keys = {'Objects': [{'Key': obj['Key']} for obj in objects_to_delete]}
        s3.delete_objects(Bucket=BUCKET_NAME, Delete=delete_keys)

# run the etl process: fetch articles for each company and save them to s3
def etl_and_save_to_s3():
    for company in COMPANIES:
        try:
            # send a request to our fastapi endpoint with the company's name as the topic
            response = requests.get(FASTAPI_URL, params={'topic': company}, timeout=10)
            response.raise_for_status()
            articles = response.json().get('articles', [])
            key = query_to_key(company)
            # save the processed articles to s3 under the appropriate key
            s3.put_object(Bucket=BUCKET_NAME, Key=key, Body=json.dumps(articles))
        except requests.exceptions.RequestException as e:
            # handle the exception (e.g., log the error, skip this company, etc.)
            print(f"request failed for {company}: {e}")

# set some default arguments for the dag, like who owns it, start date, and retry settings
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=1),
}

# define our dag, which will run once a day
dag = DAG(
    'daily_market_data_etl',
    default_args=default_args,
    description='a pipeline that fetches market data and stores it in s3',
    schedule_interval='@daily',
)

# task to clear the s3 bucket
clear_bucket_task = PythonOperator(
    task_id='clear_s3_bucket',
    python_callable=clear_s3_bucket,
    dag=dag,
    execution_timeout=timedelta(hours=1)  # allow up to 1 hour for this task
)

# task to run the etl process and save data to s3
etl_task = PythonOperator(
    task_id='etl_and_save_to_s3',
    python_callable=etl_and_save_to_s3,
    dag=dag,
    execution_timeout=timedelta(hours=2)  # allow up to 2 hours for this task
)

# set up the order: clear the bucket first, then run the etl process
clear_bucket_task >> etl_task
