from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# ----------------- Auth Schemas -----------------
class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: str = "BUSINESS"  # BUSINESS | INVESTOR | ADMIN

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: Dict[str, Any]

class UserOut(BaseModel):
    id: str
    email: str
    role: str
    kyc_status: str
    created_at: datetime

    class Config:
        from_attributes = True

# ----------------- Business Profile Schemas -----------------
class BusinessProfileCreate(BaseModel):
    name: str
    sector: str
    location: str
    udyam_id: str
    employees: int = 1
    business_age: float = 1.0
    website: Optional[str] = None
    description: str
    funding_goal: float = 0.0

class BusinessProfileOut(BaseModel):
    id: str
    userId: str
    name: str
    sector: str
    location: str
    udyamId: str
    employees: int
    businessAge: float
    website: Optional[str]
    description: str
    fundingGoal: float
    creditScore: int
    kycDocs: str

    class Config:
        from_attributes = True

# ----------------- Loan Schemas -----------------
class LoanCreate(BaseModel):
    businessId: Optional[str] = None
    amount: float
    interestRate: Optional[float] = 10.5
    tenure: Optional[int] = 12
    bankName: Optional[str] = "SBI"
    accountNum: Optional[str] = "1234567890"
    ifsc: Optional[str] = "SBIN0000001"

# ----------------- Campaign Schemas -----------------
class CampaignCreate(BaseModel):
    title: str
    description: str
    goal: float
    riskRating: Optional[str] = "Medium"
    roi: Optional[float] = 12.0
    repaymentModel: Optional[str] = "Revenue Share"
    businessName: Optional[str] = None
    businessId: Optional[str] = None

class InvestmentCreate(BaseModel):
    campaignId: str
    amount: float
    userId: Optional[str] = None

# ----------------- Repayment Schemas -----------------
class RepaymentCreate(BaseModel):
    loanId: str
    amount: float

# ----------------- Credit Evaluation Schemas -----------------
class CreditEvaluationInput(BaseModel):
    annualRevenue: float = 0.0
    netProfitMargin: float = 0.0
    cashFlowVariance: float = 50.0
    existingDebt: float = 0.0
    repaymentHistory: float = 50.0
    businessAge: float = 0.0
    gstFilingScore: float = 50.0
    industryRiskLevel: str = "medium"

# ----------------- Lending Circle Schemas -----------------
class LendingCircleCreate(BaseModel):
    name: str
    contribution: float
    maxMembers: int
    category: Optional[str] = "Mixed"

# ----------------- Chat / RAG Schemas -----------------
class ChatRequest(BaseModel):
    message: str

class StoryBuilderRequest(BaseModel):
    businessName: str
    sector: str
    yearsInBusiness: float
    annualRevenue: float
    fundingGoal: float
    purpose: str
    impactStory: Optional[str] = None
