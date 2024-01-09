from clasificadores.empresa.models import Empresa
from clasificadores.sector.models import Sector
from clasificadores.entidad.models import Entidad
from clasificadores.municipio.models import Municipio
from clasificadores.provincia.models import Provincia
from clasificadores.producto.models import Producto
from clasificadores.unidad_medida.models import UnidadMedida
from hecho_app.models.clasificacion_hecho import ClasificacionHecho
from hecho_app.models.tipo_hecho import TipoHecho
from hecho_app.models.hecho_extraordinario import HechoExtraordinario
from hecho_app.models.hecho_resumen import HechoExtResumen
from hecho_app.models.hecho_tipicidad_resumen import HechoExtTipoResumen
from usuarios.models import Usuario
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from usuarios.forms_usuario_groups import Usuario_Groups
from usuarios.forms_usuario_permissions import Usuario_Permissions
from he_auth.grupos_permisos.forms import Group_Permissions
from .utils import crud_url_name

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
                    "url": "he_index:dashboard",
                },
            ]
        },
        {
            "name": _("Classifiers"),
            "icon_class": 'fa fa-database',
            "url": '#',
            "validators": ["menu_generator.validators.is_superuser"],
            "submenu": [
                {
                    "name": _("Entreprises"),
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(Empresa, 'list', 'he_index:empresa:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Sectors"),
                    "icon_class": 'fa fa-university',
                    "url": crud_url_name(Sector, 'list', 'he_index:sector:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Entities"),
                    "icon_class": 'fa fa-building',
                    "url": crud_url_name(Entidad, 'list', 'he_index:entidad:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Municipalities"),
                    "icon_class": 'fa fa-city',
                    "url": crud_url_name(Municipio, 'list', 'he_index:municipio:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Provinces"),
                    "icon_class": 'fa fa-map',
                    "url": crud_url_name(Provincia, 'list', 'he_index:provincia:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Products"),
                    "icon_class": 'fa fa-tag',
                    "url": crud_url_name(Producto, 'list', 'he_index:producto:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Measurement units"),
                    "icon_class": 'fa fa-ruler',
                    "url": crud_url_name(UnidadMedida, 'list', 'he_index:unidad_medida:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ]
        },
        {
            "name": _("EVENTS"),
            "icon_class": 'fa fa-tachometer-alt',
            "url": '#',
            "submenu": [
                {
                    "name": _("Extraordinary Events"),
                    "icon_class": 'nav-icon fas fa-exclamation-triangle',
                    "url": crud_url_name(HechoExtraordinario, 'list', 'he_index:hecho_app:hecho_extraordinario:'),
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Event Classification"),
                    "icon_class": 'nav-icon fas fa-list-ol',
                    "url": crud_url_name(ClasificacionHecho, 'list', 'he_index:hecho_app:clasificacion_hecho:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Event Type"),
                    "icon_class": 'nav-icon fas fa-file-alt',
                    "url": crud_url_name(TipoHecho, 'list', 'he_index:hecho_app:tipo_hecho:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ]
        },
        {
            "name": _("REPORTS"),
            "icon_class": 'fa fa-file',
            "url": '#',
            "submenu": [
                {
                    "name": _("Events by typicality"),
                    "icon_class": 'nav-icon fas fa-list',
                    "url": crud_url_name(HechoExtTipoResumen, 'list', 'he_index:hecho_app:hecho_tipo_resumen:'),
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": _("Events Summary"),
                    "icon_class": 'nav-icon fas fa-briefcase',
                    "url": crud_url_name(HechoExtResumen, 'list', 'he_index:hecho_app:hecho_resumen:'),
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
{
                    "name": _("Events Report"),
                    "icon_class": 'nav-icon fas fa-file-word',
                    "url": 'he_index:hecho_app:hecho_extraordinario:reporte_hechos',
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
            ]
        },
        {
            "name": _("Administration"),
            "icon_class": 'fa fa-tools',
            "url": '#',
            "validators": ["menu_generator.validators.is_superuser"],
            "submenu": [
                {
                    "name": _("Users"),
                    "icon_class": 'fa fa-user',
                    "url": crud_url_name(Usuario, 'list', 'he_index:usuario:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Groups"),
                    "icon_class": 'fa fa-users',
                    "url": crud_url_name(Group, 'list', 'he_index:group:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Permissons"),
                    "icon_class": 'fa fa-lock',
                    "url": crud_url_name(Permission, 'list', 'he_index:permission:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ]
        }
    ]
}
