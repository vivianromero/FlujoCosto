# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import OrderedDict
from datetime import date, timedelta

from dateutil import relativedelta
from django.template.loader import render_to_string, get_template
from django.urls import reverse  # django 2.0

from django.db.models import Avg, Count, Max, Min, StdDev, Sum, Variance
from decimal import Decimal
from functools import wraps
import time
from crispy_forms.bootstrap import FormActions
from crispy_forms.layout import HTML
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _

# from rolepermissions.roles import registered_roles

ACTION_CREATE = 'create'
ACTION_DELETE = 'delete'
ACTION_DETAIL = 'detail'
ACTION_LIST = 'list'
ACTION_UPDATE = 'update'

INSTANCE_ACTIONS = (
    ACTION_DELETE,
    ACTION_DETAIL,
    ACTION_UPDATE,
)
LIST_ACTIONS = (
    ACTION_CREATE,
    ACTION_LIST,
)

ALL_ACTIONS = LIST_ACTIONS + INSTANCE_ACTIONS


def crud_url_name(model, action, prefix=None):
    """
    Returns url name for given model and action.
    """
    if prefix is None:
        prefix = ""
    app_label = model._meta.app_label
    model_lower = model.__name__.lower()
    return '%s%s_%s_%s' % (prefix, app_label, model_lower, action)


def get_fields(model, include=None):
    """
    Returns ordered dict in format 'field': 'verbose_name'
    """
    fields = OrderedDict()
    info = model._meta
    if include:  # self.model._meta.get_field(fsm_field_name)
        selected = {}
        for name in include:
            if '__' in name:
                related_model, field_name = name.split('__', 1)
                try:
                    selected[name] = info.get_field_by_name(
                        related_model)[0].related_model._meta.get_field_by_name(name)[0]
                except:
                    selected[name] = info.get_field(related_model).related_model._meta.get_field(field_name)
            else:
                try:
                    selected[name] = info.get_field_by_name(name)[0]
                except:
                    selected[name] = info.get_field(name)
    else:
        try:
            selected = {field.name: field for field in info.fields
                        if field.editable}
        except:
            # Python < 2.7
            selected = dict((field.name, field) for field in info.fields
                            if field.editable)
    for name, field in selected.items():
        if field.__class__.__name__ == 'ManyToOneRel':
            field.verbose_name = field.related_name
        fields[name] = [
            field.verbose_name.title(),
            field.get_internal_type]
    if include:
        fields = OrderedDict((key, fields[key]) for key in include)
    return fields


def crud_url(instance, action, prefix=None, namespace=None,
             additional_kwargs=None):
    """
    Shortcut function returns url for instance and action passing `pk` kwarg.

    Example:

        crud_url(author, 'update')

    Is same as:

        reverse('testapp_author_update', kwargs={'pk': author.pk})
    """
    if additional_kwargs is None:
        additional_kwargs = {}
    additional_kwargs['pk'] = instance.pk
    url = crud_url_name(instance._meta.model, action, prefix)
    if namespace:
        url = namespace + ':' + url
    return reverse(url, kwargs=additional_kwargs)


def get_related_class_field(obj, field):
    objfield = obj._meta.get_field(field)
    rf = objfield.remote_field.model
    return objfield.rel.model if hasattr(objfield, 'rel') else rf


def get_fields_aggregates(model, queryset=None, aggregates=None, include=None):
    """
    Returns ordered dict in format 'field': 'verbose_name'
    @type model: object with aggregates
    """
    fields = OrderedDict()
    info = model._meta
    field_aggregates = None
    keys = list(aggregates.keys())
    if include:  # self.model._meta.get_field(fsm_field_name)
        selected = {}
        for name in include:
            if '__' in name:
                related_model, field_name = name.split('__', 1)
                try:
                    selected[name] = \
                        info.get_field_by_name(related_model)[0].related_model._meta.get_field_by_name(name)[0]
                except:
                    selected[name] = info.get_field(related_model).related_model._meta.get_field(field_name)
            else:
                if name in queryset.query.annotations:
                    queryset.query.annotations[name].field.attname = name
                    queryset.query.annotations[name].field.verbose_name = name.replace('_', ' ')
                    selected[name] = queryset.query.annotations[name].field
                else:
                    try:
                        selected[name] = info.get_field_by_name(name)[0]
                    except:
                        selected[name] = info.get_field(name)
    else:
        try:
            selected = {field.name: field for field in info.fields
                        if field.editable}
        except:
            # Python < 2.7
            selected = dict((field.name, field) for field in info.fields
                            if field.editable)
    for name, field in selected.items():
        field_aggregates = None
        field_key = None
        this_key = None
        if field.__class__.__name__ == 'ManyToOneRel':
            field.verbose_name = field.related_name
        if queryset is not None and aggregates is not None:
            for key in keys:
                if name in aggregates[key]:
                    field_key = name + '__' + key
                    this_key = key
                    if key == 'avg':
                        field_aggregates = queryset.aggregate(Avg(name))
                    elif key == 'count':
                        field_aggregates = queryset.aggregate(Count(name))
                    elif key == 'max':
                        field_aggregates = queryset.aggregate(Max(name))
                    elif key == 'min':
                        field_aggregates = queryset.aggregate(Min(name))
                    elif key == 'stddev':
                        field_aggregates = queryset.aggregate(StdDev(name))
                    elif key == 'sum':
                        field_aggregates = queryset.aggregate(Sum(name))
                    elif key == 'variance':
                        field_aggregates = queryset.aggregate(Variance(name))
                    elif key == 'percent':
                        p = queryset.aggregate(Sum(aggregates[key][name][0]))
                        p_key = aggregates[key][name][0] + '__sum'
                        r = queryset.aggregate(Sum(aggregates[key][name][1]))
                        r_key = aggregates[key][name][1] + '__sum'
                        if p[p_key] == 0 or p[p_key] is None:
                            percent = '0.00'
                        else:
                            percent = str((r[r_key] / p[p_key]) * 100)
                            if '.' not in percent:
                                percent += '.00'
                        field_aggregates = {
                            field_key: Decimal(percent),
                        }
        if field_aggregates:
            fields[name] = [
                field.verbose_name.title(),
                field.get_internal_type,
                field_aggregates.get(field_key),
                this_key,
            ]
        else:
            fields[name] = [
                field.verbose_name.title(),
                field.get_internal_type,
            ]

    if include:
        fields = OrderedDict((key, fields[key]) for key in include)
    # stop()
    return fields


def timer(func):
    """helper function to estimate view execution time
    Use:
        .. code:: python

        @timer
        def your_view(request):
            pass
    """

    @wraps(func)  # used for copying func metadata
    def wrapper(*args, **kwargs):
        # record start time
        start = time.time()

        # func execution
        result = func(*args, **kwargs)

        duration = (time.time() - start) * 1000
        # output execution time to console
        print('view {} takes {:.2f} ms'.format(
            func.__name__,
            duration
        ))
        return result

    return wrapper


# Forms Actions
accept_and_add_other = _('Accept and add another')


def common_form_actions():
    form_actions = FormActions(
        HTML(
            get_template('cruds/actions/acept_button.html').template.source
            # """{% load i18n %}
            #     <button id="id_form_btn_acept" type="submit" class="btn btn-primary">
            #         <i class="fa fa-check"></i> {% translate 'Accept' %}
            #     </button>"""
        ),
        HTML(
            get_template('cruds/actions/acept_and_add_another_button.html').template.source
            # """{% load i18n %}
            #     {% if not url_update %}
            #         <button id="id_form_btn_add_another" type="submit" name="another" class="btn btn-primary">
            #             <i class="fa fa-plus"></i> {% translate 'Accept and add another' %}
            #         </button>
            #     {% endif %}"""
        ),
        HTML(
            get_template('cruds/actions/cancel_button.html').template.source
            # """{% load i18n %}
            #     {% if url_list %}
            #         <a href="{{ url_list }}{{ getparams }}" class="btn btn-secondary">
            #             <i class="fa fa-remove"></i> {% translate "Cancel" %}
            #         </a>
            #     {% endif %}"""
        ),
        HTML(
            get_template('cruds/actions/delete_button.html').template.source
            # """{% load i18n %}
            #     {% if url_delete %}
            #         <a href="{{ url_delete }}" class="btn btn-danger">
            #             <i class="fa fa-trash"></i> {% translate "Delete" %}
            #         </a>
            #     {% endif %}"""
        ),
    )
    return form_actions


# OK / Cancel form actions
def ok_cancel_form_actions():
    form_actions = FormActions(
        HTML(
            get_template('cruds/actions/ok_cancel_form_actions.html').template.source
            #     """{% load i18n %}
            #         <button type="submit" class="btn btn-primary">
            #             <i class="fa fa-check"></i> {% translate 'Accept' %}
            #         </button>"""
            # ),
            # HTML(
            #     """{% load i18n %}
            #         {% if url_list %}
            #             <a href="{{ url_list }}" class="btn btn-secondary">
            #                 <i class="fa fa-remove"></i> {% translate "Cancel" %}
            #             </a>
            #         {% endif %}"""
        ),
    )
    return form_actions


# Filter Forms Actions
def common_filter_form_actions():
    form_actions = FormActions(
        HTML(
            get_template('cruds/actions/common_filter_form_actions.html').template.source
            #     """{% load i18n crispy_forms_tags %}
            #         <button type="submit" class="btn btn-primary">
            #             <i class="fa fa-filter"></i> {% translate 'Filter' %}
            #         </button>"""
            # ),
            # HTML(
            #     """{% load i18n %}
            #             <a href="{{ url_list }}" class="btn btn-secondary">
            #                 <i class="fa fa-remove"></i> {% translate "Clean filter" %}
            #             </a>"""
        ),
    )
    return form_actions


# Detail Forms Actions
def common_detail_form_actions():
    form_actions = FormActions(
        HTML(
            get_template('cruds/actions/common_detail_form_actions.html').template.source
            # """{% load i18n crispy_forms_tags %}
            #    {% if url_update and 'update' in views_available and crud_perms.update %}
            #         <div class="card-header">
            #             <a href="{{ url_update }}{{getparams}}" class="btn btn-primary" >{% trans "Edit" %}</a>
            #         </div>
            #    {% endif %}"""
        ),
    )
    return form_actions


# Templates for tables

ACTIONS_TEMPLATE = '''
    {% load i18n l10n crud_tags %}
    {% crud_nurl object "update" namespace as nurl %}
    {% if nurl and 'update' in views_available and crud_perms.update or request.user == object.created_by %}
        <a href="{% url nurl record.pk %}{{ getparams }}"
           title="{% trans 'Edit' %}">
            <i class="fa-1x fa fa-edit"
               style="margin-right: 5px;"></i>
        </a>
    {% endif %}
    {% crud_nurl object "delete" namespace as nurl %}
    {% if nurl and 'delete' in views_available and crud_perms.delete or request.user == object.created_by %}
        <a id="delete_href" href="{% url nurl record.pk %}{{ getparams }}"
           class="delete_href"
           title="{% trans 'Delete' %}">
            <i id="trash_icon" class="fa-1x fa fa-trash">
            </i>
        </a>
    {% endif %}
    '''

# Attributes for tables
attrs_left_left = {
    "th": {'style': 'text-align: left;'},
    "td": {'style': 'text-align: left;'},
    "alignment": 'left'
}

attrs_right_right = {
    "th": {'style': 'text-align: right;'},
    "td": {'style': 'text-align: right;'},
    "alignment": 'right'
}

attrs_center_right = {
    "th": {'style': 'text-align: center;'},
    "td": {'style': 'text-align: right;'},
}

attrs_center_left = {
    "th": {'style': 'text-align: center;'},
    "td": {'style': 'text-align: left;'},
}

attrs_center_center = {
    "th": {'style': 'text-align: center;'},
    "td": {'style': 'text-align: center;'},
}

attrs_total_title = {
    'th': {'style': 'text-align: center;'},
    'td': {'style': 'text-align: left;'},
    'tf': {
        'style': 'text-align: center; font-weight: 700; color: #007bff;',
    },
}

attrs_total_data = {
    'th': {'style': 'text-align: center;'},
    'td': {'style': 'text-align: center;'},
    'tf': {
        'style': 'text-align: center; font-weight: 700; color: #007bff;',
    },
}


def get_current_record_htmx(model, current_url_abs_path):
    lista = current_url_abs_path.split('/')
    if lista[lista.__len__() - 1][0:6] == 'update':
        index = int(lista[lista.__len__() - 2])
        record = model.objects.get(id=index)
        return record
    return None


# def get_roles_choices():
#     list_choices = [(k, v) for k, v in registered_roles.items()]
#     final_choices = []
#     for list_choice in list_choices:
#         lst = [*list_choice]
#         words = lst[0].split('_')
#         for idx in range(words.__len__()):
#             words[idx] = words[idx].capitalize()
#         phrase = ' '.join(words)
#         lst[1] = _(phrase)
#         tpl = tuple(lst)
#         final_choices.append(tpl)
#     return final_choices

def get_data(data):
    text = "<ul>"
    for k, v in data.items():
        for el in k:
            # element = el['name']
            text += f'<li>{el}</li>'
        if isinstance(v, dict):
            text += get_data(v)  # recursively calling to get the lists
        else:  # this else block can be removed if you don't need it
            text += f'<li>{v}</li>'
    text += "</ul>"
    return text


def render_dict(data):
    text = get_data(data)
    return mark_safe(text)
