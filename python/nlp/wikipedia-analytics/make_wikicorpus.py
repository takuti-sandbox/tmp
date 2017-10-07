# coding: utf-8

"""USAGE: %(program)s WIKI_XML_DUMP OUTPUT_PREFIX LANG
"""

import logging
import os.path
import sys

from nltk import pos_tag, word_tokenize

import gensim.corpora.wikicorpus as wikicorpus
from gensim.corpora import Dictionary, MmCorpus, WikiCorpus
from gensim.models import TfidfModel
from gensim.utils import to_unicode, deaccent

import MeCab

# Wiki is first scanned for all distinct word types (~7M). The types that
# appear in more than 10% of articles are removed and from the rest, the
# DEFAULT_DICT_SIZE most frequent types are kept.
DEFAULT_DICT_SIZE = 100000

# tagger = MeCab.Tagger()
tagger = MeCab.Tagger(' -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
tagger.parse('')


def tokenize_ja(content):
    def tokenize(text):
        node = tagger.parseToNode(to_unicode(text, encoding='utf8', errors='ignore'))
        while node:
            if node.feature.split(',')[0] == '名詞':
                yield node.surface.lower()
            node = node.next

    return [
        to_unicode(token) for token in tokenize(content)
        if 2 <= len(token) <= 15 and not token.startswith('_')
    ]


def tokenize_en(content):
    def tokenize(text):
        text = to_unicode(text, encoding='utf8', errors='ignore')
        text = text.lower()

        # normalize unicode (i.e., remove accentuation)
        text = deaccent(text)

        for token, pos in pos_tag(word_tokenize(text)):
            # only Noun is acceptable: https://pythonprogramming.net/natural-language-toolkit-nltk-part-speech-tagging/
            if token in ['NN', 'NNS', 'NNP', 'NNPS']:
                yield token

    return [
        to_unicode(token) for token in tokenize(content)
        if 2 <= len(token) <= 15 and not token.startswith('_')
    ]


if __name__ == '__main__':
    # https://github.com/RaRe-Technologies/gensim/blob/develop/gensim/scripts/make_wikicorpus.py
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    # check and process input arguments
    if len(sys.argv) < 4:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    src, dst, lang = sys.argv[1], sys.argv[2], sys.argv[3]

    if lang == 'ja':
        wikicorpus.tokenize = tokenize_ja
        wiki = WikiCorpus(src)
    elif lang == 'en':
        wikicorpus.tokenize = tokenize_en
        wiki = WikiCorpus(src, lemmatize=False)  # honestly, token has to be somehow lemmatized, but Hive does not have the equivalent functionality
    else:
        print('invalid lang')
        sys.exit(1)

    # only keep the most frequent words
    wiki.dictionary.filter_extremes(no_below=20, no_above=0.1, keep_n=DEFAULT_DICT_SIZE)

    # save dictionary and bag-of-words (term-document frequency matrix)
    MmCorpus.serialize(dst + '_bow.mm', wiki, progress_cnt=10000, metadata=True)
    wiki.dictionary.save_as_text(dst + '_wordids.txt.bz2')

    # load back the id->word mapping directly from file
    # this seems to save more memory, compared to keeping the wiki.dictionary object from above
    dictionary = Dictionary.load_from_text(dst + '_wordids.txt.bz2')

    del wiki

    # initialize corpus reader and word->id mapping
    mm = MmCorpus(dst + '_bow.mm')

    # build tfidf
    tfidf = TfidfModel(mm, id2word=dictionary, normalize=True)
    tfidf.save(dst + '.tfidf_model')

    # save tfidf vectors in matrix market format
    MmCorpus.serialize(dst + '_tfidf.mm', tfidf[mm], progress_cnt=10000)

    logger.info('finished running %s' % program)
