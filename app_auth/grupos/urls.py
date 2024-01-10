from cruds_adminlte3.urls import crud_for_model
from django.contrib.auth.models import Group
from django.urls import path, include

from .forms import GroupForm
from .views import GroupCRUD

group_forms = {
    'add_group': GroupForm,
    'update_group': GroupForm,
    'list_group': [
        'name',
        'permissions',
    ]
}

group_crud = GroupCRUD()

app_name = 'group'
urlpatterns = [
    path('', include(group_crud.get_urls())),
]

# urlpatterns += crud_for_model(
#     Group,
#     login_required=True,
#     check_perms=True,
#     cruds_url='',
#     views=[
#         'create',
#         'list',
#         'delete',
#         'update',
#     ],
#     add_form=group_forms['add_group'],
#     update_form=group_forms['update_group'],
#     list_fields=group_forms['list_group'],
#     namespace='he_index:group',
#     template_father='he_index/cruds/base.html'
# )
