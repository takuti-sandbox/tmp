from online_lda import OnlineLDA
from sklearn.decomposition import LatentDirichletAllocation
import numpy as np


def main():
    X = np.array([[0, 1, 0, 2, 2, 0], [1, 0, 1, 1, 3, 3]])

    olda = OnlineLDA(n_topics=2)
    olda.partial_fit(X)
    print(olda.lambda_)

    lda = LatentDirichletAllocation(n_topics=2, total_samples=2)
    lda.partial_fit(X)
    print(lda.components_)


if __name__ == '__main__':
    main()
