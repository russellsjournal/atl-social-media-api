"""
Seed sample businesses into the backend API.
Uses only the Python standard library so no extra dependencies are required.
"""
import os
import json
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")

def post_business(biz):
    url = API_URL.rstrip("/") + "/businesses"
    data = json.dumps(biz).encode("utf-8")
    req = Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            print(f"Created: {biz.get('name')} -> {resp.status}")
            return json.loads(body)
    except HTTPError as e:
        print(f"HTTP error creating {biz.get('name')}: {e.code} {e.reason}")
    except URLError as e:
        print(f"Network error creating {biz.get('name')}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    return None


def main():
    this_dir = os.path.dirname(__file__)
    sample_path = os.path.join(this_dir, "sample_data.json")
    with open(sample_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for biz in data:
        post_business(biz)


if __name__ == "__main__":
    main()
