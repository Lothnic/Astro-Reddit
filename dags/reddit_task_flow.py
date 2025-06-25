from airflow.decorators import dag,task
from datetime import datetime,timedelta
import os
import json
import requests

@dag(
    dag_id='reddit_etl_airflow',
    start_date=datetime(2024,6,25),
    schedule='@daily',
    catchup=False,
    tags=['reddit','etl']
)

def reddit_etl():

    @task
    def extract():
        subreddit = 'Btechtards'
        limit = 10
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit + 5}"
        headers = {'User-Agent': 'airflow-reddit-pipeline'}
        response = requests.get(url, headers=headers)
        posts = response.json()['data']['children']
        filtered_posts = [p for p in posts if not p["data"].get("stickied", False)]
        return filtered_posts[:limit]
    
    @task
    def transform(posts):
        return [
            {
                "title": post["data"]["title"],
                "score": post["data"]["score"],
                "url": post["data"]["url"],
                "body":post['data']['selftext']
            }
            for post in posts
        ]
    
    @task
    def load(cleaned_posts):
        output_dir = "/usr/local/airflow/include/reddit_data"
        os.makedirs(output_dir, exist_ok=True)
        path = os.path.join(output_dir, f"processed_posts_{datetime.now().date()}.json")

        with open(path, "w") as f:
            json.dump(cleaned_posts, f, indent=4)

        print(f"Saved {len(cleaned_posts)} posts to {path}")

    # Flow of our DAG
    raw_data = extract()
    cleaned = transform(raw_data)
    load(cleaned)
        
# Instantiate the DAG
reddit_etl_dag = reddit_etl()