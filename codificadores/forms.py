from crispy_forms.bootstrap import (
    TabHolder,
    Tab, AppendedText, FormActions, )
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML
from django import forms
from django.db import transaction
from django.template.loader import get_template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from codificadores.models import *
from cruds_adminlte3.utils import (
    common_filter_form_actions, )
from cruds_adminlte3.widgets import SelectWidget
from . import ChoiceTiposProd, ChoiceClasesMatPrima
from django.urls import reverse_lazy


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
                        Column('activo', css_class='form-group col-md-2 mb-0'),
                        Column('is_empresa', css_class='form-group col-md-2 mb-0'),
                        Column('is_comercializadora', css_class='form-group col-md-2 mb-0'),

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


# ------------ MedidaConversion / Form ------------

class MedidaConversionForm(forms.ModelForm):
    class Meta:
        model = MedidaConversion
        fields = [
            'medidao',
            'medidad',
            'factor_conversion'
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MedidaConversionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_medidaconversion_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        queryset_um = Medida.objects.filter(activa=True)
        self.fields['medidao'] = forms.ModelChoiceField(
            queryset=queryset_um if not instance else queryset_um | Medida.objects.filter(
                pk=instance.medidao.pk, activa=False),
            label='Medida Origen')

        self.fields['medidad'] = forms.ModelChoiceField(
            queryset=queryset_um if not instance else queryset_um | Medida.objects.filter(
                pk=instance.medidad.pk, activa=False),
            label='Medida Destino')

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
                        Column('medidao', css_class='form-group col-md-6 mb-0'),
                        Column('medidad', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row',
                    ),
                    Row('factor_conversion', css_class='form-group form-row'),
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
    class Meta:
        model = Cuenta
        fields = [
            'clave',
            'descripcion',
            'activa',
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

        self.fields["clave"].disabled = True
        self.fields["descripcion"].disabled = True

        self.fields["clave"].required = False
        self.fields["descripcion"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Cuenta',
                    Row(
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),

                    Row(Column('activa', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'
                        )
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
                        Column('clave', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
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

        self.fields["clave"].disabled = True
        self.fields["descripcion"].disabled = True

        self.fields["clave"].required = False
        self.fields["descripcion"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    ('Cost center'),
                    Row(
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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
                    _('Cost center'),
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('clave', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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
    clase = forms.ModelChoiceField(
        queryset=ClaseMateriaPrima.objects.exclude(pk=ChoiceClasesMatPrima.CAPACLASIFICADA),
        label=_("Clase Materia Prima"),
        required=False,
    )

    class Meta:
        model = ProductoFlujo
        fields = [
            'codigo',
            'descripcion',
            'activo',
            'medida',
            'tipoproducto',
            'clase',
        ]

        widgets = {
            'tipoproducto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                    'hx-get': reverse_lazy('app_index:codificadores:classmatprima'),
                    'hx-target': '#div_id_clase',
                    'hx-trigger': 'load, change',
                    'hx-include': '[name="clase"]',  # Incluido para obtener el 'id' del clase seleccionado en el GET
                }
            ),
            'medida': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'clase': SelectWidget(
                attrs={'style': 'width: 100%',}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        if instance and instance.tipoproducto.pk == ChoiceTiposProd.MATERIAPRIMA:
            kwargs['initial'] = {'clase': instance.get_clasemateriaprima}
        super(ProductoFlujoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["codigo"].disabled = instance
        self.fields["codigo"].required = not instance
        # self.fields["tipoproducto"].disabled = instance
        # self.fields["tipoproducto"].widget.attrs = {"readonly":True}
        # self.fields["tipoproducto"].required = not instance
        # self.fields["clase"].disabled = instance
        # self.fields["clase"].required = not instance

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Producto Flujo',
                    Row(
                        Column('codigo', css_class='form-group col-md-2 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('medida', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'),
                    Row(
                        Column('tipoproducto', css_class='form-group col-md-2 mb-0'),
                        Column('clase', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'),
                    Row(
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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
                        Column('codigo', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('medida', css_class='form-group col-md-3 mb-0'),
                        Column('tipoproducto', css_class='form-group col-md-6 mb-0'),
                        Column('get_clasemateriaprima', css_class='form-group col-md-6 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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


# ------------ Vitola / Form ------------
class VitolaForm(forms.ModelForm):
    codigo = forms.CharField(max_length=50, required=True, label=_("Code"))
    descripcion = forms.CharField(max_length=400, required=True, label=_("Description"))
    activo = forms.BooleanField(label=_("Active"), initial=True)
    um = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label=_("U.M"),
        required=True,
    )

    class Meta:
        model = Vitola
        fields = [
            'codigo',
            'descripcion',
            'um',
            'diametro',
            'longitud',
            'cepo',
            'categoriavitola',
            'tipovitola',
            'destino',
            'activo',
        ]

        widgets = {
            'categoriavitola': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'tipovitola': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'um': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        kwargs['initial'] = {'activo': True}
        kwargs['initial'] = {'um': Medida.objects.get(clave='Tab')}
        if instance:
            kwargs['initial'] = {'um': instance.producto.medida, 'codigo': instance.producto.codigo,
                                 'descripcion': instance.producto.descripcion, 'activo': instance.producto.activo}
        super(VitolaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_vitola_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["activo"].required = False
        self.fields["codigo"].disabled = True if self.instance.producto_id else False
        self.fields["codigo"].required = False if self.instance.producto_id else True

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Vitola',
                    Row(
                        Column('codigo', css_class='form-group col-md-2 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
                        Column('um', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('destino', css_class='form-group col-md-4 mb-0'),
                        Column('categoriavitola', css_class='form-group col-md-4 mb-0'),
                        Column('tipovitola', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('diametro', css_class='form-group col-md-4 mb-0'),
                        Column('longitud', css_class='form-group col-md-4 mb-0'),
                        Column('cepo', css_class='form-group col-md-4 mb-3'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('activo', css_class='form-group col-md-3 mb-0'),
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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            codigo = self.cleaned_data.get("codigo").strip()
            descripcion = self.cleaned_data.get("descripcion").strip()
            activo = self.cleaned_data.get("activo")

            if self.instance.producto_id:
                producto = ProductoFlujo.objects.get(id=self.instance.producto.id)
                producto.descripcion = descripcion
                producto.medida = self.cleaned_data.get("um")
                producto.activo = activo
                producto.save()
                producto_capa = ProductoFlujo.objects.get(id=self.instance.capa.id)
                producto_capa.descripcion = 'CAPA ' + descripcion
                producto_capa.activo = activo
                producto_capa.save()
                producto_pesada = ProductoFlujo.objects.get(id=self.instance.pesada.id)
                producto_pesada.descripcion = 'PESADA ' + descripcion
                producto_pesada.activo = activo
                producto_pesada.save()
            else:
                producto = ProductoFlujo.objects.create(codigo=codigo,
                                                        descripcion=descripcion,
                                                        medida=self.cleaned_data.get("um"),
                                                        activo=activo,
                                                        tipoproducto=TipoProducto.objects.get(
                                                            id=ChoiceTiposProd.VITOLA))
                medida = Medida.objects.filter(clave='Mh')
                producto_capa = ProductoFlujo.objects.create(codigo='C' + codigo,
                                                             descripcion='CAPA ' + descripcion,
                                                             medida=medida[
                                                                 0] if medida.exists() else Medida.objects.create(
                                                                 clave='Mh', descripcion='Medias Hojas'),
                                                             activo=activo,
                                                             tipoproducto=TipoProducto.objects.get(
                                                                 id=ChoiceTiposProd.MATERIAPRIMA)
                                                             )
                ProductoFlujoClase.objects.create(producto=producto_capa,
                                                  clasemateriaprima=ClaseMateriaPrima.objects.get(
                                                      id=ChoiceClasesMatPrima.CAPACLASIFICADA))

                medida = Medida.objects.filter(clave='U')
                producto_pesada = ProductoFlujo.objects.create(codigo='P' + codigo,
                                                               descripcion='PESADA ' + descripcion,
                                                               medida=medida[
                                                                   0] if medida.exists() else Medida.objects.create(
                                                                   clave='U', descripcion='Uno'),
                                                               activo=activo,
                                                               tipoproducto=TipoProducto.objects.get(
                                                                   id=ChoiceTiposProd.PESADA)
                                                               )

                self.instance.producto_id = producto.id
                self.instance.capa_id = producto_capa.id
                self.instance.pesada_id = producto_pesada.id
            instance = super().save(*args, **kwargs)
        return instance


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
                        Column('producto', css_class='form-group col-md-6 mb-0'),
                        Column('destino', css_class='form-group col-md-6 mb-0'),
                        Column('categoriavitola', css_class='form-group col-md-6 mb-0'),
                        Column('tipovitola', css_class='form-group col-md-6 mb-0'),
                        Column('diametro', css_class='form-group col-md-4 mb-0'),
                        Column('longitud', css_class='form-group col-md-4 mb-0'),
                        Column('cepo', css_class='form-group col-md-4 mb-3'),
                        Column('activo', css_class='form-group col-md-2 mb-3'),
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
    descripcion = forms.CharField(widget=forms.TextInput(attrs={'oninput': 'this.value = this.value.toUpperCase()'}))

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

        self.fields["codigo"].disabled = instance
        self.fields["codigo"].required = not instance

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
                    Row(
                        Column('activa', css_class='form-group col-md-4 mb-0'),
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
            'centrocosto': SelectWidget(
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

        self.fields['relaciondepartamento'] = forms.ModelMultipleChoiceField(
            queryset=Departamento.objects.exclude(id=instance.id) if instance else Departamento.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
        queryset_uc = UnidadContable.objects.filter(activo=True)
        self.fields['unidadcontable'] = forms.ModelMultipleChoiceField(
            queryset=queryset_uc if not instance else queryset_uc | Departamento.objects.get(
                pk=instance.pk).unidadcontable.filter(activo=False),
            widget=forms.CheckboxSelectMultiple
        )
        queryset_cc = CentroCosto.objects.filter(activo=True).all()
        self.fields['centrocosto'] = forms.ModelChoiceField(
            queryset=queryset_cc if not instance else queryset_cc | CentroCosto.objects.filter(
                pk=instance.centrocosto.pk, activo=False))
        self.fields["relaciondepartamento"].required = False


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
                            css_class='form-group col-md-12 mb-0'
                        ),
                        css_class='form-row',
                    ),
                    Row(
                        Column('codigo', css_class='form-group col-md-4 mb-0'),
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('centrocosto', css_class='form-group col-md-12 mb-0'),
                        Column('unidadcontable', css_class='form-group col-md-12 mb-0'),
                        css_class='form-row',
                    ),
                ),
                style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
            ),

        )

        self.helper.layout.append(
            common_filter_form_actions()
        )


# ------------ NormaConsumo / Form ------------
class NormaConsumoForm(forms.ModelForm):
    class Meta:
        model = NormaConsumo
        fields = [
            'tipo',
            'cantidad',
            'activa',
            'fecha',
            'medida',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumo_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Norma de Consumo',
                    Row(
                        Column('tipo', css_class='form-group col-md-4 mb-0'),
                        Column('cantidad', css_class='form-group col-md-4 mb-0'),
                        Column('activa', css_class='form-group col-md-2 mb-0'),
                        Column('fecha', css_class='form-group col-md-4 mb-0'),
                        Column('medida', css_class='form-group col-md-4 mb-0'),
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


# ------------ NormaConsumo / Form Filter ------------
class NormaConsumoFormFilter(forms.Form):
    class Meta:
        model = NormaConsumo
        fields = [
            'tipo',
            'cantidad',
            'activa',
            'fecha',
            'medida',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumo_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Normas de Consumo',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                    ),
                    Row(
                        Column('tipo', css_class='form-group col-md-4 mb-0'),
                        Column('cantidad', css_class='form-group col-md-4 mb-0'),
                        Column('activa', css_class='form-group col-md-2 mb-0'),
                        Column('fecha', css_class='form-group col-md-4 mb-0'),
                        Column('medida', css_class='form-group col-md-4 mb-0'),
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


class NormaConsumoDetalleForm(forms.ModelForm):
    class Meta:
        model = NormaconsumoDetalle
        fields = [
            'norma_ramal',
            'norma_empresarial',
            'operativo',
            'producto',
            'medida',
        ]
        widgets = {
            'producto': SelectWidget(
                attrs={
                    'style': 'width: 100%; dislay: block',
                },
            ),
            'medida': SelectWidget(
                attrs={
                    'style': 'width: 100%; dislay: block',
                },
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        # self.fields['producto'].required = False
        # self.fields['medida'].required = False
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumodetalle_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Dettales Norma de Consumo',
                    Row(

                        Column('norma_ramal', css_class='form-group col-md-4 mb-0'),
                        Column('norma_empresarial', css_class='form-group col-md-4 mb-0'),

                        Column('producto', css_class='form-group col-md-4 mb-0'),

                        Column('operativo', css_class='form-group col-md-4 mb-0'),
                        Column('medida', css_class='form-group col-md-4 mb-0'),

                        css_class='form-row'
                    ),
                ),
            ),
        )
        # self.helper.layout.append(
        #     FormActions(
        #         HTML(
        #             get_template('cruds/actions/hx_common_form_actions.html').template.source
        #         )
        #     )
        # )


class NormaConsumoGroupedFormFilter(NormaConsumoFormFilter):
    class Meta:
        model = NormaConsumoGrouped
        fields = [
            'tipo',
            'cantidad',
            'activa',
            'fecha',
            'medida',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumogrouped_form_filter'
        self.helper.form_method = 'GET'


# ------------ MotivoAjuste / Form ------------
class MotivoAjusteForm(forms.ModelForm):
    class Meta:
        model = MotivoAjuste
        fields = [
            'descripcion',
            'aumento',
            'activo',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MotivoAjusteForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_motivoajuste_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Reason for Adjustment'),
                    Row(
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('aumento', css_class='form-group col-md-2 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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


# ------------ MotivoAjuste / Form Filter ------------
class MotivoAjusteFormFilter(forms.Form):
    class Meta:
        model = MotivoAjuste
        fields = [
            'descripcion',
            'aumento'
            'activo',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(MotivoAjusteFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_motivoajuste_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Reason for Adjustment'),
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('aumento', css_class='form-group col-md-2 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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


# ------------ CambioProducto / Form ------------

class CambioProductoForm(forms.ModelForm):
    class Meta:
        model = CambioProducto
        fields = [
            'productoo',
            'productod',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CambioProductoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_cambioproducto_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        queryset_prod = ProductoFlujo.objects.filter(activo=True)
        self.fields['productoo'] = forms.ModelChoiceField(
            queryset=queryset_prod if not instance else queryset_prod | ProductoFlujo.objects.filter(
                pk=instance.productoo.pk, activo=False),
            label='Producto Origen')

        self.fields['productod'] = forms.ModelChoiceField(
            queryset=queryset_prod if not instance else queryset_prod | ProductoFlujo.objects.filter(
                pk=instance.productod.pk, activo=False),
            label='Producto Destino')

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Cambio de Producto'),
                    Row(
                        Column('productoo', css_class='form-group col-md-5 mb-0'),
                        Column('productod', css_class='form-group col-md-5 mb-0'),

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


# ------------ CambioProducto / Form Filter ------------
class CambioProductoFormFilter(forms.Form):
    class Meta:
        model = CambioProducto
        fields = [
            'productoo',
            'productod',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(CambioProductoFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_cambioproducto_form_filter'
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
                        Column('productoo', css_class='form-group col-md-6 mb-0'),
                        Column('productod', css_class='form-group col-md-6 mb-0'),
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


class ObtenerDatosModalForm(forms.Form):
    valor_inicial = forms.CharField()
    clase_mat_prima = forms.ChoiceField(choices=ChoiceClasesMatPrima.CHOICE_CLASES)

    class Meta:
        fields = [
            'valor_inicial',
            'clase_mat_prima',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ObtenerDatosModalForm, self).__init__(*args, **kwargs)
        self.fields['valor_inicial'].widget.attrs = {"placeholder": _("Initial value to search...")}
        self.fields['clase_mat_prima'].widget.choices.pop(ChoiceClasesMatPrima.CAPACLASIFICADA)
        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_tag = False

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    _('Enter Data to Obtain'),
                    Row(
                        Column('valor_inicial', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('clase_mat_prima', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                ),
            ),
        )


# ------------ LineaSalida / Form ------------
class LineaSalidaForm(forms.ModelForm):
    codigo = forms.CharField(max_length=50, required=True, label=_("Code"))
    descripcion = forms.CharField(max_length=400, required=True, label=_("Description"))
    activo = forms.BooleanField(label=_("Active"), initial=True)
    um = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label=_("U.M"),
        required=True,
    )

    class Meta:
        model = LineaSalida
        fields = [
            'codigo',
            'descripcion',
            'um',
            'envase',
            'vol_cajam3',
            'peso_bruto',
            'peso_neto',
            'peso_legal',
            'marcasalida',
            'vitola',
            'activo'
        ]

        widgets = {
            'marcasalida': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'vitola': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
            'um': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        kwargs['initial'] = {'activo': True}
        if instance:
            kwargs['initial'] = {'um': instance.producto.medida, 'codigo': instance.producto.codigo,
                                 'descripcion': instance.producto.descripcion, 'activo': instance.producto.activo,
                                 'vitola': instance.vitola, 'marcasalida': instance.marcasalida}
        super(LineaSalidaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_lineasalida_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        queryset_vitola = ProductoFlujo.objects.filter(tipoproducto=ChoiceTiposProd.VITOLA, activo=True)
        self.fields['vitola'] = forms.ModelChoiceField(
            queryset=queryset_vitola if not instance else queryset_vitola | ProductoFlujo.objects.filter(
                pk=instance.vitola.pk, activo=False),
            label='Vitola')

        self.fields["activo"].required = False
        self.fields["codigo"].disabled = True if self.instance.producto_id else False
        self.fields["codigo"].required = False if self.instance.producto_id else True

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Línea de Salida',
                    Row(
                        Column('codigo', css_class='form-group col-md-2 mb-0'),
                        Column('descripcion', css_class='form-group col-md-8 mb-0'),
                        Column('um', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('marcasalida', css_class='form-group col-md-6 mb-0'),
                        Column('vitola', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('emvase', css_class='form-group col-md-2 mb-0'),
                        Column('vol_cajam3', css_class='form-group col-md-2 mb-0'),
                        Column('peso_bruto', css_class='form-group col-md-2 mb-0'),
                        Column('peso_neto', css_class='form-group col-md-2 mb-3'),
                        Column('peso_legal', css_class='form-group col-md-2 mb-3'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('activo', css_class='form-group col-md-3 mb-0'),
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

    def save(self, *args, **kwargs):
        with transaction.atomic():
            codigo = self.cleaned_data.get("codigo").strip()
            descripcion = self.cleaned_data.get("descripcion").strip()
            activo = self.cleaned_data.get("activo")

            if self.instance.producto_id:
                producto = ProductoFlujo.objects.get(id=self.instance.producto.id)
                producto.descripcion = descripcion
                producto.medida = self.cleaned_data.get("um")
                producto.activo = activo
                producto.save()
            else:
                producto = ProductoFlujo.objects.create(codigo=codigo,
                                                        descripcion=descripcion,
                                                        medida=self.cleaned_data.get("um"),
                                                        activo=activo,
                                                        tipoproducto=TipoProducto.objects.get(
                                                            id=ChoiceTiposProd.LINEASALIDA))
                self.instance.producto_id = producto.id
            instance = super().save(*args, **kwargs)
        return instance


# ------------ LineaSalida / Form Filter ------------
class LineaSalidaFormFilter(forms.Form):
    class Meta:
        model = LineaSalida
        fields = [
            'envase',
            'vol_cajam3',
            'peso_bruto',
            'peso_neto',
            'peso_legal',
            'producto',
            'marcasalida',
            'vitola',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(LineaSalidaFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_lineasalida_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Línea de Salida',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('producto', css_class='form-group col-md-12 mb-0'),
                        Column('marcasalida', css_class='form-group col-md-6 mb-0'),
                        Column('vitola', css_class='form-group col-md-6 mb-0'),
                        Column('envase', css_class='form-group col-md-2 mb-0'),
                        Column('vol_cajam3', css_class='form-group col-md-2 mb-0'),
                        Column('peso_bruto', css_class='form-group col-md-2 mb-0'),
                        Column('peso_neto', css_class='form-group col-md-3 mb-0'),
                        Column('peso_legal', css_class='form-group col-md-3 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row',

                    ),
                    style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
                ),

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


# ------------ NumeracionDocumentos / Form ------------
class NumeracionDocumentosForm(forms.ModelForm):
    class Meta:
        model = NumeracionDocumentos
        fields = [
            'tiponumeracion',
            'sistema',
            'departamento',
            'tipo_documento',
            'prefijo'
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(NumeracionDocumentosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_numeraciondocumentosform_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["tiponumeracion"].disabled = True
        self.fields["tiponumeracion"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Numeración de los documentos'),
                    Row(
                        Column('tiponumeracion', css_class='form-group col-md-5 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('sistema', css_class='form-group col-md-5 mb-0'),
                        Column('departamento', css_class='form-group col-md-5 mb-0'),
                        Column('tipo_documento', css_class='form-group col-md-5 mb-0'),
                        Column('prefijo', css_class='form-group col-md-5 mb-0'),
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


class ConfCentrosElementosOtrosForm(forms.ModelForm):
    class Meta:
        model = ConfCentrosElementosOtros
        fields = ['clave']

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ConfCentrosElementosOtrosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_confcentroselementosotrosform_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Centros de Costo',
                    Row(
                        Column('valor', css_class='form-group col-md-4 mb-0'),
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

# ------------ ProductsCapasClaPesadas / Form Filter ------------
class ProductsCapasClaPesadasFormFilter(forms.Form):
    class Meta:
        model = ProductsCapasClaPesadas
        fields = [
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
        super(ProductsCapasClaPesadasFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Pesadas y Capas Clasificadas',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('codigo', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('medida', css_class='form-group col-md-3 mb-0'),
                        Column('tipoproducto', css_class='form-group col-md-6 mb-0'),
                        Column('activo', css_class='form-group col-md-2 mb-0'),
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
