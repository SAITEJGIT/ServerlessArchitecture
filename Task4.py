import boto3
import json
from datetime import datetime

specific_volume_id = 'vol-05b137467c1f06601'
ec2 = boto3.client('ec2', region_name='ap-northeast-2')

def lambda_handler(event, context):
    res = ec2.create_snapshot(
        Description="This is a backup snapshot of the volume which i have been working on",
        VolumeId=specific_volume_id,
        TagSpecifications=[
            {
                'ResourceType': 'snapshot',
                'Tags': [
                    {
                        'Key': 'Name',
                        'Value': 'Backup-global-Jenkins'
                    },
                ]
            },
        ],
        DryRun=False
    )
    Stuff()
    return json.dumps('Snapshot created successfully')