# Deploy a Sample App in AWS Fargate

This Terraform helps you to deploy a Sample Web App in AWS Fargate.. This deploy an NGINX sample app.

### Pre-requisites 📋

1. You have to login to your AWS Console account and upload the Terraform file into your Cloud Shell, or you can use your local machine. You must have `terraform` and `aws cli` installed.

2. You have to udpate the Terraform variables (`variables.tf`).
	
	There are default values for the nginx sample app. Feel free to update all your params.

### How to deploy the sample app:

```
terraform init
```

```
terraform apply
```

If deploy is successful, you gonna see the alb_dns from terraform outputs to access to the app via Internet.

Also, you can access to AWS Console and naviagate to ECS Service, go to Cluster and you will be able to see the cluster deployed, the services and the tasks definition.

### Installing Prisma Cloud Defender

You can follow these steps: [Prisma Cloud app-embedded Defender](https://docs.paloaltonetworks.com/prisma/prisma-cloud/prisma-cloud-admin-compute/install/install_defender/install_app_embedded_defender_fargate).

**IMPORTANT NOTE:** If you are trying to deploy a Defender and the tasks are constantly rebooting, it could be because the app image your are using does not have entrypoint or command. You must configure an entrypoint.

If the task does not have an entrypoint you can execute `docker inspect` to extract the entrypoint and command params.

For example:

```
docker pull nginx
docker inspect nginx
```

When you are generating the task for Prisma Cloud, there is a help to check this.

### Cleaning Up

```
terraform destroy
```

