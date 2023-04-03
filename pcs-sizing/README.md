# Prisma Cloud License Sizing Script

## TODO



## Overview

This document describes how to prepare for, and how to run the Prisma Cloud License Sizing Script for AWS, Azure, GCP, and OCI.

## Running the Script from Cloud Shell

1. Start a Cloud Shell session from the CSP UI, which should have the CLI tool, your credentials, ```git``` and ``jq`` already prepared
2. Clone this repository, e.g. ```git clone davidaavilar/panw-prisma-cloud```
3. ```cd panw-prisma-cloud/pcs-sizing```
- ```python3 pcs-sizing.py --aws``` for AWS.
- ```python3 pcs-sizing.py --azure``` for Azure.
- ```python3 pcs-sizing.py --gcp --project <GCP_PROJECT>``` for GCP.
- ```python3 pcs-sizing.py --oci``` for OCI.