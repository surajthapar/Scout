import string
import os
from typing import List, Dict


STOP_WDS = {'a', 'about', 'above', 'after', 'again', 'against', 'all',
            'am', 'an', 'and', 'any', 'are', 'arent', 'as', 'at', 'be', 'been',
            'before', 'being', 'below', 'between', 'both', 'but', 'by', 'cant',
            'cannot', 'could', 'couldnt', 'did', 'didnt', 'do', 'does',
            'doesnt', 'doing', 'dont', 'each', 'few', 'for', 'from', 'had',
            'hadnt', 'has', 'hasnt', 'have', 'havent', 'having', 'he', 'hed',
            'hell', 'hes', 'her', 'here', 'heres', 'hers', 'herself', 'him',
            'himself', 'his', 'how', 'hows', 'i', 'im', 'ive', 'if', 'in',
            'into', 'is', 'isnt', 'it', 'its', 'its', 'itself', 'lets', 'me',
            'more', 'most', 'mustnt', 'my', 'myself', 'no', 'nor', 'not', 'of',
            'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours',
            'ourselves', 'out', 'over', 'own', 'same', 'she', 'shes', 'should',
            'shouldnt', 'so', 'some', 'such', 'than', 'that', 'thats', 'the',
            'their', 'theirs', 'them', 'themselves', 'then', 'there', 'theres',
            'these', 'they', 'theyd', 'theyll', 'theyre', 'theyve', 'this',
            'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very',
            'was', 'wasnt', 'we', 'well', 'were', 'weve', 'were', 'werent',
            'what', 'whats', 'when', 'whens', 'where', 'wheres', 'which',
            'while', 'who', 'whos', 'whom', 'why', 'whys', 'with', 'wont',
            'would', 'wouldnt', 'you', 'youd', 'youll', 'youre', 'youve',
            'your', 'yours', 'yourself', 'yourselves'}


def tokenize(text: str) -> List[str]:
    """Tokenization is a process of text simplification.

    This function returns a list of important words in a text. The
    input text is converted to all lowercase characters. Special
    characters and punctuations are removed from the text. Finally,
    stop words like 'a', 'the', 'for', 'from' etc. are removed.

    > Note : Hyphenated words are converted to single word.
    > For example, 'un-filtered' would become 'unfiltered'.

    :param text: Input text to be tokenized.
    :type text: str
    :raises TypeError: Input text variable must be of type 'str'.
    :return: List of tokenized words.
    :rtype: List[str]
    """

    if not isinstance(text, str):
        raise TypeError(f"""Param 'text' must be of \
    type 'str', not {type(text).__name__}""")

    # Joining hyphenated words
    text = text.replace('-', '')

    # Removing non-ascii char
    allowed_chars = ''.join(set(string.printable)-set(string.punctuation))
    text = ''.join(filter(lambda s: s in allowed_chars, text))

    text = text.lower()
    text = [x for x in text.split() if x not in STOP_WDS]

    return text


def ngram(text: List[str],
          min_len: int = 3,
          max_len: int = 8) -> Dict[str, List[int]]:
    """Ngram converts a text into a list of smaller text chunks.

    The Ngram dictionary contains positions of a word in
    the paragraph.

    :param text: List of tokenized text.
    :type text: List[str]
    :param min_len: Minimum length on an Ngram.
    :type min_len: int, optional
    :param max_len: Maximum length on an Ngram.
    :type max_len: int, optional
    :raises TypeError: Unsupported input text type.
    :raises IndexError: List, text is empty.
    :return: Dict of ngram and position.
    :rtype: Dict[str, List[int]]

    """

    if isinstance(text, list):
        if not text:
            raise LookupError
        if not isinstance(text[0], str):
            raise TypeError(f"""Param 'text' must be of \
    type 'list', not {type(text[0]).__name__}""")
    else:
        raise TypeError(f"""Elements of list 'text' must\
    be of type 'str', not {type(text).__name__}""")

    ngrams = dict()

    mn, mx = min_len, max_len

    for pos, blob in enumerate(text):
        ln = len(blob)
        x = [*([0] * (min(mx, ln) - mn + 1)), *list(range(1, ln + 1 - mx))]
        y = list(range(mn, ln + 1))
        if not x or not y:
            x, y = [0], [mn]
        for ng in list(zip(x, y)):
            gram = blob[ng[0]:ng[1]]
            if ngrams.get(gram):
                ngrams[gram].append(pos)
            else:
                ngrams[gram] = [pos]
    return ngrams


def partitions(ngrams: List[Dict[str, List[int]]],
               path_prefix: str,
               indexed_at: List[int]) -> str:
    """Returns a List[filepath] for term's clustering.

    :param word: List of ngrams.
    :type words: List[Dict[str, List[int]]]
    :param path_prefix: Folder containing the index.
    :type path_prefix: str
    :param indexed_at: Trim positions for a word.
    :type indexed_at: List[int]
    :return: List of relative os paths for the term file.
    :rtype: List[str]
    """
    for word, positions in ngrams.items():
        ln = len(word)
        index = [x for x in indexed_at if x < ln]
        path = ''

        # Slicing the word can help in faster file access times,
        # in case of large dataset.
        for idx in index:
            path = os.path.join(path, word[:idx])
        path = os.path.join(
            path_prefix,
            path + "_index.json"
        )
        yield (word, path)
