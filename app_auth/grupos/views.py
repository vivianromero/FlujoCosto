from django.http import HttpResponseRedirect
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, ListView, UpdateView
from django.utils.translation import gettext_lazy as _
from cruds_adminlte3.crud import CRUDView
from app_index.views import CommonCRUDView
from .filters import GroupFilter
from .forms import GroupForm
from .tables import GroupTable

# Create your views here.


class GroupCRUD(CommonCRUDView):
    model = Group

    namespace = 'app_index:group'

    template_father = 'app_index/cruds/base.html'

    views_available = [
        'create',
        'list',
        'delete',
        'update',
    ]

    fields = [
        'name',
        'permissions'
    ]

    add_form = GroupForm
    update_form = GroupForm

    check_login = True
    check_perms = True

    related_fields = [
    ]

    list_fields = [
        'name',
        'permissions'
    ]

    search_fields = [
        'name__icontains',
        'permissions',
    ]

    filter_fields = [
        'name',
        'permissions'
    ]

    filterset_class = GroupFilter

    page_length = 10

    page_length_menu = [5, 10, 15, 20]

    # Table settings
    table_class = GroupTable
    template_name = "he_index/cruds/list_table.html"
    paginate_by = 10
    exclude_columns = ("actions",)
