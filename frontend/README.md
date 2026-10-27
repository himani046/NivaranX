# NivaranX frontend

## Local setup

```bash
cd frontend
npm install
npm run dev
```

Open the URL printed by Vite, normally http://localhost:5173.

The UI uses synthetic demo records served by the FastAPI backend. Start the backend separately; see `../backend/README.md`. Set `VITE_API_URL` in a local `.env` file if the API uses a different origin.
