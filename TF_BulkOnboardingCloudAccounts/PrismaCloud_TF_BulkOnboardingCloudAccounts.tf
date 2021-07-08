terraform {
  required_providers {
    prismacloud = {
      source = "PaloAltoNetworks/prismacloud"
      version = "1.1.2"
    }
  }
}

provider "prismacloud" {
    json_config_file = ".prismacloud_auth.json"
}

locals {
    accounts = csvdecode(file("aws.csv"))
}

// Now specify the cloud account resource with a loop like so:

resource "prismacloud_cloud_account" "csv" {
    for_each = { for inst in local.accounts : inst.name => inst }
    
    aws {
        name = each.value.name
        account_id = each.value.accountId
        external_id = each.value.externalId
        group_ids = split("||", each.value.groupIDs)
        role_arn = each.value.roleArn
    }
}