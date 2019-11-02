import nltk
from newspaper import Article
from nltk import FreqDist
from bs4 import BeautifulSoup
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

stopworddic = set(stopwords.words('english'))
wordnet_lemmatizer = WordNetLemmatizer()
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def start():
    url = "https://docs.python.org/3/tutorial/appetite.html"
    article = Article(url)
    article.download()
    article.parse()

    soup = BeautifulSoup(article.html)


def extract_text(url):
    # Parse page to text
    article = Article(url)
    article.download()
    article.parse()
    return article.text


# 提取词
def extract_words(text):
    if len(text) == 0:
        return

    # PRP 人称代词
    # CC 并列连词
    # RB 副词
    filter_tags = ['PRP', 'TO', 'CC', 'RB', 'DT', 'IN', 'RP', 'VBZ', 'VBP', 'VBG', 'WDT', 'WRB']

    # 分句
    sentences = sent_detector.tokenize(text)
    for sentence in sentences:
        # 分词
        tokens = nltk.word_tokenize(sentence)

        # 词性标注
        taged_tokens = nltk.pos_tag(tokens)

        # 过滤
        words = []
        for token, tag in taged_tokens:
            # 词性/短词过滤
            if len(tag) < 2 or len(token) < 5 or tag in filter_tags:
                continue

            # 非单词过滤
            if not token.isalpha():
                continue

            # 停用词过滤
            if token in stopworddic:
                print("Stopword filter: ", token)
                continue

            token = token.lower()
            if tag != 'NNP': # 非专有名词
                # 词形还原
                token = wordnet_lemmatizer.lemmatize(token)

            words.append(token)

        freq = FreqDist(words)
        freqList = []
        for word in freq:
            freqList.append((word, freq[word], sentence))
        return freqList


if __name__ == '__main__':
    start()
