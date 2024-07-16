from functools import wraps
from urllib.parse import urlparse

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.models import AnonymousUser

from django.shortcuts import get_object_or_404, resolve_url

from django.conf import settings


def adminempresa_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                             login_url='app_index:noauthorized'):
    """
    Decorador para verificar que el usuario sea admin de la empresa
    """
    actual_decorator = user_passes_test(
        lambda u: not isinstance(u, AnonymousUser) and (u.is_superuser or u.is_adminempresa),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def admin_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                             login_url='app_index:noauthorized'):
    """
     Decorador para verificar que el usuario sea admin
    """
    actual_decorator = user_passes_test(
        lambda u: not isinstance(u, AnonymousUser) and (u.is_admin),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def opercosto_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                             login_url='app_index:noauthorized'):
    """
     Decorador para verificar que el usuario sea operador del Costo
    """
    actual_decorator = user_passes_test(
        lambda u: not isinstance(u, AnonymousUser) and (u.is_opercosto),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator

def operflujo_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
                             login_url='app_index:noauthorized'):
    """
    Decorador para verificar que el usuario sea operador del Flujo
    """
    actual_decorator = user_passes_test(
        lambda u: not isinstance(u, AnonymousUser) and (u.is_operflujo),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


