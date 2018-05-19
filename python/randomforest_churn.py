"""RandomForest classification on the churn data from a book "Discovering
Knowledge in Data: An Introduction to Data Mining."

http://www.dataminingconsultant.com/
"""

import csv
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
    quantitative_keys = ['account_length', 'vmail_message', 'day_mins', 'day_calls', 'day_charge', 'eve_mins', 'eve_calls', 'eve_charge', 'night_mins', 'night_calls', 'night_charge', 'intl_mins', 'intl_calls', 'intl_charge', 'custserv_calls']
    rows, labels = [], []
    for line in csv.DictReader(open(str(Path.home()) + '/data/churn.csv')):
        labels.append(0 if line['churn'] == 'False.' else 1)

        for k in quantitative_keys:
            line[k] = float(line[k])

        del line['churn']
        del line['phone']
        rows.append(line)

    if n_hashed_features:
        vectorizer = FeatureHasher(n_features=n_hashed_features, alternate_sign=False)
    else:
        vectorizer = DictVectorizer()
    X, y = vectorizer.fit_transform(rows), np.asarray(labels)

    return train_test_split(X, y, test_size=0.2, stratify=y)


def main():
    X_train, X_test, y_train, y_test = parse_data()
    print('- parsed data into %d training and %d testing samples' % (X_train.shape[0], X_test.shape[0]))

    clf = RandomForestClassifier()

    print('- training RandomForest classifier')
    start = time.time()
    clf.fit(X_train, y_train)
    print('-- took %f sec for training' % (time.time() - start))

    y_pred = clf.predict_proba(X_test)[:, 1]
    print('- Log Loss: %f' % log_loss(y_test, y_pred))
    print('- AUC: %f' % roc_auc_score(y_test, y_pred))


if __name__ == '__main__':
    main()
