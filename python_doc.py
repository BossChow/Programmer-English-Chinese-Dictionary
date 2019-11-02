import extract
import json
import nltk
from newspaper import Article
from bs4 import BeautifulSoup
from urllib.request import urlopen

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

def start():
    start_url = "https://docs.python.org/3/tutorial/index.html"
    next_url = get_next_url(start_url)
    word_map = dict()
    counter = 0
    while next_url:
        if counter >= 1:
            break

        text = extract.extract_text(next_url)
        words = extract.extract_words(text)

        next_url = get_next_url(next_url)
        if not words:
            print(next_url, " ==== ", words)
            continue
        print(next_url)

        for item in words:
            word = item[0]
            count = item[1]
            sentence = item[2]
            print(word, "=====")
            print(count, "=====")
            print(sentence, "=====")

            if word in word_map:
                word_map[word] += count
            else:
                word_map[word] = count
        counter = counter + 1

    result = dict()
    for k, v in word_map.items():
        if v < 3:
            continue
        result[k] = v

    with open("words.json", 'w') as json_file:
        json.dump(result, json_file)
    print("Result len: ", len(result))


def get_next_url(url):
    base_url = "https://docs.python.org/3/tutorial/"
    html = urlopen(url).read()
    soup = BeautifulSoup(html)

    for link in soup.find_all('a'):
        if link.text == 'next':
            next_url = base_url + link.get('href')
            return next_url

if __name__ == "__main__":
    start()
