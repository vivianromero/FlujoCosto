from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.core.management import call_command
from configuracion.models import UserUeb,UnidadContable


DICC_GROUP_PERMISSION = {
        (1, 2, 3, 4, 5):
            {
                'tipodocumento': ['view'],
                'documento': ['view'],
                'cuenta': ['view'],
                'unidadcontable': ['view'],
                'cambioproducto': ['view'],
                'centrocosto': ['view'],
                'confcentroselementosotros': ['view'],
                'confcentroselementosotrosdetalle': ['view'],
                'confcentroselementosotrosdetallegrouped': ['view'],
                'departamento': ['view'],
                'lineasalida': ['view'],
                'marcasalida': ['view'],
                'medida': ['view'],
                'medidaconversion': ['view'],
                'motivoajuste': ['view'],
                'normaconsumo': ['view'],
                'normaconsumodetalle': ['view'],
                'normaconsumogrouped': ['view'],
                'numeraciondocumentos': ['view'],
                'productoflujo': ['view'],
                'productoflujovitola': ['view'],
                'productscapasclapesadas': ['view'],
                'vitola': ['view'],
                'loggedinuser': ['view', 'change', 'delete', 'add'],
            },
        (1, 5):
            {'userueb': ['view', 'change', 'delete', 'add'],
             'conexionbasedato': ['view', 'change', 'delete', 'add'],
             },
        (5,):
            {
                'tipodocumento': ['change'],
                'cuenta': ['change'],
                'unidadcontable': ['change'],
                'cambioproducto': ['change', 'delete', 'add'],
                'centrocosto': ['view', 'change'],
                'confcentroselementosotros': ['change'],
                'confcentroselementosotrosdetalle': ['change'],
                'confcentroselementosotrosdetallegrouped': ['change'],
                'departamento': ['change', 'delete', 'add'],
                'lineasalida': ['change', 'delete', 'add'],
                'marcasalida': ['change', 'delete', 'add'],
                'medida': ['change'],
                'medidaconversion': ['change', 'delete', 'add'],
                'motivoajuste': ['change', 'delete', 'add'],
                'normaconsumo': ['change', 'delete', 'add'],
                'normaconsumodetalle': ['change', 'delete', 'add'],
                'normaconsumogrouped': ['change', 'delete', 'add'],
                'numeraciondocumentos': ['change', 'delete', 'add'],
                'productoflujo': ['change', 'delete', 'add'],
                'productoflujovitola': ['change', 'delete', 'add'],
                'productscapasclapesadas': ['change', 'delete', 'add'],
                'vitola': ['change', 'delete', 'add'],
            },
        (2,):{
                'documento': ['change', 'delete', 'add'],
            },
    }

class Command(BaseCommand):
    def add_datos_group_permission(self):

        print("CREANDO GRUPOS DE USUARIOS")
        print("    Administrador")
        print("    Administrador Empresa")
        print("    Operador Flujo")
        print("    Operador Costo")
        print("    Consultor")
        groups = [
            Group(pk=1, name='Administrador'),
            Group(pk=2, name='Operador Flujo'),
            Group(pk=3, name='Operador Costo'),
            Group(pk=4, name='Consultor'),
            Group(pk=5, name='Administrador Empresa'),
        ]
        try:
            Group.objects.bulk_create(groups)
        except Exception as e:
            print("GRUPOS DE USUARIOS YA EXISTEN")

        uebs_all = UnidadContable.objects.all()
        groups_all = Group.objects.all()
        print("CREANDO USUARIOS ADMINISTRADORES")
        try:
            users = [
                UserUeb(pk="000603fa-af2d-4713-b0e5-c2991a289f4b",
                        first_name="Administrador UEB-01",
                        last_name="",
                        username="admin01",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='01'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="003820bb-9dc1-4cbb-b8cf-93f28322c697",
                        first_name="Administrador UEB-02",
                        last_name="",
                        username="admin02",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='02'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="003dec56-d3ac-452d-a2be-9c07539be90f",
                        first_name="Administrador UEB-03",
                        last_name="",
                        username="admin03",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='03'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009bfd05-0357-4614-ba5b-c9876272a460",
                        first_name="Administrador UEB-04",
                        last_name="",
                        username="admin04",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='04'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009c9e8f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-05",
                        last_name="",
                        username="admin05",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='05'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009c9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-06",
                        last_name="",
                        username="admin06",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='06'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="009d9e9f-4064-4214-a051-a1f78ea26b85",
                        first_name="Administrador UEB-07",
                        last_name="",
                        username="admin07",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='07'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="109d9e9f-4064-4214-a051-a1f78ea28b65",
                        first_name="Administrador UEB-08",
                        last_name="",
                        username="admin08",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='08'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="209d9e9f-4064-4214-a051-a1f99ea26b65",
                        first_name="Administrador UEB-09",
                        last_name="",
                        username="admin09",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='09'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="309d9e9f-4064-4214-a051-a1f78ea66b65",
                        first_name="Administrador UEB-10",
                        last_name="",
                        username="admin10",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='10'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="400d9e9f-4084-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-13",
                        last_name="",
                        username="admin13",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='13'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="409f9e9f-4064-4214-a051-a1f78ea26b66",
                        first_name="Administrador UEB-14",
                        last_name="",
                        username="admin14",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='14'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="409f9e9f-4094-4214-a051-a1f78ea26b66",
                        first_name="Administrador UEB-16",
                        last_name="",
                        username="admin16",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='16'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="889d9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-22",
                        last_name="",
                        username="admin22",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='22'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els="),
                UserUeb(pk="879d9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador UEB-23",
                        last_name="",
                        username="admin23",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='23'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els=")
            ]
            UserUeb.objects.bulk_create(users)

            user_emp = [
                UserUeb(pk="809d9e9f-4064-4214-a051-a1f78ea26b65",
                        first_name="Administrador Empresa",
                        last_name="",
                        username="adminempresa",
                        is_active=True,
                        is_staff=True,
                        is_superuser=False,
                        ueb=uebs_all.get(codigo='21'),
                        password="pbkdf2_sha256$150000$SH9BpP9heMQm$VPnCX64vYKe53mfEGqJFXSax1a4qPP5vgSEmns57els=")
            ]
            UserUeb.objects.bulk_create(user_emp)

            for user in users:
                user.groups.add(groups_all.get(pk=1))

            for user in user_emp:
                user.groups.add(groups_all.get(pk=5))
        except Exception as e:
            print("USUARIOS YA EXISTEN")

        print("ASIGNANDO PERMISOS A LOS GRUPOS")
        try:
            keys_dicc = DICC_GROUP_PERMISSION.keys()
            list_permiss = []
            for k in keys_dicc:
                models = DICC_GROUP_PERMISSION[k].keys()
                list_keys_groups = list(k)
                list_permiss = []
                for m in models:
                    permiss = DICC_GROUP_PERMISSION[k][m]
                    for p in permiss:
                        list_permiss.append(p + '_' + m)
                query_permiss = Permission.objects.filter(codename__in=list_permiss).all()
                for permission in query_permiss:
                    for g in list_keys_groups:
                        group = Group.objects.get(pk=g)
                        group.permissions.add(permission)
        except Exception as e:
            print("PERMISOS A LOS GRUPOS YA EXISTEN")

    def handle(self, *args, **options):
        self.add_datos_group_permission()