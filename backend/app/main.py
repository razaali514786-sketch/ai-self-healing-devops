from datetime import datetime, timezone
from typing import Literal
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="AI-Powered Self-Healing DevOps Platform API",
    version="0.1.0",
    description=(
        "FYP starter API for incident visibility and policy-controlled demo recovery. "
        "Recovery actions are simulated; no real infrastructure is modified."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "null",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# In-memory demo data for the first milestone. A database can be added later.
INCIDENTS = [
    {
        "id": "INC-001",
        "title": "Sample pod health-check failure",
        "severity": "high",
        "status": "open",
        "description": "Demo incident used to test the controlled recovery workflow.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "id": "INC-002",
        "title": "Sample elevated CPU alert",
        "severity": "medium",
        "status": "open",
        "description": "Simulated threshold alert; no real metrics are being collected yet.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
    {
        "id": "INC-003",
        "title": "Sample deployment verification",
        "severity": "low",
        "status": "resolved",
        "description": "Example of a previously resolved demo incident.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    },
]

RECOVERY_HISTORY = []

# Explicit allowlist: requests outside this list are rejected.
APPROVED_ACTIONS = {
    "restart_pod",
    "scale_workload",
    "rollback_deployment",
}


class RecoveryRequest(BaseModel):
    incident_id: str = Field(min_length=1, max_length=40)
    action: Literal["restart_pod", "scale_workload", "rollback_deployment"]


@app.get("/")
def root():
    return {
        "message": "AI-Powered Self-Healing DevOps Platform API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "self-healing-devops-api",
        "environment": "local-development",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/summary")
def summary():
    return {
        "total_incidents": len(INCIDENTS),
        "open_incidents": sum(i["status"] == "open" for i in INCIDENTS),
        "successful_recoveries": sum(r["status"] == "simulated_success" for r in RECOVERY_HISTORY),
        "mode": "safe-simulation",
    }


@app.get("/api/incidents")
def list_incidents():
    return INCIDENTS


@app.get("/api/incidents/{incident_id}")
def get_incident(incident_id: str):
    for incident in INCIDENTS:
        if incident["id"] == incident_id:
            return incident
    raise HTTPException(status_code=404, detail="Incident not found")


@app.get("/api/recovery-history")
def recovery_history():
    return RECOVERY_HISTORY


@app.post("/api/recover")
def recover(request: RecoveryRequest):
    incident = next((i for i in INCIDENTS if i["id"] == request.incident_id), None)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    if incident["status"] != "open":
        raise HTTPException(status_code=409, detail="Only open incidents can be used for a recovery demo")
    if request.action not in APPROVED_ACTIONS:
        raise HTTPException(status_code=403, detail="Action is not approved by recovery policy")

    # IMPORTANT: this starter milestone simulates recovery only.
    # It does not connect to Kubernetes or modify real infrastructure.
    action_labels = {
        "restart_pod": "Pod restart",
        "scale_workload": "Workload scaling",
        "rollback_deployment": "Deployment rollback",
    }
    record = {
        "id": f"REC-{uuid4().hex[:8].upper()}",
        "incident_id": incident["id"],
        "action": request.action,
        "action_label": action_labels[request.action],
        "status": "simulated_success",
        "message": f"{action_labels[request.action]} passed policy validation. Demo recovery was simulated only.",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    RECOVERY_HISTORY.insert(0, record)
    incident["status"] = "resolved"
    return record
