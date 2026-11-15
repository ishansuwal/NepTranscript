# NepTranscript – Notebooks

This folder contains the Jupyter notebooks used for dataset preparation, baseline evaluation, model fine-tuning, and inference experiments for NepTranscript.

## Notebook Execution Order

| Notebook | Description |
|---|---|
| `01_dataset_preparation.ipynb` | Dataset loading, preprocessing, and preparation for Whisper training. |
| `02_whisper_baseline_professional.ipynb` | Evaluates the pretrained Whisper Small model on the Nepali dataset to establish baseline performance. |
| `03_whisper_full_finetuning.ipynb` | Fine-tunes Whisper Small using full fine-tuning (FFT) and evaluates the resulting model. |
| `04_whisper_lora_training.ipynb` | Fine-tunes Whisper Small using LoRA and evaluates its performance against the full fine-tuning approach. |
| `05_inference_gpu.ipynb` | Demonstrates GPU-based inference, Nepali transcription, English translation, and API deployment. |

## Requirements

- Python
- PyTorch
- Hugging Face Transformers
- Hugging Face Datasets
- Evaluate
- JiWER
- PEFT
- Librosa
- FastAPI
- Other dependencies specified in the respective notebooks

## Notes

- Training and inference notebooks were developed using Google Colab with GPU acceleration.
- Dataset paths and model paths may need to be adjusted for your environment.
- Some notebooks require access to the Hugging Face Hub.
- Model weights and datasets are not included in this repository.
- Performance results are documented in the notebooks and the main project README.