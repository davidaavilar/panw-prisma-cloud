# Automate Prisma Cloud Backups

This script helps you get system Backups from Prisma Cloud

### Pre-requisites 📋

1. The script will ask for a system backup you want (daily, weekly or monthly). By default is "daily", if you left it in blank.

2. You have to udpate Console and Console Credentials. You can find them in the Console:

	_console = ""_

	_accesskey = ""_
	
	_secret = ""_

### Notes:

This script only donwload the system backup from Prisma Cloud. You can use it, and add a code using Boto3 for example, to upload the backup to a Amazon S3 bucket. Deploy de code as a AWS Lambda with a CloudWatch Event as a trigger.