# Astro-Reddit ETL Pipeline

This project implements an ETL (Extract, Transform, Load) pipeline for Reddit data using Apache Airflow. The pipeline extracts posts from specified subreddits, processes the data, and stores it for analysis.

## What is ETL?

ETL stands for Extract, Transform, Load:
- **Extract**: Pull data from Reddit's API
- **Transform**: Process and structure the data as needed
- **Load**: Store the processed data in a structured format(currently local)

## Features
- Extracts top posts from specified subreddits
- Processes post data (titles, scores, URLs)
- Saves data in JSON format with timestamps
- Scheduled runs using Airflow

## Setup
1. Using Astro CLI
2. To start the Airflow instance run `astro dev start`
3. To stop the Airflow instance run `astro dev stop`

## Project Structure
- `dags/`: Contains Airflow DAG definitions
- `include/reddit_data/`: Stores the extracted JSON data

## Note
Make sure to respect Reddit's API rate limits and terms of service when using this project.