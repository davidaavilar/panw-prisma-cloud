# Useful Resources about CSPM module of Prisma Cloud...

Here you'll find some useful resources about Cloud Security Posture Managment (CSPM) module of Prisma Cloud.

Some Custom RQLs:

## AWS

1. AWS Avoid the use of the "root" account

`event from cloud.audit_logs where cloud.type = 'aws' AND operation in ( 'ConsoleLogin', 'login-auth.sso' ) AND subject = 'root'`

## Azure

1. Azure Ensure that multi-factor authentication is enabled for all non-privileged users

`config from cloud.resource where cloud.type = 'azure' AND api.name = 'azure-active-directory-credential-user-registration-details' AND json.rule = isMfaRegistered is false as X; config from cloud.resource where api.name = 'azure-active-directory-user' AND json.rule = accountEnabled is true and userType equals Guest as Y; filter '$.X.userDisplayName equals $.Y.displayName'; show X;`


1. Azure VMs with Public IPs with attached NSGs allowing "Any"

`config from cloud.resource where api.name = 'azure-network-nsg-list' AND json.rule = securityRules[*].sourceAddressPrefix is not empty AND securityRules[*].direction equals "Inbound" and securityRules[*].access does not equal "Deny" AND (securityRules[*].sourceAddressPrefix equals "Internet" OR securityRules[*].sourceAddressPrefix equals "*" OR securityRules[*].sourceAddressPrefix equals "0.0.0.0/0") as X; config from cloud.resource where api.name = 'azure-network-nic-list' AND json.rule = ['properties.ipConfigurations'][*].['properties.publicIPAddress'].id is not empty as Y; config from cloud.resource where api.name = 'azure-network-effective-nsg' as Z; filter '$.Z.value[*].association.networkInterface.id==$.Y.id and $.Z.value[*].networkSecurityGroup.id==$.X.id'; show Y; addcolumn ['properties.virtualMachine'].id`