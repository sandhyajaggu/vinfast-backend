
from fastapi import APIRouter, Depends, HTTPException, Query,File,UploadFile
from sqlalchemy.orm import Session,joinedload
from typing import List
#from sqlalchemy.orm import relationship

from app.database import get_db
from app.schemas.onboarding import FresherCreate,ExperiencedCreate,OnboardingResponse
from app.models.onboarding_documents import OnboardingDocument
from app.models.onboarding import Onboarding
from app.models.onboarding_documents import OnboardingDocument
from app.models.onboarding_nominee import (
    OnboardingNominee,
    OnboardingFamily,
    OnboardingBank,
    OnboardingReference
)
from app.utils.auth import get_current_admin  # if admin auth is required
import os,shutil
UPLOAD_DIR = "uploads/onboarding"
os.makedirs(UPLOAD_DIR, exist_ok=True)

router = APIRouter(
    prefix="/admin/onboarding",
    tags=["Onboarding"],
    
)

@router.get("/admin/onboarding")
def admin_onboarding(current_admin=Depends(get_current_admin)):
    return {
        "message": "Admin authenticated",
        "admin": current_admin
    }


@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    path = f"{UPLOAD_DIR}/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_path": path}

@router.post("/fresher")
def fresher_onboarding(data: FresherCreate, db: Session = Depends(get_db)):
    try:
        onboarding = Onboarding(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            gender=data.gender,
            location=data.location,
            candidate_type="fresher",
            status="pending"
        )

       # ✅ Documents
        for doc in data.documents:
            onboarding.documents.append(
                OnboardingDocument(
                    document_type=doc.document_type,
                    file_path=doc.file_path
                )
            )

        # ✅ Nominees
        for nominee in data.nominees:
            onboarding.nominees.append(
                OnboardingNominee(
                    nominee_type=nominee.nominee_type,
                    name=nominee.name,
                    dob=nominee.dob,
                    relationship_type =nominee.relationship_type
)
            )

        # ✅ Family
        for member in data.family:
            onboarding.family.append(
                OnboardingFamily(
                    name=member.name,
                    dob=member.dob,
                    relationship_type = member.relationship_type
                )
            )

        # ✅ Bank (ONE-TO-ONE)
        onboarding.bank = OnboardingBank(
            account_name=data.bank.account_name,
            account_number=data.bank.account_number,
            ifsc_code=data.bank.ifsc_code,
            branch_name=data.bank.branch_name
        )

        # ✅ References
        for ref in data.references:
            onboarding.references.append(
                OnboardingReference(
                    reference_type=ref.reference_type,
                    name=ref.name,
                    designation_or_occupation=ref.designation_or_occupation,
                    phone=ref.phone,
                    email=ref.email,
                    last_employer=ref.last_employer
                )
            )


        db.add(onboarding)   # 🔥 add ONLY parent
        db.commit()          # 🔥 children saved automatically
        db.refresh(onboarding)

        return {
            "message": "Fresher onboarded successfully",
            "onboarding_id": onboarding.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))




@router.post("/experienced")
def experienced_onboarding(
    data: ExperiencedCreate,
    db: Session = Depends(get_db)
):
    try:
        onboarding = Onboarding(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            gender=data.gender,
            location=data.location,
            candidate_type="experienced",
            status="pending"
        )

        # ✅ Documents
        for doc in data.documents:
            onboarding.documents.append(
                OnboardingDocument(
                    document_type=doc.document_type,
                    file_path=doc.file_path
                )
            )

        # ✅ Nominees
        for nominee in data.nominees:
            onboarding.nominees.append(
                OnboardingNominee(
                    nominee_type=nominee.nominee_type,
                    name=nominee.name,
                    dob=nominee.dob,
                    relationship_type=nominee.relationship_type
)
            )

        # ✅ Family
        for member in data.family:
            onboarding.family.append(
                OnboardingFamily(
                    name=member.name,
                    dob=member.dob,
                    relationship_type=member.relationship_type
                )
            )

        # ✅ Bank (ONE-TO-ONE)
        onboarding.bank = OnboardingBank(
            account_name=data.bank.account_name,
            account_number=data.bank.account_number,
            ifsc_code=data.bank.ifsc_code,
            branch_name=data.bank.branch_name
        )

        # ✅ References
        for ref in data.references:
            onboarding.references.append(
                OnboardingReference(
                    reference_type=ref.reference_type,
                    name=ref.name,
                    designation_or_occupation=ref.designation_or_occupation,
                    phone=ref.phone,
                    email=ref.email,
                    last_employer=ref.last_employer
                )
            )

        db.add(onboarding)
        db.commit()
        db.refresh(onboarding)

        return {
            "message": "Experienced candidate onboarded successfully",
            "onboarding_id": onboarding.id
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))






@router.get("/status/{onboarding_id}")
def get_status(onboarding_id: int, db: Session = Depends(get_db)):
    record = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()
    if not record:
        return {"error": "Not found"}
    return {"status": record.status}


# =====================================================
# 1️⃣ LIST ALL ONBOARDINGS
# =====================================================
'''
@router.get("/", response_model=List[OnboardingResponse])
def list_onboardings(db: Session = Depends(get_db)):
    onboardings = db.query(Onboarding).all()
    return onboardings'''

@router.get("/", response_model=List[OnboardingResponse])
def list_onboardings(db: Session = Depends(get_db)):
    onboardings = (
        db.query(Onboarding)
        .options(
            joinedload(Onboarding.documents),
            joinedload(Onboarding.nominees),
            joinedload(Onboarding.family),
            joinedload(Onboarding.bank),
            joinedload(Onboarding.references),
        )
        .all()
    )

    return onboardings



# =====================================================
# 2️⃣ GET ONBOARDING BY ID
# =====================================================
from sqlalchemy.orm import joinedload

@router.get("/{onboarding_id}", response_model=OnboardingResponse)
def get_onboarding_by_id(onboarding_id: int, db: Session = Depends(get_db)):
    onboarding = (
        db.query(Onboarding)
        .options(
            joinedload(Onboarding.documents),
            joinedload(Onboarding.nominees),
            joinedload(Onboarding.family),
            joinedload(Onboarding.bank),
            joinedload(Onboarding.references),
        )
        .filter(Onboarding.id == onboarding_id)
        .first()
    )

    if not onboarding:
        raise HTTPException(status_code=404, detail="Onboarding not found")

    return onboarding





# =====================================================
# 3️⃣ UPDATE ONBOARDING STATUS
# =====================================================
@router.patch("/{onboarding_id}/status")
def update_onboarding_status(
    onboarding_id: int,
    status: str = Query(..., description="approved / rejected / pending"),
    db: Session = Depends(get_db)
):
    """
    Update onboarding status
    """
    if status not in ["pending", "approved", "rejected"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid status value"
        )

    onboarding = (
        db.query(Onboarding)
        .filter(Onboarding.id == onboarding_id)
        .first()
    )

    if not onboarding:
        raise HTTPException(
            status_code=404,
            detail="Onboarding not found"
        )

    onboarding.status = status
    db.commit()

    return {
        "message": "Status updated successfully",
        "onboarding_id": onboarding_id,
        "new_status": status
    }


# =====================================================
# 4️⃣ DELETE ONBOARDING (HARD DELETE)
# =====================================================
@router.delete("/{onboarding_id}")
def delete_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db)
):
    """
    Permanently delete onboarding
    """
    onboarding = (
        db.query(Onboarding)
        .filter(Onboarding.id == onboarding_id)
        .first()
    )

    if not onboarding:
        raise HTTPException(
            status_code=404,
            detail="Onboarding not found"
        )

    db.delete(onboarding)
    db.commit()

    return {
        "message": "Onboarding deleted permanently",
        "onboarding_id": onboarding_id
    }





