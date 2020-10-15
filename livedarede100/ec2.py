import boto3
import json
import base64
import zlib

snsARN = 'arn:aws:sns:us-east-1:167798398842:Lambda'


def lambda_handler(event, context):
    log = zlib.decompress(base64.b64decode(event['awslogs']['data']), 16 + zlib.MAX_WBITS).decode('utf-8')
    snsclient = boto3.client('sns')
    json_log = json.loads(log)
    for item in json_log['logEvents']:
        if "USER_AUTH" in item['message']:
            snspublish = snsclient.publish(
	                     TargetArn = snsARN,
	                     Subject=("INCIDENTE DE SEGURANÇA - EC2"),
	                     Message=json.dumps({'default': json.dumps(item['message'])}),
	                     MessageStructure='json')
