# Prisma Cloud License Sizing Script

## TODO

- For AWS, it only works for a single account, not for Organization yet. And only for US Regions. If you want to modify, you are free to do it. ```regions``` variable.
- For GCP, it only works for a single project, not for Organization yet. You must specify the ProjectID.
- For OCI, it only works for the OCI tenant for Home Region. Not for OKE nodes yet.

## Overview

This document describes how to prepare for, and how to run the Prisma Cloud License Sizing Script for AWS, Azure, GCP, and OCI.

## Running the Script from Cloud Shell

1. Start a Cloud Shell session from the CSP UI, which should have the CLI tool, your credentials, ```git``` and ``jq`` already prepared
2. Clone this repository, e.g. ```git clone davidaavilar/panw-prisma-cloud```
3. ```cd panw-prisma-cloud/pcs-sizing```
4. ```pip install -r requeriments.txt```
- ```python3 pcs-sizing.py --aws``` for AWS.
- ```python3 pcs-sizing.py --azure``` for Azure.
- ```python3 pcs-sizing.py --gcp --project <GCP_PROJECT>``` for GCP.
- ```python3 pcs-sizing.py --oci``` for OCI.