from django.contrib.auth.models import User

#TODO ver si se va a usar
def crear_superusuario(credentials):

    user, created = User.objects.get_or_create(
        username = credentials["username"],
        email=credentials["email"],
        defaults={"is_active": True, "is_staff": True, "is_superuser": True},
    )
    if created:
        user.set_password(credentials["password"])
        user.save()
        msg = "Superusuario - %(email)s creado satisfactoriamente " % credentials
    else:
        msg = "Superusuario - %(email)s ya existe " % credentials
    return msg

#TODO esto se cambia a otro lugar más adelante
# def llena_cuenta():
#     if Cuenta.objects.all().count() != 0:
#         return
#
#     JSON_FILE = "./JSON_FILE.json"
#     dicc_cuenta = {}
#     with open(JSON_FILE, encoding='utf-8') as f:
#         dicc_cuenta = json.load(f)
#
#     list_keys = list(dicc_cuenta.keys())
#     cuentas = []
#     claveant=''
#     posicionant=1
#     parentant=None
#     dicc_pk_posicion = {}
#     for c in list_keys:
#         posicion = dicc_cuenta[c]['posicion']
#         clavenivel = dicc_cuenta[c]['clavenivel']
#         descripcion = dicc_cuenta[c]['descripcion']
#         long_niv = dicc_cuenta[c]['long_niv']
#         parent = Cuenta.objects.get(pk=dicc_pk_posicion[posicion-1]['pk_ant']) if posicion>1 else None
#         clave = dicc_pk_posicion[posicion-1]['clave_ant'] + '-' + clavenivel if posicion>1 else dicc_cuenta[c]['clave'].strip()
#         prov, created_prov = Cuenta.objects.get_or_create(
#                     long_niv = long_niv, posicion = posicion,
#                     clave = clave, clavenivel = clavenivel, descripcion = descripcion,
#                     parent = parent
#                 )
#         if created_prov:
#             prov.save()
#             dicc_pk_posicion[posicion]={'pk_ant':prov.pk, 'clave_ant':clave}

#TODO esto se cambia a otro lugar más adelante
#para consumir de la api versat
# def get_api_versat(url):
#     import requests
#     from requests.auth import HTTPBasicAuth
#
#     # url = "https://example.com/api/endpoint"
#     username = "your_username"
#     password = "your_password"
#     connection_token = "your_connection_token"
#
#     # Basic Authentication credentials
#     auth = HTTPBasicAuth(username, password)
#
#     # Headers with Connection Token
#     headers = {
#         "Connection-Token": connection_token,
#         "Content-Type": "application/json",  # Add other necessary headers
#     }
#
#     # Make a GET request Basic Authentication, and Connection Token
#     response = requests.get(url, auth=auth, headers=headers)
#
#     # Check the response
#     if response.status_code == 200:
#         print("Request successful")
#         data = response.json()  # Assuming the response is in JSON format
#         print(data)
#     else:
#         print(f"Request failed with status code {response.status_code}")
#         print(response.text)