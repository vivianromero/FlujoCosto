import django_filters
from bootstrap_datepicker_plus.widgets import DatePickerInput
from django import forms
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from django_filters.widgets import SuffixedMultiWidget

from .forms import UserUebFormFilter
from configuracion.models import UserUeb


class MyRangeWidget(SuffixedMultiWidget):
    template_name = "django_filters/widgets/multiwidget.html"
    suffixes = ["after", "before"]

    def __init__(self, attrs=None):
        widgets = (
            DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "es",
                    "showTodayButton": False,
                },
            ),
            DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    "locale": "es",
                    "showTodayButton": False,
                },
            )
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]


class UserUebFilter(django_filters.FilterSet):

    first_name = django_filters.CharFilter(
        label=_('First name'),
        widget=forms.TextInput(),
        lookup_expr='icontains',
        field_name='iduser.first_name',
    )

    last_name = django_filters.CharFilter(
        label=_('Last name'),
        widget=forms.TextInput(),
        lookup_expr='icontains',
        field_name='iduser.last_name',
    )

    username = django_filters.CharFilter(
        label=_('User name'),
        widget=forms.TextInput(),
        lookup_expr='icontains',
        field_name='iduser.username',
    )

    email = django_filters.CharFilter(
        label=_('User name'),
        widget=forms.TextInput(),
        lookup_expr='icontains',
        field_name='iduser.email',
    )

    last_login = django_filters.DateFromToRangeFilter(
        widget=MyRangeWidget(),
        label=_('Last login'),
        field_name='iduser.last_login',
    )

    date_joined = django_filters.DateFromToRangeFilter(
        widget=MyRangeWidget(),
        label=_('Date joined'),
        field_name='iduser.date_joined',
    )

    is_superuser = django_filters.BooleanFilter(
        label=_('Is superuser?'),
        field_name='iduser.is_superuser',
    )

    is_staff = django_filters.BooleanFilter(
        label=_('Is staff?'),
        field_name='iduser.is_staff',
    )

    is_active = django_filters.BooleanFilter(
        label=_('Is active?'),
        field_name='iduser.is_active',
    )

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

    class Meta:
        model = UserUeb
        fields = [
            'query',
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

    @staticmethod
    def universal_search(queryset, name, value):

        search_fields = [
            'username__icontains',
            'email__icontains',
            'nombre__icontains',
            'last_login__icontains',
        ]

        flt = None
        for field in search_fields:
            if flt is None:
                flt = Q(**{field: value})
            else:
                flt |= Q(**{field: value})

        return queryset.filter(flt)