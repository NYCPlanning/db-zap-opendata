import os
import requests
import msal

ZAP_DOMAIN = os.environ['ZAP_DOMAIN']
TENANT_ID = os.environ['TENANT_ID']
CLIENT_ID = os.environ['CLIENT_ID']
SECRET = os.environ['SECRET']

config = {
    "authority": f"https://login.microsoftonline.com/{TENANT_ID}",
    "client_id": CLIENT_ID,
    "scope": [f"{ZAP_DOMAIN}/.default"],
    "secret": SECRET,
    "endpoint": "{ZAP_DOMAIN}/api/data/v9.1"
}

app = msal.ConfidentialClientApplication(
    config["client_id"], 
    authority=config["authority"],
    client_credential=config["secret"])

result=None
if not result:
    result = app.acquire_token_for_client(scopes=config["scope"])

headers={'Authorization': 'Bearer ' + result['access_token']}