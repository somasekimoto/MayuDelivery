import boto3
from datetime import datetime, date, timedelta
import time
import urllib
import os.path
import shutil
import json

s3_client = boto3.client('s3')
s3_resource = boto3.resource('s3')
bucket_name = os.getenv('S3_BUCKET', 'stg-mayu-media-daily')


def upload(file, index):
    TEMP_DIR = "tmp"

    root, ext = os.path.splitext(file)
    qs = urllib.parse.urlparse(file).query
    if len(qs):
        ext = ext.replace('?' + qs, '')

    with urllib.request.urlopen(file, timeout=5) as data:
        img = data.read()
        local_file = '/' + TEMP_DIR + '/' + str(index) + ext
        with open(local_file, 'wb') as f:
            f.write(img)

    today_str = datetime.today().strftime(f"%Y-%m-%d")
    s3_object_path = today_str + '/dailyMayu' + str(index) + ext
    s3_client.upload_file(local_file, bucket_name, s3_object_path)


def fetch_files(event, context):
    try:
        print("event")
        print(event)
        token = event['queryStringParameters']['token']
        if(is_token_valid(token) is False):
            return {"statusCode": 401, "body": json.dumps({"message": "Unauthorized"})}
    except KeyError as ke:
        print(ke)
        return {"statusCode": 401, "body": json.dumps({"message": "Unauthorized"})}
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": json.dumps({"message": "something's wrong!"})}

    from_string = event['queryStringParameters']['from']
    to_string = event['queryStringParameters']['to']
    from_date = datetime.strptime(from_string, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_string, '%Y-%m-%d').date()
    days = (to_date - from_date).days

    keys = []
    dt = from_date
    bucket = s3_resource.Bucket(bucket_name)
    for num in range(days + 1):
        dt += timedelta(days=num)
        prefix = dt.strftime('%Y-%m-%d')
        for obj in bucket.objects.filter(Prefix=prefix):
            keys.append(obj.key)
        urls = [gen_presigned_url(key) for key in keys]

    response = {
        "statusCode": 200,
        "body": json.dumps({"urls": urls}),
    }
    return response


def gen_presigned_url(key_name):
    presigned_url = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': bucket_name, 'Key': key_name
        },
        ExpiresIn=3600
    )
    return presigned_url


def is_token_valid(token: str) -> bool:

    return (token == os.getenv("MAYU_DELIVERY_TOKEN"))


if __name__ == '__main__':
    # upload(None, None)
    event = {'queryStringParameters': {
        'from': '2021-03-06',
        'to': '2021-03-08',
        'token': os.getenv("MAYU_DELIVERY_TOKEN")
    }
    }
    print(fetch_files(event, None))
