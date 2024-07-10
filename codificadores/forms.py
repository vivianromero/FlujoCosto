from datetime import date

from crispy_forms.bootstrap import (
    TabHolder,
    Tab, AppendedText, FormActions, UneditableField, )
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Field, HTML, Div
from django import forms
from django.db.models import Q
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from app_index.widgets import MyCustomDateRangeWidget
from codificadores.models import *
from cruds_adminlte3.utils import (
    common_filter_form_actions, )
from cruds_adminlte3.widgets import SelectWidget
from . import ChoiceTiposProd, ChoiceClasesMatPrima
from utiles.utils import obtener_numero_fila


class UpperField(forms.CharField):
    def to_python(self, value):
        return value.upper()


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


# ------------ Unidad Contable / Detail Form ------------
class UnidadContableDetailForm(UnidadContableForm):

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(UnidadContableDetailForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_unidadcontable_detail_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'UEB',
                    Row(
                        Column(UneditableField('codigo'), css_class='form-group col-md-2 mb-0'),
                        Column(UneditableField('nombre'), css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column(UneditableField('activo'), css_class='form-group col-md-2 mb-0'),
                        Column(UneditableField('is_empresa'), css_class='form-group col-md-2 mb-0'),
                        Column(UneditableField('is_comercializadora'), css_class='form-group col-md-2 mb-0'),

                        css_class='form-row'
                    ),
                ),

            ),
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

    precio_lop = forms.DecimalField(
        min_value=0.0000,
        max_digits=10,
        decimal_places=4,
        label="",
        required=False,
    )

    rendimientocapa = forms.IntegerField(
        min_value=0,
        label="",
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
            'precio_lop',
            'rendimientocapa',
            'vitolas',
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
                attrs={'style': 'width: 100%',
                       }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        kwargs['initial'] = {'precio_lop': 0.0000}
        if instance and instance.tipoproducto.pk == ChoiceTiposProd.MATERIAPRIMA:
            kwargs['initial'] = {'clase': instance.get_clasemateriaprima, 'precio_lop': instance.precio_lop}
        super(ProductoFlujoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_add_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        queryset_tipos = TipoProducto.objects.filter(pk__in=[ChoiceTiposProd.MATERIAPRIMA,
                                                             ChoiceTiposProd.HABILITACIONES,
                                                             ChoiceTiposProd.SUBPRODUCTO])
        self.fields['tipoproducto'] = forms.ModelChoiceField(
            queryset=queryset_tipos,
            label='Tipo de Producto')

        self.fields['tipoproducto'].widget.attrs = {
            'style': 'width: 100%',
            'hx-get': reverse_lazy('app_index:codificadores:classmatprima'),
            'hx-target': '#prec_id',
            'hx-trigger': 'load, change',
            'hx-include': '[name="clase"]',  # Incluido para obtener el 'id' del clase seleccionado en el GET
        }

        self.fields["clase"].widget.attrs = {
            "style": 'display:none',
            'hx-get': reverse_lazy('app_index:codificadores:rendimientocapa'),
            'hx-target': '#rd_id',
            'hx-trigger': 'load, change',
            'hx-include': '[name="rendimientocapa"], [name="vitolas"]',
        }
        self.fields[
            "clase"].label = ""
        self.fields["clase"].required = False

        self.fields["precio_lop"].widget.attrs = {"min": 0.0000, "step": 0.0001,
                                                  "style": 'display:none'
                                                  }
        self.fields[
            "precio_lop"].label = ""

        self.fields["rendimientocapa"].widget.attrs = {"min": 0, "step": 1,
                                                       "style": 'display:none'
                                                       }
        self.fields["rendimientocapa"].label = ""

        self.fields["vitolas"].widget.attrs = {"style": 'display:none'}
        self.fields["vitolas"].label = ""
        self.fields["vitolas"].required = False

        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='form-group col-md-2 mb-0'),
                Column('descripcion', css_class='form-group col-md-6 mb-0'),
                Column('medida', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'),
            Row(
                Column('tipoproducto', css_class='form-group col-md-2 mb-0'),
                Div(Column('clase', css_class='form-group col-md-2 mb-0'),
                    Column('precio_lop', css_class='form-group col-md-2 mb-0'),
                    css_class='form-row', css_id='prec_id'
                    ),
                Div(
                    Column('rendimientocapa', css_class='form-group col-md-2 mb-0'),
                    Column('vitolas', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row', css_id='rd_id'
                ),
                css_class='form-row'),
            Row(
                Column('activo', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),

        )
        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_form_actions.html').template.source
                )
            )
        )

    def save(self, commit=True):
        with transaction.atomic():
            instance = super().save(commit=True)
            clase = self.cleaned_data.get('clase')
            if clase:
                producto_flujo_clase = ProductoFlujoClase.objects.create(
                    clasemateriaprima=clase,
                    producto=instance
                )
                if commit:
                    producto_flujo_clase.save()
        return instance


# ------------ ProductoFlujo / Update Form ------------
class ProductoFlujoUpdateForm(forms.ModelForm):
    clase = forms.ModelChoiceField(
        queryset=ClaseMateriaPrima.objects.exclude(pk=ChoiceClasesMatPrima.CAPACLASIFICADA),
        label="",
        required=False,
    )

    precio_lop = forms.DecimalField(
        min_value=0.0000,
        max_digits=10,
        decimal_places=4,
        label="",
        required=False,
    )

    rendimientocapa = forms.IntegerField(
        min_value=0,
        label="",
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
            'precio_lop',
            'rendimientocapa',
            'vitolas',
        ]

        widgets = {
            'codigo': forms.TextInput(
                attrs={
                    'readonly': True,
                },
            ),
            'tipoproducto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                }
            ),
            'medida': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),

            'clase': SelectWidget(
                attrs={'style': 'width: 100%',
                       }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        kwargs['initial'] = {'precio_lop': 0.00, 'rendimientocapa': 0}
        if instance and instance.tipoproducto.pk == ChoiceTiposProd.MATERIAPRIMA:
            kwargs['initial'] = {'clase': instance.get_clasemateriaprima, 'precio_lop': instance.precio_lop,
                                 'rendimientocapa': instance.rendimientocapa}
        super(ProductoFlujoUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_productoflujo_update_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["tipoproducto"].disabled = True
        self.fields["tipoproducto"].required = False

        self.fields["clase"].widget.attrs = {
            "style": 'display:none' if instance.tipoproducto.pk != ChoiceTiposProd.MATERIAPRIMA else 'dispay',
            'hx-get': reverse_lazy('app_index:codificadores:rendimientocapa'),
            'hx-target': '#rd_id',
            'hx-trigger': 'load, change',
            'hx-include': "[name='codigo'], [name='rendimientocapa'], [name='rendimientocapa']",
        }

        self.fields[
            "clase"].label = "" if instance.tipoproducto.pk != ChoiceTiposProd.MATERIAPRIMA else 'Clase Mat. Prima'
        self.fields["clase"].required = instance.tipoproducto.pk == ChoiceTiposProd.MATERIAPRIMA

        self.fields["precio_lop"].widget.attrs = {"min": 0.0000, "step": 0.0001,
                                                  "style": 'display:none' if instance.tipoproducto.pk != ChoiceTiposProd.MATERIAPRIMA else 'dispay'}
        self.fields[
            "precio_lop"].label = "" if instance.tipoproducto.pk != ChoiceTiposProd.MATERIAPRIMA else 'Precio LOP'

        clamapprima = instance.get_clasemateriaprima
        self.fields["rendimientocapa"].widget.attrs = {"min": 0, "step": 1,
                                                       "style": 'display:none' if not clamapprima or clamapprima.pk != ChoiceClasesMatPrima.CAPASINCLASIFICAR else 'dispay'}
        self.fields[
            "rendimientocapa"].label = "" if not clamapprima or clamapprima.pk != ChoiceClasesMatPrima.CAPASINCLASIFICAR else 'Rendimiento x Millar'
        self.fields["rendimientocapa"].required = False

        self.fields["vitolas"].widget.attrs = {
            "style": 'display:none' if not clamapprima or clamapprima.pk != ChoiceClasesMatPrima.CAPASINCLASIFICAR else 'dispay'}
        self.fields[
            "vitolas"].label = "" if not clamapprima or clamapprima.pk != ChoiceClasesMatPrima.CAPASINCLASIFICAR else 'Vitolas'
        self.fields["vitolas"].required = False

        self.helper.layout = Layout(
            Row(
                Column('codigo', css_class='form-group col-md-2 mb-0'),
                Column('descripcion', css_class='form-group col-md-6 mb-0'),
                Column('medida', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'),
            Row(
                Column('tipoproducto', css_class='form-group col-md-2 mb-0'),
                Column('clase', css_class='form-group col-md-2 mb-0'),
                Column('precio_lop', css_class='form-group col-md-2 mb-0'),
                Div(Column('rendimientocapa', css_class='form-group col-md-6 mb-0'),
                    Column('vitolas', css_class='form-group col-md-4 mb-0'),
                    css_class='form-row col-md-6', css_id='rd_id'
                    ),
                css_class='form-row'),
            Row(
                Column('activo', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_form_actions.html').template.source
                )
            )
        )

    def save(self, commit=True):
        with transaction.atomic():
            instance = super().save(commit=True)
            clase = self.cleaned_data.get('clase')
            rendimientocapa = self.cleaned_data.get('rendimientocapa') if clase and int(
                clase.pk) == ChoiceClasesMatPrima.CAPASINCLASIFICAR else 0.00
            precio_lop = self.cleaned_data.get('precio_lop')
            instance.rendimientocapa = rendimientocapa
            instance.save()
            if clase:
                producto_flujo_clase = ProductoFlujoClase.objects.update_or_create(producto=instance,
                                                                                   defaults={
                                                                                       'clasemateriaprima': clase,
                                                                                   })
            else:
                ProductoFlujoClase.objects.filter(producto=instance).delete()

        return instance


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
            'departamentoproductoentrada',
            'departamentoproductosalida'
        ]

        widgets = {
            'centrocosto': SelectWidget(
                attrs={'style': 'width: 100%'},
            ),
            'unidadcontable': forms.CheckboxSelectMultiple(),
            'relaciondepartamento': forms.CheckboxSelectMultiple(),
            'departamentoproductoentrada': forms.CheckboxSelectMultiple(),
            'departamentoproductosalida': forms.CheckboxSelectMultiple(),
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
                                'departamentoproductoentrada',
                                template='widgets/layout/field.html'
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),
                        Column(
                            Field(
                                'departamentoproductosalida',
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

        self.fields['relaciondepartamento'] = forms.ModelMultipleChoiceField(label="Relación Departamentos",
                                                                             queryset=Departamento.objects.exclude(
                                                                                 id=instance.id) if instance else Departamento.objects.all(),
                                                                             widget=forms.CheckboxSelectMultiple
                                                                             )
        queryset_uc = UnidadContable.objects.filter(activo=True, is_empresa=False, is_comercializadora=False)
        self.fields['unidadcontable'] = forms.ModelMultipleChoiceField(label="UEB",
                                                                       queryset=queryset_uc if not instance else (
                                                                               queryset_uc | Departamento.objects.get(
                                                                           pk=instance.pk).unidadcontable.filter(
                                                                           activo=False)).distinct(),
                                                                       widget=forms.CheckboxSelectMultiple
                                                                       )
        queryset_cc = CentroCosto.objects.filter(activo=True).all()
        self.fields['centrocosto'] = forms.ModelChoiceField(label='Centro de Costo',
                                                            queryset=queryset_cc if not instance else queryset_cc | CentroCosto.objects.filter(
                                                                pk=instance.centrocosto.pk, activo=False))
        self.fields["relaciondepartamento"].required = False

    def clean(self):
        cleaned_data = super().clean()
        unidades = cleaned_data.get('unidadcontable')
        if not unidades:
            msg = _('Debe seleccionar al menos una UEB')
            self.add_error('unidadcontable', msg)
        return cleaned_data


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

    def get_context(self):
        context = super().get_context()
        context['width_right_sidebar'] = '760px'
        context['height_right_sidebar'] = '505px'
        return context


# ------------ NormaConsumo / Form ------------
class NormaConsumoForm(forms.ModelForm):
    medida = forms.ModelChoiceField(
        queryset=Medida.objects.all(),
        label=_("Medida"),
        required=False,
    )

    fecha = forms.DateField(
        widget=MyCustomDateRangeWidget(
            format='%d/%m/%Y',
            picker_options={
                'showDropdowns': True,
                'format': 'DD/MM/YYYY',
                'singleDatePicker': True,
                'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
            },
        ),
        input_formats=['%d/%m/%Y'],
    )

    class Meta:
        model = NormaConsumo
        fields = [
            'cantidad',
            'fecha',
            'medida',
            'producto',
        ]

        widgets = {
            'producto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                    'hx-get': reverse_lazy('app_index:codificadores:productmedida'),
                    'hx-target': '#div_id_medida',
                    'hx-trigger': 'change',
                }
            ),
            'medida': SelectWidget(
                attrs={'style': 'width: 100%'}
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        data = kwargs.get('data', None)
        self.user = kwargs.pop('user', None)
        self.producto = kwargs.pop('producto', None)
        self.post = kwargs.pop('post', None)
        producto = ProductoFlujo.objects.get(codigo=self.producto.split('|')[0].strip()) if self.producto else None
        if producto:
            kwargs['initial'] = {'producto': producto, 'medida': producto.medida}
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumo_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["producto"].required = True
        self.fields["medida"].required = True

        if instance:
            self.fields['producto'].widget.enabled_choices = [instance.producto]
            self.fields['medida'].widget.enabled_choices = [instance.medida]

        elif data:
            self.fields['producto'].widget.enabled_choices = [data['producto']]
            self.fields['medida'].widget.enabled_choices = [data['medida']]

        elif self.producto:
            self.fields['producto'].widget.enabled_choices = [producto]
            self.fields['medida'].widget.enabled_choices = [kwargs['initial']['medida']]

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('fecha', id='id_fecha_normaconsumo', ),
                    css_class='form-group col-md-2 mb-0'
                ),
                Column('producto', css_class='form-group col-md-4 mb-0'),
                Column('medida', css_class='form-group col-md-2 mb-0'),
                Column('cantidad', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
        )
        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_form_actions.html').template.source
                )
            )
        )

    def clean_cantidad(self):  # Validar que que la cantidad>0
        cantidad = self.cleaned_data.get('cantidad')
        if float(cantidad) <= 0:
            raise forms.ValidationError('Debe introducir un valor > 0')
        return cantidad

    def save(self, commit=True):

        medida = self.cleaned_data.get('medida')
        self.instance.medida = medida
        instance = super().save(commit=True)
        return instance


# ------------ NormaConsumo / Form ------------
class NormaConsumoDetailForm(NormaConsumoForm):
    class Meta:
        model = NormaConsumo
        fields = [
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
        self.helper.form_id = 'id_normaconsumo_detail_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.fields['activa'].disabled = True
        self.helper.layout = Layout(
            Row(
                Column(UneditableField('fecha'), css_class='form-group col-md-2 mb-0'),
                Column(UneditableField('producto'), css_class='form-group col-md-4 mb-0'),
                Column(UneditableField('medida'), css_class='form-group col-md-2 mb-0'),
                Column(UneditableField('cantidad'), css_class='form-group col-md-2 mb-0'),
                Column('activa', css_class='form-group col align-self-end col-md-2 mb-0'),
                css_class='form-row'
            ),
        )


# ------------ NormaConsumo / Form Filter ------------
class NormaConsumoFormFilter(forms.Form):
    class Meta:
        model = NormaConsumo
        fields = [
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
                        Column('fecha', css_class='form-group col-md-3 mb-0'),
                        Column('cantidad', css_class='form-group col-md-3 mb-0'),
                        Column('activa', css_class='form-group col-md-3 mb-0'),
                        css_class='form-row',
                    ),
                ),
                style="padding-left: 0px; padding-right: 0px; padding-top: 5px; padding-bottom: 0px;",
            ),
        )

        self.helper.layout.append(
            FormActions(
                HTML(
                    get_template('cruds/actions/hx_common_filter_form_actions_normaconsumo.html').template.source
                )
            )
        )

    def get_context(self):
        context = super().get_context()
        if 'tipo' in context['form'].data and int(context['form'].data['tipo']) != 0:
            self.fields['tipo'].disabled = True
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
            'operativo': forms.CheckboxInput(
                attrs={'style': 'width: inherit;'}
            ),

            'producto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                    'id': 'id_productodetalle',
                    "onChange": 'productoMedida()',
                }
            ),
            'medida': SelectWidget(
                attrs={
                    'style': 'width: 100%; dislay: block',
                    'id': 'id_medidadetalle',
                },
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumodetalle_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('producto', css_class='form-group col-md-8 mb-0', css_id='productodetalle'),
                Column('medida', css_class='form-group col-md-4 mb-0', css_id='medidadetalle'),
                css_class='form-row'
            ),
            Row(Column('norma_ramal', css_class='form-group col-md-4 mb-0'),
                Column('norma_empresarial', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'),
            Row(
                Column('operativo', css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
        )

    def clean_norma_ramal(self):  # Validar que que la cantidad>0
        norma_ramal = self.cleaned_data.get('norma_ramal')
        if float(norma_ramal) <= 0:
            raise forms.ValidationError('Debe introducir un valor>0')
        return norma_ramal

    def clean_norma_empresarial(self):  # Validar que que la cantidad>0
        norma_empresarial = self.cleaned_data.get('norma_empresarial')
        if float(norma_empresarial) <= 0:
            raise forms.ValidationError('Debe introducir un valor>0')
        return norma_empresarial

    def save(self, commit=True):
        instance = super().save(commit=False)
        return instance


class NormaConsumoDetalleDetailForm(NormaConsumoDetalleForm):

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_normaconsumodetall_detail_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(UneditableField('producto'), css_class='form-group col-md-8 mb-0', css_id='productodetalle'),
                Column(UneditableField('medida'), css_class='form-group col-md-4 mb-0', css_id='medidadetalle'),
                css_class='form-row'
            ),
            Row(Column(UneditableField('norma_ramal'), css_class='form-group col-md-4 mb-0'),
                Column(UneditableField('norma_empresarial'), css_class='form-group col-md-4 mb-0'),
                css_class='form-row'),
            Row(
                Column(UneditableField('operativo'), css_class='form-group col-md-2 mb-0'),
                css_class='form-row'
            ),
        )


class NormaConsumoGroupedFormFilter(forms.Form):
    class Meta:
        model = NormaConsumoGrouped
        fields = [
            'tipo',
            'cantidad',
            'activa',
            'fecha',
            'medida',
            'producto',
            'Producto',
            'Cantidad_Normas',
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
        self.helper.form_tag = False

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Normas de Consumo Agrupadas',
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
                        Column('Cantidad_Normas', css_class='form-group col-md-4 mb-0'),
                        Column('Producto', css_class='form-group col-md-8 mb-0'),
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
                    'Introduzca los datos a obtener',
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
                        Column('envase', css_class='form-group col-md-2 mb-0'),
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
    tiponum = forms.CharField(max_length=50, label=_("Tipo Numero"), required=False)
    prefijo = forms.CheckboxInput()

    class Meta:
        model = NumeracionDocumentos
        fields = [
            'sistema',
            'departamento',
            'prefijo'
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        kwargs['initial'] = {
            'tiponum': TipoNumeroDoc.NUMERO_CONSECUTIVO.label if TipoNumeroDoc.NUMERO_CONSECUTIVO == instance.pk else TipoNumeroDoc.NUMERO_CONTROL.label}
        super(NumeracionDocumentosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_numeraciondocumentosform_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["tiponum"].disabled = True
        self.fields["tiponum"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Numeración de los documentos'),
                    Row(
                        Column('tiponum', css_class='form-group col-md-5 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('sistema', css_class='form-group col-md-5 mb-0'),
                        Column('departamento', css_class='form-group col-md-5 mb-0'),
                        Field('prefijo', type='hidden' if instance.pk == TipoNumeroDoc.NUMERO_CONSECUTIVO else ''),
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


class ConfCentrosElementosOtrosDetalleFormFilter(forms.Form):
    class Meta:
        model = ConfCentrosElementosOtrosDetalle
        fields = [
            'valor',
            'descripcion',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_confcentroselementosotrosdetalle_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Configurar Centros y Elementos',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                    ),
                    Row(
                        Column('descripcion', css_class='form-group col-md-4 mb-0'),
                        Column('valor', css_class='form-group col-md-4 mb-0'),
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


class ConfCentrosElementosOtrosDetalleGroupedFormFilter(forms.Form):
    class Meta:
        model = ConfCentrosElementosOtrosDetalleGrouped
        fields = [
            'clave',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_confcentroselementosotrosdetallegrouped_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Configuración Elementos y Centros',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Column('clave', css_class='form-group col-md-4 mb-0'),
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


# ------------ ConfCentrosElementosOtrosDetalle / Form ------------
class ConfCentrosElementosOtrosDetalleForm(forms.ModelForm):
    class Meta:
        model = ConfCentrosElementosOtrosDetalle
        fields = [
            'descripcion',
            'valor',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ConfCentrosElementosOtrosDetalleForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_confCentroselementosotrosfetalleform_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["descripcion"].disabled = True
        self.fields["descripcion"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    _('Configuración Centros y Elementos'),
                    Row(
                        Column('descripcion', css_class='form-group col-md-5 mb-0'),
                        Column('valor', css_class='form-group col-md-5 mb-0'),
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

    def clean(self):
        cleaned_data = super().clean()
        valor = cleaned_data.get('valor')
        valor = valor.strip() if valor else valor
        if valor and len(valor) > 0:
            elem = ConfCentrosElementosOtrosDetalle.objects.filter(clave=self.instance.clave,
                                                                   valor=valor)

            if elem and elem.first() != self.instance:
                msg = _('Valor existente')
                self.add_error('valor', msg)

        return cleaned_data


# ------------ TipoDocumento / Form ------------
class TipoDocumentoForm(forms.ModelForm):
    prefijo = UpperField()

    class Meta:
        model = TipoDocumento
        fields = [
            'descripcion',
            'operacion',
            'generado',
            'prefijo',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(TipoDocumentoForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_tipodocumento_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["descripcion"].disabled = True
        self.fields["operacion"].disabled = True
        self.fields["generado"].disabled = True

        self.fields["descripcion"].required = False
        self.fields["operacion"].required = False
        self.fields["generado"].required = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Tipo de Documento',
                    Row(
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('operacion', css_class='form-group col-md-2 mb-0'),
                        Column('prefijo', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('generado', css_class='form-group col-md-2 mb-0'),
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


# ------------- ClasificadorCargos / Form --------------
class ClasificadorCargosForm(forms.ModelForm):
    class Meta:
        model = ClasificadorCargos
        fields = [
            'codigo',
            'descripcion',
            'grupo',
            'actividad',
            'vinculo_produccion',
            'nr_media',
            'norma_tiempo',
            'activo',
            'unidadcontable'
        ]

        widgets = {
            'actividad': SelectWidget(
                attrs={'style': 'width: 100%',

                       }
            ),
            'grupo': SelectWidget(
                attrs={'style': 'width: 100%',
                       }
            ),
            'vinculo_produccion': SelectWidget(
                attrs={'style': 'width: 100%',
                       'hx-get': reverse_lazy('app_index:codificadores:cargonorma'),
                       'hx-target': '#nr_id',
                       'hx-trigger': 'load, change',
                       'hx-include': '[name="nr_media"], [name="norma_tiempo"]'
                       }
            ),
            'unidadcontable': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ClasificadorCargosForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'id_clacargos_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["nr_media"].widget.attrs = {"min": 0, "step": 1,
                                                'hx-get': reverse_lazy('app_index:codificadores:calcula_nt'),
                                                'hx-target': '#nr_id',
                                                'hx-trigger': 'change',
                                                'hx-include': '[name="norma_tiempo"]'
                                                }

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Clasificador de Cargos',
                    Row(
                        Column('codigo', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-5 mb-0'),
                        Column('grupo', css_class='form-group col-md-2 mb-0'),
                        Column('actividad', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('vinculo_produccion', css_class='form-group col-md-2 mb-0'),
                        Div(Column('nr_media', css_class='form-group col-md-4 mb-0'),
                            Column('norma_tiempo', css_class='form-group col-md-6 mb-0'),
                            css_class='form-row', css_id='nr_id'
                            ),
                        css_class='form-row'
                    ),
                    Row(
                        Column(
                            Field(
                                'unidadcontable',
                                template='widgets/layout/field.html'
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),
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

        queryset_uc = UnidadContable.objects.filter(activo=True)
        query = queryset_uc if not instance else (
                queryset_uc | ClasificadorCargos.objects.get(pk=instance.pk).unidadcontable.filter(
            activo=False)).distinct()

        self.fields['unidadcontable'] = forms.ModelMultipleChoiceField(
            label="UEB",
            queryset=query,
            widget=forms.CheckboxSelectMultiple
        )

    def clean(self):
        cleaned_data = super().clean()
        unidades = cleaned_data.get('unidadcontable')
        if not unidades:
            msg = _('Debe seleccionar al menos una UEB')
            self.add_error('unidadcontable', msg)
        return cleaned_data


class ClasificadorCargosFormFilter(forms.Form):
    unidadcontable = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        label='Choose your options'
    )

    class Meta:
        model = ClasificadorCargos
        fields = [
            'codigo',
            'descripcion',
            'grupo',
            'actividad',
            'unidadcontable',
            'grupo__salario',
            'vinculo_produccion',
            'activo',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ClasificadorCargosFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_clacargos_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Cargos',
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
                        Column('codigo', css_class='form-group col-md-2 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('grupo', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('actividad', css_class='form-group col-md-4 mb-0'),
                        Column('unidadcontable', css_class='form-group col-md-8 mb-0'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('grupo__salario', css_class='form-group col-md-8 mb-0'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('vinculo_produccion', css_class='form-group col-md-3 mb-0'),
                        Column('activo', css_class='form-group col-md-3 mb-0'),
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


# ------------- FichaCostoFilas / Form --------------
class FichaCostoFilasForm(forms.ModelForm):
    class Meta:
        model = FichaCostoFilas
        fields = [
            'fila',
            'descripcion',
            'encabezado',
            'salario',
            'vacaciones',
            'desglosado',
            'calculado',
            'filasasumar',
            'padre',
        ]

        widgets = {
            'fila': forms.TextInput(
                attrs={
                    'readonly': True,
                },
            ),
            'padre': forms.HiddenInput(),
            'encabezado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 100%',
                    'hx-get': reverse_lazy('app_index:codificadores:fila_encabezado'),
                    'hx-target': '#id_filaencab',
                    'hx-trigger': 'load, change',
                    'hx-include': '[name="calculado"], [name="fila"]',
                }
            ),
            'desglosado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 100%',
                    'hx-get': reverse_lazy('app_index:codificadores:fila_desglosado'),
                    'hx-target': '#id_filadesg',
                    'hx-trigger': 'load, change',
                    'hx-include': '[name="fila"], [name="encabezado"]',
                    # Incluido para obtener el 'id' del clase seleccionado en el GET
                }
            ),
            'calculado': forms.CheckboxInput(
                attrs={
                    'style': 'width: 100%',
                    'hx-get': reverse_lazy('app_index:codificadores:fila_calculado'),
                    'hx-target': '#id_filacalc',
                    'hx-trigger': 'load, change',
                    'hx-include': '[name="fila"], [name="encabezado"]',
                }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        self.padre = kwargs.pop('padre', None)
        kwargs['initial'] = {'fila': instance.fila if instance else obtener_numero_fila(self.padre),
                             'encabezado': instance.encabezado if instance else True if not self.padre else False,
                             'padre': self.padre}
        super(FichaCostoFilasForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_id = 'id_filasficha_Form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.fields["encabezado"].widget.attrs['disabled'] = not self.padre
        self.fields["encabezado"].widget.attrs[
            'hx-vals'] = '{"padre": "' + self.padre + '"}' if self.padre else '{"padre": "0"}'

        self.fields["descripcion"].widget.attrs['readonly'] = True if instance and instance.fila in ['1', '1.1',
                                                                                                     '1.2'] else False
        self.fields["desglosado"].widget.attrs['disabled'] = True if instance and instance.fila in ['1', '1.1',
                                                                                                    '1.2'] else False
        self.fields["desglosado"].widget.attrs[
            'hx-vals'] = '{"padre": "' + self.padre + '"}' if self.padre else '{"padre": "0"}'
        self.fields["filasasumar"].required = False

        self.fields["calculado"].widget.attrs[
            'hx-vals'] = '{"padre": "' + self.padre + '"}' if self.padre else '{"padre": "0"}'

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Filas de la Ficha de Costo',
                    Row(
                        Column('fila', css_class='form-group col-md-3 mb-0'),
                        Column('descripcion', css_class='form-group col-md-5 mb-0'),
                        css_class='form-row'
                    ),
                    Row(
                        Column('encabezado', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row',
                    ),
                    Div(
                        Column('desglosado', css_class='form-group col-md-2 mb-0'),
                        Column('calculado', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row', css_id='id_filaencab'
                    ),
                    Div(
                        Column('filasasumar', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row', css_id='id_filacalc'
                    ),
                    Div(
                        Column('salario', css_class='form-group col-md-2 mb-0'),
                        Column('vacaciones', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row', css_id='id_filadesg'
                    ),
                    Row(
                        Column('padre', css_class='form-group col-md-2 mb-0'),
                        css_class='form-row',
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
            padre = self.cleaned_data.get("padre")
            obj_padre = None
            if padre:
                obj_padre = FichaCostoFilas.objects.get(pk=padre)
            self.instance.parent = obj_padre
            self.instance.padre = None
            self.instance.encabezado = True if self.cleaned_data.get("encabezado") == True else padre == None
            instance = super().save(*args, **kwargs)
        return instance


class FichaCostoFilasFormFilter(forms.Form):
    class Meta:
        model = FichaCostoFilas
        fields = [
            'descripcion',
            'salario',
            'vacaciones',
            'desglosado',
            'calculado',
            'filasasumar'
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(FichaCostoFilasFormFilter, self).__init__(*args, **kwargs)
        self.fields['query'].widget.attrs = {"placeholder": _("Search...")}
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_filasficha_form_filter'
        self.helper.form_method = 'GET'

        self.helper.layout = Layout(

            TabHolder(
                Tab(
                    'Filas Ficha de Costo',
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
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        Column('descripcion', css_class='form-group col-md-6 mb-0'),
                        css_class='form-row',
                    ),
                    Row(
                        Column('encabezado', css_class='form-group col-md-2 mb-0'),
                        Column('desglosado', css_class='form-group col-md-2 mb-0'),
                        Column('calculado', css_class='form-group col-md-2 mb-0'),
                        Column('filasasumar', css_class='form-group col-md-2 mb-0'),
                        Column('salario', css_class='form-group col-md-2 mb-0'),
                        Column('vacaciones', css_class='form-group col-md-2 mb-0'),
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
        context['width_right_sidebar'] = '760px'
        context['height_right_sidebar'] = '505px'
        return context
