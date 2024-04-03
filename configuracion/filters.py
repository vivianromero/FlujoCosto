import django_filters
from django.utils.translation import gettext as _

from cruds_adminlte3.filter import MyGenericFilter
from .forms import *
from .models import *


# ------ ConexionBaseDato / Filter ------
class ConexionBaseDatoFilter(MyGenericFilter):
    search_fields = [
        'sistema__icontains',
        'database_name__icontains',
        'unidadcontable__codigo__icontains',
    ]
    split_space_search = ' '

    sistema = django_filters.CharFilter(
        label=_("System"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    database_name = django_filters.CharFilter(
        label=_("Database Name"),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = ConexionBaseDato
        fields = [
            'sistema',
            'database_name',
            'host',
            'port',
            'database_user',
            'password',
            'unidadcontable',
        ]

        form = ConexionBaseDatoFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }
