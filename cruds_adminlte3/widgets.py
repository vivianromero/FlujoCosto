from datetime import datetime
import json

from django import forms
from django.forms.utils import flatatt
from django.forms.widgets import Widget, Textarea, CheckboxSelectMultiple
from django.forms import Select
from django.utils.encoding import force_str
from django.utils.formats import get_format
from django.utils.translation import get_language
from django.template.loader import render_to_string
from django.template import loader
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import gettext_lazy as _


def cdn_media():
    """
    Devuelve las ubicaciones Tempus Dominus, incluidas por defecto.
    """
    css = {
        "all": (
            "plugins/tempusdominus-bootstrap-4/css/tempusdominus-bootstrap-4.min.css",
        )
    }

    if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
        moment = "moment-with-locales"
    else:
        moment = "moment"

    js = (
        (
            "plugins/moment/{moment}.min.js".format(moment=moment)
        ),
        (
            "plugins/tempusdominus-bootstrap-4/js/tempusdominus-bootstrap-4.min.js"
        ),
    )

    return forms.Media(css=css, js=js)


class TempusDominusMixin:
    """
    Tempus Dominus Mixin contiene funcionalidades compartidas para los tres tipos de selectores de fechas
    que se ofrecen.
    """

    def __init__(self, attrs=None, options=None, format=None):
        super().__init__()

        # Configure las opciones predeterminadas para incluir un elemento de reloj; de lo contrario,
        # el selector de fecha y hora no muestra ningún ícono para cambiar al modo de hora.
        self.js_options = {
            "format": self.get_js_format(),
            "icons": {"time": "fa fa-clock-o"},
        }
        # Si se pasa un diccionario de opciones, combínelo con las js_options preestablecidas.
        if isinstance(options, dict):
            self.js_options = {**self.js_options, **options}
        # save any additional attributes that the user defined in self
        self.attrs = attrs or {}
        self.format = format or None

    @property
    def media(self):
        if getattr(settings, "TEMPUS_DOMINUS_INCLUDE_ASSETS", True):
            return cdn_media()
        return forms.Media()

    def render(self, name, value, attrs=None, renderer=None):
        context = super().get_context(name, value, attrs)

        # self.attrs = atributos definidos por el usuario a partir de __init__
        # attrs = atributos agregados para hacer el renderizado.
        # context['attrs'] contiene una combinación de self.attrs y attrs
        # NB: Si se utiliza crispy-forms, ya contendrá 'clase': 'datepicker form-control' en el widget del DatePicker

        all_attrs = context["widget"]["attrs"]
        all_attrs["id"] = all_attrs["id"].replace('-', '_')
        cls = all_attrs.get("class", "")
        if "form-control" not in cls:
            cls = "form-control " + cls

        # Agregar el atributo que hace que la ventana emergente del selector de fecha se cierre
        # cuando se pierde el foco
        cls += " datetimepicker-input"
        all_attrs["class"] = cls

        # valores predeterminados para los atributos del widget
        input_toggle = True
        icon_toggle = True
        input_group = True
        append = ""
        prepend = ""
        size = ""

        attr_html = ""
        for attr_key, attr_value in all_attrs.items():
            if attr_key == "prepend":
                prepend = attr_value
            elif attr_key == "append":
                append = attr_value
            elif attr_key == "input_toggle":
                input_toggle = attr_value
            elif attr_key == "input_group":
                input_group = attr_value
            elif attr_key == "icon_toggle":
                icon_toggle = attr_value
            elif attr_key == "size":
                size = attr_value
            elif attr_key == "icon_toggle":
                icon_toggle = attr_value
            else:
                attr_html += ' {key}="{value}"'.format(key=attr_key, value=attr_value)

        options = {}
        options.update(self.js_options)

        if (
                getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False) and
                "locale" not in self.js_options
        ):
            options["locale"] = get_language()

        if context["widget"]["value"] is not None:
            # Agregar una opción para establecer el valor del datepicker usando un objeto Javascript de moment
            options.update(self.moment_option(value))

        # el picker_id a continuación debe cambiarse a guiones bajos, porque los guiones no son válidos
        # en los nombres de funciones JS.
        field_html = render_to_string(
            "tempus_dominus/widget.html",
            {
                "type": context["widget"]["type"],
                "picker_id": context["widget"]["attrs"]["id"].replace("-", "_"),
                "name": context["widget"]["name"],
                "attrs": mark_safe(attr_html),
                "js_options": mark_safe(json.dumps(options)),
                "prepend": prepend,
                "append": append,
                "icon_toggle": icon_toggle,
                "input_toggle": input_toggle,
                "input_group": input_group,
                "size": size,
            },
        )

        return mark_safe(force_str(field_html))

    def moment_option(self, value):
        """
        Devuelve un diccionario para establecer la fecha y/u hora predeterminada usando un objeto moment javascript.
        Cuando se crea una instancia de un formulario por primera vez, el valor es una fecha, hora o un
        objeto de fecha y hora, pero después de que se haya enviado un formulario con un error y es renderizado
        nuevamente, el valor contiene una cadena formateada que se debe parsear a un objeto de fecha.
        """
        if isinstance(value, str):
            if isinstance(self, DatePicker):
                formats = [self.format] if self.format else get_format(
                    "DATE_INPUT_FORMATS"
                )
            elif isinstance(self, TimePicker):
                formats = [self.format] if self.format else get_format(
                    "TIME_INPUT_FORMATS"
                )
            else:
                formats = [self.format] if self.format else get_format(
                    "DATETIME_INPUT_FORMATS"
                )
            for fmt in formats:
                try:
                    value = datetime.strptime(value, fmt)
                    if isinstance(self, TimePicker):
                        # strptime devuelve una fecha; el tiempo puede extraerse del valor obtenido.
                        value = value.time()
                    break
                except (ValueError, TypeError):
                    continue
            else:
                return {}

        # Agregar una opción para establecer el valor del datepicker usando una cadena con formato iso
        iso_date = value.isoformat()

        # el formato iso para la hora requiere una T antepuesta
        if isinstance(self, TimePicker):
            iso_date = "T" + iso_date

        return {"date": iso_date}

    def get_js_format(self):
        raise NotImplementedError


class DatePicker(TempusDominusMixin, forms.widgets.DateInput):
    """
    Widget for Tempus Dominus DatePicker.
    """

    def get_js_format(self):
        if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
            js_format = "L"
        else:
            js_format = getattr(settings, "TEMPUS_DOMINUS_DATE_FORMAT", "YYYY-MM-DD")
        return js_format


class DateTimePicker(TempusDominusMixin, forms.widgets.DateTimeInput):
    """
    Widget for Tempus Dominus DateTimePicker.
    """

    def get_js_format(self):
        if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
            js_format = "L LTS"
        else:
            js_format = getattr(settings, "TEMPUS_DOMINUS_DATETIME_FORMAT", "YYYY-MM-DD HH:mm:ss")
        return js_format


class TimePicker(TempusDominusMixin, forms.widgets.TimeInput):
    """
    Widget for Tempus Dominus TimePicker.
    """

    def get_js_format(self):
        if getattr(settings, "TEMPUS_DOMINUS_LOCALIZE", False):
            js_format = "LTS"
        else:
            js_format = getattr(settings, "TEMPUS_DOMINUS_TIME_FORMAT", "HH:mm:ss")
        return js_format


class DatePickerWidget(Widget):
    template_name = 'widgets/datepicker.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        if 'format' not in context:
            context['format'] = 'mm/dd/yyyy'
        if 'mode' not in context:
            context['mode'] = 0
        context['djformat'] = settings.DATE_FORMAT
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class TimePickerWidget(Widget):
    template_name = 'widgets/timepicker.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        if 'format' not in context:
            context['format'] = 'HH:ii P'
        context['djformat'] = settings.TIME_FORMAT
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class DateTimePickerWidget(Widget):
    template_name = 'widgets/datetimepicker.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value

        if 'format' not in context:
            context['format'] = 'mm/dd/yyyy hh:ii:ss'
        context['djformat'] = settings.DATETIME_FORMAT

        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class ColorPickerWidget(Widget):
    template_name = 'widgets/colorpicker.html'

    def get_context(self, name, value, attrs=None):
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class CKEditorWidget(Textarea):
    template_name = 'widgets/ckeditor.html'

    def get_context(self, name, value, attrs=None):
        self.attrs['flatatt'] = flatatt(self.attrs)
        context = dict(self.attrs.items())
        if attrs is not None:
            context.update(attrs)
        context['name'] = name
        if value is not None:
            context['value'] = value
        return context

    def render(self, name, value, attrs=None, renderer=None):
        context = self.get_context(name, value, attrs)
        return mark_safe(loader.render_to_string(self.template_name, context))


class CustomRelatedFieldWidgetWrapper(RelatedFieldWidgetWrapper):
    """
        Based on RelatedFieldWidgetWrapper, this does the same thing
        outside of the admin interface

        the parameters for a relation and the admin site are replaced
        by a url for the add operation
    """

    def __init__(self, widget, add_url, permission=True):
        super(CustomRelatedFieldWidgetWrapper, self).__init__()
        self.widget = widget
        self.is_hidden = widget.is_hidden
        self.needs_multipart_form = widget.needs_multipart_form
        self.attrs = widget.attrs
        self.choices = widget.choices
        self.add_url = add_url
        self.permission = permission

    def render(self, name, value, *args, **kwargs):
        self.widget.choices = self.choices
        output = [self.widget.render(name, value, *args, **kwargs)]
        if self.permission:
            output.append(
                u'<a href="%s" class="add-another" id="add_id_%s" onclick="return showAddAnotherPopup(this);"> ' % \
                (self.add_url, name))
            output.append(u'<img src="%simg/admin/icon_addlink.gif" width="10" height="10" alt="%s"/></a>' % (
                settings.ADMIN_MEDIA_PREFIX, _('Add Another')))
        return mark_safe(u''.join(output))


class SelectWidget(Select):
    """
    Subclass of Django's select widget that allows disabling options.
    """

    def __init__(self, *args, **kwargs):
        self._disabled_choices = []
        self._enabled_choices = []
        super(SelectWidget, self).__init__(*args, **kwargs)

    @property
    def disabled_choices(self):
        return self._disabled_choices

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    @property
    def enabled_choices(self):
        return self._enabled_choices

    @enabled_choices.setter
    def enabled_choices(self, other):
        self._enabled_choices = other

    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option_dict = super(SelectWidget, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if (value in self.disabled_choices) or (self._enabled_choices and value not in self.enabled_choices):
            option_dict['attrs']['disabled'] = 'disabled'
        return option_dict


class MyCheckboxSelectMultiple(CheckboxSelectMultiple):

    def __init__(self, *args, **kwargs):
        self._disabled_choices = []
        self._enabled_choices = []
        super(MyCheckboxSelectMultiple, self).__init__(*args, **kwargs)

    @property
    def disabled_choices(self):
        return self._disabled_choices

    @disabled_choices.setter
    def disabled_choices(self, other):
        self._disabled_choices = other

    @property
    def enabled_choices(self):
        return self._enabled_choices

    @enabled_choices.setter
    def enabled_choices(self, other):
        self._enabled_choices = other

    def render(self, name, value, attrs=None, renderer=None):
        return super().render(name=name, value=value)

    def create_option(
            self, name, value, label, selected, index, subindex=None, attrs=None
    ):
        option_dict = super(MyCheckboxSelectMultiple, self).create_option(
            name, value, label, selected, index, subindex=subindex, attrs=attrs
        )
        if (value in self.disabled_choices) or (self._enabled_choices and value not in self.enabled_choices):
            option_dict['attrs']['disabled'] = 'disabled'
        return option_dict


class MyDateInput(forms.DateInput):
    input_type = 'date'
