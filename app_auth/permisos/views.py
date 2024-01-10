from django.http import HttpResponseRedirect
from django.contrib.auth.models import Permission
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _
from cruds_adminlte3.crud import CRUDView
from app_index.views import CommonCRUDView
from .filters import PermissionFilter
from .forms import PermissionForm
from .tables import PermissionTable

# Create your views here.


class PermissionCRUD(CommonCRUDView):
    model = Permission

    namespace = 'app_index:permission'

    template_father = 'app_index/cruds/base.html'

    views_available = [
        'create',
        'list',
        'delete',
        'update',
    ]

    fields = [
        'name',
        'content_type',
        'codename',
    ]

    add_form = PermissionForm
    update_form = PermissionForm

    check_login = True
    check_perms = True

    related_fields = [
    ]

    list_fields = [
        'name',
        'content_type',
        'codename',
    ]

    search_fields = [
        'name__icontains',
        'content_type__icontains',
        'codename__icontains',
    ]

    filter_fields = [
        'name',
        'content_type',
        'codename',
    ]

    filterset_class = PermissionFilter

    page_length = 10

    page_length_menu = [5, 10, 15, 20]

    # Table settings
    table_class = PermissionTable
    template_name = "app_index/cruds/list_table.html"
    paginate_by = 10
    exclude_columns = ("actions",)
