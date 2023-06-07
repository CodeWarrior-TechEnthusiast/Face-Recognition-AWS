import os

import boto3
import logging
from PIL import Image
import io

s3 = boto3.resource('s3')

FRAME_BUCKET = os.environ.get('FRAME_BUCKET')
VIDEO_BUCKET = os.environ.get('VIDEO_BUCKET')
STORE_TO_S3 = os.environ.get('STORE_TO_S3', "0")

def process_image_data(data):
    img = Image.fromarray(data, 'RGB')
    out_img = io.BytesIO()
    img.save(out_img, format='png')
    out_img.seek(0)
    return out_img

def upload_video_to_s3(video_file, filename):
    if STORE_TO_S3 != "0":
        s3.Bucket(VIDEO_BUCKET).upload_file(video_file, filename)

def upload_resource_to_s3(bucket, resource_name, resource):
    if STORE_TO_S3 != "0":
        s3.Bucket(bucket).put_object(Key=resource_name, Body=resource)

