Locally build a prediction model and dump it as a .pkl file on S3:

```sh
# export AWS_ACCESS_KEY_ID=AAAAAAAAAA
# export AWS_SECRET_ACCESS_KEY=XXXXXXXXX
# export AWS_IAM_ROLE_ARN=arn:aws:iam::00000000000:role/xxxx
# export S3_BUCKET=awesome-bucket
python train.py
```

For data stored in TD, make prediction by using the picked model:

```sh
# export TD_API_KEY=1/xxxxxx
# export TD_API_SERVER=https://api.treasuredata.com
td wf push py-ml-project-prediction
td wf secrets --project py-ml-project-prediction \
              --set apikey=$TD_API_KEY \
              --set endpoint=$TD_API_SERVER \
              --set s3_bucket=$S3_BUCKET
td wf start py-ml-project-prediction py-predict-by-pickled-model --session now
```
