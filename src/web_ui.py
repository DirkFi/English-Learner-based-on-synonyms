import streamlit as st
import os
from mp3_to_cloud import generate_response, generate_dict
from PIL import Image
import pandas as pd
import string
from audiorecorder import audiorecorder
import spacy

def is_audio_file(filepath):
    audio_extensions = ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac']
    extension = filepath.rsplit('.', 1)[-1].lower()
    return extension in audio_extensions


def intro():
    st.write("# Welcome to LearnEnglish! 😉")
    st.sidebar.success("Select a func above.")

    st.markdown(
        """
        English Learner based on synonyms is an open-source program built on Python 
        framework Streamlit. The program also takes advantage of the ChatGPT 
        api to absorb the content.

        **👈 Select a function from the dropdown on the left** to see what you can 
        do and learn through our program!

        ### Upload a file to learn

        - Fill in the corret file path of your audio file
        - Fill in your ChatGPT api key ([how to find your 
        api key](https://help.openai.com/en/articles/4936850-where-do-i-find-my-secret-api-key))
        - Hit Generate Button and Wait

        ### Speak on your microphone

        - Hit Record Button to record your own voice
        - Hit it again to stop and save. *The audio file will automatically 
        be saved in the same folder in your code path.*
        - Fill in your ChatGPT api key
        - Hit Generate Button and Wait for the results
    """
    )


def from_file():
    sp = spacy.load('en_core_web_sm')
    if 'btn_clicked' not in st.session_state:
        st.session_state['btn_clicked'] = False

    def callback():
        # change state value
        st.session_state['btn_clicked'] = True

    col1, col2, col3 = st.columns([3, 3, 6])
    with col1:
        folder_path = st.text_input("**Folder path**👇" , "../MP3")
        clicked = st.button(label="Generate", key=0, on_click=callback)
    filenames = os.listdir(folder_path)
    audio_file = col2.selectbox("**Select a file**", filenames)
    audio_path = os.path.join(folder_path, audio_file)
    gpt_key = col3.text_input("**Your GPT API KEY here**👇" , "")
    puctuation_str = string.punctuation

    if st.session_state['btn_clicked'] or clicked:
        if not (audio_path and folder_path):
            st.warning('you should fill both `audio_link` and `folder_path`', icon="⚠️")
        elif not is_audio_file(audio_path):
            st.warning('you should choose the correct **audio** file', icon="⚠️")
        else: # begin the generation process
            with st.spinner('Wait for it...'):
                freq, word2sentence_dict = generate_dict(audio_path)
                data = []
                for w in word2sentence_dict:
                    sentens = word2sentence_dict[w][0].strip()
                    # remove all puctuations in the string
                    for i in puctuation_str:
                        sentens = sentens.replace(i, "")
                    sentens_list = sentens.split(" ")
                    data.append([w, sp(sentens)[sentens_list.index(w)].pos_, freq[w]])
                df = pd.DataFrame(data, columns=["word", "parts of speech", "frequency"])
                print("Congrats! Dict generation is done!")

                tab1, tab2, tab3 = st.tabs(["Improvements", "WordCloud", "Table"])
                # show wordcloud
                with tab2:
                    st.header("Wordcloud Figure")
                    image = Image.open('wordcloud.png')
                    st.image(image, caption='Your generated wordcloud', width=450)
                # show dataframe
                with tab3:
                    st.header("Top-10 Words Frequency Table")
                    st.dataframe(df, use_container_width=True)

                responses = generate_response(gpt_key, word2sentence_dict)

                for word in responses:
                    output_string = "##### You can improve the **Word {}** like this: "\
                                                                    .format(word)
                    for response in responses[word]:
                        output_string += response
                    with tab1:
                        st.markdown(output_string)


def audio_input():
    st.title("Audio Recorder")
    audio = audiorecorder("Click to record", "Recording... Click to STOP")

    if len(audio) > 0:
        # To play audio in frontend:
        st.audio(audio.tobytes())
        
        # To save audio to a file:
        wav_file = open("audio.mp3", "wb")
        wav_file.write(audio.tobytes())
    sp = spacy.load('en_core_web_sm')


    if 'btn_clicked' not in st.session_state:
        st.session_state['btn_clicked'] = False

    def callback():
        # change state value
        st.session_state['btn_clicked'] = True

    audio_path = os.path.join(".", "audio.mp3")
    gpt_key = st.text_input("**Your GPT API KEY here**👇" , "")
    puctuation_str = string.punctuation
    clicked = st.button(label="Generate", key=0, on_click=callback)

    if st.session_state['btn_clicked'] or clicked:
        with st.spinner('Wait for it...'):
            freq, word2sentence_dict = generate_dict(audio_path)
            data = []
            for w in word2sentence_dict:
                sentens = word2sentence_dict[w][0].strip()
                # remove all puctuations in the string
                for i in puctuation_str:
                    sentens = sentens.replace(i, "")
                sentens_list = sentens.split(" ")
                data.append([w, sp(sentens)[sentens_list.index(w)].pos_, freq[w]])
            df = pd.DataFrame(data, columns=["word", "parts of speech", "frequency"])

            print("Congrats! Dict generation is done!")
            # tab1, tab2, tab3 = st.tabs(["Improvements", "WordCloud", "Table"])
            # show wordcloud
            with st.expander("See Wordcloud"):
                image = Image.open('wordcloud.png')
                st.image(image, caption='Your generated wordcloud', width=450)
            # show dataframe
            with st.expander("See Frequency Table"):
                st.dataframe(df, use_container_width=True)

            responses = generate_response(gpt_key, word2sentence_dict)

            for word in responses:
                output_string = "##### You can improve the **Word {}** like this: "\
                .format(word)
                for response in responses[word]:
                    output_string += response
                st.markdown(output_string)

page_names_to_funcs = {
    "MainPage": intro,
    "Upload a file to improve your English": from_file, 
    "Speak to YOUR Mic": audio_input
}

demo_name = st.sidebar.selectbox("Choose your function", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()