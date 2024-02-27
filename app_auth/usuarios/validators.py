from menu_generator.validators import *


def is_admin(request):
    """
    Retorna verdadero si el usuario es 'Administrator', si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_admin


def is_operflujo(request):
    """
    Retorna verdadero si el usuario es operador de flujo, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_operflujo


def is_opercosto(request):
    """
    Retorna verdadero si el usuario es operador de costo, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_opercosto


def is_consultor(request):
    """
    Retorna verdadero si el usuario es consultor, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_consultor


def is_adminemp(request):
    """
    Retorna verdadero si el usuario es admin de empresa, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_adminemp


def is_consultoremp(request):
    """
    Retorna verdadero si el usuario es consultor de empresa, si no devuelve falso
    """
    return is_authenticated(request) and request.user.is_consultoremp
