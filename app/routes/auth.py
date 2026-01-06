from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.admin import Admin
from app.schemas.admin import TokenResponse

from app.utils.auth import verify_password,hash_password,create_access_token
from app.utils.jwt_dependency import get_current_admin
from app.schemas.admin import ChangePasswordRequest
from app.utils.email import send_otp_email
from app.utils.otp import generate_otp, otp_expiry


from datetime import datetime, timedelta
import random
import uuid



router = APIRouter(prefix="/admin", tags=["Admin Auth"])

@router.post("/login", response_model=TokenResponse)
def admin_login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    admin = db.query(Admin).filter(Admin.email == form_data.username).first()

    if not admin:
        raise HTTPException(status_code=401, detail="Admin not found")

    if not verify_password(form_data.password, admin.password_hash):
        raise HTTPException(status_code=401, detail="Invalid password")

    token = create_access_token(
        data={"sub": admin.email, "role": "admin"}
    )

    return {
        "access_token": token,
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
'''
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

    return {"message": "OTP sent to email"}'''

@router.post("/admin/forgot-password")
def forgot_password(email: str, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.email == email).first()
    if not admin:
        raise HTTPException(status_code=404, detail="Email not registered")

    otp = generate_otp()
    admin.otp = otp
    admin.otp_expiry = otp_expiry()
    db.commit()

    send_otp_email(email, otp)

    return {"message": "OTP sent successfully"}



@router.post("/admin/verify-otp")
def verify_otp(email: str, otp: str, db: Session = Depends(get_db)):

    admin = db.query(Admin).filter(Admin.email == email).first()

    if not admin or admin.otp != otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    if admin.otp_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP expired")

    reset_token = str(uuid.uuid4())
    admin.reset_token = reset_token
    admin.reset_token_expiry = datetime.utcnow() + timedelta(minutes=10)

    db.commit()

    return {
        "message": "OTP verified",
        "reset_token": reset_token
    }


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

@router.post("/admin/reset-password")
def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):

    admin = db.query(Admin).filter(Admin.reset_token == token).first()

    if not admin:
        raise HTTPException(status_code=400, detail="Invalid token")

    if admin.reset_token_expiry < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Token expired")

    admin.password = hash_password(new_password)
    admin.otp = None
    admin.reset_token = None

    db.commit()

    return {"message": "Password reset successful"}


    


