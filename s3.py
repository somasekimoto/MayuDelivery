import boto3
from datetime import datetime
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


def all_files(event, context):
    bucket = s3_resource.Bucket(bucket_name)
    keys = [obj.key for obj in bucket.objects.all()]
    urls = [gen_presigned_url(key) for key in keys]
    response = {
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


if __name__ == '__main__':
    # upload(None, None)
    print(all_files(None, None))
