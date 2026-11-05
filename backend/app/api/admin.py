from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import User, BusinessProfile, AuditLog
from app.api.deps import require_role
from app.services.audit_service import log_event

router = APIRouter(prefix="/admin", tags=["Admin Portal"])

@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.created_at.desc()).all()
    formatted = []
    for u in users:
        biz = u.business_profile
        formatted.append({
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "kycStatus": u.kyc_status,
            "createdAt": u.created_at.strftime("%Y-%m-%d"),
            "name": biz.name if biz else u.email.split("@")[0].capitalize(),
            "business": biz.name if biz else "—",
            "sector": biz.sector if biz else "—",
            "creditScore": biz.credit_score if biz else 0,
        })
    return {"success": True, "data": formatted}

@router.patch("/users")
def update_user_kyc(payload: Dict[str, Any], db: Session = Depends(get_db)):
    user_id = payload.get("userId")
    kyc_status = payload.get("kycStatus")

    if not user_id or not kyc_status:
        raise HTTPException(status_code=400, detail="userId and kycStatus are required")

    status_clean = kyc_status.upper()
    if status_clean not in ["PENDING", "VERIFIED", "REJECTED"]:
        raise HTTPException(status_code=400, detail="Invalid kycStatus value")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.kyc_status = status_clean
    db.commit()

    log_event(
        db,
        action="ADMIN_KYC_STATUS_UPDATED",
        user_email=user.email,
        user_id=user.id,
        category="KYC",
        status="success" if status_clean == "VERIFIED" else "warning",
        metadata={"newStatus": status_clean}
    )

    return {"success": True, "data": {"id": user.id, "kycStatus": user.kyc_status}}

@router.get("/businesses")
def get_all_businesses(db: Session = Depends(get_db)):
    businesses = db.query(BusinessProfile).order_by(BusinessProfile.created_at.desc()).all()
    formatted = []
    for b in businesses:
        u = b.user
        total_raised = sum(c.raised for c in b.campaigns)
        formatted.append({
            "id": b.id,
            "userId": b.user_id,
            "name": b.name,
            "sector": b.sector,
            "location": b.location,
            "udyamId": b.udyam_id,
            "employees": b.employees,
            "creditScore": b.credit_score,
            "kycStatus": u.kyc_status if u else "PENDING",
            "email": u.email if u else "—",
            "campaignCount": len(b.campaigns),
            "totalRaised": total_raised,
        })
    return {"success": True, "data": formatted}

@router.patch("/businesses")
def update_business_kyc(payload: Dict[str, Any], db: Session = Depends(get_db)):
    user_id = payload.get("userId")
    kyc_status = payload.get("kycStatus")

    if not user_id or not kyc_status:
        raise HTTPException(status_code=400, detail="userId and kycStatus required")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.kyc_status = kyc_status.upper()
    db.commit()

    return {"success": True, "data": {"userId": user.id, "kycStatus": user.kyc_status}}

@router.get("/audit")
def get_audit_logs(db: Session = Depends(get_db)):
    logs = db.query(AuditLog).order_by(AuditLog.timestamp.desc()).limit(100).all()
    mapped = [
        {
            "id": l.id,
            "action": l.action,
            "userEmail": l.user_email,
            "userId": l.user_id,
            "ipAddress": l.ip_address,
            "category": l.category,
            "status": l.status,
            "metadata": l.metadata_payload,
            "timestamp": l.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
        for l in logs
    ]
    return {"success": True, "data": mapped}
