# encoding: utf-8


"""
Created on 14/4/2017

@author: luisza
"""
from __future__ import unicode_literals

from django.urls import re_path
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
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
        viewclass = super(InlineHtmxCRUD, self).check_decorator(viewclass)
        return viewclass

    def get_create_view(self):
        create_view = super(InlineHtmxCRUD, self).get_create_view()

        class CreateView(create_view):
            # inline_field = self.inline_field
            # base_model = self.base_model
            # name = self.name
            # views_available = self.views_available[:]
            htmx = self.htmx

            def get_context_data(self, **kwargs):
                context = super(CreateView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['inline_model'] = self.model
                # context['name'] = self.name
                # context['views_available'] = self.views_available
                return context

            def form_valid(self, form):
                self.object = form.save(commit=False)
                setattr(self.object, self.inline_field, self.model_id)
                self.object.save()
                crud_inline_url(self.model_id, self.object, 'list', self.namespace)

                return HttpResponseLocation(
                    self.get_success_url(),
                    target=self.htmx['hx_target'],
                )

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

            def get_context_data(self, **kwargs):
                context = super(DetailView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['inline_model'] = self.object
                # context['name'] = self.name
                # context['views_available'] = self.views_available
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

            def get_context_data(self, **kwargs):
                context = super(UpdateView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['inline_model'] = self.object
                # context['name'] = self.name
                # context['views_available'] = self.views_available
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

    def get_delete_view(self):
        delete_view = super(InlineHtmxCRUD, self).get_delete_view()

        class DeleteView(delete_view):
            inline_field = self.inline_field
            base_model = self.base_model
            name = self.name
            views_available = self.views_available[:]
            htmx = self.htmx

            def get_context_data(self, **kwargs):
                context = super(DeleteView, self).get_context_data(**kwargs)
                # context['base_model'] = self.model_id
                # context['inline_model'] = self.object
                # context['name'] = self.name
                # context['views_available'] = self.views_available
                # if self.model_id:
                #     url_father = self.base_model.get_absolute_url(self=self.model_id)
                # else:
                #     url_father = self.get_success_url()
                # context['url_father'] = url_father
                return context

            def get(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id'])
                return super().get(self, request, *args, **kwargs)

            def get_success_url(self):
                url = super().get_success_url()
                if self.model_id:
                    url = self.base_model.get_absolute_url(self=self.model_id)
                return url

            def post(self, request, *args, **kwargs):
                self.model_id = get_object_or_404(
                    self.base_model, pk=kwargs['model_id']
                )
                if self.model_id:
                    url_father = self.base_model.get_absolute_url(self=self.model_id)
                else:
                    url_father = self.get_success_url()
                response = delete_view.post(self, request, *args, **kwargs)
                return response

        return DeleteView

    def __init__(self, *args, **kwargs):
        self.name = self.model.__name__.lower()
        super(InlineHtmxCRUD, self).__init__(*args, **kwargs)
