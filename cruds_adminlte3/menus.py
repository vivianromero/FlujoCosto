from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from app_auth.usuarios.forms_usuario_groups import Usuario_Groups
from app_auth.usuarios.forms_usuario_permissions import User_Permissions

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
                    "url": "app_index:under_construction",
                },
            ]
        },
        {
            "name": "Menu ejemplo 1",
            "icon_class": 'fa fa-database',
            "url": '#',
            "validators": ["menu_generator.validators.is_superuser"],
            "submenu": [
                {
                    "name": "Submenu ejemplo 1",
                    "icon_class": 'fa fa-university',
                    "url": '#',  # crud_url_name(__model__, 'list', 'he_index:empresa:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": "Submenu ejemplo 2",
                    "icon_class": 'fa fa-university',
                    "url": '#',
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": "Submenu ejemplo 3",
                    "icon_class": 'fa fa-building',
                    "url": '#',
                    "validators": ["menu_generator.validators.is_superuser"],
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
                    "validators": ["menu_generator.validators.is_authenticated"],
                },
                {
                    "name": "Submenu ejemplo 2",
                    "icon_class": 'nav-icon fas fa-list-ol',
                    "url": '#',
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": "Submenu ejemplo 3",
                    "icon_class": 'nav-icon fas fa-file-alt',
                    "url": '#',
                    "validators": ["menu_generator.validators.is_superuser"],
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
                    "url": crud_url_name(User, 'list', 'app_index:usuario:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Groups"),
                    "icon_class": 'fa fa-users',
                    "url": crud_url_name(Group, 'list', 'app_index:group:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
                {
                    "name": _("Permissons"),
                    "icon_class": 'fa fa-lock',
                    "url": crud_url_name(Permission, 'list', 'app_index:permission:'),
                    "validators": ["menu_generator.validators.is_superuser"],
                },
            ]
        }
    ]
}
