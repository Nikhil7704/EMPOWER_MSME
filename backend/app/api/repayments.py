from typing import Optional
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.models import RepaymentLedger, Loan, User
from app.schemas.schemas import RepaymentCreate
from app.api.deps import get_current_user
from app.services.audit_service import log_event

router = APIRouter(prefix="/repayments", tags=["Repayments"])

@router.get("")
def get_repayments(
    loanId: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(RepaymentLedger)
    if loanId:
        query = query.filter(RepaymentLedger.loan_id == loanId)
    
    ledgers = query.order_by(RepaymentLedger.due_date.asc()).all()

    # If no repayment records exist yet for this loan, create simulated schedule
    if not ledgers and loanId:
        loan = db.query(Loan).filter(Loan.id == loanId).first()
        if loan:
            monthly_emi = round((loan.amount / loan.tenure_months) * 1.05)
            for i in range(1, min(loan.tenure_months + 1, 13)):
                due = datetime.utcnow() + timedelta(days=30 * i)
                ledger_item = RepaymentLedger(
                    loan_id=loan.id,
                    due_date=due,
                    amount_due=monthly_emi,
                    amount_paid=monthly_emi if i == 1 else 0.0,
                    status="paid" if i == 1 else "pending",
                    paid_date=datetime.utcnow() if i == 1 else None
                )
                db.add(ledger_item)
            db.commit()
            ledgers = db.query(RepaymentLedger).filter(RepaymentLedger.loan_id == loanId).order_by(RepaymentLedger.due_date.asc()).all()

    mapped = [
        {
            "id": r.id,
            "loanId": r.loan_id,
            "dueDate": r.due_date.strftime("%Y-%m-%d"),
            "amountDue": r.amount_due,
            "amountPaid": r.amount_paid,
            "status": r.status,
            "paidDate": r.paid_date.strftime("%Y-%m-%d") if r.paid_date else None
        }
        for r in ledgers
    ]

    total_due = sum(r["amountDue"] for r in mapped)
    total_paid = sum(r["amountPaid"] for r in mapped)

    return {
        "success": True,
        "data": mapped,
        "summary": {
            "totalDue": total_due,
            "totalPaid": total_paid,
            "remainingBalance": max(0, total_due - total_paid),
            "nextPayment": mapped[0] if mapped else None
        }
    }

@router.post("")
def record_repayment(
    payment_in: RepaymentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    loan = db.query(Loan).filter(Loan.id == payment_in.loanId).first()
    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    pending_ledger = db.query(RepaymentLedger).filter(
        RepaymentLedger.loan_id == payment_in.loanId,
        RepaymentLedger.status == "pending"
    ).order_by(RepaymentLedger.due_date.asc()).first()

    if pending_ledger:
        pending_ledger.amount_paid += payment_in.amount
        pending_ledger.paid_date = datetime.utcnow()
        if pending_ledger.amount_paid >= pending_ledger.amount_due:
            pending_ledger.status = "paid"
        db.commit()
        db.refresh(pending_ledger)
        record = pending_ledger
    else:
        record = RepaymentLedger(
            loan_id=loan.id,
            due_date=datetime.utcnow(),
            amount_due=payment_in.amount,
            amount_paid=payment_in.amount,
            status="paid",
            paid_date=datetime.utcnow()
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    log_event(
        db,
        action="EMI_REPAYMENT_RECORDED",
        user_email=current_user.email,
        user_id=current_user.id,
        category="Financial",
        status="success",
        metadata={"loanId": loan.id, "amountPaid": payment_in.amount}
    )

    return {
        "success": True,
        "data": {
            "id": record.id,
            "loanId": record.loan_id,
            "amountPaid": record.amount_paid,
            "status": record.status,
            "paidDate": record.paid_date.strftime("%Y-%m-%d")
        }
    }
