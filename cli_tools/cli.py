"""
CLI for managing businesses via the backend API.
Usage examples:
  py cli_tools\cli.py list
  py cli_tools\cli.py get 1
  py cli_tools\cli.py create --file sample.json
  py cli_tools\cli.py update 1 --file update.json
  py cli_tools\cli.py delete 1
  py cli_tools\cli.py export --out businesses.csv
"""
import os
import sys
import json
import argparse
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

API_URL = os.environ.get("API_URL", "http://127.0.0.1:8000")


def request_json(method, path, payload=None):
    url = API_URL.rstrip("/") + path
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = Request(url, data=data, headers=headers, method=method)
    try:
        with urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            if body:
                return json.loads(body)
            return None
    except HTTPError as e:
        print(f"HTTP error {e.code}: {e.reason}")
        try:
            err = e.read().decode()
            print(err)
        except Exception:
            pass
        return None
    except URLError as e:
        print(f"Network error: {e}")
        return None


def cmd_list(args):
    qs = []
    if args.neighborhood:
        qs.append(f"neighborhood={args.neighborhood}")
    if args.category:
        qs.append(f"category={args.category}")
    if args.min_lead_score is not None:
        qs.append(f"min_lead_score={args.min_lead_score}")
    path = "/businesses"
    if qs:
        path += "?" + "&".join(qs)
    res = request_json("GET", path)
    if res is None:
        print("No businesses returned or an error occurred.")
        return
    print(json.dumps(res, indent=2))


def load_payload_from_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def cmd_get(args):
    res = request_json("GET", f"/businesses/{args.id}")
    if res is None:
        print("Not found or error.")
        return
    print(json.dumps(res, indent=2))


def cmd_create(args):
    if args.file:
        payload = load_payload_from_file(args.file)
    elif args.json:
        payload = json.loads(args.json)
    else:
        print("Provide --file or --json payload for create")
        return
    res = request_json("POST", "/businesses", payload)
    if res:
        print("Created:")
        print(json.dumps(res, indent=2))


def cmd_update(args):
    if args.file:
        payload = load_payload_from_file(args.file)
    elif args.json:
        payload = json.loads(args.json)
    else:
        print("Provide --file or --json payload for update")
        return
    res = request_json("PUT", f"/businesses/{args.id}", payload)
    if res:
        print("Updated:")
        print(json.dumps(res, indent=2))


def cmd_delete(args):
    res = request_json("DELETE", f"/businesses/{args.id}")
    if res is not None:
        print("Deleted")


def cmd_export(args):
    # reuse automation export script logic: fetch and write CSV
    businesses = request_json("GET", "/businesses") or []
    out_path = args.out or os.path.join(os.getcwd(), "business_lead_scores.csv")
    import csv
    fieldnames = ["id", "name", "neighborhood", "category", "lead_score", "reviews_count", "avg_rating"]
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for b in businesses:
            writer.writerow({k: b.get(k) for k in fieldnames})
    print(f"Exported {len(businesses)} businesses to {out_path}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="business-cli", description="Manage businesses via backend API")
    sub = parser.add_subparsers(dest="cmd")

    p_list = sub.add_parser("list", help="List businesses")
    p_list.add_argument("--neighborhood")
    p_list.add_argument("--category")
    p_list.add_argument("--min-lead-score", dest="min_lead_score", type=float)
    p_list.set_defaults(func=cmd_list)

    p_get = sub.add_parser("get", help="Get a business by id")
    p_get.add_argument("id", type=int)
    p_get.set_defaults(func=cmd_get)

    p_create = sub.add_parser("create", help="Create a business from JSON file or string")
    p_create.add_argument("--file", help="Path to JSON file with business payload")
    p_create.add_argument("--json", help="JSON string payload")
    p_create.set_defaults(func=cmd_create)

    p_update = sub.add_parser("update", help="Update a business by id with JSON payload")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--file", help="Path to JSON file with update payload")
    p_update.add_argument("--json", help="JSON string payload")
    p_update.set_defaults(func=cmd_update)

    p_delete = sub.add_parser("delete", help="Delete a business by id")
    p_delete.add_argument("id", type=int)
    p_delete.set_defaults(func=cmd_delete)

    p_export = sub.add_parser("export", help="Export businesses to CSV")
    p_export.add_argument("--out", help="Output CSV path")
    p_export.set_defaults(func=cmd_export)

    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    args.func(args)
    return 0


if __name__ == "__main__":
    sys.exit(main())
