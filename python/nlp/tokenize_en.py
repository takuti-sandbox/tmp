from gensim.utils import to_unicode, deaccent, PAT_ALPHABETIC


# uni- or bi-gram
VALID_WORDS = set(['machine', 'learning', 'machine learning'])


def tokenize_en(content, token_min_len, token_max_len, lower):
    """
    Note that this function does not use `token_min_len`, `token_max_len` and `lower`.

    >>> tokenize_en('Machine learning is fun!', 2, 15, True)
    ['machine', 'learning', 'machine learning']
    """
    def get_tokens(text):
        text = to_unicode(text, encoding='utf8', errors='ignore')
        text = text.lower()

        # normalize unicode (i.e., remove accentuation)
        text = deaccent(text)

        bi = []
        for match in PAT_ALPHABETIC.finditer(text):
            uni = match.group()
            yield uni

            bi.append(uni)
            if len(bi) == 1:
                continue
            yield ' '.join(bi)
            del bi[0]

    return [
        to_unicode(token) for token in get_tokens(content)
        if token in VALID_WORDS
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
