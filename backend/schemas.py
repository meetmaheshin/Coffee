"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

# ElevenLabs TTS request schema
class TTSRequest(BaseModel):
    text: str
    voice_id: Optional[str] = None  # Optional: allow custom voice


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
    optionGroups: Optional[List[Dict[str, Any]]] = None
    category: Optional[str] = None
    order_index: int


# New schema for merged questions
class MergedFlavorQuestionsResponse(BaseModel):
    primary_question: QuestionResponse
    specific_question: QuestionResponse


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
    matched_answer: Optional[str] = None
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
    answers: List[Dict[str, Any]]  # Each answer dict includes: question_id, answer, matched_answer, type, confidence, timestamp
    total_answers: int


class OptionGroup(BaseModel):
    title: str
    options: List[str]

class AdminQuestionIn(BaseModel):
    id: str
    text: str
    type: str
    optionGroups: Optional[List[OptionGroup]] = None
    category: Optional[str] = None
    order_index: Optional[int] = 0
