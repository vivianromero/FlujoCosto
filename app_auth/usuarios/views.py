from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView, LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView, ListView, UpdateView

from cruds_adminlte3.crud import CRUDView
from app_index.views import CommonCRUDView
from .filters import UserUebFilter
from .forms import RegistroUsuarioForm, EditarUsuarioForm, PassUserChangeForm
from .tables import UserTable

User = get_user_model()


# Create your views here.
class RegistroUsuario(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'registration/registrar.html'
    form_class = RegistroUsuarioForm
    success_message = _('Data creation was successful')

    # success_url = reverse_lazy('usuario:listar')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(RegistroUsuario, self).get_context_data()
        # context['pic_url'] = self.model.pic.url
        context['model'] = 'Usuario'
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        self.success_url = self.request.META.get('HTTP_REFERER')
        return context


class ListarUsuarios(ListView):
    model = User
    template_name = 'cruds/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListarUsuarios, self).get_context_data()
        # context['pic_url'] = self.model.pic.url
        context['model'] = 'Usuario'
        return context


class EditarUsuario(UpdateView):
    model = User
    form_class = EditarUsuarioForm
    template_name = 'cruds/create.html'
    success_url = reverse_lazy('usuario:listar')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.object = self.get_object

    def get_context_data(self, **kwargs):
        context = super(EditarUsuario, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        # context['pic_url'] = self.model.pic.url
        context['id'] = pk
        context['model'] = 'Usuario'
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        self.success_url = self.request.META.get('HTTP_REFERER')
        return context

    def post(self, request, *args, **kwargs):
        id_usuario = kwargs['pk']
        usuario = self.model.objects.get(id=id_usuario)
        form = self.form_class(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return HttpResponseRedirect(self.get_success_url())


class PassChangeView(PasswordChangeView):
    form_class = PassUserChangeForm
    success_url = reverse_lazy("password_change_done")
    template_name = "registration/pass_change_form.html"
    title = _("Password change")

    def get_context_data(self, **kwargs):
        context = super(PassChangeView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        context['model'] = 'Usuario'
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        # self.success_url = self.request.META.get('HTTP_REFERER')
        return context


class MyLoginView(SuccessMessageMixin, LoginView):
    success_message = _("User <<%(user)s>> were successfully logged in.")

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            user=self.request.user.username
        )


class UsuarioCRUD(CommonCRUDView):
    model = User

    namespace = 'app_index:usuario'

    template_father = 'app_index/cruds/base.html'

    template_name_base = 'usuarios/usuario/cruds'

    views_available = [
        'create',
        'list',
        'delete',
        'update',
    ]

    fields = [
        'username',
        'email',
        'last_login',
    ]

    add_form = RegistroUsuarioForm
    update_form = EditarUsuarioForm

    check_login = True
    check_perms = True

    related_fields = [
    ]

    list_fields = [
        'username',
        'email',
        'last_login',
    ]

    search_fields = [
        'username__icontains',
        'email__icontains',
        'last_login__icontains',
    ]

    filter_fields = [
        'username',
        'email',
        'last_login',
    ]

    filterset_class = UserUebFilter

    page_length = 10

    page_length_menu = [5, 10, 15, 20]

    # Table settings
    table_class = UserTable
    template_name = "he_index/cruds/list_table.html"
    paginate_by = 10
    exclude_columns = ("actions",)
