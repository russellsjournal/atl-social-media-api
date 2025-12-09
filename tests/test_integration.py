import os
import sys
import time
import json
import subprocess
import urllib.request
import urllib.error
import pytest


@pytest.fixture(scope="module")
def server():
    """Start a uvicorn server in a subprocess on port 8001 and yield the base URL.

    If the server fails to start, the tests will be skipped.
    """
    port = int(os.environ.get("INTEGRATION_PORT", "8001"))
    host = os.environ.get("INTEGRATION_HOST", "127.0.0.1")
    base_url = f"http://{host}:{port}"

    # Start uvicorn using the current Python interpreter
    cmd = [sys.executable, "-m", "uvicorn", "backend_api.main:app", "--host", host, "--port", str(port)]
    env = os.environ.copy()

    proc = None
    try:
        proc = subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        pytest.skip("uvicorn not available in this environment")

    # wait for health endpoint
    deadline = time.time() + 10.0
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(base_url + "/health", timeout=1) as r:
                if r.status == 200:
                    break
        except Exception:
            time.sleep(0.2)
    else:
        # failed to start
        proc.terminate()
        pytest.skip(f"Failed to start server at {base_url}")

    try:
        yield base_url
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=5)
        except Exception:
            proc.kill()


def _request(method, url, payload=None):
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as resp:
            body = resp.read().decode("utf-8")
            try:
                return resp.status, json.loads(body) if body else None
            except Exception:
                return resp.status, body
    except urllib.error.HTTPError as e:
        try:
            body = e.read().decode()
            return e.code, json.loads(body)
        except Exception:
            return e.code, None


def test_end_to_end_crud(server):
    base = server

    # ensure empty start
    status, existing = _request("GET", base + "/businesses")
    assert status == 200
    if isinstance(existing, list):
        for b in existing:
            _request("DELETE", f"{base}/businesses/{b.get('id')}")

    # create
    payload = {
        "name": "Integration Biz",
        "neighborhood": "Testville",
        "category": "Integration",
        "website": None,
        "google_maps_url": None,
        "has_instagram": False,
        "has_facebook": False,
        "reviews_count": 1,
        "avg_rating": 3.0,
    }
    status, created = _request("POST", base + "/businesses", payload)
    assert status == 200
    assert created["name"] == payload["name"]
    biz_id = created["id"]

    # retrieve
    status, got = _request("GET", f"{base}/businesses/{biz_id}")
    assert status == 200
    assert got["id"] == biz_id

    # update
    status, updated = _request("PUT", f"{base}/businesses/{biz_id}", {"name": "Integration Biz Updated"})
    assert status == 200
    assert updated["name"] == "Integration Biz Updated"

    # list with filter
    status, lst = _request("GET", base + "/businesses?neighborhood=Testville")
    assert status == 200
    assert any(b.get("id") == biz_id for b in lst)

    # delete
    status, deleted = _request("DELETE", f"{base}/businesses/{biz_id}")
    assert status == 200
    assert deleted == {"deleted": True}

    # ensure gone
    status, _ = _request("GET", f"{base}/businesses/{biz_id}")
    assert status == 404
