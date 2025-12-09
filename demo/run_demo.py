"""
Project demo script: exercises the FastAPI app in-process using TestClient.
No running uvicorn server required — this uses FastAPI's TestClient to make requests
against the `backend_api.main:app` object and demonstrates create/list/get/update/delete
and exporting lead scores to CSV.
"""
import csv
from fastapi.testclient import TestClient
from backend_api.main import app
from backend_api.database import db

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
        r = client.post("/businesses", json=item)
        assert r.status_code == 200, f"create failed: {r.status_code} {r.text}"
        created.append(r.json())
    return created


def list_businesses():
    r = client.get("/businesses")
    assert r.status_code == 200
    return r.json()


def get_business(bid):
    r = client.get(f"/businesses/{bid}")
    return r.status_code, r.json() if r.status_code == 200 else None


def update_business(bid, payload):
    r = client.put(f"/businesses/{bid}", json=payload)
    return r.status_code, r.json() if r.status_code == 200 else None


def delete_business(bid):
    r = client.delete(f"/businesses/{bid}")
    return r.status_code, r.json()


def export_csv(path="demo_businesses.csv"):
    businesses = list_businesses()
    fieldnames = ["id", "name", "neighborhood", "category", "lead_score", "reviews_count", "avg_rating"]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for b in businesses:
            writer.writerow({k: b.get(k) for k in fieldnames})
    return path


if __name__ == "__main__":
    print("Resetting demo database...")
    reset_db()
    print("Creating demo data...")
    created = create_demo_data()
    print("Created:")
    for c in created:
        print(f" - {c['id']}: {c['name']} (lead_score={c.get('lead_score')})")

    print("\nListing businesses:")
    for b in list_businesses():
        print(f" - {b['id']}: {b['name']} (lead_score={b['lead_score']})")

    first_id = created[0]["id"]
    print(f"\nGet business {first_id}:")
    status, biz = get_business(first_id)
    print(status, biz)

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
    for b in list_businesses():
        print(f" - {b['id']}: {b['name']} (lead_score={b['lead_score']})")

    print("\nDemo complete.")
