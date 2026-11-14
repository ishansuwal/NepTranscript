
import streamlit as st
import requests


# ---------------- CONFIGURATION ----------------

st.set_page_config(
    page_title="NepTranscript",
    page_icon="🎙️",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000"


# ---------------- SESSION STATE ----------------

if "result" not in st.session_state:
    st.session_state.result = None


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.title("🎙️ NepTranscript")

    st.write(
        "Nepali Speech Recognition & Translation"
    )

    st.divider()

    st.subheader("About")

    st.write(
        "NepTranscript converts Nepali speech into "
        "written text and translates it into English."
    )

    st.subheader("AI Models")

    st.markdown("""
    - **Speech Recognition:** Whisper Small FFT
    - **Translation:** NLLB-200
    - **Backend:** FastAPI
    - **Frontend:** Streamlit
    - **Inference:** CPU
    """)

    st.divider()

    st.caption("NepTranscript | AI-powered Nepali ASR")


# ---------------- MAIN PAGE ----------------

st.title("Nepali Speech Recognition")

st.write(
    "Upload a Nepali audio recording to generate "
    "a transcript and English translation."
)

st.divider()


# ---------------- AUDIO UPLOAD ----------------

uploaded_file = st.file_uploader(
    "Choose an audio file",
    type=["wav", "mp3", "m4a", "ogg", "flac"]
)


# ---------------- AUDIO PROCESSING ----------------

if uploaded_file is not None:

    st.audio(uploaded_file)

    if st.button(
        "🎯 Transcribe & Translate",
        type="primary",
        use_container_width=True
    ):

        with st.spinner(
            "Processing audio... Please wait."
        ):

            try:

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{API_URL}/transcribe",
                    files=files,
                    timeout=1800
                )

                response.raise_for_status()

                st.session_state.result = response.json()

            except requests.exceptions.ConnectionError:

                st.error(
                    "Cannot connect to FastAPI. "
                    "Please make sure the backend is running."
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Processing timed out. "
                    "Try a shorter recording."
                )

            except requests.exceptions.HTTPError:

                try:
                    detail = response.json().get(
                        "detail",
                        response.text
                    )
                except ValueError:
                    detail = response.text

                st.error(f"Backend error: {detail}")

            except Exception as e:

                st.error(f"Unexpected error: {e}")


# ---------------- RESULTS ----------------

if st.session_state.result is not None:

    result = st.session_state.result

    st.success(
        "Audio processing completed successfully!"
    )

    st.divider()

    # -------- TRANSCRIPTION AND TRANSLATION --------

    col1, col2 = st.columns(2)

    with col1:

        st.subheader("🇳🇵 Nepali Transcription")

        st.text_area(
            "Nepali transcript",
            value=result["nepali_transcription"],
            height=200
        )

        st.download_button(
            "⬇️ Download Nepali Transcript",
            data=result["nepali_transcription"],
            file_name="nepali_transcript.txt",
            mime="text/plain",
            use_container_width=True
        )

    with col2:

        st.subheader("🇬🇧 English Translation")

        st.text_area(
            "English translation",
            value=result["english_translation"],
            height=200
        )

        st.download_button(
            "⬇️ Download English Translation",
            data=result["english_translation"],
            file_name="english_translation.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()

    # -------- PERFORMANCE INFORMATION --------

    st.subheader("📊 Performance Metrics")

    metric1, metric2, metric3, metric4 = st.columns(4)

    metric1.metric(
        "Audio Duration",
        f'{result["audio_duration"]} sec'
    )

    metric2.metric(
        "Transcription Time",
        f'{result["processing_time"]} sec'
    )

    metric3.metric(
        "Translation Time",
        f'{result["translation_time"]} sec'
    )

    metric4.metric(
        "Total Processing Time",
        f'{result["total_processing_time"]} sec'
    )

    st.divider()

    # -------- RESET --------

    if st.button(
        "🔄 Process Another Audio",
        use_container_width=True
    ):

        st.session_state.result = None
        st.rerun()


else:

    st.info(
        "Upload an audio file above to get started."
    )
