
import torch
import librosa
import time

from transformers import (
    WhisperProcessor,
    WhisperForConditionalGeneration
)

MODEL_DIR = "./models/whisper_small_fft"

AUDIO_PATH = "./test_audio/Standard recording 234.mp3"

# Load processor and fine-tuned model
print("Loading processor...")
processor = WhisperProcessor.from_pretrained(
    "openai/whisper-small"
)

print("Loading fine-tuned Whisper model...")
model = WhisperForConditionalGeneration.from_pretrained(
    MODEL_DIR,
    torch_dtype=torch.float32
)

model.eval()

# Load audio at 16 kHz
print("\nLoading audio...")
audio, sr = librosa.load(
    AUDIO_PATH,
    sr=16000,
    mono=True
)

audio_duration = len(audio) / sr

print(f"Audio duration: {audio_duration:.2f} seconds")

# Prepare audio
inputs = processor(
    audio,
    sampling_rate=16000,
    return_tensors="pt"
)

# Transcribe
print("\nTranscribing...")

start_time = time.time()

with torch.inference_mode():
    predicted_ids = model.generate(
        inputs.input_features,
        language="ne",
        task="transcribe"
    )

transcription = processor.batch_decode(
    predicted_ids,
    skip_special_tokens=True
)[0]

processing_time = time.time() - start_time

# Results
print("\n========== RESULTS ==========")
print("Nepali transcription:")
print(transcription)

print(f"\nAudio duration: {audio_duration:.2f} seconds")
print(f"Processing time: {processing_time:.2f} seconds")
print("=============================")
