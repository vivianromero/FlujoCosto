from datetime import date

from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from django import forms
from django.db import transaction
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from app_index.widgets import MyCustomDateRangeWidget
from cruds_adminlte3.utils import crud_url_name
from cruds_adminlte3.widgets import SelectWidget
from flujo.models import *


# ------------ Documento / Form ------------
class DocumentoForm(forms.ModelForm):
    departamento_destino = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento Destino",
        required=False,
        widget=SelectWidget(attrs={
            'style': 'width: 100%; display: none;',
        }
        )
    )

    class Meta:
        model = Documento
        fields = [
            'fecha',
            'numerocontrol',
            'numeroconsecutivo',
            'suma_importe',
            'observaciones',
            'estado',
            'reproceso',
            'editar_nc',
            'comprob',
            'departamento',
            'tipodocumento',
            'ueb',
            'departamento_destino',
        ]
        widgets = {
            'fecha': MyCustomDateRangeWidget(
                format='%Y-%m-%d',
                picker_options={
                    'format': 'DD/MM/YYYY',
                    'singleDatePicker': True,
                    'maxDate': str(date.today()),  # TODO Fecha no puede ser mayor que la fecha actual
                }
            ),
            'departamento': SelectWidget(
                attrs={
                    'style': 'width: 100%;',
                }
            ),
            'tipodocumento': SelectWidget(
                attrs={
                    'style': 'width: 100%;',
                }
            ),
            'ueb': SelectWidget(
                attrs={
                    'style': 'width: 100%;',
                }
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        data = kwargs.get('data', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        self.departamento = kwargs.pop('departamento', None)
        self.tipo_doc = kwargs.pop('tipo_doc', None)
        self.destino_tipo_documento = [3, ]
        self.destino_tipo_documento_str = ['3', ]
        super(DocumentoForm, self).__init__(*args, **kwargs)
        destino_queryset = self.fields['departamento_destino'].queryset
        self.fields['departamento_destino'].disabled = True
        self.fields['departamento_destino'].label = False
        if self.user:
            self.fields['ueb'].initial = self.user.ueb
            self.fields['ueb'].widget.enabled_choices = [self.user.ueb]
        if instance:
            self.fields['departamento'].widget.enabled_choices = [instance.departamento]
            self.fields['tipodocumento'].widget.enabled_choices = [instance.tipodocumento]
            if instance.tipodocumento.pk in self.destino_tipo_documento:
                destino_queryset = destino_queryset.filter(relaciondepartamento=instance.departamento)
                self.fields['departamento_destino'].queryset = destino_queryset
                destino = DocumentoTransfDepartamento.objects.get(documento=instance)
                self.fields['departamento_destino'].initial = destino.departamento
                self.fields['departamento_destino'].widget.enabled_choices = [destino.departamento]
                self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%; display: block;', }
                self.fields['departamento_destino'].label = "Departamento Destino"
                self.fields['departamento_destino'].disabled = False
                self.fields['departamento_destino'].required = True
        elif data:
            self.fields['departamento'].widget.enabled_choices = [data['departamento']]
            self.fields['tipodocumento'].widget.enabled_choices = [data['tipodocumento']]
            if data['tipodocumento'] in self.destino_tipo_documento_str:
                destino = data.get('departamento_destino')
                self.fields['departamento_destino'].initial = destino
                self.fields['departamento_destino'].disabled = False
                self.fields['departamento_destino'].required = True
        else:
            if self.departamento:
                self.fields['departamento'].initial = self.departamento
                self.fields['departamento'].widget.enabled_choices = [self.departamento]
            if self.tipo_doc:
                print(self.tipo_doc)
                self.fields['tipodocumento'].initial = self.tipo_doc
                self.fields['tipodocumento'].widget.enabled_choices = [self.tipo_doc]
                if self.tipo_doc in self.destino_tipo_documento_str:
                    destino_queryset = destino_queryset.filter(relaciondepartamento=self.departamento)
                    self.fields['departamento_destino'].queryset = destino_queryset
                    self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%; display: block;', }
                    self.fields['departamento_destino'].label = "Departamento Destino"
                    self.fields['departamento_destino'].disabled = False
                    self.fields['departamento_destino'].required = True
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_documento_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column(
                    Field('fecha', id='id_fecha_documento_form', ),
                    css_class='form-group col-md-3 mb-0'
                ),
                # Column('departamento', css_class='form-group col-md-3 mb-0'),
                # Column('tipodocumento', css_class='form-group col-md-3 mb-0'),
                Column('numerocontrol', css_class='form-group col-md-3 mb-0'),

                Column('numeroconsecutivo', css_class='form-group col-md-3 mb-0'),
                # Column('suma_importe', css_class='form-group col-md-3 mb-0'),
                # Column('estado', css_class='form-group col-md-3 mb-0'),
                # Column('comprob', css_class='form-group col-md-1 mb-0'),

                # Column('ueb', css_class='form-group col-md-3 mb-0'),
                # Column('observaciones', css_class='form-group col-md-12 mb-0'),
                # Column('reproceso', css_class='form-group col-md-3 mb-0'),
                # Column('editar_nc', css_class='form-group col-md-3 mb-0'),
                Column('departamento_destino', css_class='form-group col-md-3 mb-0'),
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
            if self.cleaned_data['tipodocumento'].pk in self.destino_tipo_documento:
                departamento_destino = self.cleaned_data.get('departamento_destino')
                if departamento_destino:
                    documento_transf_departamento = DocumentoTransfDepartamento.objects.create(
                        documento=instance,
                        departamento=departamento_destino,
                    )
                    if commit:
                        documento_transf_departamento.save()
        return instance


# ------------ DepartamentosDocumento / Form ------------
class DepartamentoDocumentosForm(DocumentoForm):
    class Meta(DocumentoForm.Meta):
        fields = [
            'departamento',
        ]
        widgets = {
            'departamento': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(DepartamentoDocumentosForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_departamentos_documento_form'
        self.helper.form_method = 'post'
        self.helper.form_show_labels = False

        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('departamento', css_class='form-group col-md-12 mb-0'),
                css_class='form-row'
            ),
        )


# ------------ Documento / Form Filter------------
class DocumentoFormFilter(forms.Form):
    class Meta:
        model = Documento
        fields = [
            'rango_fecha',
            'numerocontrol',
            'numeroconsecutivo',
            'suma_importe',
            'observaciones',
            'estado',
            'reproceso',
            'editar_nc',
            'comprob',
            'departamento',
            'tipodocumento',
            'ueb',
        ]
        widgets = {
            'departamento': forms.RadioSelect(),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(DocumentoFormFilter, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['departamento'].label = False
        self.fields['departamento'].widget.attrs.update({
            'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
            'hx-target': '#table_content_documento_swap',
            'hx-trigger': "change, changed from:.btn-shift-column-visivility, changed from:#id_fecha_documento_formfilter",
            'hx-push-url': 'true',
            'hx-replace-url': 'true',
            # 'hx-preserve': 'true',
            'hx-include': '[name="rango_fecha"]',
        })
        self.fields['rango_fecha'].label = False
        self.fields['rango_fecha'].widget.attrs.update({
            'class': 'class="form-control',
            'style': 'height: auto; padding: 0;',
            'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
            'hx-target': '#table_content_documento_swap',
            'hx-trigger': 'change, changed from:#div_id_departamento, changed from:.btn-shift-column-visivility',
            'hx-replace-url': 'true',
            'hx-preserve': 'true',
            'hx-include': '[name="departamento"]'
        })
        self.helper.form_id = 'id_documento_form_filter'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Documento',
                    Row(
                        Column(
                            AppendedText(
                                'query', mark_safe('<i class="fas fa-search"></i>')
                            ),
                            css_class='form-group col-md-12 mb-0'
                        ),
                    ),
                    Row(
                        Column(
                            Field('fecha', id='id_fecha_documento_formfilter', ),
                            css_class='col-md-3 mb-0'
                        ),
                        Column('numerocontrol', css_class='form-group col-md-3 mb-0'),
                        Column('numeroconsecutivo', css_class='form-group col-md-3 mb-0'),
                        Column('suma_importe', css_class='form-group col-md-3 mb-0'),
                        Column('observaciones', css_class='form-group col-md-3 mb-0'),
                        Column('estado', css_class='form-group col-md-3 mb-0'),
                        Column('reproceso', css_class='form-group col-md-3 mb-0'),
                        Column('editar_nc', css_class='form-group col-md-3 mb-0'),
                        Column('comprob', css_class='form-group col-md-5 mb-0'),
                        Column(
                            Field('departamento', id='id_departamento_documento_formfilter', ),
                            css_class='form-group col-md-12 mb-0',
                        ),
                        Column('tipodocumento', css_class='form-group col-md-5 mb-0'),
                        Column('ueb', css_class='form-group col-md-5 mb-0'),
                        # css_class='form-row'
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


# ------------ DocumentoDetalle / Form ------------
class DocumentoDetalleForm(forms.ModelForm):
    class Meta:
        model = DocumentoDetalle
        fields = [
            'cantidad',
            'precio',
            'importe',
            'existencia',
            # 'documento',
            'estado',
            'producto',
        ]
        widgets = {
            'producto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                    'id': 'id_producto_documento_detalle',
                    # "onChange": 'productoMedida()',
                }
            ),
            'estado': SelectWidget(
                attrs={
                    'style': 'width: 100%; dislay: block',
                    'id': 'id_estado_documento_detalle',
                },
            ),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_documento_detalle_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            TabHolder(
                Tab(
                    'Detalles Documento',
                    Row(
                        Column('producto', css_class='form-group col-md-4 mb-0', css_id='id_producto_documento_detalle'),
                        Column('cantidad', css_class='form-group col-md-4 mb-0', css_id='id_cantidad_documento_detalle'),
                        Column('precio', css_class='form-group col-md-4 mb-0', css_id='id_cantidad_documento_detalle'),
                        css_class='form-row'
                    ),
                    Row(Column('importe', css_class='form-group col-md-4 mb-0'),
                        Column('existencia', css_class='form-group col-md-4 mb-0'),
                        Column('estado', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'),
                ),
            ),
        )

    # def clean_producto(self):
    #     producto = self.cleaned_data.get('producto')
    #     detallenc = NormaconsumoDetalle.objects.filter(~Q(pk=self.instance.pk), producto=producto)
    #
    #     if detallenc.exists():
    #         raise forms.ValidationError('Ya existe este producto para la norma')
    #     return producto
    #
    # def clean_norma_ramal(self):  # Validar que que la cantidad>0
    #     norma_ramal = self.cleaned_data.get('norma_ramal')
    #     if float(norma_ramal) <= 0:
    #         raise forms.ValidationError('Debe introducir un valor>0')
    #     return norma_ramal
    #
    # def clean_norma_empresarial(self):  # Validar que que la cantidad>0
    #     norma_empresarial = self.cleaned_data.get('norma_empresarial')
    #     if float(norma_empresarial) <= 0:
    #         raise forms.ValidationError('Debe introducir un valor>0')
    #     return norma_empresarial
