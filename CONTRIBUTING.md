# Contributing

Thanks for considering contributing! This document explains how to get the project running locally and how to run tests.

Getting started
1. Create and activate the virtual environment (Windows PowerShell):

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

2. Start the API for manual testing:

```powershell
py -m uvicorn backend_api.main:app --reload
```

Running tests
- Unit tests that don't require a running server:

```powershell
python -m pytest tests/test_lead_scoring.py -q
```

- API tests and integration tests expect a running API. Two modes are supported:
  - In-process (demo / TestClient) — see `demo/run_demo.py` for an example.
  - Integration tests spawn a temporary uvicorn process on port `8001` (see `tests/test_integration.py`). Run them with:

```powershell
python -m pytest tests/test_integration.py -q
```

Code style & PRs
- Keep changes small and focused.
- Add or update tests for new behavior.
- Describe your change clearly in the PR title and description.

Reporting bugs
- Open an issue with reproduction steps and any relevant logs.

Local development tips
- Use the sample data in `automation_suite/sample_data.json` to seed the app quickly.
- The in-memory DB is simple and resets with process restarts — useful for fast iteration.
