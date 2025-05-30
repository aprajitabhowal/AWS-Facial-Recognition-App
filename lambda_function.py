import json
import boto3
import os
import subprocess
from video_splitting_cmdline import video_splitting_cmdline


def lambda_handler(event, context):
    print(event)
    output = video_splitting_cmdline(event['Records'][0]['s3']['object']['key'])
    print("Output:", output)
    return {
        'statusCode': 200,
        'body': json.dumps('Video Split Successful')
    }
    

