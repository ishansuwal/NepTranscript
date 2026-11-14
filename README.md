# 🎙️ NepTranscript
### Nepali Speech Recognition and English Translation

NepTranscript is an AI-powered application that converts spoken Nepali audio into written Nepali text and translates the transcription into English.

The system combines a fine-tuned OpenAI Whisper Small model for Nepali Automatic Speech Recognition (ASR) with Meta's NLLB-200 model for Nepali-to-English translation. It provides a local inference pipeline through FastAPI and an interactive Streamlit interface.

## Features

- Nepali speech-to-text transcription.
- Nepali-to-English translation.
- Fine-tuned Whisper Small model.
- Local CPU-based inference.
- Support for MP3, M4A, WAV, OGG, and FLAC audio.
- Audio preprocessing and format conversion using FFmpeg.
- Downloadable Nepali transcripts and English translations.
- Processing-time measurements for transcription, translation, and the complete pipeline.
- Interactive web interface built with Streamlit.

## System Architecture

```text
          Audio Upload
                |
                v
        Streamlit Frontend
                |
                v
          FastAPI Backend
                |
                v
       Audio Preprocessing
             FFmpeg
                |
                v
       Whisper Small FFT
       Nepali Transcription
                |
                v
          NLLB-200
      Nepali to English
                |
                v
        API JSON Response
                |
                v
        Streamlit Results
          /          \
         v            v
   Nepali Text    English Text
         |            |
         v            v
      Download     Download
```

## Models Used

### 1. Automatic Speech Recognition

- Base architecture: OpenAI Whisper Small
- Fine-tuning approach: Full Fine-Tuning (FFT)
- Language: Nepali
- Dataset: OpenSLR-54
- Training subset: Approximately 3 GB

The fine-tuned model generates Nepali transcriptions from uploaded audio recordings.

### 2. Parameter-Efficient Fine-Tuning Comparison

LoRA was also evaluated against Full Fine-Tuning to compare their ASR performance.

| Method | Test WER | Test CER |
|---|---:|---:|
| Full Fine-Tuning | 28.03% | 6.78% |
| LoRA | 52.74% | 14.96% |

Full Fine-Tuning achieved better performance on the evaluated test set.

### 3. English Translation

- Model: `facebook/nllb-200-distilled-600M`
- Framework: Hugging Face Transformers
- Source language: Nepali (`npi_Deva`)
- Target language: English (`eng_Latn`)

The translation model converts the generated Nepali transcription into English.

## Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| ASR Model | Whisper Small |
| Translation Model | NLLB-200 |
| Deep Learning Framework | PyTorch |
| Model Framework | Hugging Face Transformers |
| Audio Processing | Librosa, FFmpeg |
| Backend | FastAPI |
| Frontend | Streamlit |
| API Communication | HTTP / REST |

## Performance Evaluation

The ASR models were evaluated using Word Error Rate (WER) and Character Error Rate (CER).

| Model | WER | CER |
|---|---:|---:|
| Whisper Small FFT | 28.03% | 6.78% |
| Whisper Small LoRA | 52.74% | 14.96% |

The application also measures:

- Audio duration
- Transcription processing time
- Translation processing time
- Total pipeline processing time

### Example Local Inference Timing

One recorded local CPU inference run produced the following results:

| Metric | Time |
|---|---:|
| Transcription | 16.062 seconds |
| Translation | 5.993 seconds |
| Total processing | 22.059 seconds |

*These are individual example measurements, not average benchmark results. Actual processing time varies with audio duration and hardware.*

## Project Structure

```text
NepTranscript/
│
├── backend/
│   ├── main.py
│   ├── inference.py
│   └── translation.py
│
├── models/
│   └── whisper_small_fft/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

The model weights are not included in this repository by default.

## Installation and Setup

### Prerequisites

- Python 3.10 or later
- FFmpeg
- Git
- Sufficient storage for the model weights

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd NepTranscript
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add model weights

Place your fine-tuned Whisper Small FFT model inside:

```text
models/whisper_small_fft/
```

The NLLB-200 model must also be available in the local Hugging Face cache because translation currently uses local cached weights.

### 5. Start the FastAPI backend

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

### 6. Start the Streamlit frontend

Open another terminal:

```bash
streamlit run app.py
```

Open the application:

```text
http://localhost:8501
```

## How to Use

1. Start the FastAPI backend.
2. Launch the Streamlit application.
3. Upload a Nepali audio recording.
4. Click **Transcribe & Translate**.
5. View the Nepali transcription.
6. View the English translation.
7. Download either result as a text file.
8. Review the processing-time metrics.

## Limitations

- Transcription accuracy depends on audio quality, pronunciation, accents, and recording conditions.
- Whisper may produce spelling errors or incorrect word boundaries.
- Translation quality depends on the accuracy of the Nepali transcription.
- NLLB-200 may struggle with Nepali-specific terminology, cultural expressions, and context-dependent meanings.
- CPU inference can be relatively slow, particularly for longer recordings.
- The application does not guarantee perfect transcription or translation.

## Future Improvements

- Improve Nepali transcription accuracy.
- Evaluate translation quality using appropriate translation metrics and human evaluation.
- Add video upload and audio extraction.
- Explore GPU-based local inference.
- Improve long-audio processing and progress reporting.
- Add support for additional Nepali dialects and accents.

## Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Meta NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [OpenSLR](https://www.openslr.org/)

---

**NepTranscript — Bridging Nepali Speech and English Text.**