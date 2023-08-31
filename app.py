import streamlit as st
import whisper
from whispercpp import Whisper
from audiorecorder import audiorecorder
from tempfile import NamedTemporaryFile

from streamlit.runtime.scriptrunner import add_script_run_ctx
session_id = add_script_run_ctx().streamlit_script_run_ctx.session_id
st.write(session_id)

to_language_code_dict = whisper.tokenizer.TO_LANGUAGE_CODE
to_language_code_dict["automatic"] = "auto"
language_list = list(to_language_code_dict.keys())
language_list = sorted(language_list)
language_list = [language.capitalize() for language in language_list if language != "automatic"]
language_list = ["Automatic"] + language_list

@st.cache_resource  # caching whispercpp model
def load_model(precision):
    model = Whisper('base') if precision == True else Whisper('tiny')
    return model

def inference(audio, lang):
    with NamedTemporaryFile(suffix=".mp3") as temp: # Save audio to a temporary file
        with open(f"{temp.name}", "wb") as f:
            f.write(audio.tobytes())
        result = w.transcribe(f"{temp.name}")
        text = w.extract_text(result)
    return text[0]

st.title("TranscribeApp")
language = st.selectbox('Language', language_list, index=23)
lang = to_language_code_dict[language.lower()]
precision = st.toggle("Higher precision (slower)")

w = load_model(precision)
audio = audiorecorder("Click to record", "Recording... Click when you're done", key="recorder")
cleared = st.button("Clear")

with open(f"hello-{session_id}.txt", "a") as f:
    if len(audio)>0:
        f.write(inference(audio, lang))
if cleared:
    with open(f"hello-{session_id}.txt", "w") as f:
        f.write("")
with open(f"hello-{session_id}.txt", "r") as fout:
    text = fout.read()
    text = st.text_area('Transcription', text)
    st.code(text, language="markdown")
