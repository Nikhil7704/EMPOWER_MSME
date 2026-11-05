from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import LendingCircle, LendingCircleMember, User
from app.schemas.schemas import LendingCircleCreate
from app.api.deps import get_current_user
from app.services.audit_service import log_event

router = APIRouter(prefix="/lending-circles", tags=["Lending Circles"])

@router.get("")
def list_lending_circles(db: Session = Depends(get_db)):
    circles = db.query(LendingCircle).order_by(LendingCircle.created_at.desc()).all()
    mapped = []
    for c in circles:
        members_list = []
        for m in c.members:
            email_part = m.user.email.split("@")[0] if m.user else "Member"
            members_list.append({
                "name": email_part.capitalize(),
                "trustScore": m.trust_score,
                "contributed": m.contribution_status == "paid",
                "turn": 1,
                "initials": email_part[:2].upper()
            })
        
        mapped.append({
            "id": c.id,
            "name": c.name,
            "members": len(c.members),
            "maxMembers": c.max_members,
            "contribution": c.contribution_amount,
            "totalPool": c.contribution_amount * len(c.members),
            "currentRound": c.current_round,
            "totalRounds": c.max_members,
            "myTurn": 2,
            "status": c.status,
            "category": "Mixed",
            "members_list": members_list
        })

    return {"success": True, "data": mapped}

@router.post("")
def create_lending_circle(
    circle_in: LendingCircleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    circle = LendingCircle(
        name=circle_in.name,
        contribution_amount=circle_in.contribution,
        max_members=circle_in.maxMembers,
        current_round=1,
        status="active"
    )
    db.add(circle)
    db.commit()
    db.refresh(circle)

    # Add creator as first member
    member = LendingCircleMember(
        circle_id=circle.id,
        user_id=current_user.id,
        contribution_status="paid",
        trust_score=100
    )
    db.add(member)
    db.commit()

    log_event(
        db,
        action="LENDING_CIRCLE_CREATED",
        user_email=current_user.email,
        user_id=current_user.id,
        category="Financial",
        status="success",
        metadata={"circleId": circle.id, "name": circle.name}
    )

    return {
        "success": True,
        "data": {
            "id": circle.id,
            "name": circle.name,
            "contribution": circle.contribution_amount,
            "maxMembers": circle.max_members,
            "status": circle.status
        }
    }
