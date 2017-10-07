# coding: utf-8

"""USAGE: %(program)s MODEL_PREFIX NUM_TOPICS
"""

import logging
import os.path
import sys

from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel


if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))

    if len(sys.argv) < 3:
        print(globals()['__doc__'] % locals())
        sys.exit(1)

    prefix = sys.argv[1]
    num_topics = int(sys.argv[2])

    dst = '{}_lda_{}.model'.format(prefix, num_topics)

    if os.path.isfile(dst):
        logger.info('loading LDA model')
        lda = LdaModel.load(dst)
        topics = lda.show_topics(num_topics=num_topics, num_words=5)
        for topic, words in topics:
            logger.info('[topic %3d] %s' % (topic, words))
    else:
        logger.info('creating LDA model')
        dictionary = Dictionary.load_from_text(prefix + '_wordids.txt.bz2')
        tfidf_corpus = MmCorpus(prefix + '_tfidf.mm')
        lda = LdaModel(corpus=tfidf_corpus, id2word=dictionary, num_topics=num_topics)
        lda.save(dst)

    logger.info('finished running %s' % program)
