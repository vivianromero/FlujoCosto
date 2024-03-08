import base64

import sweetify
from django.conf import settings
from django.utils.translation import gettext_lazy as _

KEY_ENCRIP="DATAZUCAR-ETTVC-SISGESFC"

def codificar(clear):
    enc = []
    key = KEY_ENCRIP
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)

    return base64.urlsafe_b64encode((''.join(enc)).encode("utf-8", "replace")).decode()

def decodificar(enc):
    dec = []
    enc = (base64.urlsafe_b64decode(enc)).decode("utf-8", "replace")
    key = KEY_ENCRIP
    for i in range(len(enc)):
        print(i)
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i])- ord(key_c)) % 256)
        dec.append(dec_c)

    return ''.join(dec)

def obtener_version():
    app_version_file = open(settings.APP_VERSION, 'r')
    valor = app_version_file.read()

    return decodificar(valor)

def message_error(request, title, text):
    sweetify.error(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )

def message_success(request, title, text):
    sweetify.success(
        request=request,
        title=title,
        text=text,
        confirmButtonColor='#3085d6',
        confirmButtonText=_('Accept'),
        backdrop=True,
        showLoaderOnConfirm=True,
        persistent=_("Close"),
    )



# #TODO ver si se va a usar
# def crear_superusuario(credentials):
#
#     user, created = User.objects.get_or_create(
#         username = credentials["username"],
#         email=credentials["email"],
#         defaults={"is_active": True, "is_staff": True, "is_superuser": True},
#     )
#     if created:
#         user.set_password(credentials["password"])
#         user.save()
#         msg = "Superusuario - %(email)s creado satisfactoriamente " % credentials
#     else:
#         msg = "Superusuario - %(email)s ya existe " % credentials
#     return msg

# #TODO esto se cambia a otro lugar más adelante
# def llena_cuenta():
#     JSON_FILE = "./JSON_FILE.json"
#     datos_cuenta = []
#     with open(JSON_FILE, encoding='utf-8') as f:
#         datos_cuenta = json.load(f)
#
#     cuentas = []
#     claveant = ''
#     posicionant = 1
#     parentant = None
#     dicc_pk_posicion = {}
#     for c in datos_cuenta:
#         posicion = c['posicion']
#         clavenivel = c['clavenivel']
#         descripcion = c['descripcion']
#         long_niv = c['long_niv']
#         parent = Cuenta.objects.get(pk=dicc_pk_posicion[posicion - 1]['pk_ant']) if posicion > 1 else None
#         clave = dicc_pk_posicion[posicion - 1]['clave_ant'] + '-' + clavenivel.ljust(long_niv) if posicion > 1 else c[
#             'cuentaversat']
#         print(clave)
#         cta = Cuenta.objects.update_or_create(clave=clave, defaults={"long_niv": long_niv, "posicion": posicion,
#                                                                      "clave": clave, "clavenivel": clavenivel,
#                                                                      "descripcion": descripcion,
#                                                                      "parent": parent}
#                                               )
#         dicc_pk_posicion[posicion] = {'pk_ant': cta[0].pk, 'clave_ant': clave}



