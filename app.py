
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

if "translation" not in st.session_state:
    st.session_state.translation = None


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
        "written text and optionally translates it into English."
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
    "a transcript. You can optionally translate it into English."
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
        "🎯 Transcribe Audio",
        type="primary",
        use_container_width=True
    ):

        # Clear previous results
        st.session_state.result = None
        st.session_state.translation = None

        with st.spinner(
            "Transcribing Nepali audio... Please wait."
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
                    "Transcription timed out. "
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
        "Nepali transcription completed successfully!"
    )

    st.divider()

    # -------- NEPALI TRANSCRIPTION --------

    st.subheader("🇳🇵 Nepali Transcription")

    st.text_area(
        "Nepali transcript",
        value=result["nepali_transcription"],
        height=200,
        key="nepali_transcript"
    )

    st.download_button(
        "⬇️ Download Nepali Transcript",
        data=result["nepali_transcription"],
        file_name="nepali_transcript.txt",
        mime="text/plain",
        use_container_width=True
    )

    st.divider()

    # -------- OPTIONAL ENGLISH TRANSLATION --------

    st.subheader("🇬🇧 English Translation")

    if st.session_state.translation is None:

        st.write(
            "Translation is optional. Click below "
            "if you want an English translation."
        )

        if st.button(
            "🌐 Translate to English",
            use_container_width=True
        ):

            with st.spinner(
                "Translating into English... Please wait."
            ):

                try:

                    response = requests.post(
                        f"{API_URL}/translate",
                        json={
                            "text": result["nepali_transcription"]
                        },
                        timeout=600
                    )

                    response.raise_for_status()

                    st.session_state.translation = response.json()

                    st.rerun()

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Cannot connect to FastAPI. "
                        "Please make sure the backend is running."
                    )

                except requests.exceptions.Timeout:

                    st.error(
                        "Translation timed out. Please try again."
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

    else:

        translation = st.session_state.translation

        st.text_area(
            "English translation",
            value=translation["english_translation"],
            height=200
        )

        st.download_button(
            "⬇️ Download English Translation",
            data=translation["english_translation"],
            file_name="english_translation.txt",
            mime="text/plain",
            use_container_width=True
        )

    st.divider()

    # -------- PERFORMANCE INFORMATION --------

    st.subheader("📊 Performance Metrics")

    if st.session_state.translation is None:

        metric1, metric2 = st.columns(2)

        metric1.metric(
            "Audio Duration",
            f'{result["audio_duration"]} sec'
        )

        metric2.metric(
            "Transcription Time",
            f'{result["processing_time"]} sec'
        )

    else:

        translation = st.session_state.translation

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
            f'{translation["translation_time"]} sec'
        )

        total_time = (
            result["processing_time"]
            + translation["translation_time"]
        )

        metric4.metric(
            "Combined Processing Time",
            f'{total_time:.3f} sec'
        )

    st.divider()

    # -------- RESET --------

    if st.button(
        "🔄 Process Another Audio",
        use_container_width=True
    ):

        st.session_state.result = None
        st.session_state.translation = None
        st.rerun()


else:

    st.info(
        "Upload an audio file above to get started."
    )
