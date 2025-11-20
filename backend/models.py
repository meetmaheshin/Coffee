"""
SQLAlchemy database models
"""

from sqlalchemy import Column, Integer, String, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base


class Session(Base):
    """Feedback session model"""
    __tablename__ = "sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=True)
    status = Column(String(20), default="active")  # active, completed, abandoned
    tester_name = Column(String(100), nullable=True)
    coffee_sample = Column(String(100), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    answers = relationship("Answer", back_populates="session", cascade="all, delete-orphan")


class Answer(Base):
    """Answer model for storing user responses"""
    __tablename__ = "answers"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    question_id = Column(String(100), nullable=False)
    answer_text = Column(Text, nullable=False)
    matched_answer = Column(String(100), nullable=True)  # Store matched/corrected value
    answer_type = Column(String(20), default="voice")  # voice, click, text
    confidence_score = Column(Float, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    
    # Relationships
    session = relationship("Session", back_populates="answers")


class Question(Base):
    """Question model for storing questionnaire structure"""
    __tablename__ = "questions"
    
    id = Column(String(100), primary_key=True, index=True)
    text = Column(Text, nullable=False)
    type = Column(String(50), nullable=False)  # intro, single_choice, multiple_choice, rating, open
    option_groups = Column(JSON, nullable=True)  # JSON array of {title, options}
    category = Column(String(100), nullable=True)
    order_index = Column(Integer, default=0)
    parent_answer = Column(String(100), nullable=True)  # For conditional questions
