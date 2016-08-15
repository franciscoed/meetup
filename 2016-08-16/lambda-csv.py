from __future__ import print_function

import json
import boto3
import csv
import urllib2
import urllib


print('Loading function')

s3 = boto3.client('s3')
lista = ('RENT3', 'KLBN4', 'ABEV3', 'BVMF3', 'EMBR3', 'HYPE3')



def downloadCSV (stock):
    url = 'http://www.google.com/finance/historical?q=BVMF%3A' + stock + '&output=csv'

    print(url)
    try:
        response = urllib2.urlopen(url).read()
    except Exception as e:
        raise e
    return response


def lambda_handler(event, context):
    bucket = 'meetup1608'

    for i in range(len(lista)):
        key=lista[i]
        csv=downloadCSV(key)
        try:
            response = s3.put_object(Bucket=bucket, Key=key, Body=csv)
            print('upload {} ok'.format(key))

        except Exception as e:
            print('Error putting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
            raise e
    return 0
