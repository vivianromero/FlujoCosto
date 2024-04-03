from django.forms.utils import flatatt
from django.forms.widgets import Widget, Textarea, CheckboxSelectMultiple
from django.forms import Select
from django.template import loader
from django.utils.safestring import mark_safe
from django.conf import settings
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from django.utils.translation import gettext_lazy as _


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
