import requests
import json
import os

# Console example: "https://us-west1.cloud.twistlock.com/us-3-159209233"
console = ""
accesskey = ""
secret = ""
print('What Backup do you want? (daily, monthly, weekly)')
system_bk = input('Backup Type (by default is daily): ')
if not system_bk:
	system_bk = 'daily'

def getToken(accesskey,secret):

	print('Authenticating')
	loginurl = "{}/api/v1/authenticate".format(console)

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

def getBackup(token):

	bkurl = console + '/api/v1/backups'

	token = 'Bearer ' + token
	
	headers = {
    'Authorization': token,
	}

	req = json.loads((requests.get(bkurl, headers=headers).text))
	if system_bk == 'daily':
		bkurl = bkurl + '/' + req[0]['id']
		target_path = req[0]['id']
	elif system_bk == 'weekly':
		bkurl = bkurl + '/' + req[2]['id']
		target_path = req[2]['id']
	else:
		bkurl = bkurl + '/' + req[1]['id']
		target_path = req[1]['id']
	response = requests.get(bkurl, headers=headers, stream=True)
	if response.status_code == 200:
		with open(target_path, 'wb') as f:
			f.write(response.raw.read())
			# f.close()

def backups_lambda_handler(event, context):

	token = []
	token = getToken(accesskey,secret)
	print("Getting the " + system_bk + " backup")
	backup = getBackup(token)
	print(system_bk + " backup saved!!")
	# You can use boto3 to upload this backup to a S3 bucket, for example.

event = []
context = []
resultado = backups_lambda_handler(event, context)