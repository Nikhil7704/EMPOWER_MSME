from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.core.database import get_db
from app.models.models import Loan, BusinessProfile, User
from app.schemas.schemas import LoanCreate
from app.api.deps import get_current_user
from app.services.audit_service import log_event

router = APIRouter(prefix="/loans", tags=["Loans"])

TIMELINE = {
    "submitted": {"label": "Submitted", "description": "Application received by the system", "icon": "upload"},
    "under_review": {"label": "Under Review", "description": "Documents being verified by lender", "icon": "search"},
    "approved": {"label": "Approved", "description": "Loan sanctioned, awaiting disbursement", "icon": "check"},
    "disbursed": {"label": "Disbursed", "description": "Funds transferred to your account", "icon": "bank"},
    "rejected": {"label": "Rejected", "description": "Application not approved", "icon": "x"},
}

STATUS_MAP = {
    "pending": "submitted",
    "approved": "approved",
    "disbursed": "disbursed",
    "repaid": "disbursed"
}

@router.get("")
def get_loans(
    businessId: Optional[str] = Query(None),
    id: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    if id:
        loan = db.query(Loan).filter(Loan.id == id).first()
        if not loan:
            raise HTTPException(status_code=404, detail="Loan not found")
        biz = loan.business
        mapped = {
            "id": loan.id,
            "businessId": loan.business_id,
            "amount": loan.amount,
            "purpose": "Working Capital",
            "status": STATUS_MAP.get(loan.status, "submitted"),
            "stage": loan.status.capitalize(),
            "submittedAt": loan.created_at.strftime("%Y-%m-%d"),
            "creditScore": biz.credit_score if biz else 650,
            "riskLevel": "Low",
            "interestRate": loan.interest_rate,
            "tenure": loan.tenure_months,
            "emi": round((loan.amount / loan.tenure_months) * 1.05),
            "documents": biz.kyc_docs if biz else "[]"
        }
        return {"success": True, "data": {**mapped, "timeline": TIMELINE}}

    query = db.query(Loan)
    if businessId:
        query = query.filter(Loan.business_id == businessId)
    loans = query.order_by(Loan.created_at.desc()).all()

    mapped_list = []
    for l in loans:
        biz = l.business
        mapped_list.append({
            "id": l.id,
            "businessId": l.business_id,
            "amount": l.amount,
            "purpose": "Working Capital",
            "status": STATUS_MAP.get(l.status, "submitted"),
            "stage": l.status.capitalize(),
            "submittedAt": l.created_at.strftime("%Y-%m-%d"),
            "creditScore": biz.credit_score if biz else 650,
            "riskLevel": "Low",
            "interestRate": l.interest_rate,
            "tenure": l.tenure_months,
            "emi": round((l.amount / l.tenure_months) * 1.05),
            "documents": biz.kyc_docs if biz else "[]"
        })

    return {"success": True, "data": mapped_list, "timeline": TIMELINE}

@router.post("")
def create_loan(
    loan_in: LoanCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Lookup business
    biz = None
    if loan_in.businessId:
        biz = db.query(BusinessProfile).filter(BusinessProfile.id == loan_in.businessId).first()
    if not biz and current_user.business_profile:
        biz = current_user.business_profile
    if not biz:
        biz = db.query(BusinessProfile).first()

    if not biz:
        # Create fallback business profile
        biz = BusinessProfile(
            user_id=current_user.id,
            name="GreenLeaf Organics",
            sector="Agriculture",
            location="Pune, Maharashtra",
            udyam_id=f"UDYAM-MH-{current_user.id[:6].upper()}",
            description="Organic agri-produce supply chain MSME",
            credit_score=720
        )
        db.add(biz)
        db.commit()
        db.refresh(biz)

    new_loan = Loan(
        business_id=biz.id,
        amount=loan_in.amount,
        platform_fee=round(loan_in.amount * 0.02, 2),
        interest_rate=loan_in.interestRate or 10.5,
        tenure_months=loan_in.tenure or 12,
        status="pending",
        bank_name=loan_in.bankName or "State Bank of India",
        account_num=loan_in.accountNum or "1234567890",
        ifsc=loan_in.ifsc or "SBIN0000001"
    )
    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)

    log_event(
        db,
        action="LOAN_APPLICATION_SUBMITTED",
        user_email=current_user.email,
        user_id=current_user.id,
        category="Financial",
        status="success",
        metadata={"loanId": new_loan.id, "amount": new_loan.amount}
    )

    return {
        "success": True,
        "data": {
            "id": new_loan.id,
            "businessId": new_loan.business_id,
            "amount": new_loan.amount,
            "status": "submitted",
            "stage": "Pending",
            "submittedAt": new_loan.created_at.strftime("%Y-%m-%d"),
            "creditScore": biz.credit_score,
            "interestRate": new_loan.interest_rate,
            "tenure": new_loan.tenure_months,
            "emi": round((new_loan.amount / new_loan.tenure_months) * 1.05),
        }
    }
