import requests
import json
import csv
from collections import defaultdict

#us-west1.cloud.twistlock.com/us-3-159209233
tenant = "us-west1.cloud.twistlock.com/us-3-159209233"
accesskey = "16a5b6df-0f4c-44a2-8365-9e921ef7a82c"
secret = "gbseAaSm9ObqoJQzpx7he2wDNrY="

activeDirectoryEndpointUrl = "https://login.microsoftonline.com"
resourceManagerEndpointUrl = "https://management.azure.com/"
activeDirectoryGraphResourceId = "https://graph.windows.net/"
sqlManagementEndpointUrl = "https://management.core.windows.net:8443/"
galleryEndpointUrl = "https://gallery.azure.com/"
managementEndpointUrl = "https://management.core.windows.net/"
filename = input('csv filename: ')
if not filename:
	filename = 'cloud_credentials.csv'

def getToken(accesskey,secret):

	print('Authenticating')
	loginurl = "https://{}/api/v1/authenticate".format(tenant)

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
		print('Authentication successful')
	else:
		print('\nValidating credentials\n')
	return token

def CreateCredential(token,cloud,name,accountID,subscriptionId,clientId,clientSecret,tenantId):

	url = "https://{}/api/v1/credentials".format(tenant)

	token = 'Bearer ' + token
	headers = {
    	"Authorization": token

	}
	azure_sdk = json.dumps({"clientId": clientId, "clientSecret": clientSecret, "subscriptionId": subscriptionId, "tenantId": tenantId, "activeDirectoryEndpointUrl": activeDirectoryEndpointUrl, "resourceManagerEndpointUrl": resourceManagerEndpointUrl, "activeDirectoryGraphResourceId": activeDirectoryGraphResourceId, "sqlManagementEndpointUrl": sqlManagementEndpointUrl, "galleryEndpointUrl": galleryEndpointUrl, "managementEndpointUrl": managementEndpointUrl})
	querystring = json.dumps({"secret":{"encrypted":"","plain": azure_sdk},"serviceAccount":{},"type":cloud,"description":"","_id":name})
	req = requests.post(url, headers=headers, data=querystring)
	if req.status_code == 200:
		print(cloud + ' credential with name ' + name + ' was created')
	else:
		print('\nSorry, something went wrong with this Azure Credential: ' + name + ' Try again')

def PutCredentialCloudDiscovery(token,cloud,name):

	token = 'Bearer ' + token
	headers = {
    	"Authorization": token

	}
	url = "https://{}/api/v1/policies/cloud-platforms".format(tenant)
	req = json.loads(requests.get(url, headers=headers).text)
	if cloud == 'azure':
		account = {'credentialId': name, 'awsRegionType': 'regular', 'discoveryEnabled': True, 'complianceEnabled': False, 'serverlessRadarEnabled': False, 'complianceCheckIDs': [100001, 100002, 100003, 100013]}
	
	req['rules'].append(account)

	url2 = "https://{}/api/v1/policies/cloud-platforms".format(tenant)
	querystring = json.dumps({"rules": req["rules"]})
	req2 = requests.put(url2, headers=headers, data=querystring)
	if req2.status_code == 200:
		print(cloud + ' credential with name ' + name + ' was added to Cloud Disocovery !!')
	else:
		print('\nSorry, something went wrong adding this ' + cloud + ' Credendial: ' + name + ' Try again')

def doCloudDiscoveryScan(token):

	token = 'Bearer ' + token
	headers = {
    	"Authorization": token

	}
	url = "https://{}/api/v1/cloud/discovery/scan".format(tenant)
	
	req = requests.post(url, headers=headers).status_code
	return req

def create_cloud_credential():
	
	token = getToken(accesskey,secret)
	with open(filename) as f:
		reader = csv.DictReader(f)
		for row in reader:
			if row['cloud'] == 'azure':
				subscriptionId = row['subscriptionId']
				clientId = row['clientId']
				clientSecret = row['clientSecret']
				tenantId = row['tenantId']
				accountID = row['accountID']
				name = row['Name']
				CreateCredential(token,cloud='azure',name=name,accountID=accountID,subscriptionId=subscriptionId,clientId=clientId,clientSecret=clientSecret,tenantId=tenantId)
				PutCredentialCloudDiscovery(token,cloud='azure',name=name)
	print('All accounts in ' + filename + ' were added to Cloud Discovery Prisma Cloud')
	print('Sending a Cloud Discovery Scan from Prisma Cloud')
	scan = doCloudDiscoveryScan(token)
	if scan == 200:
		print('Cloud Discovery Scan sent.. Check the results in Prisma Cloud Console')
	else:
		print('\nSorry, something went wrong sending the Cloud Discovery scan')

create_cloud_credential()



