# Redlock Policy Handler

This script helps you handle policies in RedLock with a specific label, to clone, delete, disable, enable, etc..

### Pre-requisites 📋

1. You have to configure some parameters in the code.

	_tenant = "YOUR TENANT appX"_

	_accesskey = "YOUR ACCESS KEY"_
	
	_secret = "YOUR SECRET"_

	_filterbylabel = "YOUR LABEL TO FILTER THE LIST POLICY"_

### How it works 🔧

TO CLONE POLICIES: OPTION 1

x.py --disable: Clone and disable the old policies.
x.py --disable --delete: Delete disabled policies.
x.py --disable --update: Update the name (disabled rules).

TO CLONE POLICIES: OPTION 2

x.py --delete: Clone and delete the old policies.
x.py --delete --update: Update the name (deleted rules).

OTHER OPTIONS

x.py --enable: Enable ALL listed policies.
x.py --alert-rules: Get Rules Names from Alerts Rules.
x.py --label <label>: Label policies.