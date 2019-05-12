#!/usr/bin/python

import boto3

def lambda_handler(event, context):
    bucket = event['bucket']
    backup(bucket)

def backup(bucket):
    #Create an s3 client
    s3 = boto3.client('s3')

    # Call to S3 to retrieve the policy for the given bucket
    bucketpolicy = str(s3.get_bucket_policy(Bucket=bucket))
    print(bucketpolicy)

    # Create new object under root of bucket
    s3write = boto3.resource('s3')
    s3write.Object(bucket, 'bucketpolicy_backup.json').put(Body=bucketpolicy)