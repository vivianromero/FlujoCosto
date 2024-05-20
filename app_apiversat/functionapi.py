import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings

URL_API = settings.URL_API
CONNECTION_TOKEN_API = settings.CONNECTION_TOKEN_API
USERNAME_API = settings.USERNAME_API
PASSWORD_API = settings.PASSWORD_API


def getAPI(opcion, *param):
    url = URL_API + 'api/' + opcion
    if len(param)>0:
        url = url+'/?'
        keys = param[0].keys()
        for k in keys:
            url += k+"="+param[0][k]+"&"
        url = url[:-1]

    auth = HTTPBasicAuth(USERNAME_API, PASSWORD_API)

    # Headers with Connection Token
    headers = {
        "Connection-Token": CONNECTION_TOKEN_API,
        # "Content-Type": "application/json",
        # "accept": "*/*", # Add other necessary headers
    }

    # Make a GET request Basic Authentication, and Connection Token
    # response = requests.get(url, auth=auth, headers=headers)
    response = requests.get(url, auth=auth, headers=headers)
    # Check the response
    if response.status_code == 200:
        return response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
