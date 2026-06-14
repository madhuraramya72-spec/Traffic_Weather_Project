import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def clean_row(row):
    cleaned = {}

    for k, v in row.items():
        if pd.isna(v):
            cleaned[k] = None
        elif isinstance(v, (np.integer, np.int64)):
            cleaned[k] = int(v)
        elif isinstance(v, (np.floating, np.float64)):
            cleaned[k] = float(v)
        else:
            cleaned[k] = v

    return cleaned


def load_to_elastic():

    # ✅ FIXED Elasticsearch client
    es = Elasticsearch(
        "http://localhost:9200",
        api_version_compatibility_mode=True
    )

    # 1. Connection check
    if not es.ping():
        raise ConnectionError("Elasticsearch is not running")

    print("✅ Connected to Elasticsearch")

    # 2. Load data
    df = pd.read_csv("data/combined/final_data.csv")

    # 3. SAFE bulk actions (FIXED)
    actions = [
        {
            "_index": "traffic_weather",
            "_id": f"{row['city']}_{i}",
            "_source": clean_row(row)
        }
        for i, row in df.iterrows()
    ]

    # 4. Correct bulk usage
    success, response = bulk(
        es,
        actions,
        raise_on_error=False,
        raise_on_exception=False
    )

    print(f"📦 Indexed documents: {success}")

    # 5. Show errors if any
    for item in response:
        if "error" in item:
            print("❌ Failed item:", item)

    es.close()


if __name__ == "__main__":
    load_to_elastic()