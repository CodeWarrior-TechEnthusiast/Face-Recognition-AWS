import os

import boto3
import json

from boto3.dynamodb.conditions import Key

import publishMQ

from eval_face_recognition import recognize_face

input_bucket = "cse-546-p2-raspberry-pi-faces"
records_key = "Records"

def face_recognition_handler(event, context):
    s3_client = boto3.resource('s3')
    records = event[records_key]
    record = records[0]
    object_key = record.get('s3').get('object').get('key')
    print(f'S3 object key: {object_key}')
    image = s3_client.Object(input_bucket,object_key).get()['Body'].read()
    name = recognize_face(image)

    mq = get_MQ()
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('Students')
    result = table.query(
        KeyConditionExpression=Key('name').eq(name)
    )['Items']
    response = ""
    for row in result:
        response += f"Student name: {row['name']}, year: {row['year']}, major: {row['major']}"

    mq.publish_message(message=bytes(response, 'utf-8'), queue=os.environ.get('MQ_NAME'))
    return {
        "statusCode": 200,
        "body": response
    }

def get_MQ():
    MQ_BROKER_ID = os.environ.get("MQ_BROKER_ID")
    MQ_USERNAME = os.environ.get("MQ_USERNAME")
    MQ_PASSWORD = os.environ.get("MQ_PASSWORD")
    MQ_REGION = os.environ.get("MQ_REGION")
    return publishMQ.MQ(str(MQ_BROKER_ID), str(MQ_USERNAME), str(MQ_PASSWORD), str(MQ_REGION))