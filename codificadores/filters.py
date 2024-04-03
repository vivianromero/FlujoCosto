import django_filters
from django import forms
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from cruds_adminlte3.filter import MyGenericFilter
from .forms import *
from .models import *


# ------ Departamento / Filter ------
class DepartamentoFilter(MyGenericFilter):
    search_fields = [
        'codigo__contains',
        'descripcion__icontains',
        'centrocosto__descripcion__icontains',
        'unidadcontable__nombre__icontains',
    ]
    split_space_search = ' '

    codigo = django_filters.CharFilter(
        label='Código',
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    descripcion = django_filters.CharFilter(
        label='Descripción',
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = Departamento
        fields = [
            'query',
            'codigo',
            'descripcion',
            'centrocosto',
            'unidadcontable'
        ]

        form = DepartamentoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ UnidadContable / Filter ------
class UnidadContableFilter(MyGenericFilter):
    search_fields = [
        'codigo__icontains',
        'nombre__icontains',
    ]
    split_space_search = ' '

    codigo = django_filters.CharFilter(
        label=_("Code"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    nombre = django_filters.CharFilter(
        label=_("Name"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = UnidadContable
        fields = [
            'codigo',
            'nombre',
            'activo',
            'is_empresa',
            'is_comercializadora',
        ]

        form = UnidadContableFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ Medida / Filter ------
class MedidaFilter(MyGenericFilter):
    search_fields = [
        'clave__icontains',
        'descripcion__icontains',
    ]
    split_space_search = ' '

    clave = django_filters.CharFilter(
        label=_("Key"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    descripcion = django_filters.CharFilter(
        label=_("Description"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = Medida
        fields = [
            'clave',
            'descripcion',
            'activa',
        ]

        form = MedidaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ MedidaConversion / Filter ------
class MedidaConversionFilter(MyGenericFilter):
    search_fields = [
        'factor_conversion__contains',
        'medidao__descripcion__icontains',
        'medidad__descripcion__icontains',
    ]
    split_space_search = ' '

    factor_conversion = django_filters.RangeFilter(
        label=_('Convertion Factor'),
        method='my_range_queryset',
    )

    class Meta:
        model = MedidaConversion
        fields = [
            'factor_conversion',
            'medidao',
            'medidad',
        ]

        form = MedidaConversionFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ Cuenta / Filter ------
class CuentaFilter(MyGenericFilter):
    search_fields = [
        'clave__icontains',
        'descripcion__icontains',
    ]
    split_space_search = ' '

    clave = django_filters.CharFilter(
        label=_("Key"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    descripcion = django_filters.CharFilter(
        label=_("Description"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = Cuenta
        fields = [
            'clave',
            'descripcion',
            'activa',
        ]

        form = CuentaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ CentroCosto / Filter ------
class CentroCostoFilter(MyGenericFilter):
    search_fields = [
        'clave__icontains',
        'descripcion__icontains',
    ]
    split_space_search = ' '

    clave = django_filters.CharFilter(
        label=_("Key"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    descripcion = django_filters.CharFilter(
        label=_("Description"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = CentroCosto
        fields = [
            'clave',
            'descripcion',
            'activo',
        ]

        form = CentroCostoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }

# ------ ProductoFlujo / Filter ------
class ProductoFlujoFilter(MyGenericFilter):
    search_fields = [
        'codigo__icontains',
        'descripcion__icontains',
        'medida__descripcion__icontains',
        'tipoproducto__descripcion__icontains',
    ]
    split_space_search = ' '

    codigo = django_filters.CharFilter(
        label=_("Code"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    descripcion = django_filters.CharFilter(
        label=_("Description"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = ProductoFlujo
        fields = [
            'codigo',
            'descripcion',
            'activo',
            'medida',
            'tipoproducto',
        ]

        form = ProductoFlujoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ ProductoFlujoClase / Filter ------
class ProductoFlujoClaseFilter(MyGenericFilter):
    search_fields = [
        'id__contains',
        'clasemateriaprima__descripcion__icontains',
        'producto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujoClase
        fields = [
            'id',
            'clasemateriaprima',
            'producto',
        ]

        form = ProductoFlujoClaseFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ ProductoFlujoDestino / Filter ------
class ProductoFlujoDestinoFilter(MyGenericFilter):
    search_fields = [
        'id__contains',
        'destino_icontains',
        'producto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujoDestino
        fields = [
            'id',
            'destino',
            'producto',
        ]

        form = ProductoFlujoClaseFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ ProductoFlujoCuenta / Filter ------
class ProductoFlujoCuentaFilter(MyGenericFilter):
    search_fields = [
        'id__contains',
        'cuenta__descripcion__icontains',
        'producto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujoCuenta
        fields = [
            'id',
            'cuenta',
            'producto',
        ]

        form = ProductoFlujoCuentaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ Vitola / Filter ------
class VitolaFilter(MyGenericFilter):
    search_fields = [
        'diametro__contains',
        'longitud__contains',
        'destino__icontains',
        'cepo__contains',
        'categoriavitola__descripcion__icontains',
        'producto__descripcion__icontains',
        'tipovitola__descripcion__icontains',
    ]
    split_space_search = ' '

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

        form = VitolaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ MarcaSalida / Filter ------
class MarcaSalidaFilter(MyGenericFilter):
    search_fields = [
        'codigo__icontains',
        'descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = MarcaSalida
        fields = [
            'codigo',
            'descripcion',
            'activa',
        ]

        form = MarcaSalidaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }

# ------ MotivoAjuste / Filter ------
class MotivoAjusteFilter(MyGenericFilter):
    search_fields = [
        'descripcion__icontains',
    ]
    split_space_search = ' '

    descripcion = django_filters.CharFilter(
        label=_("Description"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = MotivoAjuste
        fields = [
            'descripcion',
            'aumento',
            'activo',
        ]

        form = MotivoAjusteFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }