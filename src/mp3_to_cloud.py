# Programmed by Dirk
# Time: 2023/3/30 17:15
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict
import re
import warnings

def generate_dict(file_name: str):
    from faster_whisper import WhisperModel
    model_size = "large-v2"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    stopwords = set(STOPWORDS)
    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")
    segments, info = model.transcribe(file_name, beam_size=5)
    res_str = ""
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        res_str += segment.text
        # print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    if not res_str:
        # adding a single entry into warnings filter
        warnings.simplefilter('error', UserWarning)
        # displaying the warning
        warnings.warn('Check your input please, it may not include any relevant words.')
    print("null res_str looks like {}".format(res_str))
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(res_str)
    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.savefig("wordcloud.png")

    # save list first so that it contains punctuation still
    res_str_list = res_str.split(".")
    res_str = re.sub(r'[^\w\s]','',res_str)
    # count word frequency
    freq = Counter(res_str.split()).most_common()
    freq = dict(freq)

    # data cleaning
    preposition_set = set(['with', 'at', 'by', 'to', 'in', 'for', 'from', 'of', 'on'])
    prons_set = set(['me', 'my', "I", 'he', 'his', 'him', 'she', 'her', 'they', 'them', 'their', 'its', 'you', 'your'])
    article_set = set(['a', 'an', 'the', 'this'])
    delete_key = []
    for freq_key in freq:
        if freq_key in preposition_set or freq_key in prons_set or freq_key in article_set:
            delete_key.append(freq_key)
    for tmp_key in delete_key:
        freq.pop(tmp_key)

    # find top 10 words in their original sentence
    word2sentence_dict = defaultdict(list)
    freq = dict(sorted(freq.items(), key = lambda x: x[1], reverse = True)[:10])
    
    for sentence in res_str_list:
        for word in freq:
            if word in sentence:
                word2sentence_dict[word].append(sentence)
    # print("word to sentence is ", word2sentence_dict)

    # TODO: filter those words in the same sentences especially when the word is not noun or adj or verb

    
    return freq, word2sentence_dict


def generate_response( api_key: str, word2sen_dict):
    import openai
    # Set up the OpenAI API client
    openai.api_key = api_key
    # Set up the model and prompt
    model_engine = "text-davinci-003"
    responses = defaultdict(list)
    for word in word2sen_dict:
        # print("word {} used in this sentence {}\n".format(word, word2sentence_dict[word]))
        prompt = "I'm using {} a lot in my speaking. How can you help me polish the use\
            of word {} to improve my English skill. \
            My sentences are {}".format(word, word, word2sen_dict[word])
        # Generate a response
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.5,
        )

        responses[word].append(completion.choices[0].text)
    return responses


if __name__ == '__main__':
    print(generate_response("../MP3/short_test.mp3"))
