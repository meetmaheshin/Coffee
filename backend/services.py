"""
Business logic and helper services
"""

import csv
import os
from typing import Optional, Dict, List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import Question, Session, Answer
from schemas import QuestionResponse
from openai import AsyncOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv("OPENAI_API_KEY")
print(f"DEBUG: OpenAI API Key loaded: {api_key[:20] if api_key else 'NOT FOUND'}...")
openai_client = AsyncOpenAI(api_key=api_key)


# Question flow logic based on the CSV data
QUESTION_FLOW = {
    # No welcome question - start directly with flavor
    "flavor_main": {
        "next_map": {
            "Fruity": "flavor_fruity",
            "Floral": "flavor_floral",
            "Nutty": "flavor_nutty",
            "Cereal": "flavor_cereal",
            "Cocoa": "flavor_cocoa",
            "Sweet": "flavor_sweet",
            "Earthy": "flavor_earthy",
            "Roasted": "flavor_roasted",
            "Spices": "flavor_spices",
            "Vegetative": "flavor_vegetative",
            "Stale/Papery": "flavor_stale_papery",
            "Chemical": "flavor_chemical",
            "Alcohol/Fermented": "flavor_alcohol_fermented",
            "None": "intensity",
            "Not Applicable": "intensity"
        }
    },
    # After each specific flavor, end the questionnaire
    "flavor_fruity": {"next": None},
    "flavor_floral": {"next": None},
    "flavor_nutty": {"next": None},
    "flavor_cereal": {"next": None},
    "flavor_cocoa": {"next": None},
    "flavor_sweet": {"next": None},
    "flavor_earthy": {"next": None},
    "flavor_roasted": {"next": None},
    "flavor_spices": {"next": None},
    "flavor_vegetative": {"next": None},
    "flavor_stale_papery": {"next": None},
    "flavor_chemical": {"next": None},
    "flavor_alcohol_fermented": {"next": None}
}


async def match_answer_with_ai(user_answer: str, available_options: List[str]) -> Optional[str]:
    """
    Use OpenAI to intelligently match user's answer to available options.
    Handles misspellings, variations, and natural language.
    
    Examples:
    - "frooti" -> "Fruity"
    - "chocolate flavor" -> "Cocoa"
    - "earthy taste" -> "Earthy"
    """
    try:
        print(f"DEBUG AI: Trying to match '{user_answer}' against {len(available_options)} options")
        print(f"DEBUG AI: Options: {available_options[:5]}..." if len(available_options) > 5 else f"DEBUG AI: Options: {available_options}")
        
        # Create prompt for GPT
        prompt = f"""You are a coffee tasting assistant helping with voice recognition. Match the user's spoken answer to one of the available options.

User said: "{user_answer}"

Available options:
{chr(10).join(f'- {opt}' for opt in available_options)}

IMPORTANT RULES:
1. Be VERY LENIENT - match similar sounding words
2. Handle misspellings: "frooti" → "Fruity", "serial" → "Cereal", "arthi" → "Earthy"
3. Handle variations: "chocolate" → "Cocoa", "flowers" → "Floral", "nuts" → "Nutty"
4. Match phonetically similar words: "roasty" → "Roasted", "spicy" → "Spices"
5. EXTRACT keywords from longer answers: "it was roasted" → "Roasted", "I taste fruity flavor" → "Fruity"
6. Find the matching word ANYWHERE in the user's sentence
7. ALWAYS try to find the closest match - only return "NONE" if completely unrelated

Return ONLY the exact option name from the list above, nothing else."""

        print(f"DEBUG AI: Calling OpenAI API...")
        response = await openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a precise text matcher. Return only the matched option name or NONE."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,  # Deterministic
            max_tokens=50
        )
        
        print(f"DEBUG AI: Got response from OpenAI")
        matched_option = response.choices[0].message.content.strip()
        print(f"DEBUG AI: AI suggested: '{matched_option}'")
        
        # Validate that the matched option is actually in the list
        if matched_option == "NONE":
            print(f"DEBUG AI: AI returned NONE - no match found")
            return None
        
        # Case-insensitive check
        for option in available_options:
            if option.lower() == matched_option.lower():
                print(f"AI matched '{user_answer}' -> '{option}'")
                return option
        
        # If exact match not found, try fuzzy
        for option in available_options:
            if matched_option.lower() in option.lower() or option.lower() in matched_option.lower():
                print(f"AI fuzzy matched '{user_answer}' -> '{option}' (via {matched_option})")
                return option
        
        print(f"AI returned '{matched_option}' but not in options list")
        return None
        
    except Exception as e:
        print(f"AI matching error: {e}")
        return None


async def load_questions_from_csv():
    """Load questions from CSV file and populate database"""
    from database import get_async_engine_and_session
    _, async_session_maker = get_async_engine_and_session()
    
    csv_path = os.path.join(os.path.dirname(__file__), "..", "Flavor.csv")
    
    # Parse CSV to create flavor categories
    flavor_categories = {}
    
    try:
        with open(csv_path, 'r', encoding='utf-8-sig') as file:  # utf-8-sig strips BOM
            reader = csv.DictReader(file)
            print(f"DEBUG: CSV columns: {reader.fieldnames}")
            row_count = 0
            for row in reader:
                row_count += 1
                flavor_type = row.get('Fruity Types', '').strip()
                sensory_group = row.get('Sensory Group', '').strip()
                
                if row_count <= 3:
                    print(f"DEBUG: Row {row_count}: flavor_type='{flavor_type}', sensory_group='{sensory_group}'")
                
                if sensory_group and flavor_type and flavor_type != sensory_group:
                    if sensory_group not in flavor_categories:
                        flavor_categories[sensory_group] = []
                        print(f"DEBUG: Created category '{sensory_group}'")
                    if flavor_type not in flavor_categories[sensory_group]:
                        flavor_categories[sensory_group].append(flavor_type)
            print(f"DEBUG: Processed {row_count} rows from CSV")
    except FileNotFoundError:
        print(f"Warning: Flavor.csv not found at {csv_path}")
        flavor_categories = {}
    except Exception as e:
        print(f"ERROR parsing CSV: {e}")
        flavor_categories = {}
    
    # Define all questions
    questions_data = [
        {
            "id": "flavor_main",
            "text": "What is the primary flavor profile you detect?",
            "type": "single_choice",
            "options": ["Fruity", "Floral", "Nutty", "Cereal", "Cocoa", "Sweet", "Earthy", 
                       "Roasted", "Spices", "Vegetative", "Stale/Papery", "Chemical", 
                       "Alcohol/Fermented", "None", "Not Applicable"],
            "category": "Flavor",
            "order_index": 1
        }
    ]
    
    # Add specific flavor questions from CSV
    order_idx = 2
    print(f"DEBUG: Found {len(flavor_categories)} flavor categories from CSV")
    for category, flavors in flavor_categories.items():
        question_id = f"flavor_{category.lower().replace('/', '_').replace(' ', '_')}"
        print(f"DEBUG: Creating question {question_id} with {len(flavors)} options")
        questions_data.append({
            "id": question_id,
            "text": f"Which specific {category} notes do you detect?",
            "type": "multiple_choice",
            "options": flavors,
            "category": category,
            "order_index": order_idx
        })
        order_idx += 1
    
    # Insert questions into database
    async with async_session_maker() as session:
        # Check if questions already exist
        result = await session.execute(select(Question).limit(1))
        existing = result.scalar_one_or_none()
        
        if not existing:
            print(f"DEBUG: Loading {len(questions_data)} questions into database...")
            for q_data in questions_data:
                # Convert flat options to option_groups format
                option_groups = []
                if q_data.get('options'):
                    option_groups = [{"title": "", "options": q_data['options']}]
                
                question = Question(
                    id=q_data['id'],
                    text=q_data['text'],
                    type=q_data['type'],
                    option_groups=option_groups,
                    category=q_data.get('category'),
                    order_index=q_data.get('order_index', 0)
                )
                session.add(question)
            
            await session.commit()
            print(f"✅ Loaded {len(questions_data)} questions into database")
        else:
            print(f"DEBUG: Database already has questions, skipping load")


async def get_next_question(
    current_question_id: Optional[str],
    db: AsyncSession,
    current_answer: Optional[str] = None
) -> Optional[QuestionResponse]:
    """
    Get the next question based on the current question and answer
    """
    if current_question_id is None:
        # Check if there are admin questions - if so, use them instead of CSV questions
        admin_questions = await db.execute(
            select(Question)
            .where(Question.id.not_in(list(QUESTION_FLOW.keys())))
            .where(Question.id != "flavor_main")
            .order_by(Question.order_index)
        )
        admin_question = admin_questions.first()

        if admin_question:
            # Use admin questions instead of CSV questions
            print(f"DEBUG: Found admin questions, using them instead of CSV flow")
            question = admin_question[0]
        else:
            # No admin questions, use the default CSV flow
            result = await db.execute(select(Question).where(Question.id == "flavor_main"))
            question = result.scalar_one_or_none()
    else:
        # Check if current question is an admin question
        is_admin_question = current_question_id not in QUESTION_FLOW

        if is_admin_question:
            # Handle admin question flow
            print(f"DEBUG: {current_question_id} is an admin question, finding next in sequence")
            admin_questions = await db.execute(
                select(Question)
                .where(Question.id.not_in(list(QUESTION_FLOW.keys())))
                .where(Question.id != "flavor_main")
                .order_by(Question.order_index)
            )
            admin_qs = admin_questions.scalars().all()

            # Find current question index and get next one
            current_idx = next((i for i, q in enumerate(admin_qs) if q.id == current_question_id), -1)
            if current_idx >= 0 and current_idx + 1 < len(admin_qs):
                next_id = admin_qs[current_idx + 1].id
                print(f"DEBUG: Next admin question: {next_id}")
                result = await db.execute(select(Question).where(Question.id == next_id))
                question = result.scalar_one_or_none()
            else:
                print(f"DEBUG: No more admin questions after {current_question_id}")
                return None  # End of questionnaire
        else:
            # Handle CSV question flow
            flow = QUESTION_FLOW.get(current_question_id, {})

            # Check if there's a conditional next based on answer
            if "next_map" in flow and current_answer:
                # Try exact match first
                next_id = flow["next_map"].get(current_answer)

                # If no exact match, try simple fuzzy matching (singular/plural, case-insensitive)
                if not next_id:
                    answer_lower = current_answer.lower().strip()
                    for key, value in flow["next_map"].items():
                        key_lower = key.lower().strip()
                        # Check if answer matches key (with or without 's', 'ies', etc.)
                        if (answer_lower == key_lower or
                            answer_lower == key_lower.rstrip('s') or
                            answer_lower + 's' == key_lower or
                            answer_lower + 'es' == key_lower):
                            next_id = value
                            print(f"DEBUG: Fuzzy matched '{current_answer}' to '{key}' -> {next_id}")
                            break

                # If still no match, use AI to intelligently match
                if not next_id and os.getenv("OPENAI_API_KEY"):
                    print(f"DEBUG: No fuzzy match, trying AI matching...")
                    available_options = list(flow["next_map"].keys())
                    matched_option = await match_answer_with_ai(current_answer, available_options)

                    if matched_option:
                        next_id = flow["next_map"].get(matched_option)
                        print(f"DEBUG: AI matched '{current_answer}' to '{matched_option}' -> {next_id}")
                    else:
                        print(f"DEBUG: AI could not match '{current_answer}' to any option")

                print(f"DEBUG: current_question={current_question_id}, answer={current_answer}, next_id={next_id}")
            else:
                next_id = flow.get("next")
                print(f"DEBUG: current_question={current_question_id}, no answer mapping, next_id={next_id}")

            if next_id is None:
                print(f"DEBUG: No next question found for {current_question_id}")
                # Check if there are admin questions to show after CSV flow
                admin_questions = await db.execute(
                    select(Question)
                    .where(Question.id.not_in(list(QUESTION_FLOW.keys())))
                    .where(Question.id != "flavor_main")
                    .order_by(Question.order_index)
                )
                admin_question = admin_questions.first()
                if admin_question:
                    next_id = admin_question[0].id
                    print(f"DEBUG: Found admin question to show after CSV flow: {next_id}")
                else:
                    return None  # End of questionnaire

            result = await db.execute(select(Question).where(Question.id == next_id))
            question = result.scalar_one_or_none()

            if not question:
                print(f"DEBUG: Question {next_id} not found in database!")
            else:
                print(f"DEBUG: Found question: {question.id} - {question.text}")

    if question:
        # Extract options from all option groups
        all_options = []
        for group in (question.option_groups or []):
            all_options.extend(group.get('options', []))

        return QuestionResponse(
            id=question.id,
            text=question.text,
            type=question.type,
            options=all_options,  # Keep flattened options for backward compatibility
            optionGroups=question.option_groups,  # Add structured groups
            category=question.category,
            order_index=question.order_index
        )

    return None


def generate_pdf_report(session_data: Dict) -> bytes:
    """
    Generate a PDF report for a feedback session
    """
    from reportlab.lib.pagesizes import letter
    from reportlab.lib import colors
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.units import inch
    from io import BytesIO
    
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#6F4E37'),
        spaceAfter=30,
    )
    
    elements.append(Paragraph("Coffee Tasting Feedback Report", title_style))
    elements.append(Spacer(1, 0.2*inch))
    
    # Session info
    info_data = [
        ["Tester Name:", session_data.get('tester_name', 'N/A')],
        ["Coffee Sample:", session_data.get('coffee_sample', 'N/A')],
        ["Date:", session_data.get('start_time', 'N/A')],
        ["Session ID:", str(session_data.get('session_id', 'N/A'))],
    ]
    
    info_table = Table(info_data, colWidths=[2*inch, 4*inch])
    info_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#F5E6D3')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    elements.append(info_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Build the PDF
    doc.build(elements)
    
    pdf_bytes = buffer.getvalue()
    buffer.close()
    
    return pdf_bytes


async def export_session_to_csv(session_id: int, db: AsyncSession) -> str:
    """
    Export a session's feedback to CSV file
    """
    import csv
    import os
    from datetime import datetime
    
    # Get session and answers
    result = await db.execute(
        select(Session).where(Session.id == session_id)
    )
    session = result.scalar_one_or_none()
    
    if not session:
        return None
    
    result = await db.execute(
        select(Answer).where(Answer.session_id == session_id).order_by(Answer.timestamp)
    )
    answers = result.scalars().all()
    
    # Create exports directory if it doesn't exist
    export_dir = os.path.join(os.path.dirname(__file__), "..", "exports")
    os.makedirs(export_dir, exist_ok=True)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"feedback_session_{session_id}_{timestamp}.csv"
    filepath = os.path.join(export_dir, filename)
    
    # Write to CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            'Session ID', 'Tester Name', 'Coffee Sample', 
            'Question ID', 'Answer', 'Answer Type', 'Confidence',
            'Timestamp'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for answer in answers:
            writer.writerow({
                'Session ID': session.id,
                'Tester Name': session.tester_name or 'Anonymous',
                'Coffee Sample': session.coffee_sample or 'Not specified',
                'Question ID': answer.question_id,
                'Answer': answer.answer_text,
                'Answer Type': answer.answer_type,
                'Confidence': answer.confidence_score if answer.confidence_score else 'N/A',
                'Timestamp': answer.timestamp.isoformat()
            })
    
    return filepath
