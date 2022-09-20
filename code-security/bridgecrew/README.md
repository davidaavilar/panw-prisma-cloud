# Checkov Useful Commands...

## Installing Bridgecrew

```
pip install bridgecrew
```

[https://docs.bridgecrew.io/docs/ingesting-scan-data](https://docs.bridgecrew.io/docs/ingesting-scan-data)

## Getting your API Token from Bridecrew

[https://docs.bridgecrew.io/docs/get-api-token](https://docs.bridgecrew.io/docs/get-api-token)

## Useful commands

Unlike Checkov, Bridecrew uses some some additional flags for authentication.

```
export bctoken=<YOUR_KEY>
export bcrepo=<YOUR_REPO_NAME>
export bcbranch=<YOUR_BRANCH>
```

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d .` to scan all files of current directory and it shows PASSED/FAILED checks.

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -f cloudformation-example.yaml` to scan a specific file of current directory and it shows PASSED/FAILED checks.

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d . --quiet` to scan all files of current directory and it shows only FAILED checks.

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d . --compact --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch` to scan all files of current directory and it shows PASSED/FAILED checks without the specific lines that are failing (without details).

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d . --external-checks-dir policies/ ` to scan all files of current directory and it shows PASSED/FAILED checks using your own Checkov policies (written in Python).

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d . --external-checks-dir policies/ --quiet --compact` to scan all files of current directory and it shows only FAILED checks without the specific lines that are failing (without details) and using your own Checkov policies (written in Python).

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d . --framework dockerfile` to scan all files of current directory MATCHING with a framework, for example `cloudformation`, `dockerfile`, `terraform`, etc, and it shows PASSED/FAILED checks. You can use multiple framework separated by spaces.

`bridgecrew --bc-api-key $bctoken --repo-id $bcrepo --branch $bcbranch -d . --skip-framework dockerfile cloudformation` to scan all files of current directory EXCLUDING a specific framework, for example `cloudformation`, `dockerfile`, `terraform`, etc, and it shows PASSED/FAILED checks. You can use multiple framework separated by spaces.

`bridgecrew -h` for help.