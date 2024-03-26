from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML
from django import forms
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from configuracion.models import *
from cruds_adminlte3.utils import (
    common_filter_form_actions, )
from cruds_adminlte3.widgets import SelectWidget


# ------------ ConexionBaseDato de sistemas externos/ Form ------------
class ConexionBaseDatoForm(forms.ModelForm):
    password = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput(render_value=True),
        strip=False,
        required=False,
    )

    class Meta:
        model = ConexionBaseDato
        fields = [
            'sistema',
            'database_name',
            'host',
            'port',
            'database_user',
            'password',
            'unidadcontable',
        ]

        widgets = {
            'unidadcontable': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),

        }


    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ConexionBaseDatoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_conexionbasedato_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Database connection'),
                    Row(
                        Column('sistema', css_class='form-group col-md-6 mb-0'),
                        Column('database_name', css_class='form-group col-md-6 mb-0'),
                        Column('database_user', css_class='form-group col-md-6 mb-0'),
                        Column('password', css_class='form-group col-md-6 mb-0'),
                        Column('host', css_class='form-group col-md-6 mb-0'),
                        Column('port', css_class='form-group col-md-6 mb-0'),
                        Column('unidadcontable', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
            ),
        )

        if not self.user.is_superuser:
            self.fields['unidadcontable'].initial = UnidadContable.objects.get(pk=self.user.ueb.id)
        else:
            self.fields['unidadcontable'].queryset = UnidadContable.objects.filter(activo=True).all()

        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_form_actions.html').template.source
                )
            )
        )

        self.fields['unidadcontable'].disabled = not self.user.is_superuser
        self.fields['unidadcontable'].required = self.user.is_superuser

# ------------ User UEB / Form Filter ------------
class ConexionBaseDatoFormFilter(forms.Form):
    class Meta:
        model = ConexionBaseDato
        fields = [
            'sistema',
            'database_name',
            'unidadcontable',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ConexionBaseDatoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_conexionbasedato_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Database connection'),
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('sistema', css_class='form-group col-md-6 mb-0'),
                        Column('database_name', css_class='form-group col-md-6 mb-0'),
                        Column('unidadcontable', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row',
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
        context['width_right_sidebar'] = '760px'
        context['height_right_sidebar'] = '505px'
        return context