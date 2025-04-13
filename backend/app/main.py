# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

# from app.api.routes import api_router
# from app.models.database import init_db

# app = FastAPI(title="Multilingual Note-Taking AI")

# # Configure CORS
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # Include API routes
# app.include_router(api_router)

# @app.on_event("startup")
# async def startup_event():
#     # Initialize database on startup
#     init_db()

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)










from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import os
import uuid
import shutil

from app.models.database import init_db, save_transcription, get_transcription, search_transcriptions, get_all_transcriptions
from app.core.transcriber import transcribe_audio
from app.core.summarizer import summarize_transcript
from app.core.pdf_generator import generate_pdf

# Create necessary directories
os.makedirs("uploads", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

app = FastAPI(title="Multilingual Note-Taking AI")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    # Initialize database on startup
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Multilingual Note-Taking AI API"}

@app.post("/upload")
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
        shutil.copyfileobj(file.file, f)
    
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

@app.get("/transcriptions/{transcription_id}")
async def get_transcription_by_id(transcription_id: int):
    """
    Get a specific transcription by ID.
    """
    transcription = get_transcription(transcription_id)
    if not transcription:
        raise HTTPException(status_code=404, detail="Transcription not found")
    return transcription

@app.get("/transcriptions")
async def list_transcriptions():
    """
    Get all transcriptions.
    """
    return get_all_transcriptions()

@app.get("/search")
async def search(query: str):
    """
    Search transcriptions by query.
    """
    return search_transcriptions(query)

@app.get("/export/{transcription_id}")
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)