from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from codificadores.models import *
from configuracion.models import *
from .utils import crud_url_name

User = get_user_model()

MENUS = {
    'NAV_LEFT_SIDEBAR': [
        {
            "id": 'id_nav_link_dashboard',
            "name": _("Dashboard"),
            "icon_class": 'fa fa-tachometer-alt',
            "url": '#',
            "submenu": [
                {
                    "id": 'id_nav_link_cuadro_mando',
                    "name": _("Balanced scorecard"),
                    "icon_class": 'nav-icon fas fa-tools',
                    "url": "app_index:under_construction",
                },
            ]
        },
        {
            "id": 'id_nav_link_configuracion',
            "name": _("Configuration"),
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
            "submenu": [
                {
                    "id": 'id_nav_link_flujo',
                    "name": _("Flow"),
                    "icon_class": 'fa fa-project-diagram',
                    "url": '#',
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                    "submenu": [
                        {
                            "id": 'id_nav_link_unidades_contables',
                            "name": "Unidades Contable",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "id": 'id_nav_link_departamentos',
                            "name": _("Departments"),
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Departamento, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "id": 'id_nav_link_obtener_datos',
                            "name": _("Get Products data"),
                            "icon_class": 'fa fa-university',
                            "url": reverse_lazy('app_index:codificadores:obtener_datos'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                            "hx_get": reverse_lazy('app_index:codificadores:obtener_datos'),
                            "hx_target": '#dialog',
                        },

                        {
                            "id": 'id_nav_link_unidades_de_medida',
                            "name": "Unidades de Medida",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Medida, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "id": 'id_nav_link_conversion_de_unidades',
                            "name": "Conversión de Medidas",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(MedidaConversion, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "id": 'id_nav_link_motivos_de_ajuste',
                            "name": _("Reasons for Adjustment"),
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(MotivoAjuste, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "id": 'id_nav_link_productos',
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
                            "id": 'id_nav_link_vitolas',
                            "name": "Vitolas",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Vitola, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_admin"],
                        },
                        {
                            "id": 'id_nav_link_marcas_de_salida',
                            "name": "Marcas de Salida",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(MarcaSalida, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                    ]
                },
                {
                    "id": 'id_nav_link_costo',
                    "name": _("Cost"),
                    "icon_class": 'fa fa-chart-column',
                    "url": "#",
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                    "submenu": [
                        {
                            "id": 'id_nav_link_cuentas_contables',
                            "name": "Cuentas Contables",
                            "icon_class": 'fa fa-university',
                            "url": crud_url_name(Cuenta, 'list', 'app_index:codificadores:'),
                            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                        },
                        {
                            "id": 'id_nav_link_centros_de_costo',
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
            "id": 'id_nav_link_administracion',
            "name": _("Administration"),
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
            "submenu": [
                {
                    "id": 'id_nav_link_usuarios',
                    "name": _("Users"),
                    "icon_class": 'fa fa-users',
                    "url": crud_url_name(UserUeb, 'list', 'app_index:usuario:'),
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                },
                {
                    "id": 'id_nav_link_conexion_basedatos',
                    "name": _("Database connection"),
                    "icon_class": 'fa fa-database',
                    "url": crud_url_name(ConexionBaseDato, 'list', 'app_index:configuracion:'),
                    "validators": ["app_auth.usuarios.validators.is_adminempresaoradmin"],
                },
            ]
        }
    ]
}
