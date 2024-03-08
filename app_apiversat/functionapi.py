import requests
from requests.auth import HTTPBasicAuth

from django.conf import settings

URL_API = settings.URL_API
CONNECTION_TOKEN_API = settings.CONNECTION_TOKEN_API
USERNAME_API = settings.USERNAME_API
PASSWORD_API = settings.PASSWORD_API


def getAPI(opcion, *param):
    url = URL_API + 'api/' + opcion
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
        # print("Request successful")
        # data = response.json()  # Assuming the response is in JSON format
        return response
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
