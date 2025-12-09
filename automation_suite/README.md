# Automation Suite

This folder contains simple automation scripts to interact with the backend API.

Scripts:
- `seed.py` — reads `sample_data.json` and POSTs businesses to the API.
- `export_lead_scores.py` — fetches all businesses and writes `business_lead_scores.csv`.

Usage:
1. Ensure the backend API is running (default `http://127.0.0.1:8000`).
2. (Optional) Set `API_URL` environment variable to point to a different URL.

Activate your virtual environment then run:

```powershell
cd automation_suite
# Seed sample businesses
py seed.py

# Export lead scores to CSV
py export_lead_scores.py
```

If PowerShell prevents execution, run the scripts directly with `py` as shown above. The scripts use only the Python standard library.
