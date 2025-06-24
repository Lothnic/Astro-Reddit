from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
import json
import os

default_args = {
    'owner': 'mayank',
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

def fetch_reddit_posts():
    subreddit = "dataengineering"
    url = f"https://www.reddit.com/r/IIITUna/hot.json?limit=5"
    headers = {'User-Agent': 'astro-dag-agent'}
    response = requests.get(url, headers=headers)
    posts = response.json()["data"]["children"]

    output = [{
        "title": post["data"]["title"],
        "score": post["data"]["score"],
        "url": post["data"]["url"]
    } for post in posts]

    local_path = "/usr/local/airflow/include/reddit_data"

    os.makedirs(local_path, exist_ok=True)
    with open(f"{local_path}/top_posts.json", "w") as f:
        json.dump(output, f, indent=4)

with DAG(
    dag_id="reddit_scraper_dag",
    default_args=default_args,
    start_date=datetime(2024, 6, 24),
    schedule="@daily",
    catchup=False
) as dag:

    fetch_posts = PythonOperator(
        task_id="fetch_reddit_posts",
        python_callable=fetch_reddit_posts
    )

    fetch_posts
