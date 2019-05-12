#!/usr/bin/python
#
# This script creates a snapshot of an EBS volume and tags it. It also purges all old snapshots
# based on snap_to_keep. This script should run on an AWS instance with an IAM role giving the
# instance (and this script) access to the necessary resources and actions.
#

import boto.ec2
import boto.utils
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', filename='ebs-snap.log', level=logging.INFO)

instance_id = boto.utils.get_instance_metadata()['instance-id']
region = boto.utils.get_instance_metadata()['placement']['availability-zone'][:-1]
zone = boto.utils.get_instance_metadata()['placement']['availability-zone']
snap_to_keep = 1

conn = boto.ec2.connect_to_region(region)

if conn:
    exs_data_volumes = conn.get_all_volumes(filters={'tag-key': 'Name', 'tag-value': 'server'})
    if exs_data_volumes:
        # Create a new snapshot of the server data volume
        for vol in exs_data_volumes:
            logging.debug('Creating Snapshot of: %s', vol.id)

            snap = conn.create_snapshot(vol.id, "Server data snapshot")
            logging.info('Created Snapshot ID: %s', snap.id)

        # Tag the snapshot
        conn.create_tags([snap.id], {"Name": "server"})

        # Get all exs data snapshots for comparison
        exs_data_snapshots = conn.get_all_snapshots(filters={'tag-key': 'Name', 'tag-value': 'server'})

        purgeable = sorted(exs_data_snapshots, key=lambda x: x.start_time)[:-snap_to_keep]
        for old_snap in purgeable:
            conn.delete_snapshot(old_snap.id)
            logging.debug('Deleted Snapshot ID: %s', old_snap.id)
