from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
import os
import uuid
from typing import List, Optional

from app.core.transcriber import transcribe_audio
from app.core.summarizer import summarize_transcript
from app.core.pdf_generator import generate_pdf
from app.models.database import (
    save_transcription, 
    get_transcription, 
    search_transcriptions,
    get_all_transcriptions
)

# Create upload directory
os.makedirs("uploads", exist_ok=True)

api_router = APIRouter()

@api_router.post("/upload")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload audio file and transcribe it.
    """
    # Generate unique filename
    file_extension = os.path.splitext(file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join("uploads", unique_filename)
    
    # Save uploaded file
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    try:
        # Transcribe audio
        transcript, language = transcribe_audio(file_path)
        
        # Summarize transcript
        result = summarize_transcript(transcript)
        summary = result["summary"]
        action_items = result["action_items"]
        
        # Save to database
        transcription_id = save_transcription(
            filename=file.filename,
            language=language,
            transcript=transcript,
            summary=summary,
            action_items=action_items
        )
        
        return {
            "id": transcription_id,
            "filename": file.filename,
            "language": language,
            "transcript": transcript,
            "summary": summary,
            "action_items": action_items
        }
    except Exception as e:
        # Clean up the file if processing fails
        if os.path.exists(file_path):
            os.unlink(file_path)
        raise HTTPException(status_code=500, detail=str(e))

@api_router.get("/transcriptions/{transcription_id}")
async def get_transcription_by_id(transcription_id: int):
    """
    Get a specific transcription by ID.
    """
    transcription = get_transcription(transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")
    return transcription

@api_router.get("/transcriptions")
async def list_transcriptions():
    """
    Get all transcriptions.
    """
    return get_all_transcriptions()

@api_router.get("/search")
async def search(query: str):
    """
    Search transcriptions by query.
    """
    return search_transcriptions(query)

@api_router.get("/export/{transcription_id}")
async def export_pdf(transcription_id: int):
    """
    Export a transcription as PDF.
    """
    transcription = get_transcription(transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")
    
    # Generate PDF
    pdf_path = generate_pdf(
        transcript=transcription["transcript"],
        summary=transcription["summary"],
        action_items=transcription.get("action_items", []),
        filename=f"transcript_{transcription_id}.pdf"
    )
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"transcript_{transcription_id}.pdf"
    )