import pytest
from scout.term import tokenize, ngram, partitions


class TestScoutTerm:
    def test_tokenizer(self):
        text = "This.. is MY way!!! or highway??"
        assert ["way", "highway"] == tokenize(text)

    def test_tokenizer_err(self):
        with pytest.raises(TypeError):
            text = 50
            tokenize(text)

    def test_empty_tokenizer(self):
        text = ""
        assert [] == tokenize(text)

    def test_ngram(self):
        words = ["hello", "britishmen"]
        ngs = ["hel", "hell", "hello", "bri", "brit",
               "briti", "britis", "british",
               "britishm", "ritishme", "itishmen"]
        assert ngs == list(ngram(words, 3, 8))

    def test_ngram_err(self):
        with pytest.raises(TypeError):
            text = "what"
            ngram(text)

    def test_empty_ngram(self):
        with pytest.raises(LookupError):
            ngram([], 3, 8)

    def test_partitions(self):
        ngrams = {"cha": [10, 20], "chan": [20]}
        parts = partitions(ngrams, "test", [1, 2])
        assert ("chan", "test/c/ch_index.json") == list(parts)[1]
