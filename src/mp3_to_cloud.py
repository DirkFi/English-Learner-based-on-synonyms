# Programmed by Dirk
# Time: 2023/3/30 17:15
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from collections import Counter


if __name__ == '__main__':
    from faster_whisper import WhisperModel

    model_size = "large-v2"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cpu", compute_type="int8")
    stopwords = set(STOPWORDS)
    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")
    print(1)
    segments, info = model.transcribe("C:\\Users\\Dirk\\Desktop\\tttt.mp3", beam_size=5)
    res_str = ""
    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    for segment in segments:
        res_str += segment.text
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
    print(res_str)
    wordcloud = WordCloud(width=800, height=800,
                          background_color='white',
                          stopwords=stopwords,
                          min_font_size=10).generate(res_str)
    # plot the WordCloud image
    plt.figure(figsize=(8, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    plt.show()

    # word frequency
    freq = Counter(res_str.split()).most_common()
    print(freq)
