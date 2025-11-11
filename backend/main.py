"""
Coffee Tester Feedback Collection API
FastAPI backend for voice-enabled coffee tasting feedback system
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
import uvicorn
from typing import Optional, List
from datetime import datetime

from database import init_db, get_db
from models import Session, Answer, Question
from schemas import (
    SessionCreate, SessionResponse, AnswerCreate, AnswerResponse,
    QuestionResponse, SessionComplete, FeedbackReport
)
from services import load_questions_from_csv, get_next_question, generate_pdf_report


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and load questions on startup"""
    await init_db()
    await load_questions_from_csv()
    yield


app = FastAPI(
    title="Coffee Feedback API",
    description="Voice-enabled coffee tasting feedback collection system",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration - Allow production URLs
import os
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Coffee Feedback API",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.post("/api/sessions/start", response_model=SessionResponse)
async def start_session(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Initialize a new feedback session"""
    from sqlalchemy import select
    
    new_session = Session(
        start_time=datetime.now(),
        status="active",
        tester_name=session_data.tester_name,
        coffee_sample=session_data.coffee_sample
    )
    db.add(new_session)
    await db.commit()
    await db.refresh(new_session)
    
    # Get first question
    first_question = await get_next_question(None, db)
    
    return SessionResponse(
        id=new_session.id,
        status=new_session.status,
        start_time=new_session.start_time,
        tester_name=new_session.tester_name,
        coffee_sample=new_session.coffee_sample,
        current_question=first_question
    )


@app.post("/api/feedback/answer", response_model=AnswerResponse)
async def submit_answer(
    answer_data: AnswerCreate,
    db: AsyncSession = Depends(get_db)
):
    """Submit an answer and get the next question"""
    from sqlalchemy import select
    
    # Verify session exists and is active
    result = await db.execute(select(Session).where(Session.id == answer_data.session_id))
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if session.status != "active":
        raise HTTPException(status_code=400, detail="Session is not active")
    
    # Save the answer
    new_answer = Answer(
        session_id=answer_data.session_id,
        question_id=answer_data.question_id,
        answer_text=answer_data.answer_text,
        answer_type=answer_data.answer_type,
        confidence_score=answer_data.confidence_score,
        timestamp=datetime.now()
    )
    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    
    # Get next question
    next_question = await get_next_question(answer_data.question_id, db, answer_data.answer_text)
    
    return AnswerResponse(
        id=new_answer.id,
        session_id=new_answer.session_id,
        question_id=new_answer.question_id,
        answer_text=new_answer.answer_text,
        timestamp=new_answer.timestamp,
        next_question=next_question
    )


@app.get("/api/questions/{question_id}", response_model=QuestionResponse)
async def get_question(question_id: str, db: AsyncSession = Depends(get_db)):
    """Fetch a specific question by ID"""
    from sqlalchemy import select
    
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return QuestionResponse(
        id=question.id,
        text=question.text,
        type=question.type,
        options=question.options,
        category=question.category,
        order_index=question.order_index
    )


@app.post("/api/sessions/{session_id}/complete", response_model=SessionResponse)
async def complete_session(
    session_id: int,
    completion_data: SessionComplete,
    db: AsyncSession = Depends(get_db)
):
    """Mark a session as complete"""
    from sqlalchemy import select
    
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    session.status = "completed"
    session.end_time = datetime.now()
    session.notes = completion_data.notes
    
    await db.commit()
    await db.refresh(session)
    
    return SessionResponse(
        id=session.id,
        status=session.status,
        start_time=session.start_time,
        end_time=session.end_time,
        tester_name=session.tester_name,
        coffee_sample=session.coffee_sample
    )


@app.get("/api/reports/{session_id}", response_model=FeedbackReport)
async def get_report(session_id: int, db: AsyncSession = Depends(get_db)):
    """Generate a feedback report for a session"""
    from sqlalchemy import select
    
    # Get session
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get all answers
    result = await db.execute(
        select(Answer).where(Answer.session_id == session_id).order_by(Answer.timestamp)
    )
    answers = result.scalars().all()
    
    # Format report data
    answers_data = [
        {
            "question_id": answer.question_id,
            "answer": answer.answer_text,
            "type": answer.answer_type,
            "confidence": answer.confidence_score,
            "timestamp": answer.timestamp.isoformat()
        }
        for answer in answers
    ]
    
    return FeedbackReport(
        session_id=session.id,
        tester_name=session.tester_name,
        coffee_sample=session.coffee_sample,
        start_time=session.start_time,
        end_time=session.end_time,
        status=session.status,
        answers=answers_data,
        total_answers=len(answers_data)
    )


@app.get("/api/sessions", response_model=List[SessionResponse])
async def list_sessions(
    limit: int = 50,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """List all feedback sessions"""
    from sqlalchemy import select
    
    query = select(Session).order_by(Session.start_time.desc()).limit(limit)
    
    if status:
        query = query.where(Session.status == status)
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    
    return [
        SessionResponse(
            id=session.id,
            status=session.status,
            start_time=session.start_time,
            end_time=session.end_time,
            tester_name=session.tester_name,
            coffee_sample=session.coffee_sample
        )
        for session in sessions
    ]


@app.get("/api/questions", response_model=List[QuestionResponse])
async def list_questions(db: AsyncSession = Depends(get_db)):
    """List all available questions"""
    from sqlalchemy import select
    
    result = await db.execute(select(Question).order_by(Question.order_index))
    questions = result.scalars().all()
    
    return [
        QuestionResponse(
            id=question.id,
            text=question.text,
            type=question.type,
            options=question.options,
            category=question.category,
            order_index=question.order_index
        )
        for question in questions
    ]


@app.post("/api/sessions/{session_id}/export-csv")
async def export_csv(session_id: int, db: AsyncSession = Depends(get_db)):
    """Export session feedback to CSV"""
    from services import export_session_to_csv
    import os
    
    filepath = await export_session_to_csv(session_id, db)
    if not filepath:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "status": "success", 
        "message": "CSV exported successfully",
        "filename": os.path.basename(filepath),
        "filepath": filepath
    }


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
