import boto3
from datetime import datetime, timezone, timedelta

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = 'kstsai'  
    expiry = 30
    max = datetime.now(timezone.utc) - timedelta(days=expiry)
    
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    if 'Contents' in response:
        for items in response['Contents']:
            if items['LastModified'] < max:
                print(f"Deleting {items['Key']}")
                s3.delete_object(Bucket=bucket_name, Key=items['Key'])
            else:
                print(f"Retaining {items['Key']}")
                
    return {
        'statusCode': 200,
        'body': 'Cleanup job completed.'
    }