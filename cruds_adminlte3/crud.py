# encoding: utf-8
import json
import types

import sweetify
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.messages.views import SuccessMessageMixin
from sweetify.views import SweetifySuccessMixin
from django.db.models import ProtectedError
from django.db.models.query_utils import Q
from django.forms import Select, SelectMultiple
from django.http.response import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import re_path, include
from django.urls.base import reverse_lazy, reverse
from django.urls.exceptions import NoReverseMatch
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import (ListView, CreateView, DeleteView,
                                  UpdateView, DetailView)
from django.views.generic.edit import FormMixin, ModelFormMixin
from django_filters.views import FilterView
from django_tables2 import RequestConfig
from django_tables2.export import ExportMixin, TableExport
from django_tables2.views import SingleTableMixin
from extra_views import CreateWithInlinesView, UpdateWithInlinesView
from tablib import Dataset

# Own imports
from cruds_adminlte3 import utils
from cruds_adminlte3.domains import (
    normalize_domain,
    prefix_to_infix
)
from cruds_adminlte3.filter import get_filters, get_filter_fields
from utiles.utils import message_error
from .config import CONFIG

User = get_user_model()


class MyTableExport(TableExport):

    def table_to_dataset(self, table, exclude_columns, dataset_kwargs=None):
        """Transform a table to a tablib dataset."""

        def default_dataset_title():
            try:
                return table.Meta.model._meta.verbose_name_plural.title()
            except AttributeError:
                return "Export Data"

        kwargs = {"title": default_dataset_title()}
        kwargs.update(dataset_kwargs or {})
        dataset = Dataset(**kwargs)
        for i, row in enumerate(table.as_values(exclude_columns=exclude_columns)):
            if i == 0:
                dataset.headers = row
            else:
                dataset.append(row)
        if 'footer' in kwargs and kwargs['footer']:
            dataset.append(kwargs['footer'])
        return dataset


class CRUDMixin(object):
    def get_template_names(self):
        dev = []
        base_name = "%s/%s/" % (self.model._meta.app_label,
                                self.model.__name__.lower())
        dev.append(base_name + self.template_name)
        dev.append(self.template_name)
        base = self.template_name.split("/")[-1]
        dev.append("cruds/" + base)

        return dev

    def get_search_fields(self, context):
        try:
            context['search'] = self.search_fields
        except AttributeError:
            context['search'] = False
        if self.view_type == 'list' and 'q' in self.request.GET:
            context['q'] = self.request.GET.get('q', '')
        if self.view_type == 'list' and 'query' in self.request.GET:
            context['query'] = self.request.GET.get('query', '')

    def get_filters(self, context):
        filter_params = []
        active_filters = False
        if self.view_type == 'list' and self.list_filter:
            filters = get_filters(self.model, self.list_filter, self.request)
            context['filters'] = filters
            for filter in filters:
                param = filter.get_params(self.related_fields or [])
                if param:
                    filter_params += param

        elif self.view_type in ['list'] and self.filter_fields:
            if self.filterset_class(self.request.GET).form.changed_data:
                active_filters = self.filterset_class(self.request.GET).form.changed_data != []
            else:
                active_filters = self.filterset_class(self.request.GET).form.data != []

        elif self.view_type in ['list', 'detail', 'update'] and self.request.htmx:
            active_filters = self.request.htmx.current_url_abs_path.split('?').__len__() > 1

        if active_filters:
            filters = []
            if self.view_type in ['list', 'detail', 'update'] and self.request.htmx:
                if self.request.htmx.current_url_abs_path.split('?').__len__() > 1:
                    filters = [i for i in self.request.htmx.current_url_abs_path.split('?')[1].split('&') if i != '']
            else:
                filters = self.request.GET.urlencode().split('&')
            getparams = self.getparams.split('&') or []
            if filters:
                if filters[0]:
                    for filter in filters:
                        if '%3F' in filter:
                            filter = filter.split('%3F')[0]
                        value = filter.split('=')
                        if value[1] and (
                                value[0] != 'csrfmiddlewaretoken' and value[0] != 'vis' and value[
                            0] != 'set_visibility_value'
                        ):
                            param = filter
                            if param and param not in getparams:
                                filter_params.append(param)

        if filter_params:
            if self.getparams:
                self.getparams += "&"
            self.getparams += "&".join(filter_params)

    def validate_user_perms(self, user, perm, view):
        if isinstance(perm, types.FunctionType):
            return perm(user, view)
        return user.has_perm(perm)

    def validate_user_object_perms(self, *args, **kwargs):
        # Falso por defecto, implementar si se necesita por cada CRUDView y especificar los permisos

        return False

    def get_check_perms(self, context):
        user = self.request.user
        available_perms = {}
        for perm in self.all_perms:
            if self.check_perms:
                if perm in self.views_available:
                    available_perms[perm] = all([
                        self.validate_user_perms(user, x, perm)
                        for x in self.all_perms[perm]])
                else:
                    available_perms[perm] = False
            else:
                available_perms[perm] = True
        context['crud_perms'] = available_perms

    # def get_urls_and_fields(self, context):
    #     include = None
    #     if hasattr(self, 'display_fields') and self.view_type == 'detail':
    #         include = getattr(self, 'display_fields')
    #
    #     if hasattr(self, 'list_fields') and self.view_type == 'list':
    #         include = getattr(self, 'list_fields')
    #
    #     context['fields'] = utils.get_fields(self.model, include=include)
    #     if hasattr(self, 'object') and self.object:
    #         for action in utils.INSTANCE_ACTIONS:
    #             try:
    #                 nurl = utils.crud_url_name(self.model, action)
    #                 if self.namespace:
    #                     nurl = self.namespace + ':' + nurl
    #                 url = reverse(nurl, kwargs={'pk': self.object.pk})
    #             except NoReverseMatch:
    #                 url = None
    #             context['url_%s' % action] = url
    #
    #     for action in utils.LIST_ACTIONS:
    #         try:
    #             nurl = utils.crud_url_name(self.model, action)
    #             if self.namespace:
    #                 nurl = self.namespace + ':' + nurl
    #             url = reverse(nurl)
    #         except NoReverseMatch:
    #             url = None
    #         context['url_%s' % action] = url

    def get_urls_and_fields(self, context):
        context['fields'] = self.get_aggregate_context(queryset=self.get_queryset())
        if hasattr(self, 'object') and self.object:
            for action in utils.INSTANCE_ACTIONS:
                try:
                    nurl = utils.crud_url_name(self.model, action)
                    if self.namespace:
                        nurl = self.namespace + ':' + nurl
                    url = reverse(nurl, kwargs={'pk': self.object.pk})
                except NoReverseMatch:
                    url = None
                context['url_%s' % action] = url

        for action in utils.LIST_ACTIONS:
            try:
                nurl = utils.crud_url_name(self.model, action)
                if self.namespace:
                    nurl = self.namespace + ':' + nurl
                url = reverse(nurl)
            except NoReverseMatch:
                url = None
            context['url_%s' % action] = url

    def get_aggregate_context(self, queryset):
        include = None
        queryset = queryset  # self.get_queryset()
        aggregates = self.aggregates
        if hasattr(self, 'display_fields') and self.view_type == 'detail':
            include = getattr(self, 'display_fields')

        if hasattr(self, 'list_fields') and self.view_type == 'list':
            include = getattr(self, 'list_fields')

        return utils.get_fields_aggregates(self.model, queryset, aggregates, include=include)

    def get_aggregates(self, context):
        if hasattr(self, 'list_fields') and self.view_type == 'list':
            if hasattr(self, 'aggregates'):
                aggregates_keys = list(self.aggregates.keys())
                for key in aggregates_keys:
                    if self.aggregates[key].__len__() > 0:
                        context['aggregates'] = True
                        break

    def get_queryset(self):
        if self.queryset:
            queryset = self.queryset
        else:
            queryset = super(CRUDMixin, self).get_queryset()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Adds available urls and names.
        """

        context = super(CRUDMixin, self).get_context_data(**kwargs)
        context.update({
            'model_verbose_name': self.model._meta.verbose_name,
            'model_verbose_name_plural': self.model._meta.verbose_name_plural,
            'namespace': self.namespace
        })
        context.update({'blocks': self.template_blocks})

        if self.view_type in ['create', 'update', 'detail']:
            context['inlines'] = self.inlines

        if 'object' not in context:
            context['object'] = self.model
        if 'view_type' not in context:
            context['view_type'] = self.view_type
        if 'inline_actions' not in context:
            context['inline_actions'] = self.inline_actions

        self.get_urls_and_fields(context)
        self.get_check_perms(context)
        self.get_search_fields(context)
        self.get_filters(context)
        self.get_aggregates(context)

        context['views_available'] = self.views_available
        if self.view_type == 'list':
            context['paginate_template'] = self.paginate_template
            context['paginate_position'] = self.paginate_position
            if self.paginate_by:
                self.page_length = self.paginate_by
            context['page_length'] = self.page_length
            if self.page_length_menu:
                context['page_length_menu'] = self.page_length_menu
            else:
                context['page_length_menu'] = [5, 10, 25, 50, 100]

        context['template_father'] = self.template_father

        context['inline_tables'] = self.inline_tables

        context.update(self.context_rel)
        context['getparams'] = "?" + self.getparams
        context['getparams'] += "&" if self.getparams else ""
        context.update(CONFIG)
        return context

    def dispatch(self, request, *args, **kwargs):
        basename = self.template_name_base
        partial_basename = self.partial_template_name_base
        self.related_fields = self.related_fields or []
        self.context_rel = {}
        getparams = []
        self.getparams = ''
        params = self.request.GET.urlencode().split('&')
        for related in self.related_fields:
            pk = self.request.GET.get(related, '')
            if pk:
                Classrelated = utils.get_related_class_field(
                    self.model, related)
                self.context_rel[related] = get_object_or_404(
                    Classrelated, pk=pk)
                getparams.append("%s=%s" % (
                    related, str(self.context_rel[related].pk)))
        if params and params[0] != '':
            for param in params:
                if '%3F' in param:
                    param = param.split('%3F')[0]
                value = param.split('=')
                if value[1] and (
                        value[0] != 'csrfmiddlewaretoken' and value[0] != 'vis' and value[0] != 'set_visibility_value'
                ):
                    temp = param
                    if temp and temp not in getparams:
                        getparams.append(param)
        if getparams:
            self.getparams = "&".join(getparams)
        if self.validate_user_object_perms(self, *args, **kwargs):
            return View.dispatch(self, request, *args, **kwargs)
        for perm in self.perms:
            if not self.validate_user_perms(request.user, perm,
                                            self.view_type):
                return HttpResponseForbidden(render_to_string(
                    basename + '/403.html', request=request
                ))
        return View.dispatch(self, request, *args, **kwargs)


class CRUDView(object):
    """
        CRUDView is a generic way to provide create, list, detail, update,
        delete views in one class,
        you can inherit for it and manage login_required, model perms,
        pagination, update and add forms
        how to use:

        In views

        .. code:: python

            from testapp.models import Customer
            from cruds_adminlte3.crud import CRUDView
            class Myclass(CRUDView):
                model = Customer

        In urls.py

        .. code:: python
            myview = Myclass()
            urlpatterns = [
                url('path', include(myview.get_urls()))  # also support
                                                         # namespace
            ]

        The default behavior is check_login = True and check_perms=True but
        you can turn off with

        .. code:: python
            from testapp.models import Customer
            from cruds_adminlte3.crud import CRUDView

            class Myclass(CRUDView):
                model = Customer
                check_login = False
                check_perms = False

        You also can defined extra perms with

        .. code:: python

            class Myclass(CRUDView):
                model = Customer
                perms = { 'create': ['applabel.mycustom_perm'],
                          'list': [],
                          'delete': [],
                          'update': [],
                          'detail': []
                        }
        If check_perms = True we will add default django model perms
         (<applabel>.[add|change|delete|view]_<model>)

        You can also overwrite add and update forms

        .. code:: python

            class Myclass(CRUDView):
                model = Customer
                add_form = MyFormClass
                update_form = MyFormClass

        And of course overwrite base template name

        .. code:: python

            class Myclass(CRUDView):
                model = Customer
                template_name_base = "mybase"

        Remember basename is generated like app_label/modelname if
        template_name_base is set as None and
        'cruds' by default so template loader search this structure

        basename + '/create.html'
        basename + '/detail.html'
        basename + '/update.html'
        basename + '/list.html'
        basename + '/delete.html'

        The same is applied to partial templates trough htmx use, if
        partial_template_name_base is set as None and
        'partials' by default so template loader search this structure

        basename + '/partial_create.html'
        basename + '/partial_detail.html'
        basename + '/partial_update.html'
        basename + '/partial_list.html'
        basename + '/partial_delete.html'

        Note: also import <applabel>/<model>/<basename>/<view type>.html

        Using namespace

        In views

        .. code:: python

            from testapp.models import Customer
            from cruds_adminlte3.crud import CRUDView
            class Myclass(CRUDView):
                model = Customer
                namespace = "mynamespace"

        In urls.py

        .. code:: python

            myview = Myclass()
            urlpatterns = [
                url('path', include(myview.get_urls(),
                                    namespace="mynamespace"))
            ]

        If you want to filter views add views_available list

        .. code:: python
            class Myclass(CRUDView):
                model = Customer
                views_available = ['create', 'list', 'delete',
                                   'update', 'detail']


        It's obligatory this structure
           aggregates = {
           'avg': [],
           'count': [],
           'max': [],
           'min': [],
           'stddev': [],
           'sum': [],
           'variance': [],
           'percent': [],
           }

        Use this dictionary for total columns in tables. For example, if a column sum is needed,
        and the name of filed for that column is 'my_column', aggregates dictionary in Views.py
        shoud be:

            .. code:: python
             aggregates = {
                'sum': [
                    'my_column',
                ]
            }

        If a column maximun value is nedded for 'my_column', then shoud be:

            .. code:: python
            aggregates = {
                'max': [
                    'my_column'
                ]
            }

        In cases of total percent calculation, a 'plan' and a 'real' parts are needed for
        'my_column' total percent calculation. The 'plan' part must be placed first. For
        example, supose we have a column named 'my_column_plan', and other named 'my_column_real'
        and we want to place the total percent in 'my_column'. The aggregates dictionary
        in Views.py shoud be:

        .. code:: python
            aggregates = {
                'percent': {
                    'my_column': [
                        'my_column_plan',
                        'my_column_real',
                    ]
                }
            }
        Note that, in percent case, the percent key is not a list like avg, sum, count, but dictionary

    """
    aggregates = None
    filterset_class = None
    filter_fields = None

    """
        default_filters contains the dafault filter for de filter View. It is a dictionary containing
        lookup field expresions.

        default_filter = {
            'field1__expr': value_1,
            'field2__expr': value_2,
            ......
            'fieldn__expr': value_n
        }
        """
    default_filters = None

    dynamic_filters = None
    """
        'env' contains basically the additional models for use them in the environment application.
         It is a dictionary containing models name as key and its corresponding objects as values.
         The models have to be imported previously for its use in the view:
         .. code:: python
         'from account.models import Account'
         'from headlines.models import Headlines'

         And then, in the defined CRUDView class:

         .. code:: python
         env = {
            'account' : Account,
            'headlines' HeadLines,
         } 
        """
    env = None
    menu = None
    page_length = 10
    page_length_menu = None
    model = None
    queryset = None
    template_name_base = "cruds"
    partial_template_name_base = "partials"
    template_blocks = {}
    namespace = None
    fields = '__all__'
    urlprefix = ""
    check_login = True
    check_perms = True
    paginate_by = 10
    page_elide_range_on_each_side = 2
    page_elide_range_on_ends = 1
    paginate_template = 'cruds/pagination/prev_next.html'
    paginate_position = 'Bottom'
    update_form = None
    add_form = None
    detail_form = None
    modal = False
    table_class = None
    table_data = None
    col_vis = []
    display_fields = None
    list_fields = None
    inlines = None
    inline_tables = None
    inline_actions = True
    views_available = None
    template_father = "cruds/base.html"
    search_method = None
    search_fields = None
    split_space_search = False
    related_fields = None
    list_filter = None
    mixin = CRUDMixin

    """
    It's obligatory this structure
        perms = {
        'create': [],
        'list': [],
        'delete': [],
        'update': [],
        'detail': []
        }
    """
    perms = None

    #  DECORATORS

    def check_decorator(self, viewclass):
        if self.check_login:
            return login_required(viewclass)
        return viewclass

    def decorator_create(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_detail(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_list(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_update(self, viewclass):
        return self.check_decorator(viewclass)

    def decorator_delete(self, viewclass):
        return self.check_decorator(viewclass)

    #  GET GENERIC CLASS

    def get_create_view_class(self):
        # if self.inlines:
        #     return CreateWithInlinesView
        # else:
        return CreateView

    def get_create_view(self):
        CreateViewClass = self.get_create_view_class()

        class OCreateView(
            self.mixin,
            SweetifySuccessMixin,
            LoginRequiredMixin,
            CreateViewClass,
        ):
            namespace = self.namespace
            template_name_base = self.template_name_base
            partial_template_name_base = self.partial_template_name_base
            perms = self.perms['create']
            all_perms = self.perms
            form_class = self.add_form
            view_type = 'create'
            inlines = self.inlines
            inline_actions = self.inline_actions
            inline_tables = self.inline_tables
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
            template_blocks = self.template_blocks
            related_fields = self.related_fields
            aggregates = self.aggregates
            modal = self.modal
            success_message = _('Data creation was successful')

            def form_valid(self, form):
                if not self.related_fields:
                    return super(OCreateView, self).form_valid(form)

                self.object = form.save(commit=False)
                for key, value in self.context_rel.items():
                    setattr(self.object, key, value)
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

            def get_success_url(self):
                if "another" in self.request.POST and not self.modal:
                    url = self.request.path
                else:
                    url = super(OCreateView, self).get_success_url()
                if self.getparams:  # fixed filter create action
                    url += '?' + self.getparams
                return url

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'modal': self.modal
                })
                return ctx

        return OCreateView

    def get_detail_view_class(self):
        return DetailView

    def get_detail_view(self):
        ODetailViewClass = self.get_detail_view_class()

        class ODetailView(self.mixin, ModelFormMixin, ODetailViewClass):
            namespace = self.namespace
            template_name_base = self.template_name_base
            partial_template_name_base = self.partial_template_name_base
            perms = self.perms['detail']
            all_perms = self.perms
            view_type = 'detail'
            display_fields = self.display_fields
            inlines = self.inlines
            inline_actions = self.inline_actions
            form_class = self.detail_form
            inline_tables = self.inline_tables
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
            template_blocks = self.template_blocks
            related_fields = self.related_fields
            aggregates = self.aggregates
            modal = self.modal

            def get_success_url(self):
                url = super(ODetailView, self).get_success_url()
                if (self.getparams):  # fixed filter detail action
                    url += '?' + self.getparams
                return url

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'form': self.form_class(),
                    'modal': self.modal,
                })
                return ctx

        return ODetailView

    def get_update_view_class(self):
        # if self.inlines:
        #     return UpdateWithInlinesView
        # else:
        return UpdateView

    def get_update_view(self):
        EditViewClass = self.get_update_view_class()

        class OEditView(
            self.mixin,
            SweetifySuccessMixin,
            LoginRequiredMixin,
            PermissionRequiredMixin,
            EditViewClass,
            # FilterView
        ):
            namespace = self.namespace
            template_name_base = self.template_name_base
            partial_template_name_base = self.partial_template_name_base
            perms = self.perms['update']
            form_class = self.update_form
            modal = self.modal
            all_perms = self.perms
            view_type = 'update'
            inlines = self.inlines
            inline_actions = self.inline_actions
            inline_tables = self.inline_tables
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
            template_blocks = self.template_blocks
            related_fields = self.related_fields
            aggregates = self.aggregates
            success_message = _('Data modification was successful')

            def form_valid(self, form):
                if not self.related_fields:
                    return super(OEditView, self).form_valid(form)

                self.object = form.save(commit=False)
                for key, value in self.context_rel.items():
                    setattr(self.object, key, value)
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

            def get_success_url(self):
                url = super(OEditView, self).get_success_url()
                if (self.getparams):  # fixed filter edit action
                    url += '?' + self.getparams
                return url

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'modal': self.modal,
                    # 'form': self.form_class
                })
                return ctx

        return OEditView

    def get_list_view_class(self):
        return ListView

    def get_list_view(self):
        OListViewClass = self.get_list_view_class()

        class OListView(self.mixin, OListViewClass):
            namespace = self.namespace
            template_name_base = self.template_name_base
            partial_template_name_base = self.partial_template_name_base
            perms = self.perms['list']
            all_perms = self.perms
            table_class = self.table_class
            table_data = self.table_data
            inline_tables = self.inline_tables
            inline_actions = self.inline_actions
            list_fields = self.list_fields
            view_type = 'list'
            paginate_by = self.paginate_by
            page_elide_range_on_each_side = self.page_elide_range_on_each_side
            page_elide_range_on_ends = self.page_elide_range_on_ends
            page_length = self.page_length
            page_length_menu = self.page_length_menu
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
            template_blocks = self.template_blocks
            search_fields = self.search_fields
            split_space_search = self.split_space_search
            related_fields = self.related_fields
            paginate_template = self.paginate_template
            paginate_position = self.paginate_position
            list_filter = self.list_filter
            aggregates = self.aggregates
            filter_fields = self.filter_fields
            search_method = self.search_method
            default_filters = self.default_filters
            dynamic_filters = self.dynamic_filters
            queryset = self.queryset
            env = self.env
            modal = self.modal

            def get_listfilter_queryset(self, queryset):
                if self.list_filter:
                    filters = get_filters(
                        self.model, self.list_filter, self.request)
                    for filter in filters:
                        queryset = filter.get_filter(queryset)

                return queryset

            def search_queryset(self, query):
                if self.split_space_search is True:
                    self.split_space_search = ' '

                if self.search_fields and 'q' in self.request.GET:
                    q = self.request.GET.get('q')
                    if self.split_space_search:
                        q = q.split(self.split_space_search)
                    elif q:
                        q = [q]
                    sfilter = None
                    for field in self.search_fields:
                        for qsearch in q:
                            if field not in self.context_rel:
                                if sfilter is None:
                                    sfilter = Q(**{field: qsearch})
                                else:
                                    sfilter |= Q(**{field: qsearch})
                    if sfilter is not None:
                        query = query.filter(sfilter)

                if self.related_fields:
                    query = query.filter(**self.context_rel)
                return query

            def get_success_url(self):
                url = super(OListView, self).get_success_url()
                if (self.getparams):  # fixed filter detail action
                    url += '?' + self.getparams
                return url

            def get_queryset(self):
                queryset = super(OListView, self).get_queryset()
                queryset = self.search_queryset(queryset)
                queryset = self.get_listfilter_queryset(queryset)
                return queryset

            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                context.update({
                    'modal': self.modal
                })
                return context

        return OListView

    def get_filter_list_view_class(self):
        return FilterView

    def get_filter_list_view(self):
        OFilterListViewClass = self.get_filter_list_view_class()

        class OFilterListView(self.mixin, OFilterListViewClass, ExportMixin, SingleTableMixin):
            namespace = self.namespace
            template_name_base = self.template_name_base
            partial_template_name_base = self.partial_template_name_base
            # template_name = "django_tables2/bootstrap4.html"
            perms = self.perms['list']
            all_perms = self.perms
            list_fields = self.list_fields
            table_class = self.table_class
            inline_tables = self.inline_tables
            inline_actions = self.inline_actions
            table_data = self.table_data
            view_type = 'list'
            paginate_by = self.paginate_by
            page_elide_range_on_each_side = self.page_elide_range_on_each_side
            page_elide_range_on_ends = self.page_elide_range_on_ends
            page_length = self.page_length
            page_length_menu = self.page_length_menu
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
            template_blocks = self.template_blocks
            search_method = self.search_method
            search_fields = self.search_fields
            split_space_search = self.split_space_search
            related_fields = self.related_fields
            paginate_template = self.paginate_template
            paginate_position = self.paginate_position
            list_filter = self.list_filter
            aggregates = self.aggregates
            filter_fields = self.filter_fields
            default_filters = self.default_filters
            dynamic_filters = self.dynamic_filters
            queryset = self.queryset
            env = self.env
            col_vis = self.col_vis
            modal = self.modal

            if self.filterset_class is None:
                filterset_class = get_filter_fields(
                    self.model,
                    filter_fields=filter_fields,
                )
            else:
                filterset_class = self.filterset_class

            def get_listfilter_queryset(self, queryset):
                if self.filter_fields:
                    return self.filterset_class(self.request.GET, queryset).qs
                else:
                    return queryset

            def search_queryset(self, query):
                if self.search_method:
                    return self.search_method(
                        self.request,
                        self.search_fields,
                        self.split_space_search,
                        self.context_rel,
                        self.related_fields,
                        query
                    )
                if self.split_space_search is True:
                    self.split_space_search = ' '

                if self.search_fields and 'q' in self.request.GET:
                    q = self.request.GET.get('q')
                    if self.split_space_search:
                        q = q.split(self.split_space_search)
                    elif q:
                        q = [q]
                    sfilter = None
                    for field in self.search_fields:
                        for qsearch in q:
                            if field not in self.context_rel:
                                if sfilter is None:
                                    sfilter = Q(**{field: qsearch})
                                else:
                                    sfilter |= Q(**{field: qsearch})
                    if sfilter is not None:
                        query = query.filter(sfilter)

                    if self.related_fields:
                        query = query.filter(**self.context_rel)
                return query

            def get_success_url(self):
                url = super(OFilterListView, self).get_success_url()
                if (self.getparams):  # fixed filter detail action
                    url += '?' + self.getparams
                return url

            def get_queryset(self):
                queryset = super(OFilterListView, self).get_queryset()
                queryset = self.search_queryset(queryset)
                queryset = self.get_listfilter_queryset(queryset)
                if self.default_filters is not None:
                    queryset = queryset.filter(**self.default_filters)
                elif self.dynamic_filters is not None:
                    domain = normalize_domain(self.dynamic_filters)
                    queryset = queryset.filter(prefix_to_infix(self, domain))

                return queryset

            def get_context_data(self, *, object_list=None, **kwargs):
                context = super(OFilterListView, self).get_context_data(**kwargs)
                table = self.get_table(**self.get_table_kwargs())
                context[self.get_context_table_name(table)] = table
                # context.update({'table': self.table_class})
                request = self.request.GET
                paginator = context['paginator']
                page_number = context['page_obj'].number
                page_range = paginator.get_elided_page_range(
                    page_number,
                    on_each_side=self.page_elide_range_on_each_side,
                    on_ends=self.page_elide_range_on_ends
                )
                context['page_range'] = page_range
                context['modal'] = self.modal

                fields_order = []
                if 'filter' in context:
                    extra_context = context['filter'].form.get_context()
                    context.update(extra_context)
                    keys = list(context['filter'].form.fields)
                    for key in keys:
                        this_type = type(context['filter'].form.fields[key].widget)
                        if this_type == Select or this_type == SelectMultiple:
                            if 'class' not in context['filter'].form.fields[key].widget.attrs:
                                context['filter'].form.fields[key].widget.attrs.update(
                                    {'class': 'form-control select2'}
                                )
                            if 'style' not in context['filter'].form.fields[key].widget.attrs:
                                context['filter'].form.fields[key].widget.attrs.update(
                                    {'style': 'width: 100%'}
                                )
                        else:
                            if 'class' not in context['filter'].form.fields[key].widget.attrs:
                                context['filter'].form.fields[key].widget.attrs.update(
                                    {'class': 'form-control'}
                                )

                return context

            def get_paginate_by(self, queryset):
                if 'length_change' in self.request.GET:
                    if self.getparams:
                        self.getparams += "&"
                    self.getparams += 'length_change=' + self.request.GET.get('length_change')
                return self.request.GET.get("length_change", self.paginate_by)

            def get(self, request, *args, **kwargs):
                super_get = super().get(self, request, *args, **kwargs)
                table = self.get_table(**self.get_table_kwargs())
                table_columns = table.columns.columns
                RequestConfig(request).configure(table)
                export_format = request.GET.get("_export", None)
                if MyTableExport.is_valid_format(export_format):
                    footer = []
                    for column in table.columns.columns:
                        footer.append(table_columns[column].footer)
                    exporter = MyTableExport(
                        export_format,
                        table,
                        exclude_columns=self.request.GET.get('excluded_columns').split(','),
                        dataset_kwargs={'footer': footer}
                    )
                    return exporter.response(f"table.{export_format}")
                else:
                    return super_get

        return OFilterListView

    def get_delete_view_class(self):
        return DeleteView

    def get_delete_view(self):
        ODeleteClass = self.get_delete_view_class()

        class ODeleteView(self.mixin, SweetifySuccessMixin, ODeleteClass):
            namespace = self.namespace
            template_name_base = self.template_name_base
            partial_template_name_base = self.partial_template_name_base
            perms = self.perms['delete']
            all_perms = self.perms
            view_type = 'delete'
            inline_tables = self.inline_tables
            inline_actions = self.inline_actions
            views_available = self.views_available[:]
            check_perms = self.check_perms
            template_father = self.template_father
            template_blocks = self.template_blocks
            related_fields = self.related_fields
            aggregates = self.aggregates
            modal = self.modal
            success_message = _('The data was successfully deleted')

            def get_success_url(self):
                url = super(ODeleteView, self).get_success_url()
                print(self.getparams)
                if (self.getparams):  # fixed filter delete action
                    url += '?' + self.getparams
                return url

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data()
                ctx.update({
                    'modal': self.modal
                })
                return ctx

            # Esta redefinición de los métodos 'get' y 'post, para eliminar, obedece al uso de sweetalert2,
            # si no se va a usar, eliminar estas funciones
            def get(self, *args, **kwargs):
                if 'model_id' in kwargs:
                    return super().get(self.request)
                return self.post(*args, **kwargs)

            def post(self, request, *args, **kwargs):
                self.object = self.get_object()
                try:
                    self.object.delete()
                except ProtectedError as e:
                    protected_details = ", ".join([str(obj) for obj in e.protected_objects])
                    # messages.error(self.request, 'No se puede eliminar, está siendo utilizado.')
                    title = _('Cannot delete ')
                    text = _('This element is related to: ')
                    message_error(self.request,
                                  title + self.object.__str__() + '!',
                                  text=text + protected_details)
                    return HttpResponseRedirect(self.get_success_url())
                if self.success_message:
                    # messages.success(self.request, self.success_message)
                    sweetify.success(self.request, self.success_message)
                return HttpResponseRedirect(self.get_success_url())

        return ODeleteView

    #  INITIALIZERS
    def initialize_create(self, basename):
        OCreateView = self.get_create_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url

        fields = self.fields
        if self.add_form:
            fields = None
        self.create = self.decorator_create(OCreateView.as_view(
            model=self.model,
            fields=fields,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def initialize_detail(self, basename):
        ODetailView = self.get_detail_view()
        fields = self.fields
        if self.detail_form:
            fields = None
        self.detail = self.decorator_detail(
            ODetailView.as_view(
                model=self.model,
                template_name=basename,
                form_class=self.detail_form
            ))

    def initialize_update(self, basename):
        OUpdateView = self.get_update_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url
        fields = self.fields
        if self.update_form:
            fields = None
        self.update = self.decorator_update(OUpdateView.as_view(
            model=self.model,
            fields=fields,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def initialize_list(self, basename):
        OListView = self.get_list_view()
        self.list = self.decorator_list(OListView.as_view(
            model=self.model,
            template_name=basename
        ))

    def initialize_list_detail(self, basename):
        OListView = self.get_list_view()
        self.list_detail = self.decorator_list(OListView.as_view(
            model=self.model,
            template_name=basename
        ))

    def initialize_delete(self, basename):
        ODeleteView = self.get_delete_view()
        url = utils.crud_url_name(
            self.model, 'list', prefix=self.urlprefix)
        if self.namespace:
            url = self.namespace + ":" + url
        self.delete = self.decorator_delete(ODeleteView.as_view(
            model=self.model,
            success_url=reverse_lazy(url),
            template_name=basename
        ))

    def initialize_filter_list(self, basename):
        OFilterListView = self.get_filter_list_view()
        self.list = self.decorator_list(OFilterListView.as_view(
            model=self.model,
            template_name=basename
        ))

    def initialize_filter_list_detail(self, basename):
        OFilterListView = self.get_filter_list_view()
        self.list_detail = self.decorator_list(OFilterListView.as_view(
            model=self.model,
            template_name=basename
        ))

    def initialize_aggregates(self):
        if self.aggregates is None:
            self.aggregates = {
                'avg': [],
                'count': [],
                'max': [],
                'min': [],
                'stddev': [],
                'sum': [],
                'variance': [],
                'percent': {},
            }

    def initialize_env(self):
        if self.env is None:
            self.env = {}

    def get_base_name(self):
        ns = self.template_name_base
        if not self.template_name_base:
            ns = "%s/%s" % (
                self.model._meta.app_label,
                self.model.__name__.lower())
        return ns

    def get_partial_base_name(self):
        ns = self.partial_template_name_base
        if not self.partial_template_name_base:
            ns = "%s/%s" % (
                self.model._meta.app_label,
                self.model.__name__.lower())
        return ns

    def check_create_perm(self, applabel, name):
        notfollow = False
        try:
            model, created = ContentType.objects.get_or_create(
                app_label=applabel, model=name)
        except:
            notfollow = True
        if not notfollow and not Permission.objects.filter(content_type=model,
                                                           codename="view_%s" %
                                                                    (name,)).exists():
            Permission.objects.create(
                content_type=model,
                codename="view_%s" % (name,),
                name=_("Can see available %s" % (name,)))

    def initialize_perms(self):
        if self.perms is None:
            self.perms = {
                'create': [],
                'list': [],
                'delete': [],
                'update': [],
                'detail': []

            }
        applabel = self.model._meta.app_label
        name = self.model.__name__.lower()
        if self.check_perms:
            self.check_create_perm(applabel, name)
            self.perms['create'].append("%s.add_%s" % (applabel, name))
            self.perms['update'].append("%s.change_%s" % (applabel, name))
            self.perms['delete'].append("%s.delete_%s" % (applabel, name))
            # maybe other default perm can be here
            self.perms['list'].append("%s.view_%s" % (applabel, name))
            self.perms['detail'].append("%s.view_%s" % (applabel, name))

    def initialize_views_available(self):
        if self.views_available is None:
            self.views_available = [
                'create', 'list', 'delete', 'update', 'detail']

    def initialize_values(self):
        # Initialize some specific values required for the view.
        # Should be overridden for behavior needed
        pass

    def __init__(
            self, namespace=None, model=None, template_name_base=None, partial_template_name_base=None,
            mixin=None
    ):
        if namespace:
            self.namespace = namespace
        if model:
            self.model = model
        if template_name_base:
            self.template_name_base = template_name_base
        if partial_template_name_base:
            self.partial_template_name_base = partial_template_name_base
        if mixin:
            self.mixin = mixin

        basename = self.get_base_name()
        partial_basename = self.get_partial_base_name()
        self.initialize_env()
        self.initialize_views_available()
        self.initialize_perms()
        self.initialize_aggregates()
        self.initialize_values()
        if 'create' in self.views_available:
            self.initialize_create(basename + '/create.html')

        if 'detail' in self.views_available:
            self.initialize_detail(basename + '/detail.html')

        if 'update' in self.views_available:
            self.initialize_update(basename + '/update.html')

        if 'list' in self.views_available:
            if self.filter_fields is None:
                self.initialize_list(basename + '/list.html')
            else:
                if self.table_class is None:
                    self.initialize_filter_list(basename + '/list.html')
                else:
                    self.initialize_filter_list(basename + '/list_table.html')

        if 'list_detail' in self.views_available:
            if self.filter_fields is None:
                self.initialize_list_detail(basename + '/list_detail.html')
            else:
                if self.table_class is None:
                    self.initialize_filter_list_detail(basename + '/list.html')
                else:
                    self.initialize_filter_list_detail(basename + '/list_detail_table.html')

        if 'delete' in self.views_available:
            self.initialize_delete(basename + '/delete.html')

    def get_urls(self):

        pre = ""
        try:
            if self.cruds_url:
                pre = "%s/" % self.cruds_url
        except AttributeError:
            pre = ""
        base_name = "%s%s/%s" % (pre, self.model._meta.app_label,
                                 self.model.__name__.lower())
        myurls = []
        if 'list' in self.views_available:
            myurls.append(re_path("^%s/list$" % (base_name,),
                                  self.list,
                                  name=utils.crud_url_name(
                                      self.model, 'list', prefix=self.urlprefix)))
        if 'list_detail' in self.views_available:
            myurls.append(re_path("^%s/list_detail$" % (base_name,),
                                  self.list_detail,
                                  name=utils.crud_url_name(
                                      self.model, 'list_detail', prefix=self.urlprefix)))
        if 'create' in self.views_available:
            myurls.append(re_path("^%s/create$" % (base_name,),
                                  self.create,
                                  name=utils.crud_url_name(
                                      self.model, 'create', prefix=self.urlprefix))
                          )
        if 'detail' in self.views_available:
            myurls.append(re_path('^%s/(?P<pk>[^/]+)$' % (base_name,),
                                  self.detail,
                                  name=utils.crud_url_name(
                                      self.model, 'detail', prefix=self.urlprefix))
                          )
        if 'update' in self.views_available:
            myurls.append(re_path("^%s/(?P<pk>[^/]+)/update$" % (base_name,),
                                  self.update,
                                  name=utils.crud_url_name(
                                      self.model, 'update', prefix=self.urlprefix))
                          )
        if 'delete' in self.views_available:
            myurls.append(re_path(r"^%s/(?P<pk>[^/]+)/delete$" % (base_name,),
                                  self.delete,
                                  name=utils.crud_url_name(
                                      self.model, 'delete', prefix=self.urlprefix))
                          )

        myurls += self.add_inlines(base_name)
        return myurls

    def add_inlines(self, base_name):
        dev = []
        if self.inlines:
            for i, inline in enumerate(self.inlines):
                klass = inline
                if isinstance(klass, type):
                    # FIXME: This is a dirty hack to act on repeated calls to get_urls()
                    #        as those mean that inline is a type instance not a class from
                    #        the second run onwars.
                    klass = klass()
                self.inlines[i] = klass
                if self.namespace:
                    dev.append(re_path('^inline/', include(klass.get_urls(), )))
                else:
                    dev.append(re_path('^inline/', include(klass.get_urls())))
        return dev


class UserCRUDView(CRUDView):

    def get_create_view(self):
        View = super(UserCRUDView, self).get_create_view()

        class UCreateView(View):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

        return UCreateView

    def get_update_view(self):
        View = super(UserCRUDView, self).get_update_view()

        class UUpdateView(View):

            def form_valid(self, form):
                self.object = form.save(commit=False)
                self.object.user = self.request.user
                self.object.save()
                return HttpResponseRedirect(self.get_success_url())

        return UUpdateView

    def get_list_view(self):
        View = super(UserCRUDView, self).get_list_view()

        class UListView(View):

            def get_queryset(self):
                queryset = super(UListView, self).get_queryset()
                queryset = queryset.filter(user=self.request.user)
                return queryset

        return UListView
