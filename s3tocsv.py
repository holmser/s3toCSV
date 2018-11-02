import boto3
import json
import csv
# from bson import json_util
from datetime import datetime
client = boto3.client('cloudwatch')

# Query CloudWatch for a list of AWS/S3 metrics
metrics_list = client.list_metrics(
    Namespace='AWS/S3',
    MetricName='BucketSizeBytes',
)

print(json.dumps(metrics_list, indent=2))

# need to deserialize datetime
def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()


# Create queries array
queries = []

# CloudWatch charges per API call, we can stuff multiple requests in a single API call so we will.
for metric in metrics_list["Metrics"]:
    queries.append({
        'Id': 'configbucket',
        'MetricStat': {
            'Metric': {
                'Namespace':
                'AWS/S3',
                'MetricName':
                'BucketSizeBytes',
                "Dimensions": [{
                    "Name": "StorageType",
                    "Value": "StandardStorage"
                }, {
                    "Name": "BucketName",
                    "Value": "config-bucket-487312177614"
                }]
            },
            'Period': 86400,
            'Stat': 'Average',
            'Unit': 'Bytes'
        },
    })

# metric = metrics_list["Metrics"][0]
for metric in metrics_list["Metrics"]:
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'configbucket',
                'MetricStat': {
                    'Metric': {
                        'Namespace':
                        'AWS/S3',
                        'MetricName':
                        'BucketSizeBytes',
                        "Dimensions": [{
                            "Name": "StorageType",
                            "Value": "StandardStorage"
                        },
                                       {
                                           "Name": "BucketName",
                                           "Value":
                                           "config-bucket-487312177614"
                                       }]
                    },
                    'Period': 86400,
                    'Stat': 'Average',
                    'Unit': 'Bytes'
                },
            },
        ],
        StartTime=datetime(2018, 10, 1),
        EndTime=datetime(2018, 10, 31))
    #ScanBy='TimestampDescending')

    # with open('eggs.csv', 'w', newline='') as csvfile:
    #     spamwriter = csv.writer(
    #         csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)
    #     row = ['']
    #     for result in response['MetricDataResults']:
    #         for stamp in result["Timestamps"]:
    #             row.append(stamp)

    #         spamwriter.writerow(row)
    #         row = ['']

    #         for val in result['Values']:
    #             row.append(val)

    #         spamwriter.writerow(row)
