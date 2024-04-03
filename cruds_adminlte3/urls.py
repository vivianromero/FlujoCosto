# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.urls import path
from django.apps import apps

from .crud import CRUDView, CRUDMixin
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='adminlte/index.html'), name='index')
]


def crud_for_model(model, urlprefix=None, namespace=None,
                   login_required=False, check_perms=False,
                   add_form=None,
                   update_form=None, views=None, cruds_url=None,
                   list_fields=None, related_fields=None,
                   template_name_base=None,
                   template_father=None,
                   mixin=None):
    """
    Returns list of ``url`` items to CRUD a model.
    @param template_father:
    @param template_name_base:
    @param related_fields:
    @param list_fields:
    @param cruds_url:
    @param views:
    @param update_form:
    @param add_form:
    @param check_perms:
    @param login_required:
    @param namespace:
    @param urlprefix:
    @param model:
    @param mixin=none -- mixin to be used as a base.
    """
    if mixin and not issubclass(mixin, CRUDMixin):
        raise ValueError(
            'Mixin needs to be a subclass of <%s>', CRUDMixin.__name__
        )

    mymodel = model
    myurlprefix = urlprefix
    mynamespace = namespace
    mycheck_perms = check_perms
    myadd_form = add_form
    myupdate_form = update_form
    mycruds_url = cruds_url
    mylist_fields = list_fields
    myrelated_fields = related_fields
    my_template_name_base = template_name_base
    my_template_father = template_father
    mymixin = mixin

    class NOCLASS(CRUDView):
        model = mymodel
        urlprefix = myurlprefix
        namespace = mynamespace
        check_login = login_required
        check_perms = mycheck_perms
        update_form = myupdate_form
        add_form = myadd_form
        views_available = views
        cruds_url = mycruds_url
        list_fields = mylist_fields
        related_fields = myrelated_fields
        template_father = my_template_father
        template_name_base = my_template_name_base
        # mixin = mymixin  # @FIXME TypeError: metaclass conflict: the metaclass
        # of a derived class must be a (non-strict) subclass of the metaclasses
        # of all its bases

    nc = NOCLASS()
    return nc.get_urls()


def crud_for_app(app_label, urlprefix=None, namespace=None,
                 login_required=False, check_perms=False,
                 modelforms={}, views=None, cruds_url=None,
                 template_name_base=None,
                 template_father=None,
                 mixin=None):
    """
    Returns list of ``url`` items to CRUD an app.
    @param template_father:
    @param template_name_base:
    @param cruds_url:
    @param modelforms:
    @param views:
    @param check_perms:
    @param login_required:
    @param namespace:
    @param urlprefix:
    @param app_label:
    @param mixin=none -- mixin to be used for all the CRUD views that can be
                            customized to allow custom "get_context_data"
                            variables for all the views.
    """
    #     if urlprefix is None:
    #         urlprefix = app_label + '/'
    app = apps.get_app_config(app_label)
    urls = []

    if mixin and not issubclass(mixin, CRUDMixin):
        raise ValueError(
            'Mixin needs to be a subclass of <%s>', CRUDMixin.__name__
        )

    for modelname, model in app.models.items():
        name = model.__name__.lower()
        add_form = None
        update_form = None
        if 'add_' + name in modelforms:
            add_form = modelforms['add_' + name]

        if 'update_' + name in modelforms:
            update_form = modelforms['update_' + name]

        list_fields = None
        if 'list_' + name in modelforms:
            list_fields = modelforms['list_' + name]

        related_fields = None
        if 'related_' + name in modelforms:
            related_fields = modelforms['related_' + name]

        urls += crud_for_model(model, urlprefix,
                               namespace, login_required, check_perms,
                               add_form=add_form,
                               update_form=update_form,
                               views=views,
                               cruds_url=cruds_url,
                               list_fields=list_fields,
                               related_fields=related_fields,
                               template_name_base=template_name_base,
                               template_father=template_father,
                               mixin=mixin)
    return urls
