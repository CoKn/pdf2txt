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
        choice = st.radio("Navigation", ["Process", "Download"])
        st.info("This app will take your pdf files and convert them into plane text.")

    if choice == "Process":
        st.title("Upload your text file")
        uploaded_file = st.file_uploader("Upload your files here")


        # Initialization
        if 'upload' not in st.session_state:
            st.session_state.upload = None

        if uploaded_file:
            st.success("file uploaded")
            text = extract_text(uploaded_file)
            st.session_state.upload = clean_text(text)

            with st.expander("Show extracted text"):
                st.write(st.session_state.upload)

    if choice == "Download":
        st.title("Download your text file")

        if st.session_state.upload:

            with st.expander("Show extracted text"):
                st.write(st.session_state.upload)

            st.download_button(
                label='Download text file',
                data=st.session_state.upload,
                file_name='text.txt',
                mime='text/plain',
                # on_click=st.success("Successfully downloaded")
            )
        else:
            st.info("Upload a file first")



