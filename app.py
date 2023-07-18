import os
import time
from gtts import gTTS
import streamlit as st
from pdfminer.high_level import extract_text


def clean_text(raw_text):
    # Remove leading and trailing whitespaces from each line
    lines = [line.strip() for line in raw_text.splitlines()]

    # Remove lines consisting of a single character
    lines = [line for line in lines if len(line.strip()) > 1]

    # Join the lines with a single space separator
    cleaned_text = '\n'.join(lines)

    return cleaned_text


if __name__ == "__main__":

    with st.sidebar:
        st.image("./data_no_bg.png")
        st.title("Pdf2Txt")
        choice = st.radio("Navigation", ["Pdf2Txt", "Txt2Audio"])
        st.info("This app will take your pdf files and convert them into plane text.")

    if choice == "Pdf2Txt":
        st.title("Upload your text file")
        uploaded_file = st.file_uploader("Upload your files here", type=["pdf"])

        # Initialization
        if 'upload' not in st.session_state:
            st.session_state.upload = None

        if uploaded_file:
            with st.spinner('Wait for it...'):
                text = extract_text(uploaded_file)
                st.session_state.upload = clean_text(text)
            alert = st.success('Done!')
            time.sleep(1.5)
            alert.empty()

            with st.expander("Show extracted text"):
                st.write(st.session_state.upload)

            st.download_button(
                label='Download text file',
                data=st.session_state.upload
            )

    if choice == "Txt2Audio":
        st.title("Convert your text into audio (Sample)")
        if st.session_state.upload:

            with st.expander("Show extracted text"):
                st.write(st.session_state.upload[:100])

            with st.spinner('Wait for it...'):
                if st.button('Convert'):
                    tts = gTTS(st.session_state.upload[:100])
                    tts.save('audio.mp3')

                    with open('audio.mp3', 'rb') as audio_file:
                        audio_bytes = audio_file.read()

                        alert = st.success('Done!')
                        time.sleep(1.5)
                        alert.empty()

                        st.audio(audio_bytes, format='audio.mp3')

                        st.download_button(
                            label='Download mp3 file',
                            data=audio_bytes,
                            file_name="audio.mp3"
                        )

                        if st.button("Delete File"):
                            if os.path.exists("audio.mp3"):
                                os.remove("audio.mp3")
                            else:
                                st.error("The file does not exist")
        else:
            st.info("Upload a file first")
