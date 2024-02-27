from django.urls import path

from .cuentas import function

app_name = 'appversat'
urlpatterns = [
    path('uc_appversat/', function.get_ucontables, name='uc_appversat'),
]

# urlpatterns += crud_for_app(
#     'usuarios',
#     login_required=True,
#     check_perms=True,
#     cruds_url='',
#     views=[
#         'create',
#         'list',
#         'delete',
#         'update',
#     ],
#     modelforms=user_forms,
#     namespace='he_index:usuario',
#     template_father='he_index/cruds/base.html',
# )
