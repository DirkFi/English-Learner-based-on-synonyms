# Programmed by Dirk
# Time: 2023/3/30 17:15
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter
from collections import defaultdict

def generate_response(file_name: str):
    from faster_whisper import WhisperModel
    import openai
    model_size = "large-v2"
    # Set up the OpenAI API client
    openai.api_key = "YOUR_API_KEY"
    # Set up the model and prompt
    model_engine = "text-davinci-003"
    
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
    print(freq)

    # find top 10 words in their original sentence
    word2sentence_dict = defaultdict(list)
    freq = dict(sorted(freq.items(), key = lambda x: x[1], reverse = True)[:10])
    res_str_list = res_str.split(".")
    for sentence in res_str_list:
        for word in freq:
            if word in sentence:
                word2sentence_dict[word].append(sentence)
    # print(word2sentence_dict)
    # TODO: filter those words in the same sentences especially when the word is not noun or adj or verb
    responses = defaultdict(list)
    for word in word2sentence_dict:
        # print("word {} used in this sentence {}\n".format(word, word2sentence_dict[word]))
        prompt = "I'm using {} a lot in my speaking. How can you help me polish the use\
            of word {} to improve my English skill with the word {}. \
            Sentences are {}".format(word, word, word, word2sentence_dict[word])
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
