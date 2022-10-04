# Deploy a Vulnerable Web App for WAAS testing

This Terraform helps you to deploy a vulnerable web app (bWAPP) to test WAAS Protection with Prisma Cloud on Azure.

bWAPP, or a buggy web application, is a free and open source deliberately insecure web application.
It helps security enthusiasts, developers and students to discover and to prevent web vulnerabilities. More info in [bWAPP project](http://www.itsecgames.com/)

### Pre-requisites 📋

1. You have to login to your Azure Portal account and upload the Terraform file into your Cloud Shell, or you can use your local machine. You must have `terraform` and `az cli` installed.

2. You have to udpate the Terraform variables.

	_prefix = <AZURE_LOCATION>_
		default = "eastus"

	_prefix = <JUST_A_NAME_FOR_YOUR_APP>_
		default = "my-vulnerable-app"

	_mgt_address = <CIDR_TO_MGT_THE_VM>_
		default = "0.0.0.0/0"
	
	_app_address = <CIDR_TO_ACCESS_TO_THE_APP>_
		default = "0.0.0.0/0"
	
	Feel free to update all your VM params if you want.

### How to deploy the bWAPP:

```
terraform init
```

```
terraform apply
```

If deploy is successful, you gonna see the public_ip from terraform outputs to access to the app.

Also, you can access to the VM via SSH to install your Container Defender.

### How to setup bWAPP:

You can access to bWAPP from: http://<YOUR_PUBLIC_IP>/install.php and then click on "Click here to install bWAPP".

If successful now can go to Login (bee/bug).

Here you can find some common attacks to test:

[SQL Injection](https://infosecgirls.gitbook.io/infosecgirls-training/v/appsec/web-application-pentesting/injection/time-based-sql-injection)

[Broken Authentication](https://infosecgirls.gitbook.io/infosecgirls-training/v/appsec/web-application-pentesting/a2-broken-authentication-and-session/broken-authentication-with-bwapp)

### Cleaning Up

```
terraform destroy
```