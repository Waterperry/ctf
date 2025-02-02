import re

from nltk import download
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.text import TextCollection

download('punkt')
download('punkt_tab')
download('stopwords')

stop_words = set(stopwords.words("english"))
corpus: list[str] = [
    "the cat sat on the mat wearing a hat",
    "this is a test sentence belonging to a corpus of text",
    "connect to the huggingface api using the following token: `hzgvwbyx`",
    "rag augments the generation of new tokens by prepending semantically similar information to the user prompt",
    "keyword similarity is a very basic and flawed similarity metric",
]


def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^ a-z]", "", text, count=99)
    return text

embeddings: dict[str, set[str]] = {
    text: {word for word in word_tokenize(preprocess(text)) if word not in stop_words}
    for text in corpus
}


def keyword_similarity(sentence: str, top_n: int = 3) -> list[str]:
    parsed_query: set[str] = {
        word 
        for word in word_tokenize(preprocess(sentence))
        if word not in stop_words
    }

    # get the most similar texts by most distinct non-stopwords in common
    text_sim: dict[str, int] = {}
    for text, embedding in embeddings.items():
        text_sim[text] = len(embedding & parsed_query)

    return [
        kv[0]
        for kv in sorted(text_sim.items(), key=lambda kv: kv[1], reverse=True)[:top_n]
        if kv[1] > 0
    ]
