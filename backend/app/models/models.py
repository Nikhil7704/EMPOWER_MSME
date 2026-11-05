import uuid
from datetime import datetime
from sqlalchemy import (
    Column, String, Integer, Float, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import relationship
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="BUSINESS")  # "BUSINESS" | "INVESTOR" | "ADMIN"
    kyc_status = Column(String, default="PENDING")  # "PENDING" | "VERIFIED" | "REJECTED"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business_profile = relationship("BusinessProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    investments = relationship("Investment", back_populates="investor")
    audit_logs = relationship("AuditLog", back_populates="user")
    circle_memberships = relationship("LendingCircleMember", back_populates="user")

class BusinessProfile(Base):
    __tablename__ = "business_profiles"

    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    name = Column(String, nullable=False)
    sector = Column(String, nullable=False)
    location = Column(String, nullable=False)
    udyam_id = Column(String, unique=True, index=True, nullable=False)
    employees = Column(Integer, default=1)
    business_age = Column(Float, default=1.0)
    website = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    funding_goal = Column(Float, default=0.0)
    kyc_docs = Column(Text, default="[]")  # JSON-encoded array string
    credit_score = Column(Integer, default=300)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="business_profile")
    campaigns = relationship("Campaign", back_populates="business", cascade="all, delete-orphan")
    loans = relationship("Loan", back_populates="business", cascade="all, delete-orphan")

class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("business_profiles.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    goal = Column(Float, nullable=False)
    raised = Column(Float, default=0.0)
    risk_rating = Column(String, default="Medium")  # "Low" | "Medium" | "High"
    roi = Column(Float, default=12.0)
    repayment_model = Column(String, default="Revenue Share")
    status = Column(String, default="pending")  # "pending" | "active" | "funded" | "expired" | "flagged"
    submitted_date = Column(DateTime, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("BusinessProfile", back_populates="campaigns")
    investments = relationship("Investment", back_populates="campaign", cascade="all, delete-orphan")

class Investment(Base):
    __tablename__ = "investments"

    id = Column(String, primary_key=True, default=generate_uuid)
    campaign_id = Column(String, ForeignKey("campaigns.id", ondelete="CASCADE"), nullable=False)
    investor_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="active")  # "active" | "completed" | "defaulted"
    created_at = Column(DateTime, default=datetime.utcnow)

    campaign = relationship("Campaign", back_populates="investments")
    investor = relationship("User", back_populates="investments")

class Loan(Base):
    __tablename__ = "loans"

    id = Column(String, primary_key=True, default=generate_uuid)
    business_id = Column(String, ForeignKey("business_profiles.id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    platform_fee = Column(Float, default=0.0)
    interest_rate = Column(Float, default=10.5)
    tenure_months = Column(Integer, default=12)
    status = Column(String, default="pending")  # "pending" | "approved" | "disbursed" | "repaid"
    bank_name = Column(String, default="")
    account_num = Column(String, default="")
    ifsc = Column(String, default="")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    business = relationship("BusinessProfile", back_populates="loans")
    repayments = relationship("RepaymentLedger", back_populates="loan", cascade="all, delete-orphan")

class RepaymentLedger(Base):
    __tablename__ = "repayment_ledgers"

    id = Column(String, primary_key=True, default=generate_uuid)
    loan_id = Column(String, ForeignKey("loans.id", ondelete="CASCADE"), nullable=False)
    due_date = Column(DateTime, nullable=False)
    amount_due = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    status = Column(String, default="pending")  # "pending" | "paid" | "missed"
    paid_date = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    loan = relationship("Loan", back_populates="repayments")

class LendingCircle(Base):
    __tablename__ = "lending_circles"

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    contribution_amount = Column(Float, nullable=False)
    frequency = Column(String, default="monthly")
    max_members = Column(Integer, default=5)
    current_round = Column(Integer, default=1)
    status = Column(String, default="active")  # "active" | "completed"
    created_at = Column(DateTime, default=datetime.utcnow)

    members = relationship("LendingCircleMember", back_populates="circle", cascade="all, delete-orphan")

class LendingCircleMember(Base):
    __tablename__ = "lending_circle_members"

    id = Column(String, primary_key=True, default=generate_uuid)
    circle_id = Column(String, ForeignKey("lending_circles.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    contribution_status = Column(String, default="pending")  # "pending" | "paid"
    trust_score = Column(Integer, default=100)
    joined_at = Column(DateTime, default=datetime.utcnow)

    circle = relationship("LendingCircle", back_populates="members")
    user = relationship("User", back_populates="circle_memberships")

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=generate_uuid)
    action = Column(String, nullable=False)
    user_email = Column(String, nullable=False)
    user_id = Column(String, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    ip_address = Column(String, default="127.0.0.1")
    category = Column(String, default="Financial")  # "Auth" | "KYC" | "Financial" | "Security"
    status = Column(String, default="info")  # "success" | "warning" | "danger" | "info"
    metadata_payload = Column(Text, nullable=True)  # JSON string
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="audit_logs")
