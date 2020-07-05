import pytest
from scout.term import tokenize, ngram, partitions


class ScoutTerm:
    def test_tokenizer():
        text = "This.. is MY way!!! or highway??"
        assert ["way", "highway"] == tokenize(text)

    def test_tokenizer_err():
        with pytest.raises(TypeError):
            text = 50
            tokenize(text)

    def test_empty_tokenizer():
        text = ""
        assert [] == tokenize(text)

    def test_ngram():
        words = ["hello", "britishmen"]
        ngs = ["hel", "hell", "hello", "bri", "brit",
            "briti", "britis", "british",
            "britishm", "ritishme", "itishmen"]
        assert ngs == list(ngram(words, 3, 8))

    def test_ngram_err():
        with pytest.raises(TypeError):
            text = "what"
            ngram(text)

    def test_empty_ngram():
        words = []
        assert [] == list(ngram(words))

    def test_partitions():
        ngrams = {"cha": [10, 20], "chan": [20]}
        assert ("chan", "test/c/ch_index.json") == list(partitions(ngrams,"test",[1,2]))[1]
