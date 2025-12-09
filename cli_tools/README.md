# CLI Tools

Simple CLI for managing businesses via the backend API.

Usage examples (from project root):

```powershell
# List businesses
py cli_tools\cli.py list

# Filtered list
py cli_tools\cli.py list --neighborhood Midtown --min-lead-score 30

# Get a business
py cli_tools\cli.py get 1

# Create from file
py cli_tools\cli.py create --file automation_suite\sample_data.json

# Create from JSON string
py cli_tools\cli.py create --json '{"name": "Test", "neighborhood": "X"}'

# Update
py cli_tools\cli.py update 1 --file update.json

# Delete
py cli_tools\cli.py delete 1

# Export to CSV
py cli_tools\cli.py export --out my_businesses.csv
```

If your API is not running at `http://127.0.0.1:8000`, set `API_URL` environment variable.
