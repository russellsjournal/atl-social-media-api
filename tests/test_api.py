import os
import json
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
import pytest

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000").rstrip("/")


def _ping():
    try:
        with urlopen(API_URL + "/health", timeout=2) as r:
            return r.status == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(not _ping(), reason=f"API not running at {API_URL}")


def _request(method: str, path: str, payload=None):
    url = API_URL + path
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            try:
                parsed = json.loads(body) if body else None
            except Exception:
                parsed = body
            return resp.status, parsed
    except HTTPError as e:
        try:
            body = e.read().decode()
            parsed = json.loads(body)
        except Exception:
            parsed = None
        return e.code, parsed
    except URLError as e:
        pytest.skip(f"Network error communicating with API: {e}")


def setup_function():
    # try to clean existing businesses by listing and deleting
    status, body = _request("GET", "/businesses")
    if status == 200 and isinstance(body, list):
        for b in body:
            _request("DELETE", f"/businesses/{b.get('id')}")


def test_health():
    status, body = _request("GET", "/health")
    assert status == 200
    assert body == {"status": "ok"}


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

    status, created1 = _request("POST", "/businesses", payload1)
    assert status == 200
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
    status, created2 = _request("POST", "/businesses", payload2)
    assert status == 200

    status, all_biz = _request("GET", "/businesses")
    assert status == 200
    assert isinstance(all_biz, list)
    assert len(all_biz) >= 2

    status, filtered = _request("GET", "/businesses?neighborhood=North")
    assert status == 200
    assert all((b.get("neighborhood") == "North" for b in filtered))

    status, filtered_cat = _request("GET", "/businesses?category=Bookstore")
    assert status == 200
    assert all((b.get("category") == "Bookstore" for b in filtered_cat))

    status, got = _request("GET", f"/businesses/{created1['id']}")
    assert status == 200
    assert got["id"] == created1["id"]

    status, updated = _request("PUT", f"/businesses/{created1['id']}", {"name": "Updated Name"})
    assert status == 200
    assert updated["name"] == "Updated Name"

    status, deleted = _request("DELETE", f"/businesses/{created2['id']}")
    assert status == 200
    assert deleted == {"deleted": True}

    status, _ = _request("GET", f"/businesses/{created2['id']}")
    assert status == 404
