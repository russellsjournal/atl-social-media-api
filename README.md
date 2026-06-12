# Atlanta Business Directory

Lightweight FastAPI service, web directory, and tools for collecting and scoring local business leads.

Contents
- `backend_api/` - FastAPI app, in-memory DB, lead scoring logic
- `static/` - browser-facing directory page served by FastAPI
- `automation_suite/` - scripts to seed sample data and export lead scores
- `cli_tools/` - small CLI to manage businesses via the API
- `demo/` - in-process demo that exercises the API using TestClient
- `tests/` - unit and integration tests (pytest)

Quick start
1. Create and activate a virtual environment (Windows PowerShell):

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Run the API with uvicorn (from repository root):

```powershell
py -m uvicorn backend_api.main:app --reload
```

3. Open the local web directory:

```text
http://127.0.0.1:8000
```

API docs are available at:

```text
http://127.0.0.1:8000/docs
```

4. Use the CLI or automation scripts:

```powershell
# Seed sample data
py automation_suite\seed.py

# List businesses via the CLI
py cli_tools\cli.py list

# Run demo (in-process)
py demo\run_demo.py
```

Testing
- Unit tests and integration tests use `pytest`.
- To run tests:

```powershell
python -m pip install pytest
python -m pytest -q
```

Deployment
- This repo includes `render.yaml` for Render.
- Create a new Render Blueprint from the GitHub repo, or create a Python web service manually.
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn backend_api.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

Notes
- The backend uses an in-memory DB (`backend_api.database.InMemoryDB`) for simplicity. Data is not persisted between runs.
- Startup demo data is loaded so the public web page has sample businesses immediately after deploy.
- If PowerShell blocks script execution, use `py` to run scripts or adjust `Set-ExecutionPolicy` for your user.
