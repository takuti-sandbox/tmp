from sklearn import metrics
from sklearn.datasets import fetch_20newsgroups
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer


def main():
    newsgroups_train = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'))
    vectorizer = TfidfVectorizer()
    vectors_train = vectorizer.fit_transform(newsgroups_train.data)

    clf = MultinomialNB(alpha=.01)
    clf.fit(vectors_train, newsgroups_train.target)

    newsgroups_test = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'))
    vectors_test = vectorizer.transform(newsgroups_test.data)
    pred = clf.predict(vectors_test)

    print(metrics.recall_score(newsgroups_test.target, pred, average='macro'))


if __name__ == '__main__':
    main()
