# app/models/onboarding_nominee.py

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class OnboardingNominee(Base):
    __tablename__ = "onboarding_nominees"

    id = Column(Integer, primary_key=True)
    onboarding_id = Column(
        Integer,
        ForeignKey("onboardings.id", ondelete="CASCADE"),
        nullable=False
    )

    nominee_type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    relationship_type = Column(String(50), nullable=False)

    onboarding = relationship("Onboarding", back_populates="nominees")


class OnboardingFamily(Base):
    __tablename__ = "onboarding_family"

    id = Column(Integer, primary_key=True)
    onboarding_id = Column(
        Integer,
        ForeignKey("onboardings.id", ondelete="CASCADE"),
        nullable=False
    )

    name = Column(String(100), nullable=False)
    dob = Column(Date, nullable=False)
    relationship_type = Column(String(50), nullable=False)

    onboarding = relationship("Onboarding", back_populates="family")


class OnboardingBank(Base):
    __tablename__ = "onboarding_bank"

    id = Column(Integer, primary_key=True)
    onboarding_id = Column(
        Integer,
        ForeignKey("onboardings.id", ondelete="CASCADE"),
        nullable=False,
        unique=True
    )

    account_name = Column(String(150), nullable=False)
    account_number = Column(String(50), nullable=False)
    ifsc_code = Column(String(20), nullable=False)
    branch_name = Column(String(100), nullable=False)

    onboarding = relationship("Onboarding", back_populates="bank")


class OnboardingReference(Base):
    __tablename__ = "onboarding_references"

    id = Column(Integer, primary_key=True)
    onboarding_id = Column(
        Integer,
        ForeignKey("onboardings.id", ondelete="CASCADE"),
        nullable=False
    )

    reference_type = Column(String(50), nullable=False)
    name = Column(String(100), nullable=False)
    designation_or_occupation = Column(String(100))
    phone = Column(String(20))
    email = Column(String(150))
    last_employer = Column(String(150))

    onboarding = relationship("Onboarding", back_populates="references")
