from django.urls import path

from . import views

app_name = 'apiversat'
urlpatterns = [
    path('uc_versat/', views.UC_Versat, name='uc_versat'),
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
