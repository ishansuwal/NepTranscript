
import time
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM
)

# Configuration
MODEL_NAME = "facebook/nllb-200-distilled-600M"
DEVICE = "cpu"

# Load model from local Hugging Face cache only
print("Loading NLLB tokenizer from local cache...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    local_files_only=True
)

print("Loading NLLB translation model from local cache...")

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    dtype=torch.float32,
    local_files_only=True
)

model.to(DEVICE)
model.eval()

print("NLLB translation model loaded successfully!")

# Language configuration
tokenizer.src_lang = "npi_Deva"

ENGLISH_TOKEN_ID = tokenizer.convert_tokens_to_ids(
    "eng_Latn"
)


def translate_text(nepali_text):
    """
    Translate Nepali Devanagari text into English.
    """

    if not nepali_text or not nepali_text.strip():
        return ""

    start_time = time.time()

    # Tokenize Nepali input
    inputs = tokenizer(
        nepali_text,
        return_tensors="pt",
        truncation=True,
        max_length=512
    )

    # Generate English translation
    with torch.inference_mode():
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=ENGLISH_TOKEN_ID,
            max_new_tokens=256,
            num_beams=4
        )

    # Decode translated tokens
    english_text = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    processing_time = time.time() - start_time

    print(
        f"Translation completed in "
        f"{processing_time:.2f} seconds"
    )

    return english_text
