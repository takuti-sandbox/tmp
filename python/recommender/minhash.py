import binascii
import random
import MeCab
import numpy as np

tagger = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
tagger.parse('')


def tokenizer(doc):
    # TODO: more aggressive preprocessing e.g., filtering out URLs
    def get_tokens(text):
        node = tagger.parseToNode(text)
        while node:
            yield node.surface.lower()
            node = node.next

    return [token for token in get_tokens(doc)]


def recommend_minhash(docs, n_hashes=10, n_shingle=3, topk=3):
    """MinHash-based approximated similarity computation

    References:
    - https://github.com/chrisjmccormick/MinHash/blob/master/runMinHashExample.py
    - http://i.stanford.edu/~ullman/mmds/ch3n.pdf
    """

    n_docs = len(docs)

    # convert doc string into a set of shingles
    docs_shingles = [set() for i in range(n_docs)]
    shingle_words = []
    for i, doc in enumerate(docs):
        for word in tokenizer(doc):
            shingle_words.append(word)

            # wait until `n_shingle` words are observed
            if len(shingle_words) < n_shingle:
                continue

            # hash the shingle to a 32-bit integer id
            shingle = ' '.join(shingle_words)
            shingle_id = binascii.crc32(shingle.encode()) & 0xffffffff

            docs_shingles[i].add(shingle_id)

            del shingle_words[0]

    max_shingle_id = 2 ** 32 - 1  # we created shingle id as a 32-bit integer
    prime_above_max_shingle_id = 4294967311  # http://compoasso.free.fr/primelistweb/page/prime/liste_online_en.php

    # make hash functions
    #   Our random hash function will take the form of:
    #     h(x) = (a*x + b) % c
    #   where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is
    #   a prime number just greater than `max_shingle_id`.
    coefficients = []
    while len(coefficients) < n_hashes:
        a = random.randint(0, max_shingle_id)
        b = random.randint(0, max_shingle_id)

        # avoid to create the exactly same hash function
        if (a, b) not in coefficients:
            coefficients.append((a, b))

    # generate MinHash signatures
    docs_signatures = []
    for shingles in docs_shingles:

        # for each hash function
        signature = []
        for a, b in coefficients:
            min_hash = prime_above_max_shingle_id + 1
            for shingle in shingles:
                h = (a * shingle_id + b) % prime_above_max_shingle_id

                if h < min_hash:
                    min_hash = h
            signature.append(min_hash)

        docs_signatures.append(signature)

    for i in range(n_docs):
        jaccard_similarities = np.zeros(n_docs)
        i_signature = docs_signatures[i]
        for j in range(n_docs):
            if i == j:  # skip target doc itself; similarity = 1.0
                continue
            j_signature = docs_signatures[i]

            cnt = 0
            for k in range(n_hashes):
                cnt += (i_signature[k] == j_signature[k])

            jaccard_similarities[j] = cnt / n_hashes

        # find top-k most-similar articles
        top_indices = np.argsort(jaccard_similarities)[::-1][:topk]
        yield (i, top_indices)


if __name__ == '__main__':
    docs = np.array([
        '今日はいい天気です。',
        '明日もいい天気です。',
        'とても眠い。'
    ])
    rec = recommend_minhash(docs, n_hashes=10, n_shingle=3, topk=3)
    for i, recos in rec:
        print(i, docs[recos])
