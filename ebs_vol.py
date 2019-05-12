#!/usr/bin/python
#
# This script creates a new EBS volume, tags it and attaches it to an instance. If a
# snapshot exists then the volume is created from the snapshot. This script should
# run on an AWS instance with an IAM role giving the instance (and this script) access
# to the necessary resources and actions.
#

import boto.ec2
import boto.utils
import time
from boto.ec2.blockdevicemapping import BlockDeviceMapping
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='ebs-vol.log', level=logging.INFO)

instance_id = boto.utils.get_instance_metadata()['instance-id']
region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
zone = boto.utils.get_instance_metadata()['placement']['availability-zone']

conn = boto.ec2.connect_to_region(region)

if conn:
    exs_data_snapshots = conn.get_all_snapshots(filters={'tag-key': 'Name', 'tag-value': 'server'})

    if exs_data_snapshots:
        # If snapshot exists, create volume from the snapshot
        vol = conn.create_volume(100, zone, snapshot=exs_data_snapshots[0], volume_type='gp2')
        logging.info('Created Volume ID: %s', vol.id)
    else:
        vol = conn.create_volume(100, zone, volume_type='gp2')
        logging.info('Created Volume ID: %s', vol.id)

    # Tag the volume
    conn.create_tags([vol.id], {"Name": "server"})

    # Allow time for volume to become available
    time.sleep(15)

    # Check that the volume is now ready and available
    curr_vol = conn.get_all_volumes([vol.id])[0]
    logging.info('Volume Status: %s', curr_vol.status)
    logging.info('Volume Zone: %s', curr_vol.zone)

    # Attach volume to instance
    attach_vol = conn.attach_volume(vol.id, instance_id, "/dev/sdx")
    logging.debug('Attach Volume Result: %s', attach_vol)
    time.sleep(15)

    # Set new volume to delete on instance termination
    logging.debug('Set volume to delete on instance termination')
    conn.modify_instance_attribute(instance_id, 'blockDeviceMapping', {"/dev/sdx": True})
