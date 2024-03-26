from crispy_forms.bootstrap import (
    TabHolder,
    Tab, AppendedText, FormActions, )
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field, Div, Fieldset
from crispy_formset_modal.layout import ModalEditFormsetLayout
from crispy_formset_modal.helper import ModalEditFormHelper
from crispy_formset_modal.layout import ModalEditLayout
from django import forms
from django.contrib import messages
from django.forms import HiddenInput
from django.template.loader import render_to_string, get_template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from codificadores.models import *
from cruds_adminlte3.utils import (
    common_form_actions,
    common_filter_form_actions, crud_url_name,
)
from cruds_adminlte3.widgets import SelectWidget, MyCheckboxSelectMultiple
from mptt.forms import TreeNodeChoiceField


# ------------ Unidad Contable / Form ------------

class UnidadContableForm(forms.ModelForm):
    class Meta:
        model = UnidadContable
        fields = [
            'codigo',
            'nombre',
            'activo',
            'is_empresa',
            'is_comercializadora',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(UnidadContableForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_unidadcontable_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["codigo"].disabled = True
        self.fields["nombre"].disabled = True

        self.fields["codigo"].required = False
        self.fields["nombre"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'UEB',
                    Row(
                        Column('codigo', css_class='form-group col-md-2 mb-0'),
                        Column('nombre', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('activo', css_class='form-group col-md-2 mb-0'),
                        Column('is_empresa', css_class='form-group col-md-2 mb-0'),
                        Column('is_comercializadora', css_class='form-group col-md-2 mb-0'),

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


# ------------ Unidad Contable / Form Filter ------------
class UnidadContableFormFilter(forms.Form):
    class Meta:
        model = UnidadContable
        fields = [
            'codigo',
            'nombre',
            'activo',
            'is_empresa',
            'is_comercializadora',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(UnidadContableFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_undadcontable_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'UEB',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('nombre', css_class='form-group col-md-8 mb-0'),
                        Column('activo', css_class='form-group col-md-4 mb-0'),
                        Column('is_empresa', css_class='form-group col-md-4 mb-0'),
                        Column('is_comercializadora', css_class='form-group col-md-4 mb-0'),

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


# ------------ Medida / Form ------------

class MedidaForm(forms.ModelForm):
    class Meta:
        model = Medida
        fields = [
            'clave',
            'descripcion',
            'activa',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MedidaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_medida_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["clave"].disabled = True
        self.fields["descripcion"].disabled = True

        self.fields["clave"].required = False
        self.fields["descripcion"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Unit of measurement'),
                    Row(
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),

                        css_class='form-row'
                    ),
                    Row(
                        Column('activa', css_class='form-group col-md-4 mb-0'),
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


# ------------ Medida / Form Filter ------------
class MedidaFormFilter(forms.Form):
    class Meta:
        model = Medida
        fields = [
            'clave',
            'descripcion',
            'activa',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MedidaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_medida_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Unit of measurement'),
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
                        Column('activa', css_class='form-group col-md-3 mb-0'),

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


# ------------ MedidaConversion / Form ------------

class MedidaConversionForm(forms.ModelForm):
    medidao = forms.ModelChoiceField(queryset=Medida.objects.filter(activa=True).all(),
                                          widget=forms.Select(attrs={'style': 'width: 100%'}))
    medidad = forms.ModelChoiceField(queryset=Medida.objects.filter(activa=True).all(),
                                     widget=forms.Select(attrs={'style': 'width: 100%'}))
    class Meta:
        model = MedidaConversion
        fields = [
            'medidao',
            'medidad',
            'factor_conversion'
        ]

        # widgets = {
        #     # 'medidao': SelectWidget(
        #     #     attrs={'style': 'width: 100%'}
        #     # ),
        #     'medidad': SelectWidget(
        #         attrs={'style': 'width: 100%'}
        #     ),
        # }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MedidaConversionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_medidaconversion_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        # medidao_queryset = self.fields['medidao'].choices.queryset
        # self.fields['medidao'].choices.queryset = medidao_queryset.filter(activa=True)

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Convert unit of measurement'),
                    Row(
                        Column('medidao', css_class='form-group col-md-5 mb-0'),
                        Column('medidad', css_class='form-group col-md-5 mb-0'),
                        Column('factor_conversion', css_class='form-group col-md-2 mb-0'),

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


# ------------ MedidaConversión / Form Filter ------------
class MedidaConversionFormFilter(forms.Form):
    class Meta:
        model = MedidaConversion
        fields = [
            'medidao',
            'medidad',
            'factor_conversion',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MedidaConversionFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_medidaconversion_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Convert unit of measurement'),
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('medidao', css_class='form-group col-md-5 mb-0'),
                        Column('medidad', css_class='form-group col-md-5 mb-0'),
                        Column('factor_conversion', css_class='form-group col-md-2 mb-0'),

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


# ------------ Cuenta / Form ------------
class CuentaForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Cuenta.objects.all(), level_indicator='+--')

    class Meta:
        model = Cuenta
        fields = [
            'long_niv',
            'posicion',
            'clave',
            'descripcion',
            'activa',
            'parent',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CuentaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_cuenta_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Cuenta',
                    Row(
                        Column('long_niv', css_class='form-group col-md-2 mb-0'),
                        Column('posicion', css_class='form-group col-md-2 mb-0'),
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('activa', css_class='form-group col-md-2 mb-0'),
                        Column('parent', css_class='form-group col-md-4 mb-0'),

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


# ------------ Cuenta / Form Filter ------------
class CuentaFormFilter(forms.Form):
    class Meta:
        model = Cuenta
        fields = [
            'long_niv',
            'posicion',
            'clave',
            'descripcion',
            'activa',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CuentaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_cuenta_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Cuenta',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('long_niv', css_class='form-group col-md-2 mb-0'),
                        Column('posicion', css_class='form-group col-md-2 mb-0'),
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('activa', css_class='form-group col-md-2 mb-0'),

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


# ------------ CentroCosto / Form ------------
class CentroCostoForm(forms.ModelForm):
    class Meta:
        model = CentroCosto
        fields = [
            'clave',
            'clavenivel',
            'descripcion',
            'activo',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CentroCostoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_centrocosto_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Centro de Costo',
                    Row(
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('clavenivel', css_class='form-group col-md-4 mb-0'),
                        Column('activo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-12 mb-0'),
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


# ------------ CentroCosto / Form Filter ------------
class CentroCostoFormFilter(forms.Form):
    class Meta:
        model = CentroCosto
        fields = [
            'clave',
            'clavenivel',
            'descripcion',
            'activo',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CentroCostoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_centrocosto_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Centro de Costo',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('clavenivel', css_class='form-group col-md-4 mb-0'),
                        Column('activo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-12 mb-0'),
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


# ------------ TipoProducto / Form ------------
class TipoProductoForm(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = [
            # 'id',
            'descripcion',
        ]

        widgets = {
            'id': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(TipoProductoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_tipoproducto_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Tipo Producto',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
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


# ------------ TipoProducto / Form Filter ------------
class TipoProductoFormFilter(forms.Form):
    class Meta:
        model = TipoProducto
        fields = [
            'id',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(TipoProductoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_tipoproducto_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Tipo Producto',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
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


# ------------ EstadoProducto / Form ------------
class EstadoProductoForm(forms.ModelForm):
    class Meta:
        model = EstadoProducto
        fields = [
            # 'id',
            'descripcion',
        ]

        widgets = {
            'id': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(EstadoProductoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_estadoproducto_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Estado Producto',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
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


# ------------ EstadoProducto / Form Filter ------------
class EstadoProductoFormFilter(forms.Form):
    class Meta:
        model = EstadoProducto
        fields = [
            'id',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(EstadoProductoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_estadoproducto_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Estado Producto',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
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


# ------------ ClaseMateriaPrima / Form ------------
class ClaseMateriaPrimaForm(forms.ModelForm):
    class Meta:
        model = ClaseMateriaPrima
        fields = [
            # 'id',
            'descripcion',
            'capote_fortaleza',
        ]

        widgets = {
            'id': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ClaseMateriaPrimaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_clasemateriaprima_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Estado Producto',
                    Row(
                        # Column('id', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('capote_fortaleza', css_class='form-group col-md-6 mb-0'),
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


# ------------ ClaseMateriaPrima / Form Filter ------------
class ClaseMateriaPrimaFormFilter(forms.Form):
    class Meta:
        model = EstadoProducto
        fields = [
            'id',
            'descripcion',
            'capote_fortaleza',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ClaseMateriaPrimaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_clasemateriaprima_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Estado Producto',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('capote_fortaleza', css_class='form-group col-md-3 mb-0'),
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


# ------------ ProductoFlujo / Form ------------
class ProductoFlujoForm(forms.ModelForm):
    class Meta:
        model = ProductoFlujo
        fields = [
            # 'id',
            'codigo',
            'descripcion',
            'activo',
            'medida',
            'tipoproducto',
        ]

        widgets = {
            'medida': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'tipoproducto': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Producto Flujo',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
                        Column('medida', css_class='form-group col-md-5 mb-0'),
                        Column('tipoproducto', css_class='form-group col-md-5 mb-0'),
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


# ------------ ProductoFlujo / Form Filter ------------
class ProductoFlujoFormFilter(forms.Form):
    class Meta:
        model = ProductoFlujo
        fields = [
            'id',
            'codigo',
            'descripcion',
            'activo',
            'medida',
            'tipoproducto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Producto Flujo',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
                        Column('medida', css_class='form-group col-md-5 mb-0'),
                        Column('tipoproducto', css_class='form-group col-md-5 mb-0'),
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


# ------------ ProductoFlujoClase / Form ------------
class ProductoFlujoClaseForm(forms.ModelForm):
    class Meta:
        model = ProductoFlujoClase
        fields = [
            # 'id',
            'clasemateriaprima',
            'producto',
        ]

        widgets = {
            'clasemateriaprima': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'producto': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoClaseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Producto Flujo Clase',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('clasemateriaprima', css_class='form-group col-md-5 mb-0'),
                        Column('producto', css_class='form-group col-md-5 mb-0'),
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


# ------------ ProductoFlujoClase / Form Filter ------------
class ProductoFlujoClaseFormFilter(forms.Form):
    class Meta:
        model = ProductoFlujoClase
        fields = [
            'id',
            'clasemateriaprima',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoClaseFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujoclase_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Producto Flujo Clase',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('clasemateriaprima', css_class='form-group col-md-5 mb-0'),
                        Column('producto', css_class='form-group col-md-5 mb-0'),
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


# ------------ ProductoFlujoDestino / Form ------------
class ProductoFlujoDestinoForm(forms.ModelForm):
    class Meta:
        model = ProductoFlujoDestino
        fields = [
            # 'id',
            'destino',
            'producto',
        ]

        widgets = {
            'producto': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoDestinoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujodestino_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Producto Flujo Destino',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('destino', css_class='form-group col-md-4 mb-0'),
                        Column('producto', css_class='form-group col-md-4 mb-0'),
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


# ------------ ProductoFlujoDestino / Form Filter ------------
class ProductoFlujoDestinoFormFilter(forms.Form):
    class Meta:
        model = ProductoFlujoDestino
        fields = [
            'id',
            'destino',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoDestinoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujodestino_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Producto Flujo Destino',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('destino', css_class='form-group col-md-4 mb-0'),
                        Column('producto', css_class='form-group col-md-4 mb-0'),
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


# ------------ ProductoFlujoCuenta / Form ------------
class ProductoFlujoCuentaForm(forms.ModelForm):
    class Meta:
        model = ProductoFlujoCuenta
        fields = [
            # 'id',
            'cuenta',
            'producto',
        ]

        widgets = {
            'cuenta': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'producto': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoCuentaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujocuenta_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Producto Flujo Cuenta',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('cuenta', css_class='form-group col-md-4 mb-0'),
                        Column('producto', css_class='form-group col-md-4 mb-0'),
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


# ------------ ProductoFlujoCuenta / Form Filter ------------
class ProductoFlujoCuentaFormFilter(forms.Form):
    class Meta:
        model = ProductoFlujoCuenta
        fields = [
            'id',
            'cuenta',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ProductoFlujoCuentaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujocuenta_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Producto Flujo Destino',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('cuenta', css_class='form-group col-md-4 mb-0'),
                        Column('producto', css_class='form-group col-md-4 mb-0'),
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


# ------------ CategoriaVitola / Form ------------
class CategoriaVitolaForm(forms.ModelForm):
    class Meta:
        model = CategoriaVitola
        fields = [
            # 'id',
            'descripcion',
            'orden',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CategoriaVitolaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_categoriavitola_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Producto Flujo Cuenta',
                    Row(
                        # Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('orden', css_class='form-group col-md-4 mb-0'),
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


# ------------ CategoriaVitola / Form Filter ------------
class CategoriaVitolaFormFilter(forms.Form):
    class Meta:
        model = CategoriaVitola
        fields = [
            'id',
            'descripcion',
            'orden',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CategoriaVitolaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_categoriavitola_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Categoría Vitola',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('orden', css_class='form-group col-md-4 mb-0'),
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


# ------------ TipoVitola / Form ------------
class TipoVitolaForm(forms.ModelForm):
    class Meta:
        model = TipoVitola
        fields = [
            # 'id',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(TipoVitolaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_tipovitola_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Tipo Vitola',
                    Row(
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
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


# ------------ TipoVitola / Form Filter ------------
class TipoVitolaFormFilter(forms.Form):
    class Meta:
        model = TipoVitola
        fields = [
            'id',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(TipoVitolaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_tipovitola_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Tipo Vitola',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('id', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
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


# ------------ Vitola / Form ------------
class VitolaForm(forms.ModelForm):
    class Meta:
        model = Vitola
        fields = [
            'diametro',
            'longitud',
            'destino',
            'cepo',
            'categoriavitola',
            'producto',
            'tipovitola',
        ]

        widgets = {
            'categoriavitola': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'producto': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'tipovitola': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(VitolaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_vitola_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Vitola',
                    Row(
                        Column('diametro', css_class='form-group col-md-3 mb-0'),
                        Column('longitud', css_class='form-group col-md-3 mb-0'),
                        Column('destino', css_class='form-group col-md-3 mb-0'),
                        Column('cepo', css_class='form-group col-md-4 mb-3'),
                        Column('categoriavitola', css_class='form-group col-md-4 mb-0'),
                        Column('producto', css_class='form-group col-md-4 mb-0'),
                        Column('tipovitola', css_class='form-group col-md-4 mb-0'),
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


# ------------ Vitola / Form Filter ------------
class VitolaFormFilter(forms.Form):
    class Meta:
        model = Vitola
        fields = [
            'diametro',
            'longitud',
            'destino',
            'cepo',
            'categoriavitola',
            'producto',
            'tipovitola',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(VitolaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_vitola_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Vitola',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('diametro', css_class='form-group col-md-3 mb-0'),
                        Column('longitud', css_class='form-group col-md-3 mb-0'),
                        Column('destino', css_class='form-group col-md-3 mb-0'),
                        Column('cepo', css_class='form-group col-md-4 mb-3'),
                        Column('categoriavitola', css_class='form-group col-md-4 mb-0'),
                        Column('producto', css_class='form-group col-md-4 mb-0'),
                        Column('tipovitola', css_class='form-group col-md-4 mb-0'),
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


# ------------ MarcaSalida / Form ------------
class MarcaSalidaForm(forms.ModelForm):
    class Meta:
        model = MarcaSalida
        fields = [
            'codigo',
            'descripcion',
            'activa',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MarcaSalidaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_marcasalida_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False


        self.fields["codigo"].disabled = True
        self.fields["descripcion"].disabled = True

        self.fields["codigo"].required = False
        self.fields["descripcion"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Marca Salida',
                    Row(
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('activa', css_class='form-group col-md-4 mb-0'),
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


# ------------ MarcaSalida / Form Filter ------------
class MarcaSalidaFormFilter(forms.Form):
    class Meta:
        model = MarcaSalida
        fields = [
            'codigo',
            'descripcion',
            'activa',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MarcaSalidaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_marcasalida_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Marca Salida',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
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


# ------------- Departamento / Form --------------

class DepartamentoForm(forms.ModelForm):
    class Meta:
        model = Departamento
        fields = [
            'codigo',
            'descripcion',
            'centrocosto',
            'unidadcontable',
            'relaciondepartamento',
            'departamentoproducto'
        ]

        widgets = {
            'idcentrocosto': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'unidadcontable': forms.CheckboxSelectMultiple(),
            'relaciondepartamento': forms.CheckboxSelectMultiple(),
            'departamentoproducto': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(DepartamentoForm, self).__init__(*args, **kwargs)
        self.fields['relaciondepartamento'] = forms.ModelMultipleChoiceField(
            queryset=Departamento.objects.exclude(id=instance.id),
            widget=forms.CheckboxSelectMultiple
        )
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_departamento_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Departamento',
                    Row(
                        Column('codigo', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-5 mb-0'),
                        Column('centrocosto', css_class='form-group col-md-4 mb-0'),
                        Column(
                            Field(
                                'unidadcontable',
                                template='widgets/layout/field.html'
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),
                        Column(
                            Field(
                                'relaciondepartamento',
                                template='widgets/layout/field.html'
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),
                        Column(
                            Field(
                                'departamentoproducto',
                                template='widgets/layout/field.html'
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),
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


class DepartamentoFormFilter(forms.Form):
    class Meta:
        model = Departamento
        fields = [
            'codigo',
            'descripcion',
            'centrocosto',
            'unidadcontable',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(DepartamentoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_departamento_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    '1',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-8 mb-0'
                        ),
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-12 mb-0'),
                        Column('centrocosto', css_class='form-group col-md-12 mb-0'),

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
