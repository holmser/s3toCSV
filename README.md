# S3 to CSV

This is a simple script that will grab data from cloudwatch and export it into CSV format.  The flow of the script is as follows:

1.  Get a list of all metrics in the CloudWatch Namespace "AWS/S3" and MetricName "BucketSizeBytes"
2.  Request those metrics using a period of 1 day (86400 seconds)
3.  Dump those metrics into a CSV

Dates are currently hardcoded.  Could be adapted into a lambda to write output to S3.