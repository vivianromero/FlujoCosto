from django import forms
from django.apps import apps
from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import TabHolder, Tab, FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row, Column

app = apps.get_app_config('auth')
User_Permissions = app.models['user_user_permissions']


# Crear y/o modificar nuevos grupos.
class UserPermissionsForm(forms.ModelForm):
    class Media:
        js = ['js/my_dual_listbox.js']

    class Meta:
        model = User_Permissions
        fields = [
            'user',
            'permission',
        ]
        widgets = {
            'user': forms.Select(
                attrs={
                    'style': 'width: 100%',
                }
            ),
            'permission': forms.Select(
                attrs={
                    'class': 'duallistbox',
                    'style': 'width: 100%',
                    'multiple': 'multiple',
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(UserPermissionsForm, self).__init__()
        instance = kwargs['instance']  # Ver que guarda esto en el caso de group
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_user_permissionsForm'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Información de relación Usuario - Permisos',
                    Row(
                        Column('user', css_class='form-group col-md-12 mb-0'),
                        Column('permission', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'),
                ),
            ),
        )

        self.helper.layout.append(
            FormActions(
                HTML(
                    """{% load i18n %}
                        <button type="submit" class="btn btn-primary">
                            <i class="fa fa-check"></i> {% trans 'Registrar' %}
                        </button>"""
                ),
                HTML(
                    """{% load i18n %}
                        {% if not url_update %}
                            <button type="submit" name="another" class="btn btn-primary">
                                <i class="fa fa-check"></i> {% trans 'Registrar y adicionar otro' %}
                            </button>
                        {% endif %}"""),
                HTML(
                    """{% load i18n %}
                        {% if url_list %}
                            <a href="{{ url_list }}" class="btn btn-secondary">
                                <i class="fa fa-remove"></i> {% trans "Cancelar" %}
                            </a>
                        {% endif %}"""
                ),
                HTML(
                    """{% load i18n %}
                        {% if url_delete %}
                            <a href="{{ url_delete }}" class="btn btn-danger">
                                <i class="fa fa-trash"></i> {% trans "Eliminar" %}
                            </a>
                        {% endif %}"""
                ),
            )
        )