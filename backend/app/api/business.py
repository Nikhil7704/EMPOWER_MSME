from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import BusinessProfile, User
from app.api.deps import get_current_user_optional

router = APIRouter(prefix="/business", tags=["Business Profile"])

@router.get("/profile")
def get_business_profile(
    userId: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    target_id = userId or (current_user.id if current_user else None)
    profile = None
    if target_id:
        profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == target_id).first()
    if not profile:
        profile = db.query(BusinessProfile).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    return {
        "success": True,
        "data": {
            "id": profile.id,
            "userId": profile.user_id,
            "name": profile.name,
            "sector": profile.sector,
            "location": profile.location,
            "udyamId": profile.udyam_id,
            "employees": profile.employees,
            "businessAge": profile.business_age,
            "website": profile.website,
            "description": profile.description,
            "fundingGoal": profile.funding_goal,
            "creditScore": profile.credit_score,
            "kycDocs": profile.kyc_docs,
            "user": {
                "email": profile.user.email if profile.user else "",
                "kycStatus": profile.user.kyc_status if profile.user else "PENDING"
            }
        }
    }

@router.patch("/profile")
def update_business_profile(
    payload: Dict[str, Any],
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    target_id = payload.get("userId") or (current_user.id if current_user else None)
    profile = None
    if target_id:
        profile = db.query(BusinessProfile).filter(BusinessProfile.user_id == target_id).first()
    if not profile:
        profile = db.query(BusinessProfile).first()

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    if "name" in payload and payload["name"]:
        profile.name = payload["name"]
    if "sector" in payload and payload["sector"]:
        profile.sector = payload["sector"]
    if "location" in payload and payload["location"]:
        profile.location = payload["location"]
    if "description" in payload and payload["description"]:
        profile.description = payload["description"]
    if "employees" in payload and payload["employees"] is not None:
        profile.employees = int(payload["employees"])
    if "fundingGoal" in payload and payload["fundingGoal"] is not None:
        profile.funding_goal = float(payload["fundingGoal"])
    if "website" in payload:
        profile.website = payload["website"]

    db.commit()
    db.refresh(profile)

    return {
        "success": True,
        "data": {
            "id": profile.id,
            "userId": profile.user_id,
            "name": profile.name,
            "sector": profile.sector,
            "location": profile.location,
            "description": profile.description,
            "employees": profile.employees,
            "fundingGoal": profile.funding_goal,
            "website": profile.website
        }
    }
