# OPTION 1

# Clone and disable the old policies 						x.py --disable 					WORKING
# Delete disabled policies 									x.py --disable --delete			WORKING
# Update the name (disabled rules)							x.py --disable --update			WORKING

# OPTION 2

# Clone and delete the old policies 						x.py --delete 					WORKING
# Update the name (deleted rules)							x.py --delete --update			WORKING

####### OTHER OPTIONS #######

# Enable ALL listed policies 								x.py --enable 					WORKING

# Get Rules Names from Alerts Rules 						x.py --alert-rules				WORKING

# Label the policies 										x.py --label <label>			WORKING

# Enable labeled policies 									x.py --enable <label>			PENDING
# Disable labeled policies 									x.py --disable <label>			PENDING
# Delete labeled policies 									x.py --delete <label>			PENDING

import requests
import json
import os
import time
import sys

# YOUR PARAMETERS

tenant = "YOUR-TENANT-HERE"
accesskey = "YOUR-ACCESS-KEY-HERE"
secret = "YOUR-SECRET-HERE"
ciAccesskey = accesskey
ciSecret = secret

filterbylabel = 'YOUR LABEL TO FILTER THE LIST POLICY'

token = []

suffix = '-Copy'

# CLONING POLICIES PRISMA CLOUD

def getToken(accesskey,secret):
	
	loginurl = "https://{}.prismacloud.io/login".format(tenant)

	credentials = {"username": accesskey,"password": secret}
	
	payload = json.dumps(credentials)
	headers = {
	    "Accept": "application/json; charset=UTF-8",
    	"Content-Type": "application/json; charset=UTF-8"
	}

	loginresp = requests.request("POST", loginurl, data=payload, headers=headers)
	if loginresp.status_code == 200:
		loginresp = json.loads(loginresp.text)
		token = loginresp['token']
	else:
		print('Please, validate your credentials and/or your tenant. There is an error.')
	return token

def listPolicy(token,label):

	# Parameters

#########################################

	labels = filterbylabel

#########################################

	policies = "https://{}.prismacloud.io/v2/policy".format(tenant)
	if label == 'false':
		querystring = {"policy.label":labels,"policy.enabled":label}
	elif label == 'true':
		querystring = {"policy.label":labels, "policy.enabled":label}
	else:
		querystring = {"policy.label":labels}

	headers = {
        "Accept": "application/json; charset=UTF-8",
        "x-redlock-auth": token
    }
	
	listPolicy = requests.request("GET", policies, headers=headers, params=querystring)
	listPolicy = json.loads(listPolicy.text)
	# print(json.dumps(listPolicy[0], indent= 4))
	return listPolicy

def clonePolicy(token,i):

	# Paramters

	cloudType 		= i['cloudType']
	description 	= i['description']
	name 			= i['name'] + suffix
	policyType 		= i['policyType']
	ruleCCriteria 	= i['rule']['children'][0]['criteria']
	ruleCName 		= i['rule']['children'][0]['name'] + suffix
	ruleCType 		= i['rule']['children'][0]['type']
	children 		= [{'criteria':ruleCCriteria,'name':ruleCName,'type':ruleCType}]
	ruleName 		= i['rule']['name'] + suffix
	ruleParameters 	= i['rule']['parameters']
	ruleType 		= i['rule']['type']
	severity 		= i['severity']
	SubTypes        = ['build']
	labels			= i['labels']

	print('Cloning the policy: ' + i['name'] + ' to ' + name)

	policies = "https://{}.prismacloud.io/policy".format(tenant)

	headers = {
	    "Accept": "application/json; charset=UTF-8",
	    "Content-Type": "application/json; charset=UTF-8",
	    "x-redlock-auth": token
	}

	querystring = json.dumps({"cloudType":cloudType,"description":description,"name":name,"policyType":policyType,"severity":severity,"rule":{"name":ruleName,"parameters":ruleParameters,"type":ruleType,"children":children},"labels":labels})
	clonePolicy = requests.request("POST", policies, headers=headers, data=querystring)
	if clonePolicy.status_code == 200:
		print('The policy ' + i['name'] + ' was successfully cloned.')
	else:
		print('There was a problem trying to clone the policy ' + i['name'] + '. Please try later.')

def handleOldPolicy(token,e,arg,label):

	# Paramters

	policyId = e
	labels = [label]

	policy = "https://{}.prismacloud.io/policy/{}".format(tenant,policyId)

	headers = {
	    "Accept": "application/json; charset=UTF-8",
	    "Content-Type": "application/json; charset=UTF-8",
	    "x-redlock-auth": token
	}

	if arg == "disable" and label == '':
		print('Disabling the policy ' + policyId)
		querystring = json.dumps({"enabled":"false"})
		disablePolicy = requests.request("PUT", policy, headers=headers, data=querystring)
		if disablePolicy.status_code != 200:
			print('There was an error trying to disable this policy: ' + policyId)
		else:
			print('The policy ' + policyId + ' was successfully disabled')
	elif arg == "disable" and label != '':
		print('Disabling the policy ' + policyId)
		querystring = json.dumps({"labels":labels,"enabled":"false"})
		disablePolicy = requests.request("PUT", policy, headers=headers, data=querystring)
		if disablePolicy.status_code != 200:
			print('There was an error trying to disable this policy: ' + policyId)
		else:
			print('The policy ' + policyId + ' was successfully disabled')
	elif arg == "delete" and label == '':
		print('Deleting the policy ' + policyId)
		deletePolicy = requests.request("DELETE", policy, headers=headers)
		if deletePolicy.status_code != 204:
			print('There was an error trying to delete this policy: ' + policyId)
		else:
			print('The policy ' + policyId + ' was successfully removed')
	elif arg == "delete" and label != '':
		print('Deleting the policy ' + policyId)
		querystring = json.dumps({"labels":labels})
		deletePolicy = requests.request("DELETE", policy, headers=headers, data=querystring)
		if deletePolicy.status_code != 204:
			print('There was an error trying to delete this policy: ' + policyId)
		else:
			print('The policy ' + policyId + ' was successfully removed')
	elif arg == "enable" and label == '':
		print('Enabling the policy ' + policyId)
		querystring = json.dumps({"enabled":"true"})
		disablePolicy = requests.request("PUT", policy, headers=headers, data=querystring)
		if disablePolicy.status_code != 200:
			print('There was an error trying to enable this policy: ' + policyId)
		else:
			print('The policy ' + policyId + ' was successfully enabled')
	elif arg == "update":
		print('Updating the policy ' + policyId)
		querystring = json.dumps({"name":label[:len(suffix)]})
		updatePolicy = requests.request("PUT", policy, headers=headers, data=querystring)
		if updatePolicy.status_code != 200:
			print('There was an error trying to update this policy: ' + policyId)
		else:
			print('The policy ' + policyId + ' was successfully updated')
	else:
		print('Do nothing!')
		pass

def LabelPolicy(token,p,label):

	# Paramters

	policyId = p
	labels = [label]

	label = "https://{}.prismacloud.io/policy/{}".format(tenant,policyId)

	headers = {
	    "Accept": "application/json; charset=UTF-8",
	    "Content-Type": "application/json; charset=UTF-8",
	    "x-redlock-auth": token
	}

	print('Labeling the policy ' + policyId)
	querystring = json.dumps({"labels":labels})
	labelPolicy = requests.request("PUT", label, headers=headers, data=querystring)

	if labelPolicy.status_code != 200:
		print('There was an error trying to label this policy: ' + policyId)
		print(labelPolicy.status_code)
	else:
		print('The policy ' + policyId + ' was successfully labeled')

def listAlertRules(token):

	alertRules = "https://{}.prismacloud.io/v2/alert/rule".format(tenant)

	headers = {
        "Accept": "application/json; charset=UTF-8",
        "x-redlock-auth": token
    }
	
	listAlertRules = requests.request("GET", alertRules, headers=headers)
	listAlertRules = json.loads(listAlertRules.text)
	# print(json.dumps(listAlertRules, indent= 4))
	return listAlertRules

def getPolicyInfo(token,ids):

	policyinfo = "https://{}.prismacloud.io/policy/{}".format(tenant,ids)

	headers = {
        "Accept": "application/json; charset=UTF-8",
        "x-redlock-auth": token
    }
	
	policyinfoResp = requests.request("GET", policyinfo, headers=headers)
	policyinfoResp = json.loads(policyinfoResp.text)
	# print(json.dumps(listAlertRules, indent= 4))
	return policyinfoResp['name']

def handler(arg,label):
	
	# Authentication to Prisma Cloud
	myList = []
	mylistName = []
	token = getToken(accesskey,secret)
	ciToken = getToken(ciAccesskey,ciSecret)

	if arg == 'label':
		print('Getting the policies... ')
		listPolicies = listPolicy(token,label='')
		for i in listPolicies:
			myList.append(i['policyId'])
		for p in myList:
			LabelPolicy(token,p,label)

	elif arg == 'enable':
		print('Getting the policies... ')
		listPolicies = listPolicy(token,label='')
		for i in listPolicies:
			myList.append(i['policyId'])
		for p in myList:
			handleOldPolicy(token,p,arg,label)

	elif arg == 'update':
		print('Getting the policies... ')
		listPolicies = listPolicy(token,label)
		for i in listPolicies:
			policyid = i['policyId']
			name = i['name']
			print(policyid,name)
			handleOldPolicy(token,policyid,arg,label=name)

	elif arg == 'alertrules':
		listAlertRule = listAlertRules(token)
		for i in listAlertRule:
			print('This is the name of the Alert-Rule: ' + i['name'])
			print('These are the policies associated: ')
			policyList = []
			for e in i['policies']:
				getPolicyInf = getPolicyInfo(token,e)
				print(getPolicyInf)

	else:
		# Clone currrent Config Build Custom Policies and add them to a myList
		print('Getting the policies... ')
		if label == "false":
			listPolicies = listPolicy(token,label)
			for i in listPolicies:
				myList.append(i['policyId'])
		else:
			listPolicies = listPolicy(token,label='')
			for i in listPolicies:
				clonePolicy(ciToken, i)
				myList.append(i['policyId'])

		# Handling old Policies
		for p in myList:
			handleOldPolicy(token,p,arg,label)
		print('Process ended!!')

try:
	# WORKING ARGUMENTS

	if len(sys.argv) == 2 and sys.argv[1] == '--enable':
		print('It will enable ALL policies listed.')
		handler(arg='enable',label='')
	elif len(sys.argv) == 2 and sys.argv[1] == '--disable':
		print('It will clone and disable the old policies.')
		handler(arg='disable',label='')
	elif len(sys.argv) == 2 and sys.argv[1] == '--delete':
		print('It will clone and delete the old policies.')
		handler(arg='delete',label='')
	elif len(sys.argv) > 2 and sys.argv[2] == '--update' and sys.argv[1] == '--disable':
		print('It will update new policies (after disabled).')
		handler(arg='update',label='true')
	elif len(sys.argv) > 2 and sys.argv[2] == '--delete' and sys.argv[1] == '--disable':
		print('It will delete the disabled policies.')
		handler(arg='delete',label='false')
	elif len(sys.argv) > 2 and sys.argv[2] == '--update' and sys.argv[1] == '--delete':
		print('It will update new policies (after deleted).')
		handler(arg='update',label='')
	elif len(sys.argv) == 2 and sys.argv[1] == '--alert-rules':
		print('Getting the alert-rules names...')
		handler(arg='alertrules',label='')
	elif len(sys.argv) == 3 and sys.argv[1] == '--label':
		print('It will put the label ' + sys.argv[2] + ' to listed policies.')
		handler(arg='label',label=sys.argv[2])
	elif len(sys.argv) == 2 and sys.argv[1] == '--help':
		print('\nTO CLONE POLICIES: OPTION 1')
		print('x.py --disable: Clone and disable the old policies')
		print('x.py --disable --delete: Delete disabled policies')
		print('x.py --disable --update: Update the name (disabled rules)')
		print('\nTO CLONE POLICIES: OPTION 2')
		print('x.py --delete: Clone and delete the old policies')		
		print('x.py --delete --update: Update the name (deleted rules)')
		print('\nOTHER OPTIONS')
		print('x.py --enable: Enable ALL listed policies')
		print('x.py --alert-rules: Get Rules Names from Alerts Rules')
		print('x.py --label <label>: Label policies')
		
	# PENDING ARGUMENTS

	elif len(sys.argv) > 2 and sys.argv[1] == '--delete':
		# PENDING
		print('It will DELETE ONLY the labeled policies: ' + sys.argv[2])
		# handler(arg='delete',label=sys.argv[2])
	elif len(sys.argv) > 2 and sys.argv[1] == '--disable':
		# PENDING
		print('It will DISABLE ONLY the labeled policies: ' + sys.argv[2])
		# handler(arg='disable',label=sys.argv[2])
	elif len(sys.argv) > 2 and sys.argv[1] == '--enable':
		# PENDING
		print('It will ENABLE ONLY the labeled policies: ' + sys.argv[2])
		# handler(arg='disable',label=sys.argv[2])
	else:
		print('Use --help for available arguments')

except IndexError:
	print('You must put a valid argument')
	exit()



