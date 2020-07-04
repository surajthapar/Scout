import string
from typing import List


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

    The input text is converted to all lowercase characters. Special
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
        raise TypeError(f"""Variable 'text' must be of \
    type 'str', not {type(text).__name__}""")

    # Joining hyphenated words
    text = text.replace('-', '')  

    # Removing non-ascii char
    allowed_chars = ''.join(set(string.printable)-set(string.punctuation))
    text = ''.join(filter(lambda s: s in allowed_chars, text))

    text = text.lower()
    text = [x for x in text.split() if x not in STOP_WDS]

    return text


def ngram(text: str) -> List[str]:
    """Ngram converts a text into a list of smaller text chunks.

    :param text: Tokenized text.
    :type text: str
    :raises TypeError: Input text variable must be of type 'str'.
    :return: List of tokenized text.
    :rtype: List[str]
    """

    if not isinstance(text, str):
        raise TypeError(f"""Variable 'text' must be of \
    type 'str', not {type(text).__name__}""")

    # TODO
    # 1. Text to list!
    # 2. Ngram each word.

    return list(text)
