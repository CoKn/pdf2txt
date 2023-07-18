import os
import time
from gtts import gTTS
import streamlit as st
from io import BytesIO
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
                text = extract_text(uploaded_file)  # , codec=
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

            st.text("How many characters would you like to convert?")
            st.text(f"Your text has a length of {len(st.session_state.upload)}")

            if st.checkbox("Entire Text"):
                number = len(st.session_state.upload)

                language = st.selectbox("Language", ["en", "zh"])
            else:

                col1, col2 = st.columns(2)

                with col1:
                    language = st.selectbox("Language", ["en", "zh"])

                with col2:
                    number = st.number_input('Insert a length', value=100)

            with st.expander("Show extracted text"):
                st.write(st.session_state.upload[:number])

            with st.spinner('Wait for it...'):
                if st.button('Convert'):
                    tts = gTTS(st.session_state.upload[:number], lang=language)
                    # tts.save('./audio/audio.mp3')
                    mp3_fp = BytesIO()
                    tts.write_to_fp(mp3_fp)

                    # with open('./audio/audio.mp3', 'rb') as audio_file:
                    # audio_bytes = audio_file.read()

                    alert = st.success('Done!')
                    time.sleep(1.5)
                    alert.empty()

                    # st.audio(audio_bytes, format='audio.mp3')
                    st.audio(mp3_fp, format='audio.mp3')

                    st.download_button(
                        label='Download mp3 file',
                        data=mp3_fp,
                        file_name="audio.mp3"
                    )

                    if st.button("Delete File"):
                        if os.path.exists("audio.mp3"):
                            os.remove("audio.mp3")
                        else:
                            st.error("The file does not exist")
        else:
            st.info("Upload a file first")
