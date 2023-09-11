import streamlit as st
import whisper
from whispercpp import Whisper
from audiorecorder import audiorecorder
from tempfile import NamedTemporaryFile

to_language_code_dict = whisper.tokenizer.TO_LANGUAGE_CODE
to_language_code_dict["automatic"] = "auto"
language_list = list(to_language_code_dict.keys())
language_list = sorted(language_list)
language_list = [language.capitalize() for language in language_list if language != "automatic"]
language_list = ["Automatic"] + language_list

@st.cache_resource  # caching whispercpp model
def load_model(precision):
    if precision == "whisper-tiny":
        model = Whisper('tiny')
    elif precision == "whisper-base":
        model = Whisper('base')
    else:
        model = Whisper('small')
    return model

if "full_text" not in st.session_state:
    st.session_state["full_text"] = ""

def inference(audio, lang):
    with NamedTemporaryFile(suffix=".mp3") as temp: # Save audio to a temporary file
        with open(f"{temp.name}", "wb") as f:
            f.write(audio.export().read())
        result = w.transcribe(f"{temp.name}", lang=lang)
        text = w.extract_text(result)
    return text[0]

st.title("TranscribeApp")
language = st.selectbox('Language', language_list, index=23)
lang = to_language_code_dict[language.lower()]
precision = st.selectbox("Precision", ["whisper-tiny", "whisper-base", "whisper-small"])

w = load_model(precision)
col1, col2   = st.columns(2)
with col1:
    audio = audiorecorder("Click to record", "Recording... Click when you're done", key="recorder")
with col2:
    clear_text = st.button("Clear")
    if clear_text:
        st.session_state["full_text"] = ""
        audio = ""

if len(audio)>0:
    st.audio(audio.export().read())
    full_text = st.session_state["full_text"]
    text = inference(audio, lang)
    full_text = full_text + text
    text = st.text_area('Transcription', full_text)
    st.code(full_text, language="markdown")
    st.session_state["full_text"] = full_text
