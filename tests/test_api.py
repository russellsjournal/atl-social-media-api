from fastapi.testclient import TestClient

from backend_api.database import db
from backend_api.main import app


client = TestClient(app)


def setup_function():
    db._businesses.clear()
    db._next_id = 1


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_crud_business_lifecycle_and_filters():
    payload1 = {
        "name": "Test Biz 1",
        "neighborhood": "North",
        "category": "Cafe",
        "website": "http://example.com/1",
        "google_maps_url": None,
        "has_instagram": True,
        "has_facebook": False,
        "reviews_count": 10,
        "avg_rating": 4.0,
    }

    response = client.post("/businesses", json=payload1)
    assert response.status_code == 200
    created1 = response.json()
    assert created1["name"] == payload1["name"]
    assert "id" in created1
    assert "lead_score" in created1

    payload2 = {
        "name": "Test Biz 2",
        "neighborhood": "South",
        "category": "Bookstore",
        "website": None,
        "google_maps_url": None,
        "has_instagram": False,
        "has_facebook": True,
        "reviews_count": 2,
        "avg_rating": 3.5,
    }
    response = client.post("/businesses", json=payload2)
    assert response.status_code == 200
    created2 = response.json()

    response = client.get("/businesses")
    assert response.status_code == 200
    all_biz = response.json()
    assert isinstance(all_biz, list)
    assert len(all_biz) == 2

    response = client.get("/businesses?neighborhood=North")
    assert response.status_code == 200
    assert all((b.get("neighborhood") == "North" for b in response.json()))

    response = client.get("/businesses?category=Bookstore")
    assert response.status_code == 200
    assert all((b.get("category") == "Bookstore" for b in response.json()))

    response = client.get(f"/businesses/{created1['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created1["id"]

    response = client.put(f"/businesses/{created1['id']}", json={"name": "Updated Name"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"

    response = client.delete(f"/businesses/{created2['id']}")
    assert response.status_code == 200
    assert response.json() == {"deleted": True}

    response = client.get(f"/businesses/{created2['id']}")
    assert response.status_code == 404
