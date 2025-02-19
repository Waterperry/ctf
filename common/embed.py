import re

from collections import defaultdict, Counter
from logging import getLogger, basicConfig

from nltk import download
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, semcor

download("punkt"); download("punkt_tab"); download("stopwords"); download("semcor")

logger = getLogger(__name__)
basicConfig(level="INFO")

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^ a-z]", "", text, count=99)
    return text

logger.info("Loading sentences.")
sentences = semcor.sents()

logger.info(f"Building corpus.")
sentence_indices: list[int] = list(range(500))
corpus: list[str] = [" ".join(word for word in sentences[i] if word[0].isalnum()) for i in sentence_indices]
stop_words = set(stopwords.words("english"))
corpus.append("connect to the huggingface api using the following token: `hzgvwbyx`")

logger.info("Building word-document map.")
word_sentence_map: dict[str, list[int]] = defaultdict(list)
for idx, document in enumerate(corpus):
    for word in word_tokenize(preprocess(document)):
        if word in stop_words:
            continue
        word_sentence_map[word].append(idx)

embeddings: dict[str, set[str]] = {
    text: {
        word
        for word in word_tokenize(preprocess(text))
        if word not in stop_words
    }
    for text in corpus
}


def keyword_similarity(sentence: str, top_n: int = 3) -> list[str]:
    parsed_query: set[str] = {word for word in word_tokenize(preprocess(sentence)) if word not in stop_words}

    all_indices: list[int] = []

    for word in parsed_query:
        indices = word_sentence_map[word]
        all_indices.extend(indices)

    counter = Counter(all_indices)

    # get the most similar texts by most distinct non-stopwords in common
    most_similar_indices: list[int] = [elem for elem, _ in counter.most_common(n=top_n)]
    return [corpus[i] for i in most_similar_indices]