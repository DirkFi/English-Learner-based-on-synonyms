# English-Learner-based-on-synonyms
This project aims to give an easy web to practise English for English learners. The idea is to input your voice as the format of audio file, an then the program will calculate and show the wordcloud based on your use of words. 

Then, you will get your polished version of your audio content through the ChatGPT api In this way, you can learn how to use the words **differently** to express yourself.
## Installation
To use this program, you need to

```
pip install faster-whisper
pip install wordcloud
pip install openai
pip install streamlit
```

Or, you can just run
```
pip install -r requirements.txt
```
## Run
Make sure you are in the folder of ```English-Learner-based-on-synonyms/src```. Then run
```
streamlit run web_ui.py
```
to start the whole program.
## Current UI
### The page for submitting your file
![](https://github.com/DirkFi/English-Learner-based-on-synonyms/blob/main/img/from_file.png)

### The page for giving an audio input
![](https://github.com/DirkFi/English-Learner-based-on-synonyms/blob/main/img/audio_input.png)



