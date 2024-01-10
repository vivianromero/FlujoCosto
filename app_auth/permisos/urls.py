from django.urls import path, include

from cruds_adminlte3.urls import crud_for_model
from django.contrib.auth.models import Permission

from .forms import PermissionForm
from .views import PermissionCRUD

permission_forms = {
    'add_permission': PermissionForm,
    'update_permission': PermissionForm,
    'list_permission': [
        'name',
        'content_type',
        'codename',
    ]
}

permission_crud = PermissionCRUD()

app_name = 'permission'
urlpatterns = [
    path('', include(permission_crud.get_urls())),
]

# urlpatterns += crud_for_model(
#     Permission,
#     login_required=True,
#     check_perms=True,
#     cruds_url='',
#     views=[
#         'create',
#         'list',
#         'delete',
#         'update',
#     ],
#     add_form=permission_forms['add_permission'],
#     update_form=permission_forms['update_permission'],
#     list_fields=permission_forms['list_permission'],
#     namespace='he_index:permission',
#     template_father='he_index/cruds/base.html'
# )
