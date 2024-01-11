import json, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--azure", "-az", help="Sizing for Azure", action='store_true')
parser.add_argument("--aws", "-a", help="Sizing for AWS", action='store_true')
parser.add_argument("--gcp", "-g", help="Sizing for GCP", action='store_true')
parser.add_argument("--oci", "-o", help="Sizing for OCI", action='store_true')
parser.add_argument("--project", "-p", help="Project (only for GCP)", type=str)
args = parser.parse_args()
separator = "--------------------------------------------------------------------"

def tables(account,acc,data):
    for i in data:
        a,b = i
        print ("{:<40} {:<20} {:<10}".format(acc,a,b))
    print(separator)

def pcs_sizing_aws():
    import boto3
    import botocore
    from botocore.exceptions import ClientError

    client_ec2 = boto3.client('ec2')
    sts = boto3.client("sts")
    org = boto3.client('organizations')

    print("\n{}\nGetting Resources from AWS for all Regions\n{}".format(separator,separator))

    accounts = []
    # paginator = org.get_paginator('list_accounts')
    # for page in paginator.paginate():
    #     for account in page['Accounts']:
    #         accounts.append(account['Id'])
    #         response = sts.assume_role(
    #             RoleArn="arn:aws:iam::" + account['Id'] + ":role/OrganizationAccountAccessRole",
    #             RoleSessionName=account['Id']
    #         )
    try:
        account = sts.get_caller_identity()["Account"]
    except botocore.exceptions.ClientError as error:
        # Put your error handling logic here
        raise error

    try:
        regions = [region['RegionName'] for region in client_ec2.describe_regions()['Regions']]
    except botocore.exceptions.ClientError as error:
        raise error
    
    us_regions = [x for x in regions if x.startswith("us")]

    try:
        ec2_all = 0
        eks_all = 0
        fargate_all = 0
        lambdas_all = 0

        for region in regions:

            ec2 = boto3.client('ec2',region_name=region)
            client_ecs = boto3.client('ecs',region_name=region)
            lambda_client = boto3.client('lambda',region_name=region)
            # Get EC2 instances running.
            try:
                ec2_group = ec2.describe_instances(
                    Filters=[{
                    'Name': 'instance-state-code',
                    'Values': ["16"] # 0 (pending), 16 (running), 32 (shutting-down), 48 (terminated), 64 (stopping), and 80 (stopped)
                        },
                    ]
                    )['Reservations']
                ec2_all += len(ec2_group)
            except botocore.exceptions.ClientError as error:
                raise error
    
            try:
            # Get EC2 instances running on EKS.
                eks_list = []
                for ec2 in ec2_group:
                    tags = ec2['Instances'][0]['Tags']
                    for tag in tags:
                        if "eks:" in tag["Key"]:
                            eks_list.append(ec2['Instances'][0])
                            eks_all += 1
                            break
            except botocore.exceptions.ClientError as error:
                raise error
            
            try:
                # Get Fargate task running.
                fargate_tasks = client_ecs.list_task_definitions()['taskDefinitionArns']
                fargate_all += len(fargate_tasks)
            except botocore.exceptions.ClientError as error:
                raise error
            
            try:
            # Get AWS Lambdas
                lambdas = lambda_client.list_functions()['Functions']
                lambdas_all += len(lambdas)
            except botocore.exceptions.ClientError as error:
                raise error
        print ("{:<40} {:<20} {:<10}\n{}".format('Account','Service','Count',separator))
        
        tables("Account",account,
            [
            ["EC2", ec2_all],
            ["EKS_NODES", eks_all],
            ["FARGATE_TASKS", fargate_all],
            ["LAMBDAS_FUNCTIONS", lambdas_all]
            ])
        
    except botocore.exceptions.ClientError as error:
        raise error

def pcs_sizing_az():

    from azure.mgmt.compute import ComputeManagementClient
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.containerservice import ContainerServiceClient
    from azure.mgmt.subscription import SubscriptionClient
    from azure.mgmt.web import WebSiteManagementClient
    sub_client = SubscriptionClient(credential=DefaultAzureCredential())
    print("\n{}\nGetting Resources from AZURE\n{}".format(separator,separator))
    for sub in sub_client.subscriptions.list():
        compute_client = ComputeManagementClient(credential=DefaultAzureCredential(), subscription_id=sub.subscription_id)
        containerservice_client = ContainerServiceClient(credential=DefaultAzureCredential(), subscription_id=sub.subscription_id)
        app_service_client = WebSiteManagementClient(credential=DefaultAzureCredential(), subscription_id=sub.subscription_id)
        # List VMs in subscription
        vm_list = []
        for vm in compute_client.virtual_machines.list_all():
            array = vm.id.split("/")
            resource_group = array[4]
            vm_name = array[-1]
            statuses = compute_client.virtual_machines.instance_view(resource_group, vm_name).statuses
            status = len(statuses) >= 2 and statuses[1]
            if status and status.code == 'PowerState/running':
                vm_list.append(vm_name)

        # List AKS Clusters in subscription
        clusters_list = []
        node_count = 0
        for cl in containerservice_client.managed_clusters.list():
            clusters_list.append(cl.name)
            agent_pool = containerservice_client.agent_pools.list(
                cl.id.split('/')[4].strip(),
                cl.name
            )
            for ap in agent_pool:
                node_count += ap.count

        # List Azure Functions
        function_list = 0
        for function in app_service_client.web_apps.list():
            if function.kind.startswith('function'):
                function_list += 1
        print ("{:<40} {:<20} {:<10}\n{}".format('Subscription','Service','Count',separator))
        tables("Subscription",str(sub.display_name + " (" + sub.subscription_id.split('-')[4].strip() + ")"),
            [
            ["VM", len(vm_list)],
            ["AKS_NODES", node_count],
            ["AZURE_FUNCTIONS",function_list]
            ])

def pcs_sizing_gcp(project):

    from google.auth import compute_engine
    from google.cloud.resourcemanager import ProjectsClient
    from google.cloud import compute_v1
    from google.cloud import container_v1beta1
    from google.cloud import resourcemanager_v3
    from collections import defaultdict
    
    print("\n{}\nGetting Resources from GCP\n{}".format(separator,separator))

    # pj_client = resourcemanager_v3.ProjectsClient()
    # request = resourcemanager_v3.ListProjectsRequest(
    #     parent="parent_value",
    # )
    # page_result = pj_client.list_projects()
    # for response in page_result:
    #     print(response)

    # Getting the Compute Instances
    compute_client = compute_v1.InstancesClient()
    request = compute_v1.AggregatedListInstancesRequest()
    request.project = project
    agg_list = compute_client.aggregated_list(request=request)
    all_instances = defaultdict(list)
    compute_list = []
    for zone, response in agg_list:
        if response.instances:
            for instance in response.instances:
                if instance.status == "RUNNING":
                    compute_list.append(instance.name)

    # Getting the Compute Instances for GKE
    gke_client = container_v1beta1.ClusterManagerClient()
    gke_request = container_v1beta1.ListClustersRequest()
    gke_request.project_id = project
    gke_request.zone = "-"
    response = gke_client.list_clusters(request=gke_request)
    node_count = 0
    for cluster in response.clusters:
        node_count += cluster.current_node_count

    print ("{:<40} {:<20} {:<10}\n{}".format('Project','Service','Count',separator))
    tables("Project",project,
           [
        ["VM", len(compute_list)],
        ["GKE_NODES", node_count]
        ])

def pcs_sizing_oci():

    import oci
    
    print("\n{}\nGetting Resources from OCI\n{}".format(separator,separator))
    config = oci.config.from_file()
    IdentityClient = oci.identity.IdentityClient(config)
    ComputeClient = oci.core.ComputeClient(config)
    ContainerClient = oci.container_engine.ContainerEngineClient(config)

    # List all Compartments

    compartments = IdentityClient.list_compartments(
        compartment_id=config['tenancy']
    )
    
    # Adding the compartment root to the list
    compartments_list = []
    compartments_list.append({'Name':"root","Id":config['tenancy']})

    for compartment in compartments.data:
        data = {'Name':compartment.name,"Id":compartment.id}
        compartments_list.append(data)

    # For every compartment, list all the VMs and OKE nodes (TODO)
    
    print ("{:<40} {:<20} {:<10}\n{}".format('Compartment','Service','Count',separator))
    for compartment in compartments_list:
        response = ComputeClient.list_instances(compartment_id=compartment['Id'])
        compute_oci = 0
        for instance in response.data:
            if instance.lifecycle_state == "RUNNING":
                compute_oci += 1

        # node_pool = ContainerClient.list_node_pools(compartment_id=compartment['Id'])
        # print(node_pool.data)
    
        tables("Compartment",compartment['Name'],
            [
            ["Compute_Instances", compute_oci]
            ])
        
if __name__ == '__main__':
    if args.aws == True:
        pcs_sizing_aws()
    elif args.azure == True:
        pcs_sizing_az()  
    elif args.oci == True:
        pcs_sizing_oci()  
    elif args.gcp == True:#and args.project:
        pcs_sizing_gcp(project=args.project)
    elif args.gcp == True and not args.project:
        print("If GCP is selected, you must specify a project.")
        exit()
    else:
        print("You must specify an argument.\n\x1B[3m'--aws'\x1B[0m for AWS\n\x1B[3m'--azure'\x1B[0m for Azure\n\x1B[3m'--gcp --project <project-name>'\x1B[0m for GCP\n\x1B[3m'--oci'\x1B[0m for OCI")