from django import forms
from django.contrib.auth.models import Permission
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, HTML, Row, Column

from cruds_adminlte3.utils import common_form_actions, common_filter_form_actions


# Crear y/o modificar nuevos grupos.
class PermissionForm(forms.ModelForm):
    class Media:
        js = ['js/my_dual_listbox.js']

    class Meta:
        model = Permission
        fields = [
            'name',
            'content_type',
            'codename',
        ]

    def __init__(self, *args, **kwargs):
        self.user_pop = kwargs.pop('user', None)
        super(PermissionForm, self).__init__(*args, **kwargs)
        instance = kwargs['instance']  # Ver que guarda esto en el caso de group
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_permissionForm'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Permission Information'),
                    Row(
                        Column('name', css_class='form-group col-md-4 mb-0'),
                        Column('content_type', css_class='form-group col-md-4 mb-0'),
                        Column('codename', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'),
                ),
            ),
        )

        self.helper.layout.append(
            common_form_actions()
        )


class PermissionFormFilter(forms.Form):
    class Meta:
        model = Permission
        fields = [
            'query',
            'name',
            'content_type',
            'codename',
        ]

    def __init__(self, *args, **kwargs) -> None:
        self.user = kwargs.pop('user', None)
        super(PermissionFormFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id-permission-form-filter'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    '1',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('name', css_class='form-group col-md-6 mb-0'),
                        Column('codename', css_class='form-group col-md-6 mb-0'),
                        Column('content_type', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'),
                ),
            ),
        )

        self.helper.layout.append(
            common_filter_form_actions()
        )

    def get_context(self):
        context = super().get_context()
        context['width_right_sidebar'] = '750px'
        context['height_right_sidebar'] = '500px'
        return context
