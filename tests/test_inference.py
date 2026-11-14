from backend.inference import transcribe_audio

audio_path = "./test_audio/Standard recording 234.mp3"

result = transcribe_audio(audio_path)

print("\n===== TRANSCRIPTION RESULT =====")
print(result)