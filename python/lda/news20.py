from sklearn.decomposition import LatentDirichletAllocation
import numpy as np
import time


path = '/Users/kitazawa/data/news20-multiclass'


def main():
    k = 20
    n_features = 62061

    labels = [0] * k
    X = np.zeros((k, n_features))

    t0 = time.time()

    with open(path) as f:
        for l in f.readlines():
            line = l.rstrip().split(' ')
            idx = int(line[0]) - 1
            if labels[idx] == 0:
                labels[idx] = 1
                for f in line[1:]:
                    fi, val = f.split(':')
                    X[idx, int(fi) - 1] = float(val)

    # print(np.count_nonzero(X))  # 1497

    lda = LatentDirichletAllocation(n_topics=20, learning_decay=.8, learning_offset=80, max_iter=30, total_samples=2000,
                                    batch_size=2, perp_tol=1e-1, mean_change_tol=1e-3)
    lda.fit(X)

    print('Elapsed time: %d sec for 30 iters' % (time.time() - t0))  # ~ 15 sec


if __name__ == '__main__':
    main()
