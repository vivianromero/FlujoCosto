import math

import six
from django import forms
from django.core.exceptions import FieldDoesNotExist
from django.db.models import Q
from django.forms.models import modelform_factory
from django.db import models
from django.utils.translation import gettext_lazy as _
from bootstrap_datepicker_plus.widgets import DatePickerInput
from bootstrap_daterangepicker.fields import DateRangeField
from datetime import date, datetime, timedelta
from django.utils.timezone import now
import django_filters
from django_filters import ChoiceFilter
from django_filters.filters import _truncate, RangeFilter
from django_filters.widgets import SuffixedMultiWidget


class FormFilter:
    form = None

    def __init__(self, request, form=None):
        if form:
            self.form = form
        self.request = request
        self.form_instance = self.form(request.GET)
        for key in self.form_instance.fields:
            self.form_instance.fields[key].required = False
        self.form_instance.is_valid()
        self.form_instance._errors = {}

    def get_cleaned_fields(self):
        values = {}
        for value in self.form_instance.cleaned_data:
            rq_value = self.request.GET.get(value, '')
            if value and rq_value:
                data_value = self.form_instance.cleaned_data[value]
                if type(data_value) == models.QuerySet:
                    if data_value.count() == 1:
                        data_value = data_value.first()
                    elif '__in' not in value:
                        value = value + '__in'
                values[value] = data_value
        return values

    def render(self):
        return self.form_instance

    def get_filter(self, queryset):
        clean_value = self.get_cleaned_fields()
        if clean_value:
            queryset = queryset.filter(**clean_value)
        return queryset

    def get_build_param(self, value, data, params):
        if isinstance(data, models.base.Model):
            data = str(data.pk)
        params.append("%s=%s" % (value, str(data)))
        return params

    def get_params(self, exclude=[]):
        params = []
        for value in self.form_instance.cleaned_data:
            if value in exclude:
                continue
            rq_value = self.request.GET.get(value, '')
            if rq_value:
                data = self.form_instance.cleaned_data[value]
                if type(data) == models.QuerySet:
                    for q in data:
                        params = self.get_build_param(value, q, params)
                else:
                    params = self.get_build_param(value, data, params)
        return params


def get_filters(model, list_filter, request):
    fields = []
    forms = []
    for field in list_filter:
        if type(field) in [six.string_types, six.text_type, six.binary_type]:
            # this is a model field
            try:
                model._meta.get_field(field)
                fields.append(field)
            except FieldDoesNotExist:
                pass
        else:
            forms.append(field(request))

    if fields:
        form = modelform_factory(model, fields=fields)
        forms.insert(0, FormFilter(request, form=form))

    return forms


def get_filter_fields(cur_model, filter_fields=None):
    class GenericFilter(django_filters.FilterSet):

        class Meta:
            model = cur_model
            if filter_fields is not None:
                fields = filter_fields
            else:
                exclude = '__all__'

            filter_overrides = {
                models.CharField: {
                    'filter_class': django_filters.CharFilter,
                    'extra': lambda f: {
                        'lookup_expr': 'icontains',
                    },
                },
                models.DateField: {
                    'filter_class': django_filters.DateFromToRangeFilter,
                    # 'filter_class': django_filters.CharFilter,
                    #    'extra': lambda f: {
                    #     'widget': DatePickerInput(),
                    # },
                },
                models.ForeignKey: {
                    'filter_class': django_filters.ModelMultipleChoiceFilter,
                    'extra': lambda f: {
                        'queryset': django_filters.filterset.remote_queryset(f),
                    }
                },
                # models.ForeignKey: {
                #     'filter_class': django_filters.CharFilter,
                #     'extra': lambda f: {
                #         'lookup_expr': 'icontains',
                #     },
                # },
                models.DecimalField: {
                    'filter_class': django_filters.RangeFilter
                    # 'filter_class': django_filters.CharFilter,
                    # 'extra': lambda f: {
                    #     'lookup_expr': 'icontains',
                    # },
                },
                models.IntegerField: {
                    'filter_class': django_filters.RangeFilter
                    # 'filter_class': django_filters.CharFilter,
                    # 'extra': lambda f: {
                    #     'lookup_expr': 'icontains',
                    # },
                },
                models.TextChoices: {
                    'filter_class': django_filters.ModelMultipleChoiceFilter,
                    # 'filter_class': django_filters.CharFilter,
                    # 'extra': lambda f: {
                    #     'lookup_expr': 'icontains',
                    # },
                },
                models.SmallIntegerField: {
                    'filter_class': django_filters.ModelMultipleChoiceFilter,
                    # 'filter_class': django_filters.CharFilter,
                    # 'extra': lambda f: {
                    #     'lookup_expr': 'icontains',
                    # },
                }
            }

    return GenericFilter


class MyGenericFilter(django_filters.FilterSet):
    search_fields = []
    split_space_search = ' '

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
        fields = [
            'query',
        ]

        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            # models.DateField: {
            #     'filter_class': django_filters.DateFromToRangeFilter,
            #     # 'filter_class': django_filters.CharFilter,
            #     #    'extra': lambda f: {
            #     #     'widget': DatePickerInput(),
            #     # },
            # },
            models.ForeignKey: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                'extra': lambda f: {
                    'queryset': django_filters.filterset.remote_queryset(f),
                }
            },
            # models.ForeignKey: {
            #     'filter_class': django_filters.CharFilter,
            #     'extra': lambda f: {
            #         'lookup_expr': 'icontains',
            #     },
            # },
            models.DecimalField: {
                'filter_class': django_filters.RangeFilter
                # 'filter_class': django_filters.CharFilter,
                # 'extra': lambda f: {
                #     'lookup_expr': 'icontains',
                # },
            },
            models.IntegerField: {
                'filter_class': django_filters.RangeFilter
                # 'filter_class': django_filters.CharFilter,
                # 'extra': lambda f: {
                #     'lookup_expr': 'icontains',
                # },
            },
            models.TextChoices: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                # 'filter_class': django_filters.CharFilter,
                # 'extra': lambda f: {
                #     'lookup_expr': 'icontains',
                # },
            },
            models.SmallIntegerField: {
                'filter_class': django_filters.ModelMultipleChoiceFilter,
                # 'filter_class': django_filters.CharFilter,
                # 'extra': lambda f: {
                #     'lookup_expr': 'icontains',
                # },
            }
        }

    def __int__(self, search_fields=None, split_space_search=None):
        self.search_fields = search_fields or None
        self.split_space_search = split_space_search or None

    def universal_search(self, queryset, name, value):
        flt = None
        if self.split_space_search:
            value = value.split(self.split_space_search)
        elif value:
            value = [value]
        for field in self.search_fields:
            for val in value:
                if flt is None:
                    flt = Q(**{field: val})
                else:
                    flt |= Q(**{field: val})

        return queryset.filter(flt)

    @staticmethod
    def my_range_queryset(queryset, name, value):
        qset = None
        if value.start and not value.stop:
            qset = Q(('%s__gte' % name, value.start))
        elif value.stop and not value.start:
            qset = Q(('%s__lte' % name, value.stop))
        elif value.start and value.stop:
            qset = Q(('%s__gte' % name, value.start)) & Q(('%s__lte' % name, value.stop))
        if qset:
            return queryset.filter(qset)
        else:
            return queryset

    @staticmethod
    def my_date_range_queryset(queryset, name, value):
        date_str1 = value.split('-')[0].strip()
        date_str2 = value.split('-')[1].strip()
        date_start = datetime.strptime(date_str1, "%d/%m/%Y").date()
        date_stop = datetime.strptime(date_str2, "%d/%m/%Y").date()
        qset = None
        if date_start and not date_stop:
            qset = Q(('%s__gte' % name, date_start))
        elif date_stop and not date_start:
            qset = Q(('%s__lte' % name, date_stop))
        elif date_start and date_stop:
            qset = Q(('%s__gte' % name, date_start)) & Q(('%s__lte' % name, date_stop))
        if qset:
            return queryset.filter(qset)
        else:
            return queryset
