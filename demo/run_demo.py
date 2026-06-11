"""
Project demo script: exercises the FastAPI app in-process using TestClient.
No running uvicorn server required. This uses FastAPI's TestClient to make
requests against the `backend_api.main:app` object and demonstrates
create/list/get/update/delete and exporting lead scores to CSV.
"""
import csv
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from fastapi.testclient import TestClient

from backend_api.database import db
from backend_api.main import app

client = TestClient(app)


def reset_db():
    db._businesses.clear()
    db._next_id = 1


SAMPLE = [
    {
        "name": "Demo Coffee",
        "neighborhood": "DemoTown",
        "category": "Cafe",
        "website": "http://democoffee.local",
        "google_maps_url": None,
        "has_instagram": True,
        "has_facebook": False,
        "reviews_count": 34,
        "avg_rating": 4.6,
    },
    {
        "name": "Demo Books",
        "neighborhood": "DemoTown",
        "category": "Bookstore",
        "website": None,
        "google_maps_url": None,
        "has_instagram": False,
        "has_facebook": True,
        "reviews_count": 8,
        "avg_rating": 4.1,
    },
]


def create_demo_data():
    created = []
    for item in SAMPLE:
        response = client.post("/businesses", json=item)
        assert response.status_code == 200, f"create failed: {response.status_code} {response.text}"
        created.append(response.json())
    return created


def list_businesses():
    response = client.get("/businesses")
    assert response.status_code == 200
    return response.json()


def get_business(business_id):
    response = client.get(f"/businesses/{business_id}")
    return response.status_code, response.json() if response.status_code == 200 else None


def update_business(business_id, payload):
    response = client.put(f"/businesses/{business_id}", json=payload)
    return response.status_code, response.json() if response.status_code == 200 else None


def delete_business(business_id):
    response = client.delete(f"/businesses/{business_id}")
    return response.status_code, response.json()


def export_csv(path="demo_businesses.csv"):
    businesses = list_businesses()
    fieldnames = ["id", "name", "neighborhood", "category", "lead_score", "reviews_count", "avg_rating"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for business in businesses:
            writer.writerow({key: business.get(key) for key in fieldnames})
    return path


if __name__ == "__main__":
    print("Resetting demo database...")
    reset_db()
    print("Creating demo data...")
    created = create_demo_data()
    print("Created:")
    for business in created:
        print(f" - {business['id']}: {business['name']} (lead_score={business.get('lead_score')})")

    print("\nListing businesses:")
    for business in list_businesses():
        print(f" - {business['id']}: {business['name']} (lead_score={business['lead_score']})")

    first_id = created[0]["id"]
    print(f"\nGet business {first_id}:")
    status, business = get_business(first_id)
    print(status, business)

    print("\nUpdating first business name...")
    status, updated = update_business(first_id, {"name": "Demo Coffee Updated"})
    print(status, updated)

    print("\nExporting to CSV...")
    out = export_csv()
    print(f"Exported to: {out}")

    print("\nDeleting second business...")
    status, deleted = delete_business(created[1]["id"])
    print(status, deleted)

    print("\nFinal list:")
    for business in list_businesses():
        print(f" - {business['id']}: {business['name']} (lead_score={business['lead_score']})")

    print("\nDemo complete.")
