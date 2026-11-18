# 🎙️ NepTranscript

### Nepali Speech Recognition and Optional English Translation

NepTranscript is an AI-powered application that converts spoken Nepali audio into written Nepali text and optionally translates the transcription into English.

The system combines a fine-tuned OpenAI Whisper Small model for Nepali Automatic Speech Recognition (ASR) with Meta's NLLB-200 model for Nepali-to-English translation.

It provides a local inference pipeline using FastAPI and an interactive web interface built with Streamlit. Users can first generate a Nepali transcript and then request an English translation separately.

## ✨ Features

- Nepali speech-to-text transcription.
- Optional Nepali-to-English translation.
- Fine-tuned Whisper Small model using Full Fine-Tuning (FFT).
- Comparison of Full Fine-Tuning and LoRA approaches.
- Local CPU-based inference.
- Support for MP3, M4A, WAV, OGG, and FLAC audio formats.
- Audio preprocessing and format conversion using FFmpeg.
- Downloadable Nepali transcripts and English translations.
- Separate transcription and translation operations.
- Processing-time measurements for individual operations.

## 🏗️ System Architecture

NepTranscript uses separate API endpoints for speech recognition and translation.

### 1. Nepali Speech Recognition

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
              |
              v
      Nepali Transcript
              |
              v
      Streamlit Results
              |
              v
      Download Transcript
```

### 2. Optional English Translation

```text
      Nepali Transcript
              |
              v
      Translate Button
              |
              v
       FastAPI Backend
              |
              v
          NLLB-200
              |
              v
     English Translation
              |
              v
      Streamlit Results
              |
              v
     Download Translation
```

## 🤖 Models Used

### 1. Automatic Speech Recognition

| Configuration | Details |
|---|---|
| Base Architecture | OpenAI Whisper Small |
| Fine-Tuning Approach | Full Fine-Tuning (FFT) |
| Language | Nepali |
| Dataset | OpenSLR-54 |
| Training Subset | Approximately 3 GB |

The fine-tuned Whisper model generates Nepali transcriptions from uploaded audio recordings.

### 2. Parameter-Efficient Fine-Tuning Comparison

LoRA was also evaluated against Full Fine-Tuning to compare their ASR performance.

| Method | Test WER | Test CER |
|---|---:|---:|
| Full Fine-Tuning | 28.03% | 6.78% |
| LoRA | 52.74% | 14.96% |

Full Fine-Tuning achieved better performance on the evaluated test set.

### 3. English Translation

| Configuration | Details |
|---|---|
| Model | `facebook/nllb-200-distilled-600M` |
| Framework | Hugging Face Transformers |
| Source Language | Nepali (`npi_Deva`) |
| Target Language | English (`eng_Latn`) |

The NLLB-200 model translates the generated Nepali transcript into English when requested by the user.

## 🛠️ Technology Stack

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

## 📊 Performance Evaluation

### ASR Model Evaluation

The ASR models were evaluated using Word Error Rate (WER) and Character Error Rate (CER).

| Model | WER | CER |
|---|---:|---:|
| Whisper Small FFT | 28.03% | 6.78% |
| Whisper Small LoRA | 52.74% | 14.96% |

These results represent performance on the evaluated test set.

### Application Performance

The application measures:

- Audio duration.
- Transcription processing time.
- Translation processing time.
- Combined model processing time.

### Example Local Inference Timing

One recorded local CPU inference run produced the following results:

| Metric | Time |
|---|---:|
| Transcription | 10.255 seconds |
| Translation | 4.681 seconds |
| Total Processing | 14.936 seconds |

*These are individual example measurements, not average benchmark results. Actual processing time varies depending on audio duration and hardware.*

## 📁 Project Structure

```text
NepTranscript/
│
├── backend/
│   ├── main.py
│   ├── inference.py
│   └── translation.py
│
├── notebooks/
│   ├── 01_dataset_preparation.ipynb
│   ├── 02_whisper_baseline.ipynb
│   ├── 03_whisper_full_finetuning.ipynb
│   ├── 04_whisper_lora_training.ipynb
│   └── 05_inference_gpu.ipynb
│
├── models/
│   └── whisper_small_fft/
│
├── tests/
│
├── app.py
├── requirements.txt
└── README.md
```

**Note:** Model weights, datasets, virtual environments, and test audio files are excluded from the repository.

## 🚀 Installation and Setup

### Prerequisites

- Python 3.10 or later.
- FFmpeg.
- Git.
- Sufficient storage for the model weights.

### 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd NepTranscript
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```powershell
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add Whisper Model Weights

Place the fine-tuned Whisper Small FFT model files inside:

```text
models/whisper_small_fft/
```

The model directory should contain the required configuration and model weights.

The NLLB-200 model must also be available in the local Hugging Face cache because translation uses locally cached weights.

### 5. Start the FastAPI Backend

```bash
uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

API documentation: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

### 6. Start the Streamlit Frontend

Open another terminal, activate the virtual environment, and run:

```bash
streamlit run app.py
```

Open the application at:

http://localhost:8501

## 🎯 How to Use

1. Start the FastAPI backend.
2. Launch the Streamlit application.
3. Upload a Nepali audio recording.
4. Click **Transcribe Audio**.
5. View and download the generated Nepali transcript.
6. Click **Translate to English** if an English translation is required.
7. View and download the English translation.
8. Review the processing-time metrics.

Translation is optional. Users can obtain and download their Nepali transcript without waiting for the translation process.

## ⚠️ Limitations

- Transcription accuracy depends on audio quality, pronunciation, accents, and recording conditions.
- Whisper may produce spelling errors or incorrect word boundaries.
- Translation quality depends on the accuracy of the Nepali transcription.
- NLLB-200 may struggle with Nepali-specific terminology, cultural expressions, and context-dependent meanings.
- CPU inference can be relatively slow, particularly for longer recordings.
- The application does not guarantee perfect transcription or translation.

## 🔮 Future Improvements

- Improve Nepali transcription accuracy.
- Evaluate translation quality using appropriate translation metrics and human evaluation.
- Add video upload and audio extraction.
- Explore GPU-based local inference.
- Improve long-audio processing and progress reporting.
- Add support for additional Nepali dialects and accents.

## 🙏 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper)
- [Meta NLLB-200](https://huggingface.co/facebook/nllb-200-distilled-600M)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers)
- [OpenSLR](https://www.openslr.org/)

---

**NepTranscript — Bridging Nepali Speech and English Text.**