import glob
import json
import os
import random
import pandas as pd

def transform_data():
    # 1. Get files and sort them strictly by modification time (oldest to newest)
    weather_files = sorted(glob.glob("data/raw/weather/*.json"), key=os.path.getmtime)
    traffic_files = sorted(glob.glob("data/raw/traffic/*.json"), key=os.path.getmtime)

    # Safety check: ensure files actually exist
    if not weather_files or not traffic_files:
        raise FileNotFoundError("No raw weather or traffic data files found to transform!")

    # Now [-1] is guaranteed to be the most recently created file
    latest_weather = weather_files[-1]
    latest_traffic = traffic_files[-1]

    with open(latest_weather) as file_handle:
        weather = json.load(file_handle)

    with open(latest_traffic) as file_handle:
        traffic = json.load(file_handle)

    cities = ["Paris", "London", "Berlin", "Madrid"]
    rows = []

    for city in cities:
        try:
            combined = {
                "city": city,
                # Using .get() fallback methods prevents unexpected KeyErrors from crashing the DAG
                "temperature": weather.get("main", {}).get("temp", 15) + random.uniform(-5, 5),
                "humidity": weather.get("main", {}).get("humidity", 50) + random.randint(-10, 10),
                "traffic_speed": traffic.get("flowSegmentData", {}).get("currentSpeed", 40) + random.randint(-3, 3),
                "free_flow_speed": traffic.get("flowSegmentData", {}).get("freeFlowSpeed", 50),
                "timestamp": pd.Timestamp.now().isoformat() # Crucial for Elasticsearch indexing!
            }
            rows.append(combined)
        except KeyError as e:
            print(f"Skipping processing layout due to missing key: {e}")

    # Ensure output directory exists before saving
    os.makedirs("data/combined", exist_ok=True)
    
    df = pd.DataFrame(rows)
    df.to_csv("data/combined/final_data.csv", index=False)
    print("Transformation successful. Current DataFrame:")
    print(df)

if __name__ == "__main__":
    transform_data()