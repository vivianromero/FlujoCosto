from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from codificadores.models import *
from configuracion.models import *
from .utils import crud_url_name

User = get_user_model()

MENUS = {
    'NAV_LEFT_SIDEBAR': [
        {
            "name": _("Dashboard"),
            "icon_class": 'fa fa-tachometer-alt',
            "url": '#',
            "submenu": [
                {
                    "name": _("Balanced scorecard"),
                    "icon_class": 'nav-icon fas fa-tools',
                    "url": "app_index:under_construction",
                },
            ]
        },
        {
            "name": "Configuración",
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["app_auth.usuarios.validators.is_admin"],
            "submenu": [
                {
                    "name": "Departamentos",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(Departamento, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Unidad Contable",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Medida",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(Medida, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Medida Conversión",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(MedidaConversion, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Cuenta",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(Cuenta, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Centro Costo",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(CentroCosto, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin" or "app_auth.usuarios.validators.is_superuser"],
                },
                {
                    "name": "Tipo Producto",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(TipoProducto, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Estado Producto",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(EstadoProducto, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Clase Materia Prima",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(ClaseMateriaPrima, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Producto Flujo",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(ProductoFlujo, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Producto Flujo Clase",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(ProductoFlujoClase, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Producto Flujo Destino",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(ProductoFlujoDestino, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Producto Flujo Cuenta",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(ProductoFlujoCuenta, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Categoría Vitola",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(CategoriaVitola, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Tipo Vitola",
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(TipoVitola, 'list', 'app_index:codificadores:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": "Submenu ejemplo 3",
                    "icon_class": 'fa fa-building',
                    "url": '#',
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },

            ]
        },
        {
            "name": "Menu ejemplo 2",
            "icon_class": 'fa fa-tachometer-alt',
            "url": '#',
            "submenu": [
                {
                    "name": "Submenu ejemplo 1",
                    "icon_class": 'nav-icon fas fa-exclamation-triangle',
                    "url": '#',
                    "validators": ["app_auth.usuarios.validators.is_authenticated"],
                },
                {
                    "name": "Submenu ejemplo 2",
                    "icon_class": 'nav-icon fas fa-list-ol',
                    "url": '#',
                    "validators": ["app_auth.usuarios.validators.is_superuser"],
                },
                {
                    "name": "Submenu ejemplo 3",
                    "icon_class": 'nav-icon fas fa-file-alt',
                    "url": '#',
                    "validators": ["app_auth.usuarios.validators.is_superuser"],
                },
            ]
        },
        {
            "name": _("Administration"),
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["app_auth.usuarios.validators.is_admin"],
            "submenu": [
                {
                    "name": _("Users"),
                    "icon_class": 'fa fa-user',
                    "url": crud_url_name(User, 'list', 'app_index:usuario:'),
                    "validators": ["app_auth.usuarios.validators.is_superuser"],
                },
                {
                    "name": _("Groups"),
                    "icon_class": 'fa fa-users',
                    "url": crud_url_name(Group, 'list', 'app_index:group:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": _("Permissons"),
                    "icon_class": 'fa fa-lock',
                    "url": crud_url_name(Permission, 'list', 'app_index:permission:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
                {
                    "name": _("UEB User"),
                    "icon_class": 'fa fa-user',
                    "url": crud_url_name(UserUeb, 'list', 'app_index:configuracion:'),
                    "validators": ["app_auth.usuarios.validators.is_admin"],
                },
            ]
        }
    ]
}
