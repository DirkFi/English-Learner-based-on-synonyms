import streamlit as st
import os
from mp3_to_cloud import generate_response
from PIL import Image

def is_audio_file(filepath):
    audio_extensions = ['mp3', 'wav', 'flac', 'ogg', 'm4a', 'aac']
    extension = filepath.rsplit('.', 1)[-1].lower()
    return extension in audio_extensions

def intro():
    import streamlit as st

    st.write("# Welcome to Streamlit! 👋")
    st.sidebar.success("Select a func above.")

    st.markdown(
        """
        Streamlit is an open-source app framework built specifically for
        Machine Learning and Data Science projects.

        **👈 Select a demo from the dropdown on the left** to see some examples
        of what Streamlit can do!

        ### Want to learn more?

        - Check out [streamlit.io](https://streamlit.io)
        - Jump into our [documentation](https://docs.streamlit.io)
        - Ask a question in our [community
          forums](https://discuss.streamlit.io)

        ### See more complex demos

        - Use a neural net to [analyze the Udacity Self-driving Car Image
          Dataset](https://github.com/streamlit/demo-self-driving)
        - Explore a [New York City rideshare dataset](https://github.com/streamlit/demo-uber-nyc-pickups)
    """
    )


def plotting_demo():
    import streamlit as st
    import time
    import numpy as np

    st.markdown(f'# {list(page_names_to_funcs.keys())[1]}')
    st.write(
        """
        This demo illustrates a combination of plotting and animation with
        Streamlit. We're generating a bunch of random numbers in a loop for around
        5 seconds. Enjoy!
        """
    )

    progress_bar = st.sidebar.progress(0)
    status_text = st.sidebar.empty()
    last_rows = np.random.randn(1, 1)
    chart = st.line_chart(last_rows)

    for i in range(1, 101):
        new_rows = last_rows[-1, :] + np.random.randn(5, 1).cumsum(axis=0)
        status_text.text("%i%% Complete" % i)
        chart.add_rows(new_rows)
        progress_bar.progress(i)
        last_rows = new_rows
        time.sleep(0.05)

    progress_bar.empty()

    # Streamlit widgets automatically run the script from top to bottom. Since
    # this button is not connected to any other logic, it just causes a plain
    # rerun.
    st.button("Re-run")

def from_file():
    import streamlit as st
    if 'btn_clicked' not in st.session_state:
        st.session_state['btn_clicked'] = False

    def callback():
        # change state value
        st.session_state['btn_clicked'] = True

    col1, col2, col3 = st.columns([3, 3, 6])
    with col1:
        folder_path = st.text_input("**Folder path**👇" , ".")
        clicked = st.button(label="Generate", key=0, on_click=callback)
    filenames = os.listdir(folder_path)
    audio_file = col2.selectbox("**Select a file**", filenames)
    audio_path = os.path.join(folder_path, audio_file)
    gpt_key = col3.text_input("**Your GPT API KEY here**👇" , "")

    # show wordcloud
    image = Image.open('wordcloud.png')
    st.image(image, caption='Your generated wordcloud', width=450)

    if st.session_state['btn_clicked'] or clicked:
        if not (audio_path and folder_path):
            st.warning('you should fill both `audio_link` and `folder_path`', icon="⚠️")
        elif not is_audio_file(audio_path):
            st.warning('you should choose the correct **audio** file', icon="⚠️")
        else: # begin the generation process
            with st.spinner('Wait for it...'):
                responses = generate_response(audio_path, gpt_key)
            for word in responses:
                output_string = "You can improve **Word {}** like this: ".format(word)
                for response in responses[word]:
                    output_string += response
                st.markdown(output_string)


page_names_to_funcs = {
    "—": intro,
    "Plotting Demo": plotting_demo,
    "sss": from_file
}

demo_name = st.sidebar.selectbox("Choose your function", page_names_to_funcs.keys())
page_names_to_funcs[demo_name]()