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
            "name": _("Configuration"),
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
            "submenu": [
                {
                    "name": _("Flow"),
                    "icon_class": 'fa fa-project-diagram',
                    "url": '#',
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                    "submenu": [
                        {
                            "name": "Unidades Contable",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": _("Departments"),
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Departamento, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },

                        {
                            "name": "Unidades de Medida",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Medida, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": "Conversión de Medidas",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(MedidaConversion, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": _("Reasons for Adjustment"),
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(MotivoAjuste, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": "Productos",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(ProductoFlujo, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": "Cambio de Productos",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(CambioProducto, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": "Vitolas",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Vitola, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_admin"],
                        },
                        {
                            "name": "Marcas de Salida",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(MarcaSalida, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                    ]
                },
                {
                    "name": _("Cost"),
                    "icon_class": 'fa fa-chart-column',
                    "url": "#",
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                    "submenu": [
                        {
                            "name": "Cuentas Contables",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Cuenta, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "name": "Centros de Costo",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(CentroCosto, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                    ]
                },

            ]
        },
        {
            "name": _("Administration"),
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
            "submenu": [
                {
                    "name": _("Users"),
                    "icon_class": 'fa fa-users',
                    "url": crud_url_name(UserUeb, 'list', 'app_index:usuario:'),
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                },
                {
                    "name": _("Database connection"),
                    "icon_class": 'fa fa-database',
                    "url": crud_url_name(ConexionBaseDato, 'list', 'app_index:configuracion:'),
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                },
            ]
        }
    ]
}
