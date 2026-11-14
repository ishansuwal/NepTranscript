
import os
import time
import subprocess
import tempfile

import librosa
import torch

from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration
)


# ---------------- CONFIGURATION ----------------

MODEL_DIR = "./models/whisper_small_fft"
DEVICE = "cpu"
SAMPLE_RATE = 16000


# ---------------- LOAD WHISPER MODEL ----------------

print("Loading Whisper processor...")

processor = WhisperProcessor.from_pretrained(
    "openai/whisper-small"
)

print("Loading fine-tuned Whisper model...")

model = WhisperForConditionalGeneration.from_pretrained(
    MODEL_DIR,
    torch_dtype=torch.float32
)

model.to(DEVICE)
model.eval()

print("Whisper model loaded successfully!")


# ---------------- AUDIO TRANSCRIPTION ----------------

def transcribe_audio(audio_path):

    start_time = time.time()

    wav_path = None

    try:
        # Create temporary WAV file
        with tempfile.NamedTemporaryFile(
            suffix=".wav",
            delete=False
        ) as temp:
            wav_path = temp.name

        # Convert uploaded audio to 16 kHz mono WAV
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i", audio_path,
                "-ar", str(SAMPLE_RATE),
                "-ac", "1",
                "-c:a", "pcm_s16le",
                wav_path
            ],
            check=True,
            capture_output=True,
            text=True
        )

        # Load converted audio
        audio, sr = librosa.load(
            wav_path,
            sr=SAMPLE_RATE,
            mono=True
        )

        if len(audio) == 0:
            raise ValueError("The uploaded audio contains no sound.")

        audio_duration = len(audio) / sr

        print(f"Audio duration: {audio_duration:.2f} seconds")

        # Extract Whisper input features
        inputs = processor(
            audio,
            sampling_rate=SAMPLE_RATE,
            return_tensors="pt"
        )

        # Generate Nepali transcription
        with torch.inference_mode():

            predicted_ids = model.generate(
                inputs.input_features.to(DEVICE),
                language="ne",
                task="transcribe"
            )

        # Decode generated tokens
        transcription = processor.batch_decode(
            predicted_ids,
            skip_special_tokens=True
        )[0]

        processing_time = time.time() - start_time

        print("Transcription completed successfully!")

        return {
            "nepali_transcription": transcription,
            "audio_duration": round(audio_duration, 3),
            "processing_time": round(processing_time, 3)
        }

    except subprocess.CalledProcessError as e:

        print("FFmpeg conversion failed:")
        print(e.stderr)

        raise RuntimeError(
            "Could not convert the uploaded audio file."
        ) from e

    finally:

        # Remove temporary WAV file
        if wav_path and os.path.exists(wav_path):
            os.remove(wav_path)
