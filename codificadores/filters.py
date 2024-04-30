import django_filters
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from cruds_adminlte3.filter import MyGenericFilter
from cruds_adminlte3.utils import crud_url_name
from .forms import *
from .models import *

ACTIVO_CHOICES = (
    (1, "Si"),
    (0, "No"),
)

EMPTY_LABEL = '-- Todos --'


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


# ------ NormaConsumo / Filter ------
class NormaConsumoFilter(MyGenericFilter):
    # tipo = django_filters.ChoiceFilter(
    #     field_name='tipo',
    #     choices=ChoiceTiposNormas.CHOICE_TIPOS_NORMAS,
    #     empty_label='Todas',
    #     widget=forms.Select(
    #         attrs={
    #             'style': 'width: 90%',
    #             'hx-get': reverse_lazy(crud_url_name(NormaConsumo, 'list', 'app_index:codificadores:')),
    #             'hx-target': '#main_content_swap',
    #             'hx-trigger': 'change',
    #         }
    #     ),
    # )
    search_fields = [
        # 'tipo',
        'cantidad__contains',
        'fecha',
        'medida__descripcion__icontains',
        'producto__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = NormaConsumo
        fields = [
            # 'tipo',
            'cantidad',
            'activa',
            'fecha',
            'medida',
            'producto',
        ]

        form = NormaConsumoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ NormaConsumo / Filter ------
class NormaConsumoGroupedFilter(MyGenericFilter):
    tipo = django_filters.ChoiceFilter(
        field_name='tipo',
        choices=ChoiceTiposNormas.CHOICE_TIPOS_NORMAS,
        empty_label='Todas',
        widget=forms.Select(
            attrs={
                'style': 'width: 100%',
                'hx-get': reverse_lazy(crud_url_name(NormaConsumoGrouped, 'list', 'app_index:codificadores:')),
                'hx-target': '#main_content_swap',
                'hx-trigger': 'change',
            }
        ),
    )
    search_fields = [
        'tipo',
        'cantidad__contains',
        'fecha',
        'medida__descripcion__icontains',
        'producto__descripcion__icontains',
    ]
    split_space_search = ' '

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

        form = NormaConsumoGroupedFormFilter

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

    activo = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

    is_empresa = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

    is_comercializadora = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
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

    activa = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
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
        field_name="factor_conversion",
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

    activo = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
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

    tipoproducto = django_filters.ModelMultipleChoiceFilter(
        label="Tipo de Producto",
        queryset=TipoProducto.objects.filter(id__in=[ChoiceTiposProd.MATERIAPRIMA, ChoiceTiposProd.SUBPRODUCTO]),
    )

    activo = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

    get_clasemateriaprima = django_filters.ModelMultipleChoiceFilter(
        label="Clase de Materia Prima",
        queryset=ClaseMateriaPrima.objects.exclude(pk=ChoiceClasesMatPrima.CAPACLASIFICADA),
        method="filter_by_clasemateriaprima",
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

    def filter_by_clasemateriaprima(self, queryset, name, value):
        if value:
            prods = [p.producto.pk for p in ProductoFlujoClase.objects.filter(clasemateriaprima__in=value).all()]
            return queryset.filter(pk__in=prods)
        return queryset


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
    producto = django_filters.ModelMultipleChoiceFilter(
        label="Producto",
        queryset=ProductoFlujo.objects.filter(tipoproducto__id__in=[ChoiceTiposProd.VITOLA]),
    )
    activo = django_filters.ChoiceFilter(
        label="Activo",
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
        method="filter_by_vitolaproductoactivo",
    )
    search_fields = [
        'diametro__contains',
        'longitud__contains',
        'destino__icontains',
        'cepo__contains',
        'categoriavitola__descripcion__contains',
        'producto__descripcion__icontains',
        'tipovitola__descripcion__icontains',
        'producto__codigo__icontains'
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

    def filter_by_vitolaproductoactivo(self, queryset, name, value):
        if value:
            return queryset.filter(producto__activo=value)
        return queryset


# ------ MarcaSalida / Filter ------
class MarcaSalidaFilter(MyGenericFilter):
    search_fields = [
        'codigo__icontains',
        'descripcion__icontains',
    ]
    split_space_search = ' '

    activa = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

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

    activo = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

    aumento = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
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


# ------ CambioProducto / Filter ------
class CambioProductoFilter(MyGenericFilter):
    search_fields = [
        'productoo__descripcion__icontains',
        'productod__descripcion__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = CambioProducto
        fields = [
            'productoo',
            'productod',
        ]

        form = CambioProductoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }


# ------ LineaSalida / Filter ------
class LineaSalidaFilter(MyGenericFilter):
    producto = django_filters.ModelMultipleChoiceFilter(
        label="Producto",
        queryset=ProductoFlujo.objects.filter(tipoproducto__id__in=[ChoiceTiposProd.LINEASALIDA]),
    )
    vitola = django_filters.ModelMultipleChoiceFilter(
        label="Vitola",
        queryset=ProductoFlujo.objects.filter(tipoproducto=ChoiceTiposProd.VITOLA),
    )

    activo = django_filters.ChoiceFilter(
        label="Activo",
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
        method="filter_by_productoactivo",
    )

    search_fields = [
        'producto__codigo__icontains',
        'producto__descripcion__icontains',
        'envase__contains',
        'vol_cajam3__contains',
        'peso_bruto__contains',
        'peso_neto__contains',
        'peso_legal__contains',
        'marcasalida__descripcion__contains',
        'vitola__descripcion__contains'
    ]
    split_space_search = ' '

    class Meta:
        model = LineaSalida
        fields = [
            'producto',
            'envase',
            'vol_cajam3',
            'peso_bruto',
            'peso_neto',
            'peso_legal',
            'marcasalida',
            'vitola',
        ]

        form = LineaSalidaFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }

    def filter_by_productoactivo(self, queryset, name, value):
        if value:
            return queryset.filter(producto__activo=value)
        return queryset


# ------ ProductsCapasClaPesadas / Filter ------
class ProductsCapasClaPesadasFilter(MyGenericFilter):
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

    tipoproducto = django_filters.ModelMultipleChoiceFilter(
        label="Tipo de Producto",
        queryset=TipoProducto.objects.filter(id__in=[ChoiceTiposProd.PESADA, ChoiceTiposProd.MATERIAPRIMA]),
    )

    activo = django_filters.ChoiceFilter(
        choices=ACTIVO_CHOICES,
        empty_label=EMPTY_LABEL,
        widget=forms.Select(attrs={
            'style': 'width: 100%',
        }),
    )

    class Meta:
        model = ProductsCapasClaPesadas
        fields = [
            'codigo',
            'descripcion',
            'activo',
            'medida',
            'tipoproducto',
        ]

        form = ProductsCapasClaPesadasFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }
