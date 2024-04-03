from django.urls import path, include
from django.contrib.auth import views as auth_views

from cruds_adminlte3.urls import crud_for_app
from . import views
from .forms import RegistroUsuarioForm, EditarUsuarioForm
from .forms_usuario_groups import UserGroupForm
from .forms_usuario_permissions import UserPermissionsForm
from cruds_adminlte3.crud import CRUDView


usuario_crud = views.UsuarioCRUD()

user_forms = {
    'add_usuario': RegistroUsuarioForm,
    'update_usuario': EditarUsuarioForm,
    'list_usuario': [
        'username',
        'email',
        'last_login',
    ],
    'add_usuario_groups': UserGroupForm,
    'update_usuario_groups': UserGroupForm,
    'list_usuario_groups': [
        'usuario',
        'group',
    ],
    'add_usuario_user_permissions': UserPermissionsForm,
    'update_usuario_user_permissions': UserPermissionsForm,
    'list_usuario_user_permissions': [
        'usuario',
        'permission',
    ],
}

app_name = 'usuario'
urlpatterns = [
    path('password/', views.PassChangeView.as_view(), name='password'),
    # path('', include('django.contrib.auth.urls')),
    # path('login/', auth_views.LoginView.as_view(), name='login'),
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('accounts/login/', views.MyLoginView.as_view(), name='login'),
    path('logout/', views.MyLogoutView.as_view(), name='logout'),
    path('accounts/logout/', views.MyLogoutView.as_view(), name='logout'),
    path('register/', views.RegistroUsuario.as_view(), name='register'),
    path('password_change/', views.PassChangeView.as_view(), name="password_change"),
    path('password_show/', views.password_show, name="password_show"),
    path('password_hide/', views.password_hide, name="password_hide"),
    path('password_change/done/', views.MyPasswordChangeDoneView.as_view(), name="password_change_done"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done",),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm",),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete",),
    path("", include(usuario_crud.get_urls())),
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
