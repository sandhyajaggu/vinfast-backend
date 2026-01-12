from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    DateTime,
    Text
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Onboarding(Base):
    __tablename__ = "onboardings"

    id = Column(Integer, primary_key=True, index=True)

    # ---------- Personal Details ----------
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    gender = Column(String(20), nullable=False)
    marital_status = Column(String(50), nullable=True)

    father_name = Column(String(255), nullable=True)
    mother_name = Column(String(255), nullable=True)
    spouse_name = Column(String(255), nullable=True)

    blood_group = Column(String(10), nullable=True)

    # ---------- Contact Details ----------
    email = Column(String(150), nullable=False, index=True, unique=True)
    phone = Column(String(20), nullable=False, index=True)  # primary mobile
    landline_number = Column(String(20), nullable=True)

    emergency_contact1 = Column(String(20), nullable=False)
    emergency_contact2 = Column(String(20), nullable=True)

    # ---------- Address ----------
    communication_address = Column(Text, nullable=False)
    permanent_address = Column(Text, nullable=False)
    location = Column(String(100), nullable=False)

    # ---------- Government / Identity ----------
    aadhar_number = Column(String(20), nullable=False, unique=True)
    driving_license = Column(String(50), nullable=True)

    # ---------- Education & Application ----------
    education_qualification = Column(String(255), nullable=True)
    applied_role = Column(String(255), nullable=False)

    # ---------- Vehicle ----------
    vehicle_number = Column(String(50), nullable=True)

    # ---------- Employment Status ----------
    candidate_type = Column(String(20), nullable=False, index=True)  # fresher / experienced
    status = Column(String(20), nullable=False, default="pending", index=True)

    # ---------- Experienced Candidate Details ----------
    company_name = Column(String(255), nullable=True)
    job_role = Column(String(255), nullable=True)
    date_of_joining = Column(Date, nullable=True)
    date_of_exit = Column(Date, nullable=True)
    total_experience = Column(String(100), nullable=True)

    esi_number = Column(String(255), nullable=True)
    uan_number = Column(String(255), nullable=True)

    # ---------- Audit ----------
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

    # ---------- Relationships ----------
    documents = relationship(
        "OnboardingDocument",
        back_populates="onboarding",
        cascade="all, delete-orphan"
    )

    nominees = relationship(
        "OnboardingNominee",
        back_populates="onboarding",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    family = relationship(
        "OnboardingFamily",
        back_populates="onboarding",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    bank = relationship(
        "OnboardingBank",
        back_populates="onboarding",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    references = relationship(
        "OnboardingReference",
        back_populates="onboarding",
        cascade="all, delete-orphan",
        lazy="joined"
    )

    checklist = relationship(
        "OnboardingChecklist",
        back_populates="onboarding",
        uselist=False,
        cascade="all, delete-orphan"
    )
