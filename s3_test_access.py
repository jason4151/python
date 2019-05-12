#!/usr/bin/env python

import os
import boto
from boto.s3.key import Key

prefix = 'bucker-prefix' # Bucket Prefix
conn = boto.connect_s3()
bucket = conn.get_bucket('bucket-name-us-east-1') # Bucket Name
k = Key(bucket)
k.key = os.path.join(prefix, 'foo.txt')
k.set_contents_from_filename('foo.txt')
k.get_contents_to_filename('foo.txt')