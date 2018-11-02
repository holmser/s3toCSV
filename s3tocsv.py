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
def clean_metric_id(metric_id):
    clean = metric_id.replace("-","")
    clean = clean.replace(".","")
    return clean
    
# need to deserialize datetime
def myconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

metric_queries = []
for metric in metrics_list["Metrics"]:
    metric_id = [x['Value'] for x in metric["Dimensions"] if x["Name"] == "BucketName"][0]
    
    print(metric_id)
    metric_queries.append({
                'Id': clean_metric_id(metric_id),
                'MetricStat': {
                    'Metric': metric,
                    'Period': 86400,
                    'Stat': 'Average',
                    'Unit': 'Bytes'
                },
            })
    
response = client.get_metric_data(
        MetricDataQueries=metric_queries,
        StartTime=datetime(2018, 10, 1),
        EndTime=datetime(2018, 10, 31))

print(response)



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
