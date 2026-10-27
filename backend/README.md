# NivaranX backend

## Local setup

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate  # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API health: http://127.0.0.1:8000/api/health
Interactive API docs: http://127.0.0.1:8000/docs

The current backend uses synthetic in-memory data for demonstration. Status edits are not persistent and reset on restart. Authentication and a persistent database are not implemented yet, so do not deploy this starter as a production service.
