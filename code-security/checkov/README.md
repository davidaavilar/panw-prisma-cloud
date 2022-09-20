# Checkov Useful Commands...

## Installing Checkov

```
pip install checkov
```

[https://www.checkov.io/2.Basics/Installing%20Checkov.html](https://www.checkov.io/2.Basics/Installing%20Checkov.html)

## Useful commands

`checkov -d .` to scan all files of current directory and it shows PASSED/FAILED checks.

`checkov -f cloudformation-example.yaml` to scan a specific file of current directory and it shows PASSED/FAILED checks.

`checkov -d . --quiet` to scan all files of current directory and it shows only FAILED checks.

`checkov -d . --compact` to scan all files of current directory and it shows PASSED/FAILED checks without the specific lines that are failing (without details).

`checkov -d . --external-checks-dir policies/` to scan all files of current directory and it shows PASSED/FAILED checks using your own Checkov policies (written in Python).

`checkov -d . --external-checks-dir policies/ --quiet --compact` to scan all files of current directory and it shows only FAILED checks without the specific lines that are failing (without details) and using your own Checkov policies (written in Python).

`checkov -d . --framework dockerfile` to scan all files of current directory MATCHING with a framework, for example `cloudformation`, `dockerfile`, `terraform`, etc, and it shows PASSED/FAILED checks. You can use multiple framework separated by spaces.

`checkov -d . --skip-framework dockerfile cloudformation` to scan all files of current directory EXCLUDING a specific framework, for example `cloudformation`, `dockerfile`, `terraform`, etc, and it shows PASSED/FAILED checks. You can use multiple framework separated by spaces.

`checkov -h` for help.