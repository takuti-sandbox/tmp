"""
- parsing train data
-- density: 0.000335
- parsing test data
-- density: 0.000337
- training RandomForest classifier
-- took 288.545904 sec for training
- accuracy: 0.889712
"""

import time
import numpy as np
import scipy.sparse as sp
from sklearn.ensemble import RandomForestClassifier


def parse_data():
    """
    sort -R news20.binary > news20.random
    # [mac]
    # $ brew install coreutils
    # $ gsort -R news20.binary > news20.random
    head -15000 news20.random > news20.train
    tail -4996 news20.random > news20.test
    """
    n_train, n_test = 15000, 4996
    n_features = 1355191

    print('- parsing train data')
    X_train = sp.lil_matrix((n_train, n_features))
    y_train = np.zeros(n_train)
    with open('/Users/kitazawa/data/news20.train') as f:
        lines = map(lambda l: l.rstrip().split(' '), f.readlines())
        for i, line in enumerate(lines):
            y_train[i] = int(line[0])

            for fv in line[1:]:
                f, v = fv.split(':')
                X_train[i, (int(f) - 1)] = float(v)
    print('-- density: %f' % (X_train.nnz / (n_train * n_features)))

    print('- parsing test data')
    X_test = sp.lil_matrix((n_test, n_features))
    y_test = np.zeros(n_test)
    with open('/Users/kitazawa/data/news20.test') as f:
        lines = map(lambda l: l.rstrip().split(' '), f.readlines())
        for i, line in enumerate(lines):
            y_test[i] = int(line[0])

            for fv in line[1:]:
                f, v = fv.split(':')
                X_test[i, (int(f) - 1)] = float(v)
    print('-- density: %f' % (X_test.nnz / (n_test * n_features)))

    return X_train, y_train, X_test, y_test


def main():
    X_train, y_train, X_test, y_test = parse_data()

    clf = RandomForestClassifier(n_estimators=50)

    print('- training RandomForest classifier')
    start = time.time()
    clf.fit(X_train, y_train)
    print('-- took %f sec for training' % (time.time() - start))

    y_pred = clf.predict(X_test)
    hit = sum(np.equal(y_pred, y_test))
    print('- accuracy: %f' % (hit / y_test.size))


if __name__ == '__main__':
    main()
