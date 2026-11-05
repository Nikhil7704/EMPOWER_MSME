from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.models import Campaign, BusinessProfile, Investment, User
from app.schemas.schemas import CampaignCreate, InvestmentCreate
from app.api.deps import get_current_user
from app.services.audit_service import log_event

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])

@router.get("")
def get_campaigns(
    sector: Optional[str] = Query(None),
    region: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    businessId: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Campaign).join(BusinessProfile, Campaign.business_id == BusinessProfile.id)
    if status:
        query = query.filter(Campaign.status == status)
    if businessId:
        query = query.filter(Campaign.business_id == businessId)
    if sector and sector != "all":
        query = query.filter(BusinessProfile.sector == sector)
    if region and region != "all":
        query = query.filter(BusinessProfile.location.ilike(f"%{region}%"))

    campaigns = query.order_by(Campaign.created_at.desc()).all()
    mapped = []
    for c in campaigns:
        biz = c.business
        mapped.append({
            "id": c.id,
            "businessId": c.business_id,
            "businessName": biz.name if biz else "MSME Partner",
            "sector": biz.sector if biz else "General",
            "region": biz.location if biz else "India",
            "title": c.title,
            "description": c.description,
            "goal": c.goal,
            "raised": c.raised,
            "investors": len(c.investments) if c.investments else 0,
            "daysLeft": 30,
            "riskLevel": c.risk_rating,
            "expectedROI": c.roi,
            "repaymentModel": c.repayment_model,
            "status": c.status,
            "createdAt": c.created_at.strftime("%Y-%m-%d"),
        })

    return {"success": True, "data": mapped, "total": len(mapped)}

@router.post("")
def create_campaign(
    campaign_in: CampaignCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    biz = None
    if campaign_in.businessId:
        biz = db.query(BusinessProfile).filter(BusinessProfile.id == campaign_in.businessId).first()
    if not biz and current_user.business_profile:
        biz = current_user.business_profile
    if not biz and campaign_in.businessName:
        biz = db.query(BusinessProfile).filter(BusinessProfile.name == campaign_in.businessName).first()
    if not biz:
        biz = db.query(BusinessProfile).first()

    if not biz:
        biz = BusinessProfile(
            user_id=current_user.id,
            name=campaign_in.businessName or "EcoTech Innovations",
            sector="Clean Energy",
            location="Bengaluru, Karnataka",
            udyam_id=f"UDYAM-KA-{current_user.id[:6].upper()}",
            description="Clean energy and green tech for small scale farming",
            funding_goal=campaign_in.goal
        )
        db.add(biz)
        db.commit()
        db.refresh(biz)

    new_camp = Campaign(
        business_id=biz.id,
        title=campaign_in.title,
        description=campaign_in.description,
        goal=campaign_in.goal,
        raised=0.0,
        risk_rating=campaign_in.riskRating or "Medium",
        roi=campaign_in.roi or 12.0,
        repayment_model=campaign_in.repaymentModel or "Revenue Share",
        status="active"
    )
    db.add(new_camp)
    db.commit()
    db.refresh(new_camp)

    log_event(
        db,
        action="CAMPAIGN_LAUNCHED",
        user_email=current_user.email,
        user_id=current_user.id,
        category="Financial",
        status="success",
        metadata={"campaignId": new_camp.id, "goal": new_camp.goal}
    )

    return {
        "success": True,
        "data": {
            "id": new_camp.id,
            "businessId": new_camp.business_id,
            "businessName": biz.name,
            "title": new_camp.title,
            "goal": new_camp.goal,
            "raised": 0.0,
            "status": new_camp.status,
            "expectedROI": new_camp.roi
        }
    }

@router.post("/invest")
def invest_campaign(
    inv_in: InvestmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if inv_in.amount <= 0:
        raise HTTPException(status_code=400, detail="Investment amount must be greater than zero")

    camp = db.query(Campaign).filter(Campaign.id == inv_in.campaignId).first()
    if not camp:
        raise HTTPException(status_code=404, detail="Campaign not found")

    investor = current_user
    if inv_in.userId:
        investor_override = db.query(User).filter(User.id == inv_in.userId).first()
        if investor_override:
            investor = investor_override

    investment = Investment(
        campaign_id=camp.id,
        investor_id=investor.id,
        amount=inv_in.amount,
        status="active"
    )
    camp.raised += inv_in.amount
    db.add(investment)
    db.commit()
    db.refresh(investment)
    db.refresh(camp)

    log_event(
        db,
        action="INVESTMENT_EXECUTED",
        user_email=investor.email,
        user_id=investor.id,
        category="Financial",
        status="success",
        metadata={"campaignId": camp.id, "amount": inv_in.amount}
    )

    return {
        "success": True,
        "data": {
            "id": investment.id,
            "campaignId": investment.campaign_id,
            "investorId": investment.investor_id,
            "amount": investment.amount,
            "status": investment.status,
            "updatedRaised": camp.raised
        }
    }
