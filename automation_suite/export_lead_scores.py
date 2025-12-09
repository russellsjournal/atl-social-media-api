"""
Export businesses and lead scores from the backend API to CSV.
Uses only the Python standard library so no extra dependencies are required.
"""
import os
import json
import csv
from urllib.request import urlopen
from urllib.error import URLError, HTTPError

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")


def fetch_businesses():
    url = API_URL.rstrip("/") + "/businesses"
    try:
        with urlopen(url, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body)
    except HTTPError as e:
        print(f"HTTP error fetching businesses: {e.code} {e.reason}")
    except URLError as e:
        print(f"Network error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return []


def export_csv(businesses, out_path):
    fieldnames = ["id", "name", "neighborhood", "category", "lead_score", "reviews_count", "avg_rating"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for b in businesses:
            writer.writerow({k: b.get(k) for k in fieldnames})
    print(f"Exported {len(businesses)} businesses to {out_path}")


def main():
    businesses = fetch_businesses()
    out_path = os.path.join(os.path.dirname(__file__), "business_lead_scores.csv")
    export_csv(businesses, out_path)


if __name__ == "__main__":
    main()
