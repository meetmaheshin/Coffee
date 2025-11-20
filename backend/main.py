import requests
# ElevenLabs TTS endpoint
from schemas import TTSRequest, OptionGroup
"""
Coffee Tester Feedback Collection API
FastAPI backend for voice-enabled coffee tasting feedback system
"""

from fastapi import FastAPI, HTTPException, Depends, Response
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
    QuestionResponse, SessionComplete, FeedbackReport, MergedFlavorQuestionsResponse
)
from sqlalchemy import select
from services import load_questions_from_csv, get_next_question, generate_pdf_report


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database and load questions on startup"""
    await init_db()
    # Only load questions if database is empty
    from services import load_questions_from_csv
    from sqlalchemy import select
    from database import get_async_engine_and_session
    _, async_session_maker = get_async_engine_and_session()
    async with async_session_maker() as session:
        result = await session.execute(select(Question).limit(1))
        existing = result.scalar_one_or_none()
        if not existing:
            await load_questions_from_csv()
    yield



app = FastAPI(
    title="Coffee Feedback API",
    description="Voice-enabled coffee tasting feedback collection system",
    version="1.0.0",
    lifespan=lifespan
)


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

# CORS configuration - Allow production URLs
import os
import hashlib
allowed_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:5174").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/tts")
async def tts_11labs(request: TTSRequest):
    """
    Convert text to speech using ElevenLabs API and return audio (mp3), with caching.
    """
    import sys
    api_key = os.getenv("ELEVENLABS_API_KEY")
    print(f"[TTS DEBUG] ELEVENLABS_API_KEY loaded: {api_key[:8] if api_key else 'NOT FOUND'}...", file=sys.stderr)
    print(f"[TTS DEBUG] Request text: {request.text}", file=sys.stderr)
    if not api_key:
        print("[TTS DEBUG] ELEVENLABS_API_KEY not set in environment", file=sys.stderr)
        raise HTTPException(status_code=500, detail="ELEVENLABS_API_KEY not set in environment")


    voice_id = request.voice_id or "gfRt6Z3Z8aTbpLfexQ7N"  # Default voice
    cache_key = hashlib.sha256((request.text + "|" + voice_id).encode("utf-8")).hexdigest()
    cache_dir = os.path.join(os.path.dirname(__file__), "tts_cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"{cache_key}.mp3")

    # Extra debug logging
    print(f"[TTS DEBUG] text: {request.text}", file=sys.stderr)
    print(f"[TTS DEBUG] voice_id: {voice_id}", file=sys.stderr)
    print(f"[TTS DEBUG] cache_key: {cache_key}", file=sys.stderr)
    print(f"[TTS DEBUG] cache_path: {cache_path}", file=sys.stderr)

    # Serve from cache if exists
    if os.path.exists(cache_path):
        print(f"[TTS CACHE] Serving cached audio: {cache_path}", file=sys.stderr)
        with open(cache_path, "rb") as f:
            audio_data = f.read()
        return Response(content=audio_data, media_type="audio/mpeg")

    # Otherwise, call ElevenLabs API
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": request.text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        print(f"[TTS DEBUG] ElevenLabs response status: {response.status_code}", file=sys.stderr)
        if response.status_code != 200:
            print(f"[TTS DEBUG] ElevenLabs response text: {response.text}", file=sys.stderr)
            raise HTTPException(status_code=500, detail=f"TTS failed: {response.text}")
        # Save to cache
        with open(cache_path, "wb") as f:
            f.write(response.content)
        print(f"[TTS CACHE] Saved audio to cache: {cache_path}", file=sys.stderr)
        return Response(content=response.content, media_type="audio/mpeg")
    except Exception as e:
        print(f"[TTS DEBUG] Exception: {str(e)}", file=sys.stderr)
        raise HTTPException(status_code=500, detail=f"TTS error: {str(e)}")
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
    
    # Use AI to match/correct answer (if possible)
    from services import match_answer_with_ai
    # Get options for this question
    result = await db.execute(select(Question).where(Question.id == answer_data.question_id))
    question = result.scalar_one_or_none()
    matched = None
    if question and question.option_groups:
        # Extract options from all option groups
        available_options = []
        for group in question.option_groups:
            available_options.extend(group.get('options', []))
        matched = await match_answer_with_ai(answer_data.answer_text, available_options)
    # Save the answer
    new_answer = Answer(
        session_id=answer_data.session_id,
        question_id=answer_data.question_id,
        answer_text=answer_data.answer_text,
        matched_answer=matched,
        answer_type=answer_data.answer_type,
        confidence_score=answer_data.confidence_score,
        timestamp=datetime.now()
    )
    db.add(new_answer)
    await db.commit()
    await db.refresh(new_answer)
    # Get next question
    next_question = await get_next_question(answer_data.question_id, db, matched or answer_data.answer_text)
    return AnswerResponse(
        id=new_answer.id,
        session_id=new_answer.session_id,
        question_id=new_answer.question_id,
        answer_text=new_answer.answer_text,
        matched_answer=new_answer.matched_answer,
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
        options=[opt for group in (question.option_groups or []) for opt in group.get('options', [])],
        optionGroups=question.option_groups,
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
    
    # Format report data, include matched_answer
    answers_data = [
        {
            "question_id": answer.question_id,
            "answer": answer.answer_text,
            "matched_answer": answer.matched_answer,
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



# --- Admin Question Management Endpoints ---
from fastapi import status as http_status
from pydantic import BaseModel
from typing import Optional, List

class AdminQuestionIn(BaseModel):
    id: str
    text: str
    type: str
    optionGroups: Optional[List[OptionGroup]] = None
    category: Optional[str] = None
    order_index: Optional[int] = 0

@app.get("/api/admin/questions")
async def admin_list_questions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).order_by(Question.order_index))
    questions = result.scalars().all()
    return [
        {
            "id": q.id,
            "text": q.text,
            "type": q.type,
            "optionGroups": q.option_groups or [],
            "category": q.category,
            "order_index": q.order_index
        } for q in questions
    ]

@app.post("/api/admin/questions", status_code=http_status.HTTP_201_CREATED)
async def admin_create_question(q: AdminQuestionIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).where(Question.id == q.id))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Question ID already exists")
    question = Question(
        id=q.id,
        text=q.text,
        type=q.type,
        option_groups=[group.dict() for group in (q.optionGroups or [])],
        category=q.category,
        order_index=q.order_index or 0
    )
    db.add(question)
    await db.commit()
    await db.refresh(question)
    return {"status": "created", "id": question.id}

@app.put("/api/admin/questions/{question_id}")
async def admin_update_question(question_id: str, q: AdminQuestionIn, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    question.text = q.text
    question.type = q.type
    question.option_groups = [group.dict() for group in (q.optionGroups or [])]
    question.category = q.category
    question.order_index = q.order_index or 0
    await db.commit()
    await db.refresh(question)
    return {"status": "updated", "id": question.id}

@app.delete("/api/admin/questions/{question_id}")
async def admin_delete_question(question_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Question).where(Question.id == question_id))
    question = result.scalar_one_or_none()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    await db.delete(question)
    await db.commit()
    return {"status": "deleted", "id": question_id}

@app.get("/api/sessions/{session_id}/next", response_model=QuestionResponse)
async def get_next_question_endpoint(session_id: int, db: AsyncSession = Depends(get_db)):
    """Get the next question for a session (fallback endpoint)"""
    from sqlalchemy import select
    
    # Get session
    result = await db.execute(select(Session).where(Session.id == session_id))
    session = result.scalar_one_or_none()
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get next question (first if none answered yet)
    question = await get_next_question(None, db)
    
    return QuestionResponse(
        id=question.id,
        text=question.text,
        type=question.type,
        options=[opt for group in (question.option_groups or []) for opt in group.get('options', [])],
        optionGroups=question.option_groups,
        category=question.category,
        order_index=question.order_index
    )

@app.post("/api/sessions", response_model=SessionResponse)
async def start_session_alias(
    session_data: SessionCreate,
    db: AsyncSession = Depends(get_db)
):
    """Alias for start_session"""
    return await start_session(session_data, db)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
