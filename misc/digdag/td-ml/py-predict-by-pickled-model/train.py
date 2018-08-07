import os
import pickle
import boto3
import numpy as np
import pandas as pd
import io
import requests
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction import DictVectorizer


def load_churn_data():
    """Data source:
    https://www.amazon.com/Discovering-Knowledge-Data-Introduction-Mining/dp/0471666572
    """
    url = 'https://gist.githubusercontent.com/takuti/409788f38199e8429384259d25dfc4b5/raw/8977da6e5bf29b156e5609cb6bb828ba6a31c0dc/churn.csv'
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))

    rows_dict = df.drop(['phone', 'churn'], axis=1).to_dict('records')
    y = df['churn'].apply(lambda x: 1 if x == 'True.' else 0).tolist()

    return rows_dict, y


def run():
    rows_dict, y = load_churn_data()

    vectorizer = DictVectorizer(sparse=False)
    X = vectorizer.fit_transform(rows_dict)

    clf = RandomForestClassifier(n_estimators=30)
    clf.fit(X, np.asarray(y))

    # boto3 internally checks "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    # Create AWS session with specific IAM role:
    # https://dev.classmethod.jp/cloud/aws/aws-sdk-for-python-boto3-assumerole/
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=os.environ['AWS_IAM_ROLE_ARN'],
        RoleSessionName='ml-prediction')
    session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])
    s3 = session.resource('s3')

    # If this code can access to the bucket
    # from Docker container, ACL does not
    # necessarily have to be public.
    s3.Object(os.environ['S3_BUCKET'], 'churn_prediction_model.pkl').put(ACL='public-read', Body=pickle.dumps({'vectorizer': vectorizer, 'classifier': clf}))


if __name__ == '__main__':
    run()
