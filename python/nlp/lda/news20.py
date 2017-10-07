import numpy as np
import time

from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation


def main():
    newsgroups = fetch_20newsgroups(shuffle=True, random_state=101, subset='train', remove=('headers', 'footers', 'quotes'))

    vectorizer = CountVectorizer(max_df=0.9, min_df=2, max_features=1000, stop_words='english')
    vectors = vectorizer.fit_transform(newsgroups.data)
    vocab = vectorizer.get_feature_names()

    with open('news20-vectorized', 'w') as f:
        prev_row = 0
        tokens = []
        rows, cols = vectors.nonzero()
        for row, col in zip(rows, cols):
            if row != prev_row:
                f.write(str(newsgroups.target[prev_row]) + ' ' + ' '.join(tokens) + '\n')
                prev_row = row
                tokens = []
            tokens.append(vocab[col] + ':' + str(vectors[row, col]))

    n_samples, n_features = vectors.shape
    print(n_samples, n_features)

    K = 20

    t0 = time.time()

    lda = LatentDirichletAllocation(n_topics=K, learning_decay=.8, learning_offset=40, max_iter=5, total_samples=n_samples,
                                    batch_size=128, perp_tol=1e-1, mean_change_tol=1e-3)
    lda.fit(vectors)

    print('Elapsed time: %d sec for 30 iters' % (time.time() - t0))  # ~ 15 sec

    for k in range(K):
        print('=== Topic %2d ===' % k)
        top5words_indices = np.argsort(lda.components_[k])[::-1][:5]
        for i in top5words_indices:
            print(vocab[i])


if __name__ == '__main__':
    main()
