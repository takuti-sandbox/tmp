import os
import pickle
import time
# import boto3
import urllib.request
import tdclient


def process_row(row):
    column_names = ['state', 'account_length', 'area_code', 'phone', 'intl_plan', 'vmail_plan', 'vmail_message', 'day_mins', 'day_calls', 'day_charge', 'eve_mins', 'eve_calls', 'eve_charge', 'night_mins', 'night_calls', 'night_charge', 'intl_mins', 'intl_calls', 'intl_charge', 'custserv_calls', 'churn', 'time']

    d = dict(zip(column_names, row))
    del d['time']

    key = d['phone']
    del d['phone']

    label = 1 if d['churn'] == 'True.' else 0
    del d['churn']

    return key, d, label


def run():
    database = 'takuti'
    model_filename = 'churn_prediction_model.pkl'

    # boto3 internally checks "AWS_ACCESS_KEY_ID" and "AWS_SECRET_ACCESS_KEY":
    # http://boto3.readthedocs.io/en/latest/guide/configuration.html#environment-variables
    # Create AWS session with specific IAM role:
    # https://dev.classmethod.jp/cloud/aws/aws-sdk-for-python-boto3-assumerole/
    """
    # Option #1:
    # If S3_BUCKET is accessible from Docker container, create AWS session with
    # your IAM role ARN and download the model dump.
    client = boto3.client('sts')
    response = client.assume_role(
        RoleArn=os.environ['AWS_IAM_ROLE_ARN'],
        RoleSessionName='ml-prediction')
    session = boto3.Session(
        aws_access_key_id=response['Credentials']['AccessKeyId'],
        aws_secret_access_key=response['Credentials']['SecretAccessKey'],
        aws_session_token=response['Credentials']['SessionToken'])
    s3 = session.resource('s3')

    with open(model_filename, 'w+b') as f:
        s3.Bucket(os.environ['S3_BUCKET']).download_fileobj(model_filename, f)
    """

    # Option #2:
    # For S3 bucket that is not accessible from Docker container, upload model
    # dump with public ACL in `train.py`, and simply download it from its
    # public URL.
    url = 'https://s3.amazonaws.com/' + os.environ['S3_BUCKET'] + '/' + model_filename
    urllib.request.urlretrieve(url, model_filename)

    with open(model_filename, 'rb') as f:
        obj = pickle.load(f)
        clf, vectorizer = obj['classifier'], obj['vectorizer']

    os.remove(model_filename)

    td = tdclient.Client(apikey=os.environ['TD_API_KEY'], endpoint=os.environ['TD_API_SERVER'])

    job = td.query(database, 'select * from churn', type='presto')
    job.wait()

    keys, rows_dict = [], []
    for row in job.result():
        key, row_dict, _ = process_row(row)
        keys.append(key)
        rows_dict.append(row_dict)

    y = clf.predict(vectorizer.transform(rows_dict))

    with open('churn_prediction_result.csv', 'w') as f:
        f.write('time,key,predict\n')
        t = int(time.time())
        for key, yi in zip(keys, y):
            f.write('%d,%s,%f\n' % (t, key, yi))

    table = 'churn_predict'
    try:
        td.table(database, table)
    except tdclient.errors.NotFoundError:
        pass
    else:
        td.delete_table(database, table)
    td.create_log_table(database, table)
    td.import_file(database, table, 'csv', 'churn_prediction_result.csv')

    os.remove('churn_prediction_result.csv')

    # Wait for a while until imported records are fully available on TD
    # console.
    while True:
        job = td.query(database, 'select count(key) from ' + table, type='presto')
        job.wait()
        if not job.error():
            break
        time.sleep(10)


if __name__ == '__main__':
    run()
