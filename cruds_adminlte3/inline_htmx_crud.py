# encoding: utf-8

from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.urls import re_path, reverse_lazy
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django_htmx.http import HttpResponseLocation, HttpResponseClientRedirect

from cruds_adminlte3 import utils
from cruds_adminlte3.templatetags.crud_tags import crud_inline_url
from django_ajax.decorators import ajax

from .crud import CRUDView
from .inline_crud import InlineAjaxCRUD
from .utils import crud_url_name


class InlineHtmxCRUD(InlineAjaxCRUD):
    base_model = None
    template_name_base = "cruds/htmx"
    inline_field = None
    list_fields = []
    title = ""
    htmx = {
        'hx_get': '',
        'hx_target': '',
        'hx_swap': '',
        'hx_triger': '',
        'hx_replace_url': '',
        'hx_swap_oob': '',
        'hx_preserve': '',
    }

    def check_decorator(self, viewclass):
        if self.check_login:
            return login_required(viewclass)
        return viewclass

    def get_create_view(self):
        create_view = super(InlineHtmxCRUD, self).get_create_view()

        class CreateView(create_view):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]
            htmx = self.htmx
            hx_target = self.hx_target
            hx_swap = self.hx_swap
            hx_form_target = self.hx_form_target
            hx_form_swap = self.hx_form_swap
            hx_retarget = self.hx_retarget
            hx_reswap = self.hx_reswap

            def get_context_data(self, **kwargs):
                context = super(CreateView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['inline_model'] = self.model
                # context['name'] = self.name
                # context['views_available'] = self.views_available
                context.update({
                    'max_width': '950px',
                    'hx_target': '#id_%s_myList' % self.name,
                    'object_model': self.model,
                })
                self.htmx['hx_target'] = '#id_%s_myList' % self.name
                self.hx_target = '#id_%s_myList' % self.name
                context.update(self.htmx)
                return context

            def get_success_url(self):
                return crud_inline_url(self.model_id, self.object, 'list', self.namespace)

            def form_valid(self, form):
                event_action = None
                if self.request.method == 'POST':
                    event_action = self.request.POST.get('event_action', None)
                elif self.request.method == 'GET':
                    event_action = self.request.GET.get('event_action', None)
                target = '#id_%s_myList' % self.name
                try:
                    self.object = form.save(commit=False)
                    setattr(self.object, self.inline_field, self.model_id)
                    self.object.save()

                except IntegrityError as e:
                    # Maneja el error de integridad (duplicación de campos únicos)
                    mess_error = "Erro de Integridad"
                    form.add_error(None, mess_error)
                    return self.form_invalid(form)
                return HttpResponseLocation(
                    self.get_success_url(),
                    target=target,
                    headers={
                        'HX-Trigger': self.request.htmx.trigger,
                        'HX-Trigger-Name': self.request.htmx.trigger_name,
                        'event_action': event_action,
                    },
                    values={
                        'event_action': event_action,
                    }
                )

            def form_invalid(self, form, **kwargs):
                """If the form is invalid, render the invalid form."""
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                tpl = self.get_template_names()
                crud_inline_url(self.model_id, form.instance, 'create', self.namespace)
                response = render(self.request, tpl, ctx)
                response['HX-Retarget'] = '#edit_modal_inner'
                response['HX-Reswap'] = 'innerHTML'
                return response

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                self.name = self.model.__name__.lower()
                return create_view.get(self, request, *args, **kwargs)

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return create_view.post(self, request, *args, **kwargs)

        return CreateView

    def get_detail_view(self):
        detai_view = super(InlineHtmxCRUD, self).get_detail_view()

        class DetailView(detai_view):
            # inline_field = self.inline_field
            # views_available = self.views_available[:]
            # name = self.name
            htmx = self.htmx
            hx_target = self.hx_target
            hx_swap = self.hx_swap
            hx_form_target = self.hx_form_target
            hx_form_swap = self.hx_form_swap
            hx_retarget = self.hx_retarget
            hx_reswap = self.hx_reswap

            def get_context_data(self, **kwargs):
                context = super(DetailView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['inline_model'] = self.object
                # context['name'] = self.name
                # context['views_available'] = self.views_available
                # context.update({
                #     'form': self.form_class(),
                # })
                if 'pk' in kwargs:
                    obj = self.model.objects.get(id=self.kwargs['pk'])
                    context['form'] = self.form_class(instance=obj)
                elif 'object' in kwargs:
                    context['form'] = self.form_class(instance=kwargs['object'])
                context.update(self.htmx)
                return context

            def get(self, request, *args, **kwargs):
                self.model_id = kwargs['model_id']
                return detai_view.get(self, request, *args, **kwargs)

        return DetailView

    def get_update_view(self):
        update_uiew = super(InlineHtmxCRUD, self).get_update_view()

        class UpdateView(update_uiew):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]
            htmx = self.htmx
            hx_target = self.hx_target
            hx_swap = self.hx_swap
            hx_form_target = self.hx_form_target
            hx_form_swap = self.hx_form_swap
            hx_retarget = self.hx_retarget
            hx_reswap = self.hx_reswap

            def get_context_data(self, **kwargs):
                context = super(UpdateView, self).get_context_data(**kwargs)
                context.update({
                    'max_width': '950px',
                    'hx_target': '#id_%s_myList' % self.name,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                    'object_model': self.model,
                })
                self.htmx.update({
                    'hx_target': '#id_%s_myList' % self.name,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                self.hx_target = '#id_%s_myList' % self.name
                context.update(self.htmx)
                return context

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return update_uiew.get(self, request, *args, **kwargs)

            def form_valid(self, form):
                self.object = form.save(commit=False)
                setattr(self.object, self.inline_field, self.model_id)
                self.object.save()
                crud_inline_url(self.model_id,
                                self.object, 'list', self.namespace)

                return HttpResponseLocation(
                    self.get_success_url(),
                    target=self.htmx['hx_target'],
                )

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return update_uiew.post(self, request, *args, **kwargs)

        return UpdateView

    def get_list_view(self):
        list_view = super(InlineHtmxCRUD, self).get_list_view()

        class ListView(list_view):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]
            htmx = self.htmx

            def get_context_data(self, **kwargs):
                context = super(ListView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['name'] = self.name
                # context['views_available'] = self.views_available
                context.update(self.htmx)
                return context

            def get_queryset(self):
                queryset = super(ListView, self).get_queryset()
                params = {
                    self.inline_field: self.model_id
                }
                queryset = queryset.filter(**params)
                return queryset

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return list_view.get(self, request, *args, **kwargs)

        return ListView

    def get_filter_list_view(self):
        filter_list_view = super(InlineHtmxCRUD, self).get_filter_list_view()

        class FilterListView(filter_list_view):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]
            htmx = self.htmx
            hx_target = self.hx_target
            hx_swap = self.hx_swap
            hx_form_target = self.hx_form_target
            hx_form_swap = self.hx_form_swap
            hx_retarget = self.hx_retarget
            hx_reswap = self.hx_reswap

            def get_context_data(self, **kwargs):
                context = super().get_context_data(**kwargs)
                table = self.get_table(**self.get_table_kwargs())
                table.empty_text = 'No existen elementos aún'
                context[self.get_context_table_name(table)] = table
                context.update({
                    'hx_target': '#id_%s_myList' % self.name,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                    'object_model': self.model,
                })
                self.htmx.update({
                    'hx_target': '#id_%s_myList' % self.name,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                self.hx_target = '#id_%s_myList' % self.name
                return context

            def get_queryset(self):
                queryset = super(FilterListView, self).get_queryset()
                params = {
                    self.inline_field: self.model_id
                }
                queryset = queryset.filter(**params)
                return queryset

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return filter_list_view.get(self, request, *args, **kwargs)

        return FilterListView

    def get_delete_view(self):
        delete_view = super(InlineHtmxCRUD, self).get_delete_view()

        class DeleteView(delete_view):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]
            htmx = self.htmx
            hx_target = self.hx_target
            hx_swap = self.hx_swap
            hx_form_target = self.hx_form_target
            hx_form_swap = self.hx_form_swap
            hx_retarget = self.hx_retarget
            hx_reswap = self.hx_reswap

            def get_context_data(self, **kwargs):
                context = super(DeleteView, self).get_context_data(**kwargs)
                context.update({
                    'hx_target': '#id_%s_myList' % self.name,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                    'object_model': self.model,
                })
                self.htmx.update({
                    'hx_target': '#id_%s_myList' % self.name,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                self.hx_target = '#id_%s_myList' % self.name
                context.update(self.htmx)
                return context

            def get_success_url(self):
                return crud_inline_url(self.model_id, self.object, 'list', 'app_index:codificadores')

            def get(self, request, *args, **kwargs):
                event_action = None
                if self.request.method == 'POST':
                    event_action = self.request.POST.get('event_action', None)
                elif self.request.method == 'GET':
                    event_action = self.request.GET.get('event_action', None)
                target = '#id_%s_myList' % self.name
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id']
                )
                return HttpResponseLocation(
                    self.get_success_url(),
                    target=target,
                    headers={
                        'HX-Trigger': self.request.htmx.trigger,
                        'HX-Trigger-Name': self.request.htmx.trigger_name,
                        'event_action': event_action,
                    },
                    values={
                        'event_action': event_action,
                    }
                )

        return DeleteView

    def __init__(self, *args, **kwargs):
        self.name = self.model.__name__.lower()
        super(InlineHtmxCRUD, self).__init__(*args, **kwargs)
