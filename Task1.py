import boto3
import json

ec2 = boto3.client('ec2', region_name='ap-northeast-2')
run = []
stop = []
stopped_instances = []
running_instances = []

def lambda_handler(event, context):
    instances = ec2.describe_instances()
    for items in instances['Reservations']:
        for instance in items['Instances']:
            if instance['State']['Name'] == 'stopped':
                stopped_instances.append(instance)
            elif instance['State']['Name'] == 'running':
                running_instances.append(instance)


    print("----> Stopped Instances <----")

    stopped = [tag['Value'] for instance in stopped_instances for tag in instance.get('Tags', []) if tag['Key'] == 'Name']
    for item in stopped:
        stop.append(item)
        print('Stopped instance: {}'.format(item))

    print("----> Running Instances <----")

    running= [tag['Value'] for instance in running_instances for tag in instance.get('Tags', []) if tag['Key'] == 'Name']
    for item in running:
        run.append(item)
        print('Running instance: {}'.format(item))
    
    Condition()
    return {
        'statusCode': 200,
        'body': json.dumps({'stopped': run, 'running': stop})
    }
    # return json.dumps({'stopped': stopped, 'running': running})

def Condition():
    # start instance by tag-name using boto3
    def start_instance():
        for instance in stopped_instances:
            if 'Auto-Start' in [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']:
                ec2.start_instances(InstanceIds=[instance['InstanceId']])
                print('Starting instance: {}'.format(instance['InstanceId']))
            elif 'Auto-Start' not in [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']:
                print('Auto-Start not found running')
            else:
                print("Condition satisfied")
    # stop instance by tag-name using boto3
    def stop_instance():
        for instance in running_instances:
            if 'Auto-Stop' in [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']:
                ec2.stop_instances(InstanceIds=[instance['InstanceId']])
                print('Stopping instance: {}'.format(instance['InstanceId']))
            elif 'Auto-Stop' not in [tag['Value'] for tag in instance.get('Tags', []) if tag['Key'] == 'Name']:
                print('Auto-Stop not found running')
            else:
                print('Condition satisfied')
    start_instance()
    stop_instance()