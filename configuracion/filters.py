import django_filters

from cruds_adminlte3.filter import MyGenericFilter
from .forms import *
from .models import *


# ------ Departamento / Filter ------
# class UebFilter(MyGenericFilter):
#     search_fields = [
#         'idunidadcontable__nombre__contains',
#     ]
#     split_space_search = ' '
#
#     class Meta:
#         model = Ueb
#         fields = [
#             'query',
#             'idunidadcontable',
#         ]
#
#         form = UebFormFilter
#
#         filter_overrides = {
#             models.ForeignKey: {
#                 'filter_class': django_filters.ModelMultipleChoiceFilter,
#                 'extra': lambda f: {
#                     'queryset': django_filters.filterset.remote_queryset(f),
#                 }
#             },
#         }


# ------ User UEB / Filter ------
class UserUebFilter(MyGenericFilter):
    search_fields = [
        'idueb__idunidadcontable__nombre__icontains',
        'username__icontains',
    ]
    split_space_search = ' '

    class Meta:
        model = UserUeb
        fields = [
            'idueb',
            'username',
        ]

        form = UserUebFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }