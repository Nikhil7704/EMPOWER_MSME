from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.models import User, BusinessProfile
from app.schemas.schemas import UserRegister, UserLogin, Token, UserOut
from app.api.deps import get_current_user, get_current_user_optional
from app.services.audit_service import log_event

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register")
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists"
        )

    hashed_pw = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        password_hash=hashed_pw,
        role=user_in.role.upper(),
        kyc_status="PENDING"
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # If Business role, create placeholder business profile
    if new_user.role == "BUSINESS":
        clean_name = user_in.email.split("@")[0].capitalize() + " Enterprises"
        profile = BusinessProfile(
            user_id=new_user.id,
            name=clean_name,
            sector="Manufacturing",
            location="Mumbai, Maharashtra",
            udyam_id=f"UDYAM-MH-{new_user.id[:8].upper()}",
            description="Established MSME seeking alternative financing.",
            funding_goal=500000.0,
            credit_score=680
        )
        db.add(profile)
        db.commit()

    log_event(
        db,
        action="USER_REGISTERED",
        user_email=new_user.email,
        user_id=new_user.id,
        category="Auth",
        status="success"
    )

    token = create_access_token(subject=new_user.id, role=new_user.role)
    return {
        "success": True,
        "data": {
            "id": new_user.id,
            "email": new_user.email,
            "role": new_user.role,
            "kycStatus": new_user.kyc_status,
            "accessToken": token
        }
    }

@router.post("/login")
def login(login_in: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == login_in.email).first()
    if not user or not verify_password(login_in.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    token = create_access_token(subject=user.id, role=user.role)
    log_event(
        db,
        action="USER_LOGIN_SUCCESS",
        user_email=user.email,
        user_id=user.id,
        category="Auth",
        status="success"
    )

    return {
        "success": True,
        "token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role,
            "kycStatus": user.kyc_status
        }
    }

@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = create_access_token(subject=user.id, role=user.role)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "role": user.role
        }
    }

@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return {
        "success": True,
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
            "kycStatus": current_user.kyc_status
        }
    }

@router.get("/session")
def get_session(current_user: User = Depends(get_current_user_optional)):
    if not current_user:
        return {"user": None}
    return {
        "user": {
            "id": current_user.id,
            "email": current_user.email,
            "role": current_user.role,
            "kycStatus": current_user.kyc_status
        }
    }
