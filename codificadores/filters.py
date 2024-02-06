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
        'idcentrocosto__contains',
        'idunidadcontable__contains',
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
            'idcentrocosto',
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


# ------ DepartamentoRelacion / Filter ------
# class DepartamentoRelacionFilter(MyGenericFilter):
#     search_fields = [
#         'iddepartamentoo__descripcion__icontains',
#         'iddepartamentod__descripcion__icontains',
#     ]
#     split_space_search = ' '
#
#     class Meta:
#         model = DepartamentoRelacion
#         fields = [
#             'iddepartamentoo',
#             'iddepartamentod',
#         ]
#
#         form = DepartamentoRelacionFormFilter
#
#         filter_overrides = {
#             models.ForeignKey: {
#                 'filter_class': django_filters.ModelMultipleChoiceFilter,
#                 'extra': lambda f: {
#                     'queryset': django_filters.filterset.remote_queryset(f),
#                 }
#             },
#         }


# ------ UnidadContable / Filter ------
class UnidadContableFilter(MyGenericFilter):
    search_fields = [
        'codigo__icontains',
        'nombre__icontains',
        'activo',
        'is_empresa',
        'is_comercializadora',
    ]
    split_space_search = ' '

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

    class Meta:
        model = Medida
        fields = [
            'clave',
            'descripcion',
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
        'long_niv_contains',
        'posicion_contains',
        'clave_icontains',
        'descripcion_icontains',
        'activa',
    ]
    split_space_search = ' '

    class Meta:
        model = Cuenta
        fields = [
            'long_niv',
            'posicion',
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
        'clavenivel__icontains',
        'descripcion__icontains',
        'activo',
    ]
    split_space_search = ' '

    class Meta:
        model = CentroCosto
        fields = [
            'clave',
            'clavenivel',
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


# ------ TipoProducto / Filter ------
class TipoProductoFilter(MyGenericFilter):
    search_fields = [
        'id__contains',
        'descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = TipoProducto
        fields = [
            'id',
            'descripcion',
        ]

        form = TipoProductoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ EstadoProducto / Filter ------
class EstadoProductoFilter(TipoProductoFilter):

    class Meta(TipoProductoFilter.Meta):
        model = EstadoProducto
        form = EstadoProductoFormFilter


# ------ ClaseMaateriaPrima / Filter ------
class ClaseMateriaPrimaFilter(MyGenericFilter):
    search_fields = [
        'id__contains',
        'descripcion__icontains',        
        'capote_fortaleza__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ClaseMateriaPrima
        fields = [
            'id',
            'descripcion',
            'capote_fortaleza',
        ]

        form = ClaseMateriaPrimaFormFilter

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
        'id__contains',
        'codigo__icontains',
        'id__contains',
        'descripcion__icontains', 
        'activo',
        'idmedida__descripcion__icontains',
        'idtipoproducto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujo
        fields = [
            'id',
            'codigo',
            'descripcion',
            'activo',
            'idmedida',
            'idtipoproducto',
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
        'idclasemateriaprima__descripcion__icontains',
        'idproducto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujoClase
        fields = [
            'id',
            'idclasemateriaprima',
            'idproducto',
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
        'idproducto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujoDestino
        fields = [
            'id',
            'destino',
            'idproducto',
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
        'idcuenta__descripcion__icontains',
        'idproducto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = ProductoFlujoCuenta
        fields = [
            'id',
            'idcuenta',
            'idproducto',
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


# ------ CategoriaVitola / Filter ------
class CategoriaVitolaFilter(MyGenericFilter):
    search_fields = [
        'id__contains',  
        'descripcion__icontains',
        'orden__contains',
    ]
    split_space_search = ' '

    class Meta:
        model = CategoriaVitola
        fields = [
            'id',
            'descripcion',
            'orden',
        ]

        form = CategoriaVitolaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ TipoVitola / Filter ------
class TipoVitolaFilter(MyGenericFilter):
    search_fields = [
        'id__contains',  
        'descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = TipoVitola
        fields = [
            'id',
            'descripcion',
        ]

        form = TipoVitolaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }
