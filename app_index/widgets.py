from datetime import date, timedelta

from bootstrap_datepicker_plus.widgets import DatePickerInput
from bootstrap_daterangepicker import widgets as drp_widgets
from bootstrap_daterangepicker.widgets import format_to_js_re, format_to_js, add_month
from django.utils.translation import gettext as _
from django_filters.widgets import SuffixedMultiWidget, RangeWidget


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


class MyCustomRangeWidget(RangeWidget):
    template_name = "app_index/widgets/my_custom_range_widget.html"


class MyCustomDateRangeWidget(drp_widgets.DateRangeWidget):
    template_name = 'app_index/daterangepicker/daterangepicker.html'

    def get_context(self, name, value, attrs):
        date_format = format_to_js_re.sub(lambda m: format_to_js[m.group()], self._get_format())
        self.picker_options.update(
            {
                'locale':
                    {
                        'format': date_format,
                        'applyLabel': 'Aceptar',
                        'cancelLabel': "Cancelar",
                        'weekLabel': _('S'),
                        'customRangeLabel': 'Rango personalizado'
                    }
            }
        )

        if 'singleDatePicker' in self.picker_options and self.picker_options['singleDatePicker']:
            value = self._format_date_value(value)

        if 'use_ranges' in self.picker_options and self.picker_options['use_ranges']:
            start_date = date.today()
            one_day = timedelta(days=1)
            past_year = start_date.year - 1
            formating = '%d/%m/%Y'
            self.picker_options['ranges'] = {
                'Hoy': (start_date.strftime(formating), start_date.strftime(formating)),
                'Ayer': (
                    (start_date - one_day).strftime(formating), (start_date - one_day).strftime(formating)),
                'Esta semana': ((start_date - timedelta(days=start_date.weekday())).strftime(formating),
                                 start_date.strftime(formating)),
                'Última semana': ((start_date - timedelta(days=start_date.weekday() + 7)).strftime(formating),
                                 (start_date - timedelta(days=start_date.weekday() + 1)).strftime(formating)),
                'Semana atrás': ((start_date - timedelta(days=7)).strftime(formating), start_date.strftime(formating)),
                'Este mes': ((start_date.replace(day=1)).strftime(formating), start_date.strftime(formating)),
                'Últim mes': ((add_month(start_date.replace(day=1), -1)).strftime(formating),
                                  (start_date.replace(day=1) - one_day).strftime(formating)),
                '3 meses atrás': ((add_month(start_date, -3)).strftime(formating), start_date.strftime(formating)),
                'Año atrás': ((add_month(start_date, -12)).strftime(formating), start_date.strftime(formating)),
                'Este año': (
                    (start_date.replace(day=1, month=1)).strftime(formating), start_date.strftime(formating)),
                _('Año pasado'): (
                    (start_date.replace(day=1, month=1, year=past_year)).strftime(formating),
                    (start_date.replace(day=31, month=12, year=past_year)).strftime(formating)
                ),
            }

        return super().get_context(name, value, attrs)
