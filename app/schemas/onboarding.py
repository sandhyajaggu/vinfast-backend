# app/schemas/onboarding.py
from pydantic import BaseModel, EmailStr,Field
from datetime import date
from typing import List,Optional
from enum import Enum

class CandidateType(str, Enum):
    fresher = "fresher"
    experienced = "experienced"

class DocumentCreate(BaseModel):
    document_type: str
    file_path: str

class NomineeCreate(BaseModel):
    nominee_type: str
    name: str
    dob: date
    relationship_type: str 

    



class FamilyCreate(BaseModel):
    name: str
    dob: date
    relationship_type: str 

    

class BankCreate(BaseModel):
    account_name: str
    account_number: str
    ifsc_code: str
    branch_name: str

class ReferenceCreate(BaseModel):
    reference_type: str
    name: str
    designation_or_occupation: str
    phone: str
    email: str | None = None
    last_employer: str | None = None

# =========================
# MAIN ONBOARDING SCHEMA (🔥 THIS WAS MISSING)
# =========================
class OnboardingCreate(BaseModel):
    candidate_type: CandidateType

    # -------- Personal Info --------
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    dob: date
    gender: str
    location: str
    pan_number: str
    linkedin_url: Optional[str] = None

    # -------- Education --------
    highest_qualification: Optional[str] = None
    specialization: Optional[str] = None
    university: Optional[str] = None
    college: Optional[str] = None
    year_of_passing: Optional[int] = None

    # -------- Job --------
    position_applied: str
    preferred_work_mode: str
    key_skills: str
    expected_salary: int
    why_hire_me: Optional[str] = None

    # -------- Experience (Experienced only) --------
    previous_company: Optional[str] = None
    previous_role: Optional[str] = None
    date_of_joining: Optional[date] = None
    date_of_exit: Optional[date] = None
    total_experience: Optional[str] = None
    esi_number: Optional[str] = None
    uan_number: Optional[str] = None

    # -------- Nested Sections --------
    documents: List[DocumentCreate]
    nominees: List[NomineeCreate]
    family_members: List[FamilyCreate]
    bank_details: BankCreate
    references: List[ReferenceCreate]

class FresherCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    dob: date
    gender: str
    location: str
    highest_qualification: Optional[str] = None
    college: Optional[str] = None
    year_of_passing: int

    documents: List[DocumentCreate]
    nominees: List[NomineeCreate]
    family: List[FamilyCreate]
    bank: BankCreate
    references: List[ReferenceCreate]


class ExperiencedCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    dob: date
    gender: str
    location: str

    company_name: str
    job_role: str
    date_of_joining: date
    date_of_exit: date
    total_experience: str

    # ✅ FIX HERE
    esi_number: Optional[str] = None
    uan_number: Optional[str] = None

    documents: List[DocumentCreate]
    nominees: List[NomineeCreate]
    family: List[FamilyCreate]
    bank: BankCreate
    references: List[ReferenceCreate]

class DocumentResponse(BaseModel):
    document_type: str
    file_path: str

    class Config:
        from_attributes = True

class NomineeResponse(BaseModel):
    nominee_type: str
    name: str
    dob: date
    relationship_type: str

    class Config:
        from_attributes = True


class FamilyResponse(BaseModel):
    name: str
    dob: date
    relationship_type : str

    class Config:
        from_attributes = True


class ReferenceResponse(BaseModel):
    reference_type: str
    name: str
    phone: str
    email: str
    last_employer: str

    class Config:
        from_attributes = True

class BankResponse(BaseModel):
    account_name: str
    account_number: str
    ifsc_code: str
    branch_name: str

    class Config:
        from_attributes = True






class OnboardingResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: str
    phone: str
    gender: str
    location: str
    candidate_type: str
    status: str

    documents: List[DocumentResponse] = []
    nominees: List[NomineeResponse] = []
    family: List[FamilyResponse] = []
    references: List[ReferenceResponse] = []

    bank: Optional[BankResponse] = None

    class Config:
        from_attributes = True








