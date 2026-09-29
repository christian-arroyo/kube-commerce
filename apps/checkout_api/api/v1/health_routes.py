"""This module contains the health routes API"""

from fastapi import APIRouter, HTTPException

from apps.checkout_api.db.schema import SessionLocal

from sqlalchemy import select

router = APIRouter()
# Kubernetes liveness check
@router.get("/healthz")
def get_health():
    return {"status:" "ok"}


# Kubernetes readiness check
@router.get("/ready")
def get_ready():
    session = SessionLocal()
    try:
        session.execute(select(1))
    except:
        raise HTTPException(status_code=505, detail="database is unavailable")
