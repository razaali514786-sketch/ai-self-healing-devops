# AI-Powered Self-Healing DevOps Platform

FYP starter implementation based on the submitted proposal.

## Current milestone
- Dashboard frontend using HTML, CSS, and JavaScript
- Python FastAPI backend
- Sample incident list and summary
- Explicit allowlist for recovery actions
- Simulated recovery history

**Safety note:** Recovery is simulated. This milestone does not connect to Kubernetes, restart real pods, scale workloads, or roll back deployments. AI/LLM, persistent database, monitoring, CI/CD, Terraform, Helm, and AWS deployment are later milestones.

## Run backend on Windows (Git Bash / VS Code terminal)

```bash
cd backend
python -m venv .venv
source .venv/Scripts/activate
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

If `source .venv/Scripts/activate` does not work in PowerShell, use:
```powershell
.venv\Scripts\Activate.ps1
```

API docs: http://127.0.0.1:8000/docs

## Run frontend
Open `frontend/index.html` with VS Code Live Server. The frontend expects the backend at `http://127.0.0.1:8000`.

If using a different frontend port, add that exact local origin to `allow_origins` in `backend/app/main.py`.

## Current demo endpoints
- `GET /health`
- `GET /api/summary`
- `GET /api/incidents`
- `GET /api/incidents/{incident_id}`
- `GET /api/recovery-history`
- `POST /api/recover`

Do not expose this development server publicly. Before cloud deployment, add authentication, persistent storage, production CORS settings, TLS, least-privilege credentials, and audit controls.
