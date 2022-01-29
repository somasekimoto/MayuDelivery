import boto3
from datetime import datetime
import time
import urllib
import os.path
import shutil
import json


def upload(file, index):
    TEMP_DIR = "tmp"

    s3 = boto3.client('s3')
    bucket_name = os.getenv('S3_BUCKET')

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
    s3.upload_file(local_file, bucket_name, s3_object_path)


def all_files(event, context):
    s3 = boto3.resource('s3')
    bucket_name = os.getenv('S3_BUCKET', 'stg-mayu-media-daily')
    bucket = s3.Bucket(bucket_name)
    keys = [obj.key for obj in bucket.objects.all()]
    response = {
        "body": json.dumps({"keys": keys}),
    }
    return response


if __name__ == '__main__':
    # upload(None, None)
    print(all_files(None, None))
