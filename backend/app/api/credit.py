from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import User, BusinessProfile
from app.schemas.schemas import CreditEvaluationInput
from app.services.credit_service import evaluate_credit, WEIGHTS, LABELS
from app.api.deps import get_current_user_optional
from app.services.audit_service import log_event

router = APIRouter(prefix="/credit", tags=["Credit Scoring Engine"])

@router.get("/evaluate")
def get_credit_metadata():
    return {
        "success": True,
        "engine": "EmpowerMSME 7-Factor Transparent Credit Engine",
        "version": "2.0-fastapi",
        "scoreRange": [300, 900],
        "weights": WEIGHTS,
        "labels": LABELS,
        "tiers": [
            {"tier": "Tier 1 - Prime", "minScore": 750, "rate": "8.5%", "maxMultiplier": "3.0x Revenue"},
            {"tier": "Tier 2 - Standard", "minScore": 650, "rate": "11.5%", "maxMultiplier": "2.0x Revenue"},
            {"tier": "Tier 3 - Subprime", "minScore": 500, "rate": "15.0%", "maxMultiplier": "1.0x Revenue"},
            {"tier": "Not Eligible", "minScore": 300, "rate": "18.0%", "maxMultiplier": "0.3x Revenue"},
        ]
    }

@router.post("/evaluate")
def run_credit_evaluation(
    input_data: CreditEvaluationInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    result = evaluate_credit(input_data.model_dump())

    # If current user is a business, persist their calculated credit score
    if current_user and current_user.business_profile:
        current_user.business_profile.credit_score = result["creditScore"]
        db.commit()

    if current_user:
        log_event(
            db,
            action="CREDIT_SCORE_EVALUATED",
            user_email=current_user.email,
            user_id=current_user.id,
            category="Financial",
            status="info",
            metadata={"score": result["creditScore"], "tier": result["eligibilityTier"]}
        )

    return {
        "success": True,
        "data": result
    }
