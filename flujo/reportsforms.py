from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms

from cruds_adminlte3.widgets import SelectWidget
from flujo.models import *
from codificadores.models import EstadoProducto
from django_select2.forms import Select2MultipleWidget
from app_index.widgets import MyCustomDateRangeWidget
from datetime import date


# ------------ Report Existencia / Form ------------
class ReportForm(forms.Form):
    ESTADO_CHOICES = [(0, '--Todos--')] + list(EstadoProducto.choices)
    departamento = forms.ModelChoiceField(
        queryset=Departamento.objects.all(),
        label="Departamento",
        required=True,
        widget=SelectWidget(attrs={
            'style': 'width: 100%;',
        }
        )
    )

    fechai = forms.DateField(
        widget=MyCustomDateRangeWidget(
            format='%d/%m/%Y',
            picker_options={
                'showDropdowns': True,
                'format': 'DD/MM/YYYY',
                'singleDatePicker': True,
                'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
            },
        ),
        input_formats=['%d/%m/%Y'],
        label = 'Desde',
    )

    fechaf = forms.DateField(
        widget=MyCustomDateRangeWidget(
            format='%d/%m/%Y',
            picker_options={
                'showDropdowns': True,
                'format': 'DD/MM/YYYY',
                'singleDatePicker': True,
                'maxDate': date.today().strftime('%d/%m/%Y'),  # TODO Fecha no puede ser mayor que la fecha actual
            },
        ),
        input_formats=['%d/%m/%Y'],
        label='Hasta',
    )

    producto = forms.ModelChoiceField(
        queryset=ProductoFlujo.objects.all(),
        label="Producto",
        required=False,
        widget=SelectWidget(attrs={
            'style': 'width: 100%;',
        }),
        empty_label="---Todos---"
    )

    estados = forms.MultipleChoiceField(
        choices=ESTADO_CHOICES,
        required=False,
        widget=Select2MultipleWidget,
        label="Selecciona los estados",
        initial=[0]
    )

    class Meta:
        fields = [
            'departamento',
            'fechai',
            'fechaf',
            'estados',
            'producto',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ReportForm, self).__init__(*args, **kwargs)

        self.fields['fechai'].initial = date.today().replace(day=1)
        self.fields['fechai'].widget.attrs['readonly'] = True

        self.fields['fechaf'].initial = date.today()
        self.fields['fechaf'].widget.attrs['readonly'] = True

        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('fechai', css_class='form-group col-md-2 mb-0'),
                Column('fechaf', css_class='form-group col-md-2 mb-0'),
                Column('departamento', css_class='form-group col-md-8 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('producto', css_class='form-group col-md-8 mb-0'),
                Column('estados', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )

    def clean(self):
        cleaned_data = super().clean()
        fechai = cleaned_data.get("fechai")
        fechaf = cleaned_data.get("fechaf")

        if fechai and fechaf and fechai > fechaf:
            msg = 'La fecha Hasta debe ser mayor que la fecha Desde'
            self.add_error('fechaf', msg)
        return cleaned_data

