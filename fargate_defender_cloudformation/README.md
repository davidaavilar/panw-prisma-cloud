# Convert a unprotected task to a protected task Definition (Fargate)

This script help you to convert a YAML AWS CloudFormation with a Fargate Task Definition into a protected TaskDefinition with Prisma Cloud App-Embedded Defender for Fargate.

The script will find the resource with "AWS::ECS::TaskDefinition" in the Cloudformation and will add the Defender en every taskDefinition.

### Pre-requisites 📋

1. The script will ask for a YAML file name you have in the folder that you are running the script

2. You have to udpate your Defender parameters. You can find them in the Console:

   _tokenConsole = 'tokenConsole'_

   _wssConsole = 'wss://us-east1.cloud.twistlock.com:443'_

   _defenderImage = 'registry-auth.twistlock.com/tw_TOKEN/twistlock/defender:defender_21_04_421'_

### Output 🔧

The output will put a new filename ending with "protected".