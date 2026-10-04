from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from services.pdf_processor import extract_text_from_pdf
from services.ai_generator import generate_podcast_script
from services.tts_generator import generate_podcast_audio

import tempfile
import os


app = FastAPI(
    title="PodForge AI",
    description="Turn documents into AI-powered podcasts.",
    version="1.0.0"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

allowed_origins = [
    "http://localhost:5173",
]

frontend_url = os.getenv("FRONTEND_URL")

if frontend_url:
    allowed_origins.append(frontend_url)


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Paths
# --------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "outputs")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# --------------------------------------------------
# Basic routes
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "PodForge AI backend is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# --------------------------------------------------
# PDF upload and text extraction
# --------------------------------------------------

@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    contents = await file.read()

    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        result = extract_text_from_pdf(temp_path)

        return {
            "filename": file.filename,
            "pages": result["pages"],
            "words": result["words"],
            "characters": result["characters"],
            "text_preview": result["text"][:2000]
        }

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# --------------------------------------------------
# Generate podcast script
# --------------------------------------------------

@app.post("/generate-podcast")
async def generate_podcast(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    contents = await file.read()
    temp_path = None

    try:
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_path = temp_file.name

        result = extract_text_from_pdf(temp_path)

        if not result["text"]:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF."
            )

        podcast_script = generate_podcast_script(
            result["text"]
        )

        return {
            "filename": file.filename,
            "pages": result["pages"],
            "words": result["words"],
            "characters": result["characters"],
            "podcast_script": podcast_script
        }

    except HTTPException:
        raise

    except Exception as error:
        print(
            f"Podcast generation error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate the podcast script."
        )

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# --------------------------------------------------
# Generate podcast + audio
# --------------------------------------------------

@app.post("/generate-podcast-audio")
async def generate_podcast_audio_endpoint(
    file: UploadFile = File(...)
):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    contents = await file.read()
    temp_pdf = None

    try:
        # Save uploaded PDF temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".pdf"
        ) as temp_file:

            temp_file.write(contents)
            temp_pdf = temp_file.name

        # Extract PDF text
        result = extract_text_from_pdf(temp_pdf)

        if not result["text"]:
            raise HTTPException(
                status_code=400,
                detail="Could not extract text from this PDF."
            )

        # Generate podcast script with Gemini
        podcast_script = generate_podcast_script(
            result["text"]
        )

        # Generate podcast audio with Kokoro
        output_path = os.path.join(
            OUTPUT_DIR,
            "podcast.wav"
        )

        generate_podcast_audio(
            podcast_script,
            output_path
        )

        return {
            "filename": file.filename,
            "pages": result["pages"],
            "words": result["words"],
            "characters": result["characters"],
            "podcast_script": podcast_script,
            "audio_url": "/podcast-audio"
        }

    except HTTPException:
        raise

    except Exception as error:
        print(
            f"Podcast audio generation error: {error}"
        )

        raise HTTPException(
            status_code=500,
            detail="Failed to generate podcast audio."
        )

    finally:
        if temp_pdf and os.path.exists(temp_pdf):
            os.remove(temp_pdf)


# --------------------------------------------------
# Serve generated podcast audio
# --------------------------------------------------

@app.get("/podcast-audio")
def get_podcast_audio():

    audio_path = os.path.join(
        OUTPUT_DIR,
        "podcast.wav"
    )

    if not os.path.exists(audio_path):
        raise HTTPException(
            status_code=404,
            detail="Podcast audio has not been generated yet."
        )

    return FileResponse(
        audio_path,
        media_type="audio/wav",
        filename="podcast.wav"
    )