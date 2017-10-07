from online_lda import OnlineLDA
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def main():
    X = np.array([[1, 1, 1, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 1, 1, 1, 1, 2, 1]])

    olda = OnlineLDA(n_topics=2, tau0=80)
    olda.partial_fit(X)
    print(olda.lambda_)

    lda = LatentDirichletAllocation(n_topics=2, total_samples=2, learning_offset=80, learning_decay=0.8, mean_change_tol=0.00001, max_iter=10000)
    lda.fit(X)
    print(lda.perplexity(X))

    lda = LatentDirichletAllocation(n_topics=2, total_samples=2, learning_offset=80, learning_decay=0.8, mean_change_tol=0.00001, max_iter=10000)
    lda.partial_fit(X)
    print(lda.perplexity(X))


if __name__ == '__main__':
    main()
