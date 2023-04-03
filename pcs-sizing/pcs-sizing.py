import json, os, argparse

parser = argparse.ArgumentParser()
parser.add_argument("--azure", "-az", help="Sizing for Azure", action='store_true')
parser.add_argument("--aws", "-a", help="Sizing for AWS", action='store_true')
parser.add_argument("--gcp", "-g", help="Sizing for GCP", action='store_true')
parser.add_argument("--project", "-p", help="Project (only for GCP)", type=str)
args = parser.parse_args()
sep = "--------------------------------------------------------------------"

def tables(account,acc,data):
    print ("{:<40} {:<15} {:<10}\n{}".format(account,'Service','Count',sep))
    for i in data:
        a,b = i
        print ("{:<40} {:<15} {:<10}".format(acc,a,b))
    print(sep)

def pcs_sizing_aws():
    import boto3
    client_ec2 = boto3.client('ec2')
    client_ecs = boto3.client('ecs')
    sts_client = boto3.client("sts")
    org_client = boto3.client('organizations')

    # response = org_client.list_accounts()
    # print(response)
    account = sts_client.get_caller_identity()["Account"]
    print("\n{}\nGetting Resources from AWS\n{}".format(sep,sep))

    # Get EC2 instances running.
    ec2_group = client_ec2.describe_instances(
        Filters=[{
        'Name': 'instance-state-code',
        'Values': ["0","16","32","64","80"] # 0 (pending), 16 (running), 32 (shutting-down), 48 (terminated), 64 (stopping), and 80 (stopped)
            },
        ]
        )['Reservations']


    # Get EC2 instances running on EKS.
    eks_list = []
    for ec2 in ec2_group:
        tags = ec2['Instances'][0]['Tags']
        for tag in tags:
            if "eks:" in tag["Key"]:
                eks_list.append(ec2['Instances'][0])
                break

    # Get Fargate task running.
    fargate_tasks = client_ecs.list_task_definitions()['taskDefinitionArns']

    tables("Account",account,
           [
        ["EC2", len(ec2_group)],
        ["EKS_NODES", len(eks_list)],
        ["FARGATE_TASKS", len(fargate_tasks)]
        ])

def pcs_sizing_az():

    from azure.mgmt.compute import ComputeManagementClient
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.containerservice import ContainerServiceClient
    from azure.mgmt.subscription import SubscriptionClient
    sub_client = SubscriptionClient(credential=DefaultAzureCredential())
    print("\n{}\nGetting Resources from AZURE\n{}".format(sep,sep))
    for sub in sub_client.subscriptions.list():
        compute_client = ComputeManagementClient(credential=DefaultAzureCredential(), subscription_id=sub.subscription_id)
        containerservice_client = ContainerServiceClient(credential=DefaultAzureCredential(), subscription_id=sub.subscription_id)
        # List VMs in subscription
        vm_list = []
        for vm in compute_client.virtual_machines.list_all():
            vm_list.append(vm)

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

        tables("Subscription",str(sub.display_name + " (" + sub.subscription_id.split('-')[4].strip() + ")"),
            [
            ["VM", len(vm_list)],
            ["AKS_NODES", node_count]
            ])

def pcs_sizing_gcp(project):

    from google.auth import compute_engine
    from google.cloud.resourcemanager import ProjectsClient
    from google.cloud import compute_v1
    from google.cloud import container_v1beta1
    from google.cloud import resourcemanager_v3
    from collections import defaultdict
    
    print("\n{}\nGetting Resources from GCP\n{}".format(sep,sep))

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

    tables("Project",project,
           [
        ["VM", len(compute_list)],
        ["GKE_NODES", node_count]
        ])

if __name__ == '__main__':
    if args.aws == True:
        pcs_sizing_aws()
    elif args.azure == True:
        pcs_sizing_az()  
    elif args.gcp == True:#and args.project:
        pcs_sizing_gcp(project=args.project)
    elif args.gcp == True and not args.project:
        print("If GCP is selected, you must specify a project.")
        exit()
    else:
        pcs_sizing_aws(), pcs_sizing_az()