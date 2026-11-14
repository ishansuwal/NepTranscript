
import os
import time
import tempfile

from fastapi import FastAPI, UploadFile, File, HTTPException

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

    request_start_time = time.time()

    # Validate filename
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Please upload an audio file."
        )

    # Validate audio extension
    extension = os.path.splitext(file.filename)[1].lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio format."
        )

    temp_path = None

    try:

        # Read uploaded audio
        audio_bytes = await file.read()

        if not audio_bytes:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty."
            )

        # Save uploaded audio temporarily
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp:

            temp.write(audio_bytes)
            temp_path = temp.name

        # ---------------- STEP 1: WHISPER ASR ----------------

        print("Starting Nepali speech recognition...")

        result = transcribe_audio(temp_path)

        print("Transcription completed.")

        # ---------------- STEP 2: NLLB TRANSLATION ----------------

        print("Starting English translation...")

        translation_start_time = time.time()

        english_translation = translate_text(
            result["nepali_transcription"]
        )

        translation_time = (
            time.time() - translation_start_time
        )

        print("Translation completed.")

        # ---------------- STEP 3: PERFORMANCE METRICS ----------------

        total_processing_time = (
            time.time() - request_start_time
        )

        result["english_translation"] = english_translation

        result["translation_time"] = round(
            translation_time, 3
        )

        result["total_processing_time"] = round(
            total_processing_time, 3
        )

        print(
            f"Transcription time: "
            f"{result['processing_time']} seconds"
        )

        print(
            f"Translation time: "
            f"{result['translation_time']} seconds"
        )

        print(
            f"Total processing time: "
            f"{result['total_processing_time']} seconds"
        )

        # ---------------- STEP 4: API RESPONSE ----------------

        return {
            "filename": file.filename,
            **result
        }

    except HTTPException:
        raise

    except Exception as e:

        print(f"Processing error: {e}")

        raise HTTPException(
            status_code=500,
            detail="Audio processing failed."
        ) from e

    finally:

        # Remove temporary uploaded audio
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)
