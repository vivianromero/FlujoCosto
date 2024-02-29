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
    Decorator for views that checks that the user is logged in and is a super admin or member of Seller Group
    , redirecting to the login page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: not isinstance(u, AnonymousUser) and (u.is_superuser or u.is_adminemp),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if view_func:
        return actual_decorator(view_func)
    return actual_decorator


# def seller_or_admin_or_carrier_required(view_func=None,
#                                         redirect_field_name=REDIRECT_FIELD_NAME,
#                                         login_url='account:login'):
#     """
#     Decorator for views that checks that the user is logged in and is a super admin or
#     member of Seller Group
#     , redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: not isinstance(u, AnonymousUser) and (
#                 u.is_superuser or u.is_seller or u.is_carrier),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def seller_or_carrier_required(view_func=None,
#                                redirect_field_name=REDIRECT_FIELD_NAME,
#                                login_url='account:login'):
#     """
#     Decorator for views that checks that the user is logged in and is a super admin or
#     member of Seller Group
#     , redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: not isinstance(u, AnonymousUser) and (
#                 u.is_seller or u.is_carrier),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def product_seller_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME,
#                             login_url='account:login'):
#     def check_product_seller(request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         return request.user == product.seller
#
#     actual_decorator = product_passes_test(
#         check_product_seller,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def product_seller_or_admin_required(view_func, redirect_field_name=REDIRECT_FIELD_NAME,
#                                      login_url='account:login'):
#     def check_product_seller(request, pk):
#         product = get_object_or_404(Product, pk=pk)
#         return request.user.is_superuser or request.user == product.seller
#
#     actual_decorator = product_passes_test(
#         check_product_seller,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def order_seller_carrier_admin_required(view_func,
#                                         redirect_field_name=REDIRECT_FIELD_NAME,
#                                         login_url='account:login'):
#     def check_order_seller(request, pk):
#         orders = []
#         if request.user.is_seller:
#             orders = Order.objects.filter(
#                 lines__variant__product__seller_id=request.user,
#                 pk=pk)
#         if request.user.is_carrier:
#             orders = Order.objects.filter(carrier__user=request.user, pk=pk)
#
#         return request.user.is_superuser or len(orders) > 0
#
#     actual_decorator = order_passes_test(
#         check_order_seller,
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def product_passes_test(test_func, login_url=None, next_url=None,
#                         redirect_field_name=REDIRECT_FIELD_NAME):
#     """
#     Decorator for views that checks that the user passes the given test,
#     redirecting to the log-in page if necessary. The test should be a callable
#     that takes the user object and returns True if the user passes.
#     """
#
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             product_pk = kwargs.get("pk", None)
#             if product_pk is None:
#                 product_pk = kwargs.get("product_pk", None)
#             if product_pk:
#                 if test_func(request, product_pk):
#                     return view_func(request, *args, **kwargs)
#             path = resolve_url(next_url, *args,
#                                **kwargs) if next_url else request.build_absolute_uri()
#             resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
#             # If the login url is the same scheme and net location then just
#             # use the path as the "next" url.
#             login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
#             current_scheme, current_netloc = urlparse(path)[:2]
#             if (not next_url and (
#                     not login_scheme or login_scheme == current_scheme) and
#                     (not login_netloc or login_netloc == current_netloc)):
#                 path = request.get_full_path()
#             from django.contrib.auth.views import redirect_to_login
#             return redirect_to_login(
#                 path, resolved_login_url, redirect_field_name)
#
#         return _wrapped_view
#
#     return decorator
#
#
# def order_passes_test(test_func, login_url=None, next_url=None,
#                       redirect_field_name=REDIRECT_FIELD_NAME):
#     """
#     Decorator for views that checks that the user passes the given test,
#     redirecting to the log-in page if necessary. The test should be a callable
#     that takes the user object and returns True if the user passes.
#     """
#
#     def decorator(view_func):
#         @wraps(view_func)
#         def _wrapped_view(request, *args, **kwargs):
#             order_pk = kwargs.get("pk", None)
#
#             if order_pk is None:
#                 order_pk = kwargs.get("order_pk", None)
#             if order_pk:
#                 if test_func(request, order_pk):
#                     return view_func(request, *args, **kwargs)
#             path = resolve_url(next_url, *args,
#                                **kwargs) if next_url else request.build_absolute_uri()
#             resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
#             # If the login url is the same scheme and net location then just
#             # use the path as the "next" url.
#             login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
#             current_scheme, current_netloc = urlparse(path)[:2]
#             if (not next_url and (
#                     not login_scheme or login_scheme == current_scheme) and
#                     (not login_netloc or login_netloc == current_netloc)):
#                 path = request.get_full_path()
#             from django.contrib.auth.views import redirect_to_login
#             return redirect_to_login(
#                 path, resolved_login_url, redirect_field_name)
#
#         return _wrapped_view
#
#     return decorator
#
#
# def comp_seller_or_admin_required(view_func=None,
#                                   redirect_field_name=REDIRECT_FIELD_NAME,
#                                   login_url='account:login'):
#     """
#     Decorator for views that checks that the user is logged in and is a company seller
#     or superuser, redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and (u.is_superuser or u.is_company_seller),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def carrier_or_admin_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
#                               login_url='account:login'):
#     """
#     Decorator for views that checks that the user is logged in and is a carrier
#     or superuser, redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and (u.is_superuser or u.is_carrier),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def carrier_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
#                      login_url='account:login'):
#     """
#     Decorator for views that checks that the user is logged in is a carrier
#     redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and (u.is_carrier),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
#
#
# def seller_required(view_func=None, redirect_field_name=REDIRECT_FIELD_NAME,
#                     login_url='account:login'):
#     """
#     Decorator for views that checks that the user is logged in is a seller
#     redirecting to the login page if necessary.
#     """
#     actual_decorator = user_passes_test(
#         lambda u: u.is_active and (u.is_seller),
#         login_url=login_url,
#         redirect_field_name=redirect_field_name
#     )
#     if view_func:
#         return actual_decorator(view_func)
#     return actual_decorator
