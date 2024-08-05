import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings

URL_API = settings.URL_API
CONNECTION_TOKEN_API = settings.CONNECTION_TOKEN_API
USERNAME_API = settings.USERNAME_API
PASSWORD_API = settings.PASSWORD_API


def getAPI(opcion, params=None):
    url = URL_API + 'api/' + opcion

    if params:
        url = url + '/?'
        keys = params.keys()
        for k in keys:
            url += k+"="+params[k]+"&"
        url = url[:-1]


    auth = HTTPBasicAuth(USERNAME_API, PASSWORD_API)

    # Headers with Connection Token
    headers = {
        "Connection-Token": CONNECTION_TOKEN_API,
        # "Content-Type": "application/json",
        # "accept": "*/*", # Add other necessary headers
    }

    # Make a GET request Basic Authentication, and Connection Token
    response = requests.get(url, auth=auth, headers=headers)
    return response
