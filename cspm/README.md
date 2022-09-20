<H2> Useful Resources about CSPM module of Prisma Cloud...</H2>

Here you'll find some useful resources about Cloud Security Posture Managment (CSPM) module of Prisma Cloud.

Some Custom RQLs:

### AWS


### Azure

1. Azure VMs with Public IPs with attached NSGs allowing "Any"

`config from cloud.resource where api.name = 'azure-network-nsg-list' AND json.rule = securityRules[*].sourceAddressPrefix is not empty AND securityRules[*].direction equals "Inbound" and securityRules[*].access does not equal "Deny" AND (securityRules[*].sourceAddressPrefix equals "Internet" OR securityRules[*].sourceAddressPrefix equals "*" OR securityRules[*].sourceAddressPrefix equals "0.0.0.0/0") as X; config from cloud.resource where api.name = 'azure-network-nic-list' AND json.rule = ['properties.ipConfigurations'][*].['properties.publicIPAddress'].id is not empty as Y; config from cloud.resource where api.name = 'azure-network-effective-nsg' as Z; filter '$.Z.value[*].association.networkInterface.id==$.Y.id and $.Z.value[*].networkSecurityGroup.id==$.X.id'; show Y; addcolumn ['properties.virtualMachine'].id`