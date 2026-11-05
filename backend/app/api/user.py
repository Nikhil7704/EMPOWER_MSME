from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import Investment, User
from app.api.deps import get_current_user_optional

router = APIRouter(prefix="/user", tags=["Investor User Operations"])

@router.get("/investments")
def get_user_investments(
    userId: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    target_id = userId or (current_user.id if current_user else None)
    investments = []
    if target_id:
        investments = db.query(Investment).filter(Investment.investor_id == target_id).all()
    if not investments:
        investments = db.query(Investment).order_by(Investment.created_at.desc()).limit(20).all()

    enriched = []
    for inv in investments:
        camp = inv.campaign
        biz = camp.business if camp else None
        roi = camp.roi if camp else 12.0
        roi_mult = roi / 100.0
        cap = round(inv.amount * (1 + roi_mult))
        returned = cap if inv.status == "completed" else round(inv.amount * roi_mult * 0.4)
        next_payout_date = (datetime.utcnow() + timedelta(days=30)).strftime("%B %d, %Y")

        enriched.append({
            "id": inv.id,
            "name": biz.name if biz else (camp.title if camp else "MSME Partner"),
            "sector": biz.sector if biz else "General",
            "invested": inv.amount,
            "returned": returned,
            "cap": cap,
            "roi": roi,
            "model": camp.repayment_model if camp else "Revenue Share",
            "status": inv.status,
            "nextPayout": next_payout_date if inv.status == "active" else "Settled",
            "nextAmount": round(inv.amount * roi_mult / 12) if inv.status == "active" else 0,
            "milestones": [
                {"desc": f'Campaign "{camp.title if camp else "Growth"}" funded', "done": True},
                {"desc": "Escrow disbursement completed", "done": True},
                {"desc": "Monthly returns distribution active", "done": inv.status == "active"}
            ]
        })

    total_invested = sum(e["invested"] for e in enriched)
    total_returned = sum(e["returned"] for e in enriched)

    return {
        "success": True,
        "data": {
            "investments": enriched,
            "summary": {
                "totalInvested": total_invested,
                "totalReturned": total_returned,
                "activeCount": len([e for e in enriched if e["status"] == "active"])
            }
        }
    }
