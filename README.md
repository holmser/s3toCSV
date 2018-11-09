# Lambda S3 to CSV 

This is a simple Lambda that pulls metrics from Cloudwatch and spits them into a csv in s3.  It flows as follows:

1.  Get a list of all metrics in the CloudWatch Namespace "AWS/S3" and MetricName "BucketSizeBytes"
2.  Request those metrics using a period of 1 day (86400 seconds)
3.  Dump those metrics into a CSV
4.  Write to s3




# How to deploy:
First install node via `brew install node` or by visiting https://nodejs.org/en/download/ .

```sh
# Works with Python 2 and 3
brew install sls
sls deploy
```

