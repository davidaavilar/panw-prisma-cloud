import json, os, argparse

sep = "--------------------------------------------------------------------"

def pcs_sizing_aws():
    import boto3
    import botocore
    from botocore.exceptions import ClientError

    client_ec2 = boto3.client('ec2')
    sts = boto3.client("sts")

    print("\n{}\nGetting Resources from AWS\n{}".format(sep,sep))
    try:
        account = sts.get_caller_identity()["Account"]
    except botocore.exceptions.ClientError as error:
        raise error

    try:
        regions = [region['RegionName'] for region in client_ec2.describe_regions()['Regions']]
    except botocore.exceptions.ClientError as error:
        raise error
    
    us_regions = [x for x in regions if x.startswith("us")]

    print ("{:<15} {:<15} {:<40} {:<22} {:<15} {:<20}\n".format("Account", 'Region', 'Name', 'Id', 'Type', 'VpcId'))

    try:
        ec2_all = 0
        for region in us_regions:

            ec2 = boto3.client('ec2',region_name=region)
            client_ecs = boto3.client('ecs',region_name=region)
            lambda_client = boto3.client('lambda',region_name=region)
            # Get EC2 instances running.
            try:
                ec2_group = ec2.describe_instances(
                    Filters=[{
                    'Name': 'instance-state-code',
                    'Values': ["0","16","32","64","80"] # 0 (pending), 16 (running), 32 (shutting-down), 48 (terminated), 64 (stopping), and 80 (stopped)
                        },
                    ]
                    )['Reservations']
                ec2_all += len(ec2_group)
            except botocore.exceptions.ClientError as error:
                raise error

            for ec2 in ec2_group:
                ec2_id = ec2['Instances'][0]['InstanceId']
                name = ''
                for i in ec2['Instances'][0]['Tags']:
                    if i['Key'] == 'Name':
                        name = i['Value']
                        break
                vpc = ec2['Instances'][0]['VpcId']
                ec2_type = ec2['Instances'][0]['InstanceType']
                print ("{:<15} {:<15} {:<40} {:<22} {:<15} {:<20}\n".format(account, region, name, ec2_id, ec2_type, vpc))

        
    except botocore.exceptions.ClientError as error:
        raise error

if __name__ == '__main__':
    pcs_sizing_aws()