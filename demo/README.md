# Project Demo

This demo runs the backend API in-process (no uvicorn required) and demonstrates the main flows:

- Create demo businesses
- List businesses
- Get, update, and delete operations
- Export businesses and lead scores to CSV

Run the demo (from project root) after activating your virtual environment:

```powershell
# Activate venv
.\venv\Scripts\Activate.ps1

# Run demo
py demo\run_demo.py
```

The demo uses `TestClient` from FastAPI and will exercise `backend_api.main:app` directly. It writes `demo_businesses.csv` to the repository root of the demo when exporting.
