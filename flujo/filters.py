import django_filters
from django import forms
from django.db import models
from django.urls import reverse_lazy
from django.utils.safestring import mark_safe

from app_index.filters import CustomDateFromToRangeFilter
from app_index.widgets import MyCustomDateRangeWidget, MyCustomRangeWidget
from codificadores.filters import EMPTY_LABEL
from codificadores.models import Departamento
from cruds_adminlte3.filter import MyGenericFilter
from cruds_adminlte3.utils import crud_url_name
from flujo.forms import DocumentoFormFilter
from flujo.models import *


# ------ Documento / Filter ------
class DocumentoFilter(MyGenericFilter):
    departamento = django_filters.ModelChoiceFilter(
        queryset=Departamento.objects.all(),
        field_name='departamento',
        # empty_label=EMPTY_LABEL,
        widget=forms.RadioSelect(
            # attrs={
            #     'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
            #     'hx-target': '#main_content_swap',
            #     'hx-trigger': 'change',
            #     'hx-replace-url': 'true',
            #     'hx-preserve': 'true',
            #     'hx-include': '[name="departamento"]',
            # }
        ),
    )
    # tipodocumento = django_filters.ModelMultipleChoiceFilter(
    #     queryset=TipoDocumento.objects.all(),
    #     field_name='tipodocumento',
    #     widget=forms.Select(
    #         attrs={
    #             'style': 'width: 100%',
    #         }
    #     ),
    # )

    rango_fecha = CustomDateFromToRangeFilter(
        label='Fecha',
        field_name='fecha',
        widget=MyCustomDateRangeWidget(
            attrs={
                'id': 'id_fecha_documento_formfilter',
                'class': 'class="form-control',
                'style': 'height: auto; padding: 0;',
                'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:flujo:')),
                'hx-target': '#main_content_swap',
                'hx-trigger': 'change, changed from:#div_id_departamento, changed from:.btn-shift-column-visivility',
                'hx-replace-url': 'true',
                'hx-preserve': 'true',
                'hx-include': '[name="departamento"]'
            },
            format='%d/%m/%Y',
            picker_options={
                'use_ranges': True,
            }
        ),
    )

    estado = django_filters.ChoiceFilter(
        choices=Documento.CHOICE_ESTADOS_DOCUMENTO,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

    numeroconsecutivo = django_filters.RangeFilter(
        label='Cantidad',
        method='my_range_queryset',
        widget=MyCustomRangeWidget()
    )
    suma_importe = django_filters.RangeFilter(
        label='Cantidad',
        method='my_range_queryset',
        widget=MyCustomRangeWidget()
    )

    search_fields = [
        'fecha',
        'medida__descripcion__icontains',
        'producto__descripcion__icontains',
        'numerocontrol__icontains',
        'numeroconsecutivo__contains',
        'suma_importe__contains',
        'observaciones__icontains',
        'comprob__icontains',
        'departamento__descripcion__icontains',
        'tipodocumento__descripcion__icontains',
        'ueb__nombre__icontains',
    ]
    split_space_search = ' '

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
            # 'tipodocumento',
            # 'ueb',
        ]

        form = DocumentoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }
