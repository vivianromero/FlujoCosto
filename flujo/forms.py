from datetime import date

from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from django import forms
from django.conf import settings
from django.db import transaction
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from app_index.widgets import MyCustomDateRangeWidget
from codificadores import ChoiceTiposDoc
from codificadores.models import TipoNumeroDoc
from cruds_adminlte3.utils import crud_url_name
from cruds_adminlte3.widgets import SelectWidget
from flujo.models import *
from utiles.utils import genera_numero_doc


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
            'mes',
            'anno'
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
        self.destino_tipo_documento = [ChoiceTiposDoc.TRANSF_HACIA_DPTO, ]
        super(DocumentoForm, self).__init__(*args, **kwargs)
        destino_queryset = self.fields['departamento_destino'].queryset
        self.fields['departamento_destino'].disabled = True
        self.fields['departamento_destino'].label = False
        self.edicion = False if not instance else Documento.objects.filter(pk=instance.pk).exists()
        if self.user:
            self.fields['ueb'].initial = self.user.ueb
            self.fields['ueb'].widget.enabled_choices = [self.user.ueb]
        if instance:
            self.fields['departamento'].widget.enabled_choices = [instance.departamento]
            self.fields['tipodocumento'].widget.enabled_choices = [instance.tipodocumento]
            if settings.NUMERACION_DOCUMENTOS_CONFIG:
                # numeros = genera_numero_doc(self.departamento, self.user.ueb, self.tipo_doc)
                #
                # # numero consecutivo y de control
                # numero_consec = str(numeros[0][0])
                # self.fields['numeroconsecutivo'].initial = numero_consec
                self.fields["numeroconsecutivo"].widget.attrs['readonly'] = \
                settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO]['sistema']

                # numero_ctrl = str(numeros[1][0]) if not numeros[1][2] else numeros[1][2] + '/' + str(numeros[1][0])
                # self.fields['numerocontrol'].initial = numero_ctrl
                self.fields["numerocontrol"].widget.attrs['readonly'] = \
                settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONTROL]['sistema']
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
            self.fields['departamento'].widget.enabled_choices = [data.get('departamento', None)]
            self.fields['tipodocumento'].widget.enabled_choices = [data.get('tipodocumento', None)]
            estado = data.get('estado')
            self.fields['estado'].initial = estado if estado != '' else EstadosDocumentos.EDICION
            if int(data.get('tipodocumento')) in self.destino_tipo_documento:
                destino = data.get('departamento_destino')
                self.fields['departamento_destino'].initial = destino
                self.fields['departamento_destino'].disabled = False
                self.fields['departamento_destino'].required = True
        else:
            if self.departamento:
                self.fields['departamento'].initial = self.departamento
                self.fields['departamento'].widget.enabled_choices = [self.departamento]
                self.fields['estado'].initial = EstadosDocumentos.EDICION
            if self.tipo_doc:
                self.fields['tipodocumento'].initial = self.tipo_doc
                self.fields['tipodocumento'].widget.enabled_choices = [self.tipo_doc]
                if settings.NUMERACION_DOCUMENTOS_CONFIG:
                    numeros = genera_numero_doc(self.departamento, self.user.ueb, self.tipo_doc)

                    # numero consecutivo y de control
                    numero_consec = str(numeros[0][0])
                    self.fields['numeroconsecutivo'].initial = numero_consec
                    self.fields["numeroconsecutivo"].widget.attrs['readonly'] = numeros[0][1]

                    numero_ctrl = str(numeros[1][0]) if not numeros[1][2] else numeros[1][2] + '/' + str(numeros[1][0])
                    self.fields['numerocontrol'].initial = numero_ctrl
                    self.fields["numerocontrol"].widget.attrs['readonly'] = numeros[1][1]

                if int(self.tipo_doc) in self.destino_tipo_documento:
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
                Column('numeroconsecutivo', css_class='form-group col-md-3 mb-0'),
                Column('numerocontrol', css_class='form-group col-md-3 mb-0'),

                Column('departamento_destino', css_class='form-group col-md-3 mb-0'),
                Field('departamento', type="hidden"),
                Field('tipodocumento', type="hidden"),
                Field('suma_importe', type="hidden"),
                Field('estado', type="hidden"),
                Field('ueb', type="hidden"),
                Field('mes', type="hidden"),
                Field('anno', type="hidden"),
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

    @transaction.atomic
    def save(self, commit=True):
        # si los numeros son controlados por el sistema
        control_sistema = settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONTROL]['sistema']
        consec_sistema = settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO]['sistema']

        # actualiza el campo donde se guarda el tipo de configuracion de los documentos para aplicar las constraints
        self.instance.confconsec = settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO][
            'confignumero']
        self.instance.confcontrol = settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONTROL]['confignumero']

        # actializa campo mes y anno que se utilizan en las constrains
        self.instance.mes = self.instance.fecha.month
        self.instance.anno = self.instance.fecha.year

        # se bloquea el documento
        doc = Documento.objects.select_for_update().filter(pk=self.instance.pk)

        # se bloquea el registro que lleva el control de los numeros de los documentos
        numeros = NumerosDocumentos.objects.select_for_update().filter(tipodocumento=self.instance.tipodocumento,
                                                                       departamento=self.instance.departamento,
                                                                       ueb=self.instance.ueb)
        numeros_consec = genera_numero_doc(self.instance.departamento, self.instance.ueb,
                                           self.instance.tipodocumento.pk)
        if not self.edicion:
            # numero consecutivo y de control se actualizan si los controla el sistema, porque puede que se halla salvado un documento
            # después de haber asignado el numero al documento actual
            self.instance.numeroconsecutivo = numeros_consec[0][
                0] if consec_sistema else self.instance.numeroconsecutivo
            self.instance.numerocontrol = self.instance.numerocontrol if not control_sistema else str(
                numeros_consec[1][0]) if not numeros_consec[1][2] else numeros_consec[1][2] + '/' + str(
                numeros_consec[1][0])

        # se va a actualizar la tabla que lleva el control de los numeros

        # numeros de la instancia
        nrs = self.instance.numerocontrol.split('/')
        control = int(nrs[len(nrs) - 1])
        consecutivo = self.instance.numeroconsecutivo

        # numeros que estan en la tabla que controla la numeracion
        nro = None if not numeros.exists() else numeros.first()
        if not consec_sistema and nro and nro.consecutivo > consecutivo:
            consecutivo = nro.consecutivo

        if not control_sistema and nro:
            partes_ctrl = nro.control.split('/')
            nro_control = int(partes_ctrl[len(partes_ctrl) - 1])
            if nro_control > control:
                control = nro_control

        actualiza_control_numeros = NumerosDocumentos.objects.update_or_create(
            tipodocumento=self.instance.tipodocumento, departamento=self.instance.departamento, ueb=self.instance.ueb,
            defaults={
                'consecutivo': consecutivo,
                'control': control
            }
        )

        if commit:
            actualiza_control_numeros[0].save()

        if self.cleaned_data['tipodocumento'].pk in self.destino_tipo_documento:
            departamento_destino = self.cleaned_data.get('departamento_destino')
            if departamento_destino:
                documento_transf_departamento = DocumentoTransfDepartamento.objects.update_or_create(
                    documento=doc,
                    defaults={
                        'departamento': departamento_destino,
                    }
                )
                if commit:
                    documento_transf_departamento.save()

        instance = super().save(commit=True)
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
                        Column('producto', css_class='form-group col-md-4 mb-0',
                               css_id='id_producto_documento_detalle'),
                        Column('estado', css_class='form-group col-md-4 mb-0'),
                        Column('cantidad', css_class='form-group col-md-4 mb-0',
                               css_id='id_cantidad_documento_detalle'),
                        Column('precio', css_class='form-group col-md-4 mb-0', css_id='id_cantidad_documento_detalle'),
                        css_class='form-row'
                    ),
                    Row(Column('importe', css_class='form-group col-md-4 mb-0'),
                        Column('existencia', css_class='form-group col-md-4 mb-0'),
                        css_class='form-row'),
                ),
            ),
        )

    def clean_producto(self):
        producto = self.cleaned_data.get('producto')
        estado = self.cleaned_data.get('estado')
        detalledoc = DocumentoDetalle.objects.filter(~Q(pk=self.instance.pk), producto=producto, estado=estado)

        if detalledoc.exists():
            raise forms.ValidationError('Ya existe este producto con el mismo estado')
        return producto


    # def save(self, commit=True):
    #     """
    #     Save this form's self.instance object if commit=True. Otherwise, add
    #     a save_m2m() method to the form which can be called after the instance
    #     is saved manually at a later time. Return the model instance.
    #     """
    #     if self.errors:
    #         raise ValueError(
    #             "The %s could not be %s because the data didn't validate."
    #             % (
    #                 self.instance._meta.object_name,
    #                 "created" if self.instance._state.adding else "changed",
    #             )
    #         )
    #     if commit:
    #         # If committing, save the instance and the m2m data immediately.
    #         self.instance.save()
    #         self._save_m2m()
    #     else:
    #         # If not committing, add a method to the form to allow deferred
    #         # saving of m2m data.
    #         self.save_m2m = self._save_m2m
    #     return self.instance
