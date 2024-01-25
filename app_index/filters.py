import decimal
import math
import json

import django_filters
from bootstrap_daterangepicker.fields import DateRangeField
from django_filters.filters import _truncate, ChoiceFilter, RangeFilter
from django.utils.translation import gettext as _
from django.utils.timezone import now
from datetime import timedelta


class CustomDateFromToRangeFilter(django_filters.DateFromToRangeFilter):
    field_class = DateRangeField

    def filter(self, qs, value):
        if value:
            if value[0] is not None and value[1] is not None:
                self.lookup_expr = "range"
                # value = (value.start, value.stop)
            elif value[0] is not None:
                self.lookup_expr = "gte"
                value = value[0]
            elif value[1] is not None:
                self.lookup_expr = "lte"
                value = value[1]
            else:
                return qs

        if self.distinct:
            qs = qs.distinct()
        lookup = "%s__%s" % (self.field_name, self.lookup_expr)
        qs = self.get_method(qs)(**{lookup: value})
        return qs


class MyDateRangeFilter(django_filters.DateRangeFilter):
    choices = django_filters.DateRangeFilter.choices
    filters = django_filters.DateRangeFilter.filters

    choices.insert(3, ("two_weeks", _("Past 2 weeks")), )
    choices.insert(4, ("last_month", _("Past 30 days")), )

    filters.update(
        {
            "two_weeks": lambda qs, name: qs.filter(
                **{
                    "%s__gte" % name: _truncate(now() - timedelta(days=14)),
                    "%s__lt" % name: _truncate(now() + timedelta(days=1)),
                }
            ),
            "last_month": lambda qs, name: qs.filter(
                **{
                    "%s__gte" % name: _truncate(now() - timedelta(days=30)),
                    "%s__lt" % name: _truncate(now() + timedelta(days=1)),
                }
            ),
        }
    )


class DateClosingFilter(ChoiceFilter):
    choices = [
        ("closed", _("Closed")),
        ("unclosed", _("Unclosed")),
    ]

    filters = {
        "closed": lambda qs, name: qs.filter(
            **{
                "%s__isnull" % name: False,
            }
        ),
        "unclosed": lambda qs, name: qs.filter(
            **{
                "%s__isnull" % name: True,
            }
        ),
    }

    def __init__(self, choices=None, filters=None, *args, **kwargs):
        if choices is not None:
            self.choices = choices
        if filters is not None:
            self.filters = filters

        unique = set([x[0] for x in self.choices]) ^ set(self.filters)
        assert not unique, (
                "Keys must be present in both 'choices' and 'filters'. Missing keys: "
                "'%s'" % ", ".join(sorted(unique))
        )

        # null choice not relevant
        kwargs.setdefault("null_label", None)
        super().__init__(choices=self.choices, *args, **kwargs)

    def filter(self, qs, value):
        if not value:
            return qs

        assert value in self.filters

        qs = self.filters[value](qs, self.field_name)
        return qs.distinct() if self.distinct else qs
