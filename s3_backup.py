#!/usr/bin/python
#
# This script creates a zip file of a directory and uploads it to an S3 bucket. This script
# should run on an AWS instance with an IAM role giving the instance (and this script)
# access to the necessary resources and actions.
#

import os
import argparse
import boto
from boto.s3.key import Key
from datetime import datetime
from zipfile import ZipFile, ZIP_DEFLATED

def get_date():
    return datetime.today().strftime('%Y%m%d%H%M%S')

def zip_dir(dir_name, output_file):
    with ZipFile(output_file, 'w', ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(dir_name):
            for f in files:
                z.write(os.path.join(root, f))

def upload_zip(bucket, key, file_name):
    s3_prefix = '/backup/'
    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket)
    k = Key(bucket)
    k.key = s3_prefix + file_name
    k.set_contents_from_filename(file_name)

def backup_dir(path, bucket):
    if not os.path.isdir(path):
        raise ValueError('%s must be a directory.' % path)
    dir_name = os.path.basename(os.path.normpath(path))
    temp_file = '%s-backup-%s.zip' % (dir_name, get_date())
    zip_dir(path, temp_file)
    upload_zip(bucket, temp_file, temp_file)
    os.remove(temp_file)

def main(args):
    for d in args.dir:
        backup_dir(d, args.bucket)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Zips up a directory and uploads it to an S3 bucket')
    parser.add_argument('--bucket', nargs='?', required=True, help='S3 Bucket')
    parser.add_argument('--dir', nargs='+', help='Directory to zip')
    args = parser.parse_args()
    if not (args.dir):
        parser.error('--dir value required')
    main(args)