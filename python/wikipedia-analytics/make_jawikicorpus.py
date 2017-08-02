# coding: utf-8

"""USAGE: %(program)s WIKI_XML_DUMP OUTPUT_PREFIX
"""

import logging
import os.path
import sys

import gensim.corpora.wikicorpus as wikicorpus
from gensim.corpora import Dictionary, MmCorpus, WikiCorpus
from gensim.models import TfidfModel
from gensim.utils import to_unicode

import MeCab


# Wiki is first scanned for all distinct word types (~7M). The types that
# appear in more than 10% of articles are removed and from the rest, the
# DEFAULT_DICT_SIZE most frequent types are kept.
DEFAULT_DICT_SIZE = 100000

tagger = MeCab.Tagger()
tagger.parse('')


def tokenize_ja(text):
    node = tagger.parseToNode(to_unicode(text,  encoding='utf8', errors='ignore'))
    while node:
        if node.feature.split(',')[0] == '名詞':
            yield node.surface.lower()
        node = node.next


def tokenize(content):
    return [
        to_unicode(token) for token in tokenize_ja(content)
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
    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)
    src, dst = sys.argv[1], sys.argv[2]

    wikicorpus.tokenize = tokenize

    wiki = WikiCorpus(src)

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
