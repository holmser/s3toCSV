from __future__ import print_function
import boto3
import csv
import json
import os
import time
from datetime import datetime, timedelta


# Metric ID's can only contain alphanumeric characters.  drop all - and .'s
def clean_metric_id(metric_id):
    clean = metric_id.replace("-", "")
    clean = clean.replace(".", "")
    return clean

# Deserialize datetime objects for debugging


def dtconverter(o):
    if isinstance(o, datetime):
        return o.__str__()

# Query cloudwatch for metrics


def query_cloudwatch(start_time, end_time, metrics_list, client):
    metric_queries = []
    for metric in metrics_list["Metrics"]:
        metric_id = [x['Value']
                     for x in metric["Dimensions"] if x["Name"] == "BucketName"][0]

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
        ScanBy='TimestampAscending',
        MetricDataQueries=metric_queries,
        StartTime=start_time,
        EndTime=end_time)
    # print(json.dumps(response['MetricDataResults'], indent=2, default=dtconverter))
    return response


def write_csv(metrics):
    with open('/tmp/tmp.csv', 'w', newline='') as csvfile:
        csvwriter = csv.writer(
            csvfile, delimiter=',', quotechar='\'', quoting=csv.QUOTE_MINIMAL)

        temprow = [' '] + [x.date()
                           for x in metrics['MetricDataResults'][0]["Timestamps"]]
        csvwriter.writerow(temprow)

        for metric in metrics['MetricDataResults']:
            csvwriter.writerow([metric['Label']] + metric['Values'])

    print("csv_written")


def handler(event, context):
    cloudwatch = boto3.client('cloudwatch')
    s3 = boto3.client('s3')

    # get list of metrics from CloudWatch
    metrics_list = cloudwatch.list_metrics(
        Namespace='AWS/S3',
        MetricName='BucketSizeBytes',
    )

    # specify start and end time
    # start_time = datetime(2018, 10, 1)
    # end_time = datetime(2018, 10, 31)
    days_to_subtract = 8
    start_time = datetime.today() - timedelta(days=days_to_subtract)
    end_time = datetime.today() - timedelta(days=1)
    print("{} -> {}".format(start_time, end_time))

    metrics = query_cloudwatch(start_time, end_time, metrics_list, cloudwatch)
    write_csv(metrics)
    filename = '/tmp/tmp.csv'
    bucket_name = os.environ["BUCKET"]
    file_name = os.environ['FILENAME']

    timestr = time.strftime("%Y%m%d-%H%M%S")
    print(timestr)
    print(file_name)


# Uploads the given file using a managed uploader, which will split up large
# files automatically and upload parts in parallel.
    return s3.upload_file(filename, bucket_name, "{}-{}.csv".format(file_name, timestr))
