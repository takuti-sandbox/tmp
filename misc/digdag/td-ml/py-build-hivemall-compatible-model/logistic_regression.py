import os
from sklearn.datasets import load_breast_cancer
from pyhivemall import TdConnection
from pyhivemall.linear_model import SGDClassifier


def run():
    breast_cancer = load_breast_cancer()

    clf = SGDClassifier()
    clf.fit(breast_cancer.data, breast_cancer.target)

    conn = TdConnection(apikey=os.environ['TD_API_KEY'],
                        endpoint=os.environ['TD_API_SERVER'],
                        database='takuti')

    clf.store(conn,
              'breast_cancer_logress_model_sklearn',
              dict(zip(breast_cancer.feature_names, range(len(breast_cancer.feature_names)))),
              bias_feature='bias')


if __name__ == '__main__':
    run()
