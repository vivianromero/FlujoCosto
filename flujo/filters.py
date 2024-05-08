import django_filters
from django import forms
from django.db import models
from django.urls import reverse_lazy

from app_index.filters import CustomDateFromToRangeFilter
from app_index.widgets import MyCustomDateRangeWidget, MyCustomRangeWidget
from codificadores import ChoiceTiposNormas
from codificadores.filters import EMPTY_LABEL
from cruds_adminlte3.filter import MyGenericFilter
from cruds_adminlte3.utils import crud_url_name
from flujo.models import Documento


# ------ Documento / Filter ------
class DocumentoFilter(MyGenericFilter):
    deparetamento = django_filters.ModelChoiceFilter(
        field_name='departamento',
        empty_label='Todas',
        widget=forms.RadioSelect(
            attrs={
                'hx-get': reverse_lazy(crud_url_name(Documento, 'list', 'app_index:codificadores:')),
                'hx-target': '#main_content_swap',
                'hx-trigger': 'change',
            }
        ),
    )

    fecha = CustomDateFromToRangeFilter(
        label='Fecha',
        field_name='fecha',
        widget=MyCustomDateRangeWidget(
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
        'departamento',
        'tipodocumento',
        'ueb',
    ]
    split_space_search = ' '

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
        ]

        form = Documento

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }
