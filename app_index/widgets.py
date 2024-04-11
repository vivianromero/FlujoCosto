from datetime import date, timedelta

from bootstrap_datepicker_plus.widgets import DatePickerInput
from bootstrap_daterangepicker import widgets as drp_widgets
from bootstrap_daterangepicker.widgets import format_to_js_re, format_to_js, add_month
from django.utils.translation import gettext as _
from django_filters.widgets import SuffixedMultiWidget


class MyRangeWidget(SuffixedMultiWidget):
    template_name = "django_filters/widgets/multiwidget.html"
    suffixes = ["after", "before"]
    is_localized = True

    def __init__(self, attrs=None):
        widgets = (
            DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    # "locale": get_language(),
                    "showTodayButton": False,
                }

            ),
            DatePickerInput(
                options={
                    "format": "DD/MM/YYYY",
                    # "locale": get_language(),
                    "showTodayButton": False,
                },
            )
        )
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.start, value.stop]
        return [None, None]


class MyCustomDateRangeWidget(drp_widgets.DateRangeWidget):

    def get_context(self, name, value, attrs):
        date_format = format_to_js_re.sub(lambda m: format_to_js[m.group()], self._get_format())
        self.picker_options.update(
            {
                'locale':
                    {
                        'format': date_format,
                        'applyLabel': _('Apply'),
                        'cancelLabel': _("Clear"),
                        'weekLabel': _('W'),
                        'customRangeLabel': _('Custom Range')
                    }
            }
        )

        if 'use_ranges' in self.picker_options and self.picker_options['use_ranges']:
            start_date = date.today()
            one_day = timedelta(days=1)
            past_year = start_date.year - 1
            formating = '%d/%m/%Y'
            self.picker_options['ranges'] = {
                _('Today'): (start_date.strftime(formating), start_date.strftime(formating)),
                _('Yesterday'): (
                    (start_date - one_day).strftime(formating), (start_date - one_day).strftime(formating)),
                _('This week'): ((start_date - timedelta(days=start_date.weekday())).strftime(formating),
                                 start_date.strftime(formating)),
                _('Last week'): ((start_date - timedelta(days=start_date.weekday() + 7)).strftime(formating),
                                 (start_date - timedelta(days=start_date.weekday() + 1)).strftime(formating)),
                _('Week ago'): ((start_date - timedelta(days=7)).strftime(formating), start_date.strftime(formating)),
                _('This month'): ((start_date.replace(day=1)).strftime(formating), start_date.strftime(formating)),
                _('Last month'): ((add_month(start_date.replace(day=1), -1)).strftime(formating),
                                  (start_date.replace(day=1) - one_day).strftime(formating)),
                _('3 months ago'): ((add_month(start_date, -3)).strftime(formating), start_date.strftime(formating)),
                _('Year ago'): ((add_month(start_date, -12)).strftime(formating), start_date.strftime(formating)),
                _('This year'): (
                    (start_date.replace(day=1, month=1)).strftime(formating), start_date.strftime(formating)),
                _('Last year'): (
                    (start_date.replace(day=1, month=1, year=past_year)).strftime(formating),
                    (start_date.replace(day=31, month=12, year=past_year)).strftime(formating)
                ),
            }

        return super().get_context(name, value, attrs)
