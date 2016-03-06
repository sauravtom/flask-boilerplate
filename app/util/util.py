import http.client, urllib
import json
import yaml

with open("util/config.yml", 'r') as ymlfile:
    cfg = yaml.load(ymlfile)

for section in cfg:
    print(section)
cred = cfg['credentials']
client_id = cred['client_id']
client_secret = cred['client_secret']
username = cred['username']
password = cred['password']

params = urllib.parse.urlencode({'grant_type': 'password',
                                 'client_id': client_id,
                                 'client_secret': client_secret,
                                 'username': username,
                                 'password': password,
                                 'response_type': 'code'})

headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "text/json"}

base_url = "ap2.salesforce.com"

def get_connection():
    conn = http.client.HTTPSConnection("ap2.salesforce.com")
    return conn


def get_login_connection():
    conn = http.client.HTTPSConnection("login.salesforce.com")
    return conn


def get_access_token():
    conn = get_login_connection()
    conn.request("POST", "/services/oauth2/token", params, headers)
    response = conn.getresponse()
    print(response.status, response.reason)
    data = response.read().decode('ascii')
    data_json = json.loads(data)
    print('access_token: ' + data_json['access_token'])
    return data_json