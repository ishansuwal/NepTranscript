
import torch
from transformers import WhisperProcessor, WhisperForConditionalGeneration

MODEL_DIR = "./models/whisper_small_fft"

print("Loading processor...")
processor = WhisperProcessor.from_pretrained("openai/whisper-small")

print("Loading fine-tuned model...")
model = WhisperForConditionalGeneration.from_pretrained(
    MODEL_DIR,
    torch_dtype=torch.float32
)

model.eval()

print("\nModel loaded successfully!")
print("Device:", next(model.parameters()).device)
print("Processor:", type(processor).__name__)
print("Model:", type(model).__name__)
