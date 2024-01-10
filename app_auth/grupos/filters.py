import django_filters
from django import forms
from django.contrib.auth.models import Group
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .forms import GroupFormFilter


class GroupFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(
        method="universal_search",
        label=_("Universal Search"),
        widget=forms.TextInput(
            attrs={
                "placeholder": _("Search..."),
                'class': 'form-control',
                'type': 'search',
                'aria-label': 'Search',
            }
        ),
    )

    name = django_filters.CharFilter(
        label=_('Name'),
        widget=forms.TextInput(),
        lookup_expr='icontains',
    )

    class Meta:
        model = Group
        fields = [
            'query',
            'permissions',
        ]

        form = GroupFormFilter

        filter_overrides = {
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
        }

    @staticmethod
    def universal_search(queryset, name, value):

        search_fields = [
            'name__icontains',
            'permissions__name__icontains',
        ]

        flt = None
        for field in search_fields:
            if flt is None:
                flt = Q(**{field: value})
            else:
                flt |= Q(**{field: value})
        return queryset.filter(flt)
