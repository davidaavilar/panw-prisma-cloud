# Redlock Policy Handler

This script helps you handle policies in RedLock with a specific label, to clone, delete, disable, enable, etc..

### Pre-requisites 📋

1. You have to configure some parameters in the code.

	_tenant = "YOUR TENANT appX"_

	_accesskey = "YOUR ACCESS KEY"_
	
	_secret = "YOUR SECRET"_

	_filterbylabel = "YOUR LABEL TO FILTER THE LIST POLICY"_

### How it works 🔧

### TO CLONE POLICIES: OPTION 1

Use `x.py --disable` to clone and disable the old policies.

Use `x.py --disable` --delete to delete disabled policies.

Use `x.py --disable --update`  to update the name (disabled rules).

### TO CLONE POLICIES: OPTION 2

Use `x.py --delete` to clone and delete the old policies.

Use `x.py --delete --update` to update the name (deleted rules).

### OTHER OPTIONS

Use `x.py --enable` to enable ALL listed policies.

Use `x.py --alert-rules` to get Rules Names from Alerts Rules.

Use `x.py --label <label>` to label policies.
