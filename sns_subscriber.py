#!/usr/bin/python

import boto3
import json

sns = boto3.client('sns')
funks = boto3.client('lambda')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    print event
    if 'delete' != event['action']:
      print 'Adding new subscription'
      result = sns.subscribe(
          TopicArn=event['payload']['SNSTopic'], 
          Protocol=event['payload']['TopicProtocol'],
          Endpoint=event['payload']['TopicEndpoint'])
              
      print result
      return {"SubscriptionARN": result['SubscriptionArn']}
    else:
      print 'Deleting subscription for teardown'
      subscription_arn = next(sub for sub in sns.list_subscriptions_by_topic(TopicArn=event['payload']['SNSTopic'])['Subscriptions'] if sub['Protocol'] == event['payload']['TopicProtocol'] and sub['Endpoint'] == event['payload']['TopicEndpoint'])['SubscriptionArn']
      print subscription_arn
      sns.unsubscribe(SubscriptionArn=subscription_arn)
      return {"SubscriptionARN": ""}


if __name__ == '__main__':
    import sys
    session = boto3.Session(region_name='us-east-1', profile_name='demo')
    sns = session.client('sns')
    funks = session.client('lambda')
    print lambda_handler(json.loads(sys.argv[1]), None)


