from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordChangeView, LoginView, LogoutView, PasswordChangeDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.generic import CreateView, ListView, UpdateView
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required

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
        context['model'] = 'User'
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        self.success_url = self.request.META.get('HTTP_REFERER')
        return context


class ListarUsuarios(ListView):
    model = User
    template_name = 'cruds/list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListarUsuarios, self).get_context_data()
        context['model'] = 'User'
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
        context['id'] = pk
        context['model'] = 'User'
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


class PassChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = PassUserChangeForm
    success_url = reverse_lazy("app_index:index")
    success_message = _("User <<%(user)s>> has successfully changed password.")
    template_name = "registration/pass_change_form.html"
    title = _("Password change")

    def get_context_data(self, **kwargs):
        context = super(PassChangeView, self).get_context_data(**kwargs)
        pk = self.kwargs.get('pk', 0)
        if 'form' not in context:
            context['form'] = self.form_class()
        context['id'] = pk
        context['model'] = 'User'
        context['previous_url'] = self.request.META.get('HTTP_REFERER')
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            user=self.request.user.username
        )


class MyPasswordChangeDoneView(SuccessMessageMixin, PasswordChangeDoneView):
    template_name = "registration/pass_change_done.html"
    title = _("Password change")
    success_message = _("User <<%(user)s>> has successfully changed password.")


class MyLoginView(SuccessMessageMixin, LoginView):
    success_message = _("User <<%(user)s>> has successfully logged in.")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'hide_password': _('Hide password'),
            'show_password': _('Show password'),
            'title_success': _('Success'),
        })
        return context

    def get_success_message(self, cleaned_data):
        return self.success_message % dict(
            cleaned_data,
            user=self.request.user.username
        )


class MyLogoutView(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        message = _("User <<%s>> has successfully logged out.")
        messages.add_message(request, messages.SUCCESS, message % user)
        response = super().dispatch(request, *args, **kwargs)
        return response


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
    template_name = "app_index/cruds/list_table.html"
    paginate_by = 10
    exclude_columns = ("actions",)

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_queryset(self):
                qset = super().get_queryset()
                user = self.request.user
                if not user.is_superuser:
                    qset = qset.filter(is_superuser=False, ueb=user.ueb)
                return qset

        return OFilterListView


def password_show(request):
    pass_show = request.GET.get('show', 'true') == 'true'
    context = {
        'password_show': pass_show,
    }
    return render(request, 'usuarios/usuario/partials/password_show.html', context=context)


def password_hide(request):
    return render(request, 'usuarios/usuario/partials/password_hide.html')
