"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class SessionCreate(BaseModel):
    """Schema for creating a new session"""
    tester_name: Optional[str] = None
    coffee_sample: Optional[str] = None


class QuestionResponse(BaseModel):
    """Schema for question response"""
    id: str
    text: str
    type: str
    options: Optional[List[str]] = None
    category: Optional[str] = None
    order_index: int


class SessionResponse(BaseModel):
    """Schema for session response"""
    id: int
    status: str
    start_time: datetime
    end_time: Optional[datetime] = None
    tester_name: Optional[str] = None
    coffee_sample: Optional[str] = None
    current_question: Optional[QuestionResponse] = None
    
    class Config:
        from_attributes = True


class AnswerCreate(BaseModel):
    """Schema for creating an answer"""
    session_id: int
    question_id: str
    answer_text: str
    answer_type: str = "voice"  # voice, click, text
    confidence_score: Optional[float] = None


class AnswerResponse(BaseModel):
    """Schema for answer response"""
    id: int
    session_id: int
    question_id: str
    answer_text: str
    timestamp: datetime
    next_question: Optional[QuestionResponse] = None
    
    class Config:
        from_attributes = True


class SessionComplete(BaseModel):
    """Schema for completing a session"""
    notes: Optional[str] = None


class FeedbackReport(BaseModel):
    """Schema for feedback report"""
    session_id: int
    tester_name: Optional[str]
    coffee_sample: Optional[str]
    start_time: datetime
    end_time: Optional[datetime]
    status: str
    answers: List[Dict[str, Any]]
    total_answers: int
