import sys
import os

PROJECT_PATH = "/Users/ramya/Desktop/traffic_weather_project"
sys.path.append(PROJECT_PATH)

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

# FIXED: Explicit directory path imports
from scripts.fetch_weather import fetch_weather
from scripts.fetch_weather import fetch_weather
from scripts.fetch_traffic import fetch_traffic
from scripts.transform_data import transform_data
from scripts.load_to_elastic import load_to_elastic

with DAG(
    dag_id="traffic_weather_pipeline",
    start_date=datetime(2025, 1, 1),
    schedule="@hourly",
    catchup=False
) as dag:

    weather_task = PythonOperator(
        task_id="fetch_weather",
        python_callable=fetch_weather
    )

    traffic_task = PythonOperator(
        task_id="fetch_traffic",
        python_callable=fetch_traffic
    )

    transform_task = PythonOperator(
        task_id="transform_data",
        python_callable=transform_data,
        do_xcom_push=False,  # Stops the DataFrame serialization error
    )

    elastic_task = PythonOperator(
        task_id="load_elastic",
        python_callable=load_to_elastic
    )

    [weather_task, traffic_task] >> transform_task >> elastic_task