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
    if precision == True:
        model = Whisper('base')
    else:
        model = Whisper('tiny')
    return model

def inference(audio, lang):
    # Save audio to a temporary file:
    with NamedTemporaryFile(suffix=".mp3") as temp:
        with open(f"{temp.name}", "wb") as f:
            f.write(audio.tobytes())
        result = w.transcribe(f"{temp.name}", lang=lang)
        text = w.extract_text(result)
    return text[0]

st.title("TranscribeApp")
language = st.selectbox('Language', language_list, index=23)
lang = to_language_code_dict[language.lower()]
precision = st.toggle("Higher precision (slower)")

w = load_model(precision)
audio = audiorecorder("Click to record", "Recording... Click when you're done", key="recorder")

if len(audio)>0:
    text = inference(audio, lang)
    text = st.text_area('Transcription', text)
    st.code(text, language="markdown")
