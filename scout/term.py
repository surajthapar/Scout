from typing import List


def tokenize(text: str) -> str:
    """Tokenization is a process of text simplification.

    The input text is converted to all lowercase characters. Special
    characters and punctuations are removed from the text. Finally,
    stop words like 'a', 'the', 'for', 'from' etc. are removed.

    > Note : Hyphenated words are converted to single word.
    > For example, 'un-filtered' would become 'unfiltered'.

    :param text: Input text to be tokenized.
    :type text: str
    :raises TypeError: Input text variable must be of type 'str'.
    :return: Tokenized text.
    :rtype: str
    """

    if not isinstance(text, str):
        raise TypeError(f"""Variable 'text' must be of \
    type 'str', not {type(text).__name__}""")

    # TODO
    # 1. Lowercase all words
    # 2. Handle hyphenated words
    # 3. Remove punctuations
    # 4. Remove stop words

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
