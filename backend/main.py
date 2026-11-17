
import os
import time
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

from backend.inference import transcribe_audio
from backend.translation import translate_text


# ---------------- CONFIGURATION ----------------

app = FastAPI(title="NepTranscript API")

ALLOWED_EXTENSIONS = {
    ".wav",
    ".mp3",
    ".m4a",
    ".ogg",
    ".flac"
}


# ---------------- REQUEST MODEL ----------------

class TranslationRequest(BaseModel):
    text: str


# ---------------- HEALTH CHECK ----------------

@app.get("/health")
def health():

    return {
        "status": "healthy",
        "inference_mode": "cpu",
        "models": [
            "Whisper Small FFT",
            "NLLB-200"
        ]
    }


# ---------------- AUDIO TRANSCRIPTION ----------------

@app.post("/transcribe")
async def transcribe(file: UploadFile = File(...)):

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload an audio file."
        )

    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    temp_path = None

    try:

        audio_bytes = await file.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp:

            temp.write(audio_bytes)
            temp_path = temp.name

        print("Starting Nepali speech recognition...")

        result = transcribe_audio(temp_path)

        print("Transcription completed.")

        print(
            f"Transcription time: "
            f"{result['processing_time']} seconds"
        )

        return {
            "filename": file.filename,
            **result
        }

    except HTTPException:
        raise

    except Exception as e:

        print(f"Transcription error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Audio transcription failed."
        ) from e

    finally:

        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ---------------- ENGLISH TRANSLATION ----------------

@app.post("/translate")
def translate(request: TranslationRequest):

    if not request.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Please provide Nepali text to translate."
        )

    try:

        print("Starting English translation...")

        start_time = time.time()

        english_translation = translate_text(request.text)

        translation_time = time.time() - start_time

        print("Translation completed.")

        print(
            f"Translation time: {translation_time:.3f} seconds"
        )

        return {
            "english_translation": english_translation,
            "translation_time": round(translation_time, 3)
        }

    except Exception as e:

        print(f"Translation error: {e}")

        raise HTTPException(
            status_code=500,
            detail="English translation failed."
        ) from e
