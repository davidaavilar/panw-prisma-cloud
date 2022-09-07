import json, os, requests, time, boto3
from botocore.exceptions import ClientError

Region = "us-east-1"
secret_name = "netdata-firewall"

try:
    f1 = open('.prismacloud_auth.json')
except FileNotFoundError as e:
    f1 = None

def get_secret():
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager',region_name=Region)
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret " + secret_name + " was not found")
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            print("The request was invalid due to:", e)
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            print("The request had invalid params:", e)
    else:
        if 'SecretString' in get_secret_value_response:
            text_secret_data = json.loads(get_secret_value_response['SecretString'])
            return text_secret_data
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']

def getToken(accesskey,secret,tenant):
    print('Authenticating...')
    loginurl = "https://{}/login".format(tenant)
    credentials = {"username": accesskey,"password": secret}
    payload = json.dumps(credentials)
    headers = {
	    "Accept": "application/json; charset=UTF-8",
    	"Content-Type": "application/json; charset=UTF-8"
	}
    resp = requests.request("POST", loginurl, data=payload, headers=headers)
    if resp.status_code == 200:
        token = json.loads(resp.content)['token']
        print('Authenticated !')
        return token
    else:
        print('\nCheck your credentials and/or tenant...\n')
        exit()

def callPrisma(token,tenant,api,querystring=""):
    headers = {
        "Accept": "application/json; charset=UTF-8",
        "x-redlock-auth": token
    }
    url = "https://{}/{}".format(tenant,api)
    resp = requests.request("GET", url, headers=headers,params=querystring)
    resp = json.loads(resp.content)
    print(json.dumps(resp,indent=2))

def lambda_handler(event, context):
    if f1:
        secret = json.load(f1)
        tenant = secret['url']
        token = getToken(secret['username'],secret['password'],tenant)
    else:
        for key, value in get_secret().items():
            user = key
            password = value
        token = getToken(user,password,"api4.prismacloud.io")
    
    querystring = {"timeType":"to_now","timeUnit":"epoch"}
    callPrisma(token,tenant,"filter/compliance/posture/suggest")


lambda_handler(event="", context="")

	