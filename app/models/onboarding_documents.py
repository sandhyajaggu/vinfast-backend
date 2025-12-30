from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class OnboardingDocument(Base):
    __tablename__ = "onboarding_documents"

    id = Column(Integer, primary_key=True)
    onboarding_id = Column(
        Integer,
        ForeignKey("onboardings.id", ondelete="CASCADE"),
        nullable=False
    )

    document_type = Column(String(50), nullable=False)
    file_path = Column(String(255), nullable=False)

    onboarding = relationship("Onboarding", back_populates="documents")
