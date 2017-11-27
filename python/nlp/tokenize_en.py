from nltk import pos_tag_sents, sent_tokenize, word_tokenize
from gensim.utils import to_unicode, deaccent


def tokenize_en(content, token_min_len, token_max_len, lower):
    """
    >>> tokenize_en('Machine learning is fun!', 2, 15, True)
    ['machine', 'learning', 'fun']
    """
    def get_tokens(text):
        text = to_unicode(text, encoding='utf8', errors='ignore')
        text = text.lower()

        # normalize unicode (i.e., remove accentuation)
        text = deaccent(text)

        token_sents = [word_tokenize(sent) for sent in sent_tokenize(text)]

        # only Noun is acceptable: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
        return [token
                for pos_tag_sent in pos_tag_sents(token_sents)
                for token, pos in pos_tag_sent
                if pos == 'NN' or pos == 'NNS' or pos == 'NNP' or pos == 'NNPS']

    return [
        to_unicode(token) for token in get_tokens(content)
        if token_min_len <= len(token) <= token_max_len and not token.startswith('_')
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
