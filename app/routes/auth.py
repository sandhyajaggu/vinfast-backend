from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin import Admin
from app.schemas.admin import AdminLogin, TokenResponse
from app.utils.auth import verify_password,hash_password,create_access_token
from app.utils.jwt_dependency import get_current_admin
from app.schemas.admin import ChangePasswordRequest


router = APIRouter(prefix="/auth", tags=["Admin"])

@router.post("/login")
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.email == form_data.username).first()

    if not admin or not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    access_token = create_access_token(
        data={"sub": admin.email}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }


@router.post("/admin/change-password")
def change_password(
    data: ChangePasswordRequest,
    db: Session = Depends(get_db),
    admin=Depends(get_current_admin)
):
    # 1️⃣ Verify current password
    if not verify_password(data.current_password, admin.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    # 2️⃣ Update new password
    admin.password_hash = hash_password(data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}

from app.schemas.admin import ForgotPasswordRequest

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.email == data.email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    otp = generate_otp()

    record = OTP(
        email=data.email,
        otp_code=otp,
        expires_at=otp_expiry()
    )

    db.add(record)
    db.commit()

    try:
        send_otp_email(data.email, otp)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Email sending failed"
        )

    return {"message": "OTP sent to email"}

    
