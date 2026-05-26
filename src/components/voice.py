"""Voice/Audio rendering component with lazy imports."""

try:
    import streamlit as st
except Exception:
    from _stubs import st


def render_voice_input():
    """Render voice input with lazy imports inside function."""
    try:
        import speech_recognition as sr
    except ImportError:
        st.error("❌ speech_recognition não instalado")
        return None

    st.subheader("🎤 Entrada de Voz")
    if st.button("Capturar áudio"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Escutando...")
            try:
                audio = recognizer.listen(source, timeout=5)
                text = recognizer.recognize_google(audio)
                st.success(f"✅ Você disse: {text}")
                return text
            except sr.UnknownValueError:
                st.error("❌ Não consegui entender o áudio")
            except sr.RequestError:
                st.error("❌ Erro ao acessar o serviço de reconhecimento")
    return None


def render_voice_output(text):
    """Render voice output with lazy imports inside function."""
    try:
        from gtts import gTTS
        import tempfile
    except ImportError:
        st.error("❌ gtts não instalado")
        return

    st.subheader("🔊 Saída de Voz")
    if st.button("Reproduzir como áudio"):
        try:
            tts = gTTS(text=text, lang="pt-br", slow=False)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
                tts.write_to_fp(fp)
                fp.flush()
                with open(fp.name, "rb") as audio_file:
                    st.audio(audio_file.read(), format="audio/mp3")
        except Exception as e:
            st.error(f"❌ Erro ao gerar áudio: {e}")


def render_webrtc_chat():
    """Render WebRTC-based chat with lazy imports inside function."""
    try:
        import streamlit_webrtc as webrtc
        from streamlit_webrtc import WebRtcMode, RTCConfiguration
    except ImportError:
        st.error("❌ streamlit_webrtc não instalado")
        return

    st.subheader("💬 Chat com WebRTC")
    rtc_config = RTCConfiguration(
        iceServers=[{"urls": ["stun:stun.l.google.com:19302"]}]
    )
    
    class VideoProcessor:
        def recv(self, frame):
            return frame

    webrtc.webrtc_streamer(
        key="example",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_config,
        video_processor_factory=VideoProcessor,
    )
