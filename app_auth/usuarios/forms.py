from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row, Column
from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

from codificadores.models import UnidadContable
from cruds_adminlte3.utils import common_filter_form_actions, common_form_actions
from cruds_adminlte3.widgets import SelectWidget

User = get_user_model()


# Crear nuevos usuarios. Incluye todos los campos requeridos además de las contraseñas repetidas para confirmación
class RegistroUsuarioForm(UserCreationForm):
    email = forms.EmailInput()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'username',
            'ueb',
            'groups'
        ]

    widgets = {
        'groups': forms.SelectMultiple(
            attrs={
                'class': 'duallistbox',
                'style': 'width: 100%;',
                'multiple': 'multiple',
            }
        ),
        'ueb': SelectWidget(
            attrs={'style': 'width: 100%'}
        ),
    }

    def __init__(self, *args, **kwargs):
        self.user_pop = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(RegistroUsuarioForm, self).__init__(*args, **kwargs)
        self.user = kwargs['instance']
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-userCreateForm'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Registration information'),
                    Row(
                        Column('first_name', css_class='form-group col-md-4 mb-0'),
                        Column('last_name', css_class='form-group col-md-4 mb-0'),
                        Column('email', css_class='form-group col-md-4 mb-0'),

                        Column('username', css_class='form-group col-md-4 mb-0'),

                        Column('ueb', css_class='form-group col-md-4 mb-0'),
                        Column('password1', css_class='form-group col-md-6 mb-0'),
                        Column('password2', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'),
                ),
                Tab(
                    _('Groups'),
                    Row(
                        Column('groups', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'),

                ),
            ),
        )

        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_register_form_actions.html').template.source
                )
            )
        )

        if not self.user_pop.is_superuser:
            self.fields['ueb'].initial = UnidadContable.objects.get(pk=self.user_pop.ueb.id)
        else:
            self.fields['ueb'].queryset = UnidadContable.objects.filter(activo=True).all()

        self.fields['ueb'].disabled = not self.user_pop.is_superuser
        self.fields['ueb'].required = self.user_pop.is_superuser

        self.fields["groups"].queryset = Group.objects.all().exclude(
            id=5) if self.user_pop.is_admin else Group.objects.all()

    def clean_password2(self):  # Validar que ambas contraseñas coincidan
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Las contraseñas no coinciden')
        return password2

    def save(self, commit=True):  # Guardar las contraseñas en formato Hash
        usuario = super(RegistroUsuarioForm, self).save(commit=False)
        usuario.set_password(self.cleaned_data['password1'])
        usuario.active = True
        if commit:
            usuario.save()
        super(RegistroUsuarioForm, self).save()
        return usuario


# Forma para actualizar los usuarios.
class EditarUsuarioForm(UserChangeForm):
    class Media:
        js = ['js/my_dual_listbox.js']

    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        required=False,
    )

    email = forms.EmailInput()
    user = None

    class Meta:
        model = User
        fields = "__all__"

        widgets = {
            'last_login': forms.DateTimeInput(
                attrs={
                    'readonly': True,
                    'format': 'yyyy-mm-dd',
                },
            ),
            'date_joined': forms.DateTimeInput(
                attrs={
                    'readonly': True,
                    'format': 'yyyy-mm-dd',
                }
            ),
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'duallistbox',
                    'style': 'width: 100%; heigth: 100%',
                    'multiple': 'multiple',
                }
            ),
            'user_permissions': forms.SelectMultiple(
                attrs={
                    'class': 'duallistbox',
                    'style': 'width: 100%',
                    'multiple': 'multiple',
                }
            ),
            'ueb': SelectWidget(
                attrs={'style': 'width: 85%;'}
            ),

        }

    def get_context(self):
        return super().get_context()

    def __init__(self, *args, **kwargs):
        self.user_pop = kwargs.pop('user', None)
        instance = kwargs.get('instance', None)
        self.post = kwargs.pop('post', None)
        super(EditarUsuarioForm, self).__init__(*args, **kwargs)
        self.user = kwargs['instance']
        self.fields['password'].help_text = _(
            "Raw passwords are not stored, so there is no way to see this "
            "user’s password, but you can change the password using "
            '<a href="{}">this form</a>.'
        ).format("password?/")
        self.fields['password'].help_text.format("/password/")
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-userEditForm'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('User information'),
                    Row(
                        Column(
                            PrependedText(
                                'first_name', mark_safe('<i class="fa fa-user-pen"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),
                        Column(
                            PrependedText(
                                'last_name', mark_safe('<i class="fa fa-user-pen"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),
                        Column(
                            PrependedText(
                                'email', mark_safe('<i class="fa fa-envelope"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),
                        css_class='form-row'),
                    Row(
                        Column(
                            PrependedText(
                                'username', mark_safe('<i class="fa fa-user-check"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),
                        Column(
                            PrependedText(
                                'ueb', mark_safe('<i class="fa fa-building"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),

                        Column(
                            'is_active', css_class='form-group col-md-3 mb-0'
                        ),
                        css_class='form-row'
                    ),
                    Row(
                        Column(
                            PrependedText(
                                'new_password1', mark_safe('<i class="fa fa-key"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),
                        Column(
                            PrependedText(
                                'new_password2', mark_safe('<i class="fa fa-key"></i>')
                            ),
                            css_class='form-group col-md-4 mb-0'
                        ),
                        css_class='form-row'),
                ),
                Tab(
                    _('System information'),
                    Row(
                        Column(
                            PrependedText(
                                'last_login', mark_safe('<i class="fa fa-calendar-check"></i>')
                            ),
                            css_class='form-group col-md-2 mb-0'
                        ),
                        Column(
                            PrependedText(
                                'date_joined', mark_safe('<i class="fa fa-calendar-check"></i>')
                            ),
                            css_class='form-group col-md-2 mb-0'
                        ),
                        Column('is_superuser', css_class='form-group col-md-3 mb-0'),
                        Column('is_staff', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'),
                ),
                Tab(
                    _('Groups'),
                    Row(
                        Column('groups', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'),

                ),
            ),
        )

        self.helper.layout.append(
            common_form_actions()
        )
        self.fields["ueb"].disabled = not self.user_pop.is_superuser
        self.fields["ueb"].required = self.user_pop.is_superuser
        self.fields["is_superuser"].disabled = not self.user_pop.is_superuser
        self.fields["is_staff"].disabled = not self.user_pop.is_superuser
        self.fields["groups"].queryset = Group.objects.all().exclude(
            id=5) if self.user_pop.is_admin else Group.objects.all()

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise ValidationError(
                    self.error_messages["password_mismatch"],
                    code="password_mismatch",
                )
        if password1 or password2:
            password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        super(EditarUsuarioForm, self).save()
        password = self.cleaned_data["new_password1"]
        if password:
            self.user.set_password(password)
            self.user.save()
        return self.user


class PassUserChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(PassUserChangeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-userPassChangeForm'
        self.helper.form_method = 'post'

        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/ok_cancel_form_actions.html').template.source
                )
            )
        )


class GroupForm(forms.ModelForm):
    class Media:
        js = ['js/my_dual_listbox.js']

    class Meta:
        model = Group
        fields = [
            'name',
            'permissions',
        ]
        widgets = {
            'permissions': forms.Select(
                attrs={
                    'class': 'duallistbox',
                    'style': 'width: 100%',
                    'multiple': 'multiple',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']  # Ver que guarda esto en el caso de group
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_groupForm'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Información de Grupo',
                    Row(
                        Column('name', css_class='form-group col-md-12 mb-0'),
                        Column('permissions', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'),
                ),
            ),
        )

        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_register_form_actions.html').template.source
                )
            )
        )


class UserUebFormFilter(forms.Form):
    class Meta:
        model = User
        fields = [
            'query',
            'first_name',
            'last_name',
            'username',
            'email',
            'last_login',
            'date_joined',
            'is_superuser',
            'is_staff',
            'is_active',
            'ueb',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        super(UserUebFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        # self.fields['last_login'].widget.widgets[0].attrs = {'placeholder': _('Date from...')}
        # self.fields['last_login'].widget.widgets[1].attrs = {'placeholder': _('Date to...')}
        # self.fields['date_joined'].widget.widgets[0].attrs = {'placeholder': _('Date from...')}
        # self.fields['date_joined'].widget.widgets[1].attrs = {'placeholder': _('Date to...')}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-usuario-form-filter'
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    '1',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-6 mb-0'
                        ),
                        Column('first_name', css_class='form-group col-md-3 mb-0'),
                        Column('last_name', css_class='form-group col-md-3 mb-0'),
                        Column('username', css_class='form-group col-md-3 mb-0'),
                        Column('email', css_class='form-group col-md-3 mb-0'),
                        css_class='form-row',
                    ),
                ),
                Tab(
                    '2',
                    Row(
                        Column('last_login', css_class='form-group col-md-4 mb-0'),
                        Column('date_joined', css_class='form-group col-md-4 mb-0'),
                        Column('is_superuser', css_class='form-group col-md-4 mb-0'),
                        Column('is_staff', css_class='form-group col-md-3 mb-0'),
                        Column('is_active', css_class='form-group col-md-3 mb-0'),
                        css_class='form-row'
                    ),
                ),
                style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
            ),

        )

        self.helper.layout.append(
            common_filter_form_actions()
        )

    def get_context(self):
        context = super().get_context()
        context['width_right_sidebar'] = '750px'
        context['height_right_sidebar'] = '380px'
        return context
