#!/bin/zsh
set -euo pipefail

cd /Users/ramya/Desktop/traffic_weather_project
source venv/bin/activate
export PYTHONPATH="$PWD"
export AIRFLOW__CORE__DAGS_FOLDER="$PWD/dags"
export AIRFLOW__CORE__LOAD_EXAMPLES=False

airflow scheduler