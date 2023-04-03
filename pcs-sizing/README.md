# Prisma Cloud License Sizing Script

## Overview

This document describes how to prepare for, and how to run the Prisma Cloud License Sizing Script for AWS, Azure and GCP.

## Running the Script from Cloud Shell

1. Start a Cloud Shell session from the CSP UI, which should have the CLI tool, your credentials, ```git``` and ``jq`` already prepared
2. Clone this repository, e.g. ```git clone davidaavilar/panw-prisma-cloud```
3. ```cd pcs-sizing-scripts/aws```
3. ```python3 pcs-sizing.py```