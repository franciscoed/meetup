import boto3
import json

snsARN = 'arn:aws:sns:us-east-1:984680580683:summittrail'

def lambda_handler(event, context):
	eventname = event['detail']['eventName']
	snsclient = boto3.client('sns')
	if (eventname == 'StopLogging'):
	    cloudtrailArn= event['detail']['requestParameters']['name']
	    snspublish = snsclient.publish(
	                     TargetArn = snsARN,
	                     Subject=("INCIDENTE DE SEGURANÇA - Cloudtrail."),
	                     Message=json.dumps({'default': json.dumps(event)}),
	                     MessageStructure='json')
	    
	    try:
	        client = boto3.client('cloudtrail')
	        enablelogging = client.start_logging(Name=cloudtrailArn)
	    except:
	        print("Erro ativando Cloudtrail")
	else:
		snspublish = snsclient.publish(
						TargetArn= snsARN,
						Subject=("CloudTrail ativado com sucesso"),
						Message=json.dumps({'default': json.dumps(event)}),
						MessageStructure='json')

