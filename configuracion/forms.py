from crispy_forms.bootstrap import (
    TabHolder,
    Tab, AppendedText, FormActions, )
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


# ------------ UEB / Form ------------

# class UebForm(forms.ModelForm):
#     class Meta:
#         model = Ueb
#         fields = [
#             'idunidadcontable',
#         ]
#
#         widgets = {
#             'idunidadcontable': SelectWidget(
#                 attrs={'style': 'width: 100%'}
#             ),
#         }
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(UebForm, self).__init__(*args, **kwargs)
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_ueb_form'
#         self.helper.form_method = 'post'
#         self.helper.form_tag = False
#
#         self.helper.layout = Layout(
#             TabHolder(
#                 Tab(
#                     'UEB',
#                     Row(
#                         Column('idunidadcontable', css_class='form-group col-md-6 mb-0'),
#                         css_class='form-row'
#                     ),
#                 ),
#
#             ),
#         )
#         self.helper.layout.append(
#             FormActions(
#                 HTML(
#                     get_template('cruds/actions/hx_common_form_actions.html').template.source
#                 )
#             )
#         )


# ------------ UEB / Form Filter ------------
# class UebFormFilter(forms.Form):
#     class Meta:
#         model = Ueb
#         fields = [
#             'idunidadcontable',
#         ]
#
#     def __init__(self, *args, **kwargs) -> None:
#         instance = kwargs.get('instance', None)
#         self.user = kwargs.pop('user', None)
#         self.post = kwargs.pop('post', None)
#         super(UebFormFilter, self).__init__(*args, **kwargs)
#         self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
#         self.helper = FormHelper(self)
#         self.helper.form_id = 'id_ueb_form_filter'
#         self.helper.form_method = 'GET'
#
#         self.helper.layout = Layout(
#
#             TabHolder(
#                 Tab(
#                     'UEB',
#                     Row(
#                         Column(
#                             AppendedText(
#                                 'query', mark_safe('<i class="fas fa-search"></i>')
#                             ),
#                             css_class='form-group col-md-12 mb-0'
#                         ),
#                         Column('idunidadcontable', css_class='form-group col-md-6 mb-0'),
#                         css_class='form-row',
#                     ),
#                 ),
#                 style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
#             ),
#
#         )
#
#         self.helper.layout.append(
#             common_filter_form_actions()
#         )
#
#     def get_context(self):
#         context = super().get_context()
#         context['width_right_sidebar'] = '760px'
#         context['height_right_sidebar'] = '505px'
#         return context


# ------------ User UEB / Form ------------

class UserUebForm(forms.ModelForm):
    class Meta:
        model = UserUeb
        fields = [
            'idueb',

        ]

        widgets = {
            'idueb': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(UserUebForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_userueb_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('UEB User'),
                    Row(
                        Column('idueb', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),

            ),
        )
        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_form_actions.html').template.source
                )
            )
        )


# ------------ User UEB / Form Filter ------------
class UserUebFormFilter(forms.Form):
    class Meta:
        model = UserUeb
        fields = [
            'idueb',

        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(UserUebFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_userueb_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    _('UEB User'),
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('idueb', css_class='form-group col-md-6 mb-0'),
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
