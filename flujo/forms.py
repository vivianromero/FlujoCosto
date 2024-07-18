from datetime import date

from crispy_forms.bootstrap import TabHolder, Tab, FormActions, AppendedText, UneditableField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Field
from django import forms
from django.conf import settings
from django.db import transaction
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from app_index.widgets import MyCustomDateRangeWidget
from codificadores import ChoiceTiposDoc, ChoiceTiposProd, ChoiceClasesMatPrima
from codificadores.models import TipoProducto, ClaseMateriaPrima
from cruds_adminlte3.utils import crud_url_name
from cruds_adminlte3.widgets import SelectWidget
from flujo.models import *
from .utils import actualiza_existencias, genera_numero_doc, actualiza_numeros, dame_productos, \
    existencia_producto, actualiza_existencias_productos_todos


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

    departamento_origen = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento Origen",
        required=False,
        widget=SelectWidget(attrs={
            'style': 'width: 100%;',
        }
        )
    )

    ueb_destino = forms.ModelChoiceField(
        queryset=UnidadContable.objects.filter(activo=True),
        label="Destino",
        required=False,
        widget=SelectWidget(attrs={
            'style': 'width: 100%; display: none;',
        }
        )
    )

    ueb_origen = forms.ModelChoiceField(
        queryset=UnidadContable.objects.all(),
        label="Origen",
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
            'ueb_destino',
            'ueb_origen',
            'mes',
            'anno'
        ]
        widgets = {
            'fecha': MyCustomDateRangeWidget(
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
        self.fecha_procesamiento = kwargs.pop('fecha_procesamiento', None)
        self.destino_tipo_documento = [ChoiceTiposDoc.TRANSF_HACIA_DPTO, ]
        self.origen_tipo_documento = [ChoiceTiposDoc.TRANSF_DESDE_DPTO, ChoiceTiposDoc.DEVOLUCION_RECIBIDA,]
        self.destino_ueb_tipo_documento = [ChoiceTiposDoc.TRANSFERENCIA_EXTERNA,]
        self.origen_ueb_tipo_documento = [ChoiceTiposDoc.RECIBIR_TRANS_EXTERNA,]
        super(DocumentoForm, self).__init__(*args, **kwargs)
        self.fields['departamento_destino'].label = False
        self.fields['departamento_origen'].label = False
        self.origen_dpto = False
        self.destino_dpto = False
        self.destino_ueb = False
        self.origen_ueb = False
        self.edicion = False if not instance else True
        self.numeroconcecutivo_anterior = None if not instance else Documento.objects.get(
            pk=instance.pk).numeroconsecutivo

        if self.user:
            self.fields['ueb'].initial = self.user.ueb
            self.fields['ueb'].widget.enabled_choices = [self.user.ueb]
        if instance:
            self.fields['fecha'].initial = self.fecha_procesamiento
            self.fields['fecha'].widget.attrs['readonly'] = True
            self.fields['departamento'].widget.enabled_choices = [instance.departamento]
            self.fields['tipodocumento'].widget.enabled_choices = [instance.tipodocumento]
            if settings.NUMERACION_DOCUMENTOS_CONFIG:
                self.fields["numeroconsecutivo"].widget.attrs['readonly'] = \
                    settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO]['sistema']

                self.fields["numerocontrol"].widget.attrs['readonly'] = \
                    settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONTROL]['sistema']

            if instance.tipodocumento.pk in self.destino_tipo_documento:
                self.destino_dpto = True
                destino_queryset = self.fields['departamento_destino'].queryset
                destino_queryset = destino_queryset.filter(unidadcontable=self.user.ueb,
                                                           relaciondepartamento=instance.departamento)
                self.fields['departamento_destino'].queryset = destino_queryset
                destino = DocumentoTransfDepartamento.objects.get(documento=instance)
                self.fields['departamento_destino'].initial = destino.departamento
                self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%;', }
                self.fields['departamento_destino'].label = "Departamento Destino"
                self.fields['departamento_destino'].disabled = False
                self.fields['departamento_destino'].required = False
            elif instance.tipodocumento.pk in self.destino_ueb_tipo_documento:
                self.destino_ueb = True
                destino_queryset = self.fields['ueb_destino'].queryset.exclude(pk=self.user.ueb.pk)
                self.fields['ueb_destino'].queryset = destino_queryset
                destino = DocumentoTransfExterna.objects.get(documento=instance).unidadcontable
                self.fields['ueb_destino'].initial = destino
                self.fields['ueb_destino'].widget.attrs = {'style': 'width: 100%;', }
                self.fields['ueb_destino'].label = "Destino"
                self.fields['ueb_destino'].disabled = False
                self.fields['ueb_destino'].required = False
            elif instance.tipodocumento.pk in self.origen_tipo_documento:
                self.origen_dpto = True
                origen_queryset = self.fields['departamento_origen'].queryset
                tipod = instance.tipodocumento.pk
                if tipod == ChoiceTiposDoc.TRANSF_DESDE_DPTO:
                    origen_queryset = origen_queryset.filter(relaciondepartamento=instance.departamento)
                    origen = DocumentoTransfDepartamentoRecibida.objects.get(documento=instance).documentoorigen
                elif tipod == ChoiceTiposDoc.DEVOLUCION_RECIBIDA:
                    origen = DocumentoDevolucionRecibida.objects.get(documento=instance).documentoorigen
                    origen_queryset = origen_queryset.filter(pk=origen.departamento.pk)

                self.fields['departamento_origen'].queryset = origen_queryset
                self.fields['departamento_origen'].initial = origen.departamento
                self.fields['departamento_origen'].widget.enabled_choices = [origen.departamento]
                self.fields['departamento_origen'].widget.attrs = {'style': 'width: 100%;', }
                self.fields['departamento_origen'].label = "Departamento Origen"
                self.fields['departamento_origen'].disabled = False
                self.fields['departamento_origen'].required = True
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
                self.fields['fecha'].initial = self.fecha_procesamiento
                self.fields['fecha'].widget.attrs['readonly'] = True

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
                    self.destino_dpto = True
                    destino_queryset = self.fields['departamento_destino'].queryset.filter(
                        relaciondepartamento=self.departamento)
                    dptos_no_inicializados = [x.pk for x in destino_queryset if
                                              not x.fechainicio_departamento.all().exists()]
                    destino_queryset = destino_queryset.exclude(pk__in=dptos_no_inicializados)
                    self.fields['departamento_destino'].queryset = destino_queryset
                    self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%;', }
                    self.fields['departamento_destino'].label = "Departamento Destino"
                    self.fields['departamento_destino'].disabled = False
                    self.fields['departamento_destino'].required = True
                elif int(self.tipo_doc) in self.destino_ueb_tipo_documento:
                    self.destino_ueb = True
                    destino_queryset = self.fields['ueb_destino'].queryset.exclude(pk=self.user.ueb.pk)
                    self.fields['ueb_destino'].queryset = destino_queryset
                    self.fields['ueb_destino'].widget.attrs = {'style': 'width: 100%;', }
                    self.fields['ueb_destino'].label = "Destino"
                    self.fields['ueb_destino'].disabled = False
                    self.fields['ueb_destino'].required = True
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
                Column('departamento_destino', css_class='form-group col-md-3 mb-0') if self.destino_dpto else Field('departamento_destino', type="hidden"),
                Column('ueb_destino', css_class='form-group col-md-3 mb-0') if self.destino_ueb else Field('ueb_destino', type="hidden"),
                Column('departamento_origen', css_class='form-group col-md-3 mb-0') if self.origen_dpto else Field('departamento_origen', type="hidden"),
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
        conf = settings.NUMERACION_DOCUMENTOS_CONFIG
        control_sistema = conf[TipoNumeroDoc.NUMERO_CONTROL]['sistema']
        control_departamento = conf[TipoNumeroDoc.NUMERO_CONTROL]['departamento']
        consec_sistema = conf[TipoNumeroDoc.NUMERO_CONSECUTIVO]['sistema']
        consec_departamento = conf[TipoNumeroDoc.NUMERO_CONSECUTIVO]['departamento']

        # actualiza el campo donde se guarda el tipo de configuracion de los documentos para aplicar las constraints
        self.instance.confconsec = ConfigNumero.DEPARTAMENTO if conf[TipoNumeroDoc.NUMERO_CONSECUTIVO][
            'departamento'] else ConfigNumero.UNICO
        self.instance.confcontrol = ConfigNumero.DEPARTAMENTO if conf[TipoNumeroDoc.NUMERO_CONTROL][
            'departamento'] else ConfigNumero.UNICO

        # actializa campo mes y anno que se utilizan en las constrains
        self.instance.mes = self.instance.fecha.month
        self.instance.anno = self.instance.fecha.year

        # se bloquea el documento
        doc = Documento.objects.select_for_update().filter(pk=self.instance.pk)
        numeroconsec_antes = self.instance.numeroconsecutivo if not doc.exists() else doc[0].numeroconsecutivo
        NumeroDocumentos.objects.select_for_update().filter(ueb=self.user.ueb)
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

        if not control_sistema:
            partes_ctrl = nro.control.split('/')
            nro_control = int(partes_ctrl[len(partes_ctrl) - 1])
            if nro_control > control:
                control = nro_control

        actualiza_numeros(ueb=self.instance.ueb,
                          departamento=None if not consec_departamento else self.instance.departamento,
                          consecutivo=consecutivo, control=control, pk=self.instance.pk
                          )

        instance = super().save(commit=True)

        match self.cleaned_data['tipodocumento'].pk:
            case ChoiceTiposDoc.TRANSF_HACIA_DPTO:
                departamento_destino = self.cleaned_data.get('departamento_destino')
                if departamento_destino:
                    documento_transf_departamento = DocumentoTransfDepartamento.objects.update_or_create(
                        documento=instance,
                        defaults={
                            'departamento': departamento_destino,
                        }
                    )
            case ChoiceTiposDoc.TRANSFERENCIA_EXTERNA:
                ueb_destino = self.cleaned_data.get('ueb_destino')
                if ueb_destino:
                    documento_transf_ext = DocumentoTransfExterna.objects.update_or_create(
                        documento=instance,
                        defaults={
                            'unidadcontable': ueb_destino,
                        }
                    )

        if 'numeroconsecutivo' in self.changed_data and self.edicion and abs(
                self.numeroconcecutivo_anterior - instance.numeroconsecutivo) > 1:
            detalles = instance.documentodetalle_documento.all()
            departam = instance.departamento
            ueb = instance.ueb
            operacion = instance.operacion

            dicc = {'documento__estado__in': [EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES],
                    'documento__departamento': departam, 'documento__ueb': ueb}

            docs = DocumentoDetalle.objects.select_for_update().filter(**dicc).order_by('documento__numeroconsecutivo')
            dicc_prod = {}
            desde = self.numeroconcecutivo_anterior + 1 if instance.numeroconsecutivo > self.numeroconcecutivo_anterior else instance.numeroconsecutivo
            docs = docs.filter(documento__numeroconsecutivo__gte=desde)
            actualiza_existencias_productos_todos(docs, detalles, departam, ueb, consecutivo=desde)
        return instance


class DocumentoDetailForm(forms.ModelForm):
    departamento_destino = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento Destino",
        required=False,
        widget=SelectWidget(attrs={
            'style': 'width: 100%; display: none;',
        }
        )
    )

    departamento_origen = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento Origen",
        required=False,
        widget=SelectWidget(attrs={
            'style': 'width: 100%;',
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

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        data = kwargs.get('data', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        self.departamento = kwargs.pop('departamento', None)
        self.tipo_doc = kwargs.pop('tipo_doc', None)
        self.destino_tipo_documento = [ChoiceTiposDoc.TRANSF_HACIA_DPTO, ]
        super(DocumentoDetailForm, self).__init__(*args, **kwargs)
        self.origen_tipo_documento = [ChoiceTiposDoc.TRANSF_DESDE_DPTO, ]
        super(DocumentoDetailForm, self).__init__(*args, **kwargs)
        self.fields['departamento_destino'].label = ""
        self.fields['departamento_origen'].label = ""
        self.origen = False
        self.edicion = False if not instance else True  # Documento.objects.filter(pk=instance.pk).exists()
        self.numeroconcecutivo_anterior = None if not instance else Documento.objects.get(
            pk=instance.pk).numeroconsecutivo  # Documento.objects.filter(pk=instance.pk).exists()

        if instance:
            self.fields['departamento'].widget.enabled_choices = [instance.departamento]
            self.fields['tipodocumento'].widget.enabled_choices = [instance.tipodocumento]
            if settings.NUMERACION_DOCUMENTOS_CONFIG:
                self.fields["numeroconsecutivo"].widget.attrs['readonly'] = \
                    settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONSECUTIVO]['sistema']

                self.fields["numerocontrol"].widget.attrs['readonly'] = \
                    settings.NUMERACION_DOCUMENTOS_CONFIG[TipoNumeroDoc.NUMERO_CONTROL]['sistema']
            if instance.tipodocumento.pk in self.destino_tipo_documento:
                destino_queryset = self.fields['departamento_destino'].queryset.filter(
                    relaciondepartamento=instance.departamento)
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

                if int(self.tipo_doc) in self.destino_tipo_documento:
                    destino_queryset = self.fields['departamento_destino'].queryset.filter(
                        relaciondepartamento=self.departamento)
                    self.fields['departamento_destino'].queryset = destino_queryset
                    self.fields['departamento_destino'].widget.attrs = {'style': 'width: 100%; display: block;', }
                    self.fields['departamento_destino'].label = "Departamento Destino"
                    self.fields['departamento_destino'].disabled = False
                    self.fields['departamento_destino'].required = True

        self.helper = FormHelper(self)
        self.helper.form_id = 'id_documento_detalle__form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column(
                    UneditableField('fecha', id='id_fecha_documentodetail_form', ),
                    css_class='form-group col-md-3 mb-0'
                ),
                Column(UneditableField('numeroconsecutivo'), css_class='form-group col-md-3 mb-0'),
                Column(UneditableField('numerocontrol'), css_class='form-group col-md-3 mb-0'),
                Column(UneditableField('departamento_destino'), css_class='form-group col-md-3 mb-0'),
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
    documento_hidden = forms.CharField(label='', required=False)
    operacion_hidden = forms.CharField(label='', required=False)

    class Meta:
        model = DocumentoDetalle
        fields = [
            'cantidad',
            'precio',
            'estado',
            'producto',
        ]

        widgets = {
            'producto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                    'id': 'id_producto_documento_detalle',
                }
            ),
            'estado': SelectWidget(
                attrs={
                    'style': 'width: 100%; dislay: block',
                    'id': 'id_estado_documento_detalle',
                },
            ),
            'cantidad': forms.TextInput(),
            'precio': forms.TextInput(),
        }

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        self.cantidad_anterior = 0
        self.documentopadre = kwargs.pop('doc', None)
        if args:
            self.documentopadre = args[0]['doc']

        if instance:
            self.cantidad_anterior = instance.cantidad

        super(DocumentoDetalleForm, self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = dame_productos(self.documentopadre, self.fields['producto'].queryset)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_documento_detalle_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False
        self.fields['documento_hidden'].initial = '' if not self.documentopadre else self.documentopadre.pk
        self.fields[
            'operacion_hidden'].initial = '' if not self.documentopadre else self.documentopadre.tipodocumento.operacion

        if self.fields['operacion_hidden'].initial == OperacionDocumento.SALIDA:
            self.fields["precio"].widget.attrs = {'hx-get': reverse_lazy('app_index:flujo:precioproducto'),
                                                  'hx-target': '#div_id_precio',
                                                  'hx-trigger': 'change from:#div_id_producto, change from:#div_id_estado',
                                                  'hx-include': '[name="producto"], [name="documento_hidden"], [name="estado"]',
                                                  'readonly': True}

        self.helper.layout = Layout(
            Row(
                Column('producto', css_class='form-group col-md-6 mb-0',
                       css_id='id_producto_documento_detalle'),
                Column('estado', css_class='form-group col-md-2 mb-0'),
                Column(Field('cantidad', data_inputmask="'alias': 'decimal', 'digits': 4"),
                       css_class='form-group col-md-2 mb-0',
                       css_id='id_cantidad_documento_detalle'),
                Column(Field('precio', data_inputmask="'alias': 'decimal', 'digits': 7"),
                       css_class='form-group col-md-2 mb-0',
                       css_id='id_precio_documento_detalle'),
                Field('documento_hidden', type="hidden"),
                Field('operacion_hidden', type="hidden"),
                css_class='form-row'
            ),
        )

    @transaction.atomic
    def save(self, commit=True, doc=None, existencia=None):
        if not doc:
            return self.instance
        instance = super().save(commit=False)

        ueb = doc.ueb
        producto = instance.producto
        estado = instance.estado
        departamento = doc.departamento
        operacion = doc.operacion

        existencia_actual = (float(instance.existencia) - float(self.cantidad_anterior) * operacion) + float(
            instance.cantidad) * operacion if not existencia else float(existencia)
        instance.existencia = float(existencia_actual) + float(instance.cantidad)

        # actualizar las existencias de los demás documentos
        # tomo la existencia del producto
        dicc = {'documento__estado__in': [EstadosDocumentos.EDICION, EstadosDocumentos.ERRORES],
                'documento__departamento': departamento, 'producto': producto, 'estado': estado,
                'documento__ueb': ueb}

        docs_en_edicion = DocumentoDetalle.objects.select_for_update().filter(**dicc)
        # se excluyen los documentos que tengan errores para calcular la existencia del producto
        # existencia_product = existencia_producto(docs_en_edicion.filter(documento__error=False), doc, producto, estado, instance.cantidad)
        existencia_product, hay_error = existencia_producto(docs_en_edicion, doc, producto, estado, instance.cantidad)

        instance.existencia = existencia_product
        instance.error = hay_error

        # se van a actualizar las existencias de los doc posteriores que contienen el producto
        # y se dejan los documentos con error para actualizar su existencia
        actualiza_existencias(doc, docs_en_edicion, existencia_product)

        instance.importe = instance.precio * instance.cantidad

        doc_error = False
        if doc.documentodetalle_documento.filter(error=True).exclude(documento=doc).exists() or hay_error:
            doc_error = True

        doc.error = doc_error
        doc.estado = EstadosDocumentos.EDICION if not doc_error else EstadosDocumentos.ERRORES
        doc.save()
        return self.instance


# ------------ DocumentoDetalle / Form ------------
class DocumentoDetalleDetailForm(forms.ModelForm):
    class Meta:
        model = DocumentoDetalle
        fields = [
            'cantidad',
            'precio',
            'estado',
            'producto',
            'importe',
            'existencia',
        ]
        widgets = {
            'producto': SelectWidget(
                attrs={
                    'style': 'width: 100%',
                    'id': 'id_producto_documento_detalle',
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
        self.cantidad_anterior = 0
        self.documentopadre = kwargs.pop('doc', None)
        if instance:
            self.cantidad_anterior = instance.cantidad
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_id = 'id_documento_detalle_detail_form'
        self.helper.form_method = 'post'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column(UneditableField('producto'), css_class='form-group col-md-4 mb-0',
                       css_id='id_producto_documento_detail_detalle'),
                Column(UneditableField('estado'), css_class='form-group col-md-2 mb-0'),
                Column(UneditableField('cantidad'), css_class='form-group col-md-2 mb-0',
                       css_id='id_cantidad_documento_detail_detalle'),
                Column(UneditableField('precio'), css_class='form-group col-md-2 mb-0',
                       css_id='id_precio_documento_detail_detalle'),
                Column(UneditableField('importe'), css_class='form-group col-md-2 mb-0',
                       css_id='id_precio_documento_detail_detalle'),
                Column(UneditableField('existencia'), css_class='form-group col-md-2 mb-0',
                       css_id='id_precio_documento_detail_detalle'),
                css_class='form-row'
            ),
        )


# ------------ TraerProductoVersat / Form ------------
class TraerProductoVersatForm(forms.Form):
    producto_codigo = forms.CharField(label='Código', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    producto_descripcion = forms.CharField(label='Descripción', required=False,
                                           widget=forms.TextInput(attrs={'readonly': True}))
    medida_clave = forms.CharField(label='U.M', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    cantidad = forms.DecimalField(label='Cantidad', required=False)
    precio = forms.DecimalField(label='Precio', required=False)
    tipoproducto = forms.ModelChoiceField(
        queryset=TipoProducto.objects.filter(pk__in=[ChoiceTiposProd.MATERIAPRIMA, ChoiceTiposProd.HABILITACIONES]),
        label='Tipo de Producto', required=True)
    clase_mat_prima = forms.ModelChoiceField(
        queryset=ClaseMateriaPrima.objects.exclude(pk=ChoiceClasesMatPrima.CAPACLASIFICADA),
        label='Clase Materia Prima', required=False)

    class Meta:
        fields = [
            'tipoproducto',
            'clase_mat_prima',
            'producto_codigo',
            'producto_descripcion',
            'medida_clave',
            'cantidad',
            'precio',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(TraerProductoVersatForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_tag = False

        self.fields["tipoproducto"].required = True
        self.fields["clase_mat_prima"].required = False

        self.helper.layout = Layout(
            Row(
                Column('producto_codigo', css_class='form-group col-md-4 mb-0'),
                Column('producto_descripcion', css_class='form-group col-md-6 mb-0'),
                Column('medida_clave', css_class='form-group col-md-2 mb-0'),
                Field('cantidad', type="hidden"),
                Field('precio', type="hidden"),
                css_class='form-row'
            ),
            Row(
                Column('tipoproducto', css_class='form-group col-md-6 mb-0'),
                Column('clase_mat_prima', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
        )


# ------------ ObtenerDocumentoVersat / Form ------------
class ObtenerDocumentoVersatForm(forms.Form):
    iddocumento = forms.CharField(label='No Doc', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    iddocumento_numero = forms.CharField(label='No Doc', required=False,
                                         widget=forms.TextInput(attrs={'readonly': True}))
    iddocumento_numctrl = forms.CharField(label='Nro Control', required=False,
                                          widget=forms.TextInput(attrs={'readonly': True}))
    iddocumento_fecha = forms.DateField(label='Fecha', required=False, widget=forms.TextInput(attrs={'readonly': True}))
    iddocumento_fecha_hidden = forms.CharField(label='Fecha x', required=False)
    iddocumento_concepto = forms.CharField(label='Concepto', required=False,
                                           widget=forms.TextInput(attrs={'readonly': True}))
    iddocumento_almacen = forms.CharField(label='Almacén', required=False,
                                          widget=forms.TextInput(attrs={'readonly': True}))
    iddocumento_sumaimporte = forms.CharField(label='Importe', required=False,
                                              widget=forms.TextInput(attrs={'readonly': True}))
    json_data = forms.JSONField(label='json', required=False, widget=forms.TextInput(attrs={'readonly': True}))

    class Meta:
        fields = [
            'iddocumento_numero',
            'iddocumento_numctrl',
            'iddocumento_fecha',
            'iddocumento_concepto',
            'iddocumento_almacen',
            'iddocumento_sumaimporte',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ObtenerDocumentoVersatForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_tag = False

        widget = forms.TextInput(attrs={'readonly': True})
        self.helper.layout = Layout(
            Row(
                Field('iddocumento', type="hidden"),
                Field('json_data', type="hidden"),
                Field('iddocumento_fecha_hidden', type="hidden"),
                Column(UneditableField('iddocumento_numero'), css_class='form-group col-md-1 mb-0'),
                Column(UneditableField('iddocumento_numctrl'), css_class='form-group col-md-2 mb-0'),
                Column(UneditableField('iddocumento_fecha'), css_class='form-group col-md-2 mb-0'),
                Column(UneditableField('iddocumento_concepto'), css_class='form-group col-md-3 mb-0'),
                Column(UneditableField('iddocumento_almacen'), css_class='form-group col-md-3 mb-0'),
                Column(UneditableField('iddocumento_sumaimporte'), css_class='form-group col-md-1 mb-0'),
                css_class='form-row'
            ),
        )
