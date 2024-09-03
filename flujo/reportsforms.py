from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column
from django import forms

from cruds_adminlte3.widgets import SelectWidget
from flujo.models import *
from codificadores.models import EstadoProducto
from django_select2.forms import Select2MultipleWidget


# ------------ Report Existencia / Form ------------
class ReportExistenciaForm(forms.Form):
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
            'estados',
        ]

    def __init__(self, *args, **kwargs) -> None:
        instance = kwargs.get('instance', None)
        self.user = kwargs.pop('user', None)
        self.post = kwargs.pop('post', None)
        super(ReportExistenciaForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_method = 'GET'
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                Column('departamento', css_class='form-group col-md-8 mb-0'),
                Column('estados', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
        )
