# PrismaCloud_TF_BulkOnboardingCloudAccounts.tf

This script helps you to onboard your AWS Cloud Accounts in bulk to Prisma Cloud

### How to 📋

1. Install terraform - https://www.terraform.io/downloads.html

2. Install Go - https://golang.org/doc/install

3. Create .prismacloud_auth.json with the Prisma Cloud credentials - https://registry.terraform.io/providers/PaloAltoNetworks/prismacloud/latest/docs

	.prismacloud_auth.json parameters:

	url (apiX.prismacloud.io)

	username (accesskey)

	password (secret)

	protocol (https)

4. Create a csv file called aws.csv (e.g.) with all cloud accounts info: name, accountId, externalId, groupIDs and roleArn

5. Where you installed terraform, copy all files into that folder. Open command line.

6. Run './terraform init' to run the Provider

7. Run './terraform plan' to create the deploy plan.

8. Run './terraform apply' to execute the plan.

9. Validate cloud accounts are onboarded. 

PRISMACLOUD PROVIDER DOCUMENTATION > https://registry.terraform.io/providers/PaloAltoNetworks/prismacloud/latest/docs

PRISMACLOUD PROVIDER DOCUMENTATION RESOURCE CLOUD ACCOUNTS > https://registry.terraform.io/providers/PaloAltoNetworks/prismacloud/latest/docs/resources/cloud_account