"""RandomForest classification for CTR prediction.

Data: https://www.kaggle.com/c/criteo-display-ad-challenge
"""

import time
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import FeatureHasher
from sklearn.feature_extraction import DictVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import log_loss
from sklearn.metrics import roc_auc_score


def parse_data(n_hashed_features=None):
    quantitative_keys = ['i{}'.format(i) for i in range(1, 14)]
    categorical_keys = ['c{}'.format(c) for c in range(1, 27)]
    rows, labels = [], []
    with open(str(Path.home()) + '/data/criteo/dac_sample.txt') as f:
        for line in f.readlines():
            line = line.rstrip().split('\t')
            labels.append(int(line[0]))
            rows.append({
                **dict(zip(quantitative_keys, map(lambda i: 0. if i == '' else float(i), line[1:14]))),
                **dict(zip(categorical_keys, map(lambda c: '-' if c == '' else c, line[14:])))
            })

    if n_hashed_features:
        vectorizer = FeatureHasher(n_features=n_hashed_features, alternate_sign=False)
    else:
        vectorizer = DictVectorizer()
    X, y = vectorizer.fit_transform(rows), np.asarray(labels)

    return train_test_split(X, y, test_size=0.2, stratify=y)


def main():
    X_train, X_test, y_train, y_test = parse_data(n_hashed_features=1000)
    print('- parsed data into %d training and %d testing samples' % (X_train.shape[0], X_test.shape[0]))

    clf = RandomForestClassifier(n_estimators=100)

    print('- training RandomForest classifier')
    start = time.time()
    clf.fit(X_train, y_train)
    print('-- took %f sec for training' % (time.time() - start))

    y_pred = clf.predict_proba(X_test)[:, 1]
    print('- Log Loss: %f' % log_loss(y_test, y_pred))
    print('- AUC: %f' % roc_auc_score(y_test, y_pred))


if __name__ == '__main__':
    main()
