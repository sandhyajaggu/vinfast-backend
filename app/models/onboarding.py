from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship 
from sqlalchemy.sql import func
from app.database import Base


class Onboarding(Base):
    __tablename__ = "onboardings"

    id = Column(Integer, primary_key=True, index=True)

    # ---------- Personal Details ----------
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(150), nullable=False, index=True)
    phone = Column(String(20), nullable=False, index=True)
    gender = Column(String(20), nullable=False)
    location = Column(String(100), nullable=False)

    # ---------- Status ----------
    candidate_type = Column(String(20), nullable=False, index=True)  # fresher / experienced
    status = Column(String(20), nullable=False, default="pending", index=True)

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
