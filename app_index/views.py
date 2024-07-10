from __future__ import unicode_literals

import json

import sweetify
from django.db.models import Sum, Count, ProtectedError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView
from django_htmx.http import HttpResponseLocation
from django_tables2 import RequestConfig
from django.utils.translation import gettext as _
from django_tables2.views import SingleTableMixin

from cruds_adminlte3.crud import CRUDView, MyTableExport
from cruds_adminlte3.utils import crud_url_name
from utiles.utils import message_error


# from cruds_adminlte3.config import CONFIG


def get_current_url_abs_path(request_htmx=None):
    if request_htmx is not None:
        if request_htmx.current_url_abs_path.split('?').__len__() > 1:
            return '?' + request_htmx.current_url_abs_path.split('?')[1]
    return ''


class Index(TemplateView):
    template_name = 'app_index/adminlte/index.html'

    def get_context_data(self, **kwargs):
        CONFIG = {
            'app_logo_path': '/dist/img/cubatabaco_logo.png',
            'welcome_text': _('Site for the management of tobacco flows and costs.'),
            'common_background_color': 'gray',
            'main_sidebar_title': _('Flows and costs'),
            'app_logo_alt': _('Flows and costs'),

            # Dual list box text
            'filterTextClear': _('show all'),
            'filterPlaceHolder': _('Filter'),
            'moveSelectedLabel': _('Move selected'),
            'moveAllLabel': _('Move all'),
            'removeSelectedLabel': _('Remove selected'),
            'removeAllLabel': _('Remove all'),
            'infoText1': _('Showing available elements: {0}'),
            'infoText2': _('Showing selected elements: {0}'),
            'infoTextFiltered': '<span class="badge badge-warning">' + _('Filtered') + '</span> {0} from {1}',
            'infoTextEmpty': _('Empty list'),

            # Bootstrap DateTimePicker Translation
            'today': _('Go to today'),
            'clear': _('Clear selection'),
            'close': _('Close the picker'),
            'selectMonth': _('Select Month'),
            'prevMonth': _('Previous Month'),
            'nextMonth': _('Next Month'),
            'selectYear': _('Select Year'),
            'prevYear': _('Previous Year'),
            'nextYear': _('Next Year'),
            'selectDecade': _('Select Decade'),
            'prevDecade': _('Previous Decade'),
            'nextDecade': _('Next Decade'),
            'prevCentury': _('Previous Century'),
            'nextCentury': _('Next Century'),
            'pickHour': _('Pick Hour'),
            'incrementHour': _('Increment Hour'),
            'decrementHour': _('Decrement Hour'),
            'pickMinute': _('Pick Minute'),
            'incrementMinute': _('Increment Minute'),
            'decrementMinute': _('Decrement Minute'),
            'pickSecond': _('Pick Second'),
            'incrementSecond': _('Increment Second'),
            'decrementSecond': _('Decrement Second'),
            'togglePeriod': _('Toggle Period'),
            'selectTime': _('Select Time'),

            # js_swal text
            'js_swal_title': _("Are you sure you want to delete this item?"),
            'js_swal_text': _('This action cannot be reversed!'),
            'js_swal_confirmButtonText': _('Confirm Remove'),
            'js_swal_cancelButtonText': _('Cancel'),

            # DataTable buttons text
            'js_buttons_colvis_titleAttr': _('Column Visibility'),
            'js_buttons_copyHtml5_titleAttr': _('Copy'),
            'js_buttons_csvHtml5_titleAttr': _('Export to .csv'),
            'js_buttons_excelHtml5_titleAttr': _('Export to excel'),
            'js_buttons_pdfHtml5_titleAttr': _('Export to pdf'),
            'js_buttons_print_titleAttr': _('Print'),

            # Open and close buttons
            'close_event': _('Close event'),
            'open_event': _('Open event'),

            # Show or hide password
            'hide_password': _('Hide password'),
            'show_password': _('Show password'),

            # login/logout messages
            'title_success': _('Success'),
            'success_message': _("User <<%(user)s>> were successfully logged in."),

            # Tabla Documentos iconos
            'documento_edicion_icon': '/dist/img/icons8-pencil-48.png',
            'documento_confirmado_icon': '/dist/img/icons8-check-mark-48.png',
            'documento_rechazado_icon': '/dist/img/icons8-no-entry-trafic-rules-24.png',
            'documento_cancelado_icon': '/dist/img/icons8-cancel-48.png',
        }

        context = super().get_context_data()
        # CONFIG['welcome_text'] = _('Site for the management of tobacco flows and costs.'),
        context.update(CONFIG)
        return context


class Underconstruction(TemplateView):
    template_name = 'app_index/adminlte/underconstruction.html'


class Dashboard(TemplateView):
    template_name = 'app_index/adminlte/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        return context

    def get_template_names(self):
        if self.request.htmx:
            template_name = "app_index/partials/partial_dashboard.html"
        else:
            template_name = "app_index/adminlte/dashboard.html"

        return template_name


class CommonCRUDView(CRUDView):
    model = None  # Must be filled in descendant classes

    namespace = None  # Must be filled in descendant classes

    template_father = 'app_index/cruds/base.html'

    template_name_base = 'app_index/cruds'

    partial_template_name_base = 'app_index/partials'

    views_available = [
        'create',
        'list',
        'delete',
        'update',
    ]

    fields = None  # Must be filled in descendant classes

    # Hay que agregar __icontains luego del nombre del campo para que busque el contenido
    # y no distinga entre mayúsculas y minúsculas.
    # En el caso de campos relacionados hay que agregar __<nombre_campo_que_se_muestra>__icontains
    search_fields = None  # Must be filled in descendant classes

    # search_method = hecho_extraordinario_search_queryset

    add_form = None  # Must be filled in descendant classes

    update_form = None  # Must be filled in descendant classes

    detail_form = None  # Must be filled in descendant classes

    check_login = True
    check_perms = True

    list_fields = None  # Must be filled in descendant classes

    filter_fields = None  # Must be filled in descendant classes

    filterset_class = None  # Must be filled in descendant classes

    page_length = 15

    page_length_menu = [5, 10, 15, 20, 25]

    # Table settings
    table_class = None  # Must be filled in descendant classes
    template_name = "app_index/cruds/list_table.html"
    paginate_by = 10
    exclude_columns = ("actions",)

    modal = True

    hx_target = '#main_content_swap'
    hx_swap = 'outerHTML'

    hx_form_target = '#dialog'
    hx_form_swap = 'outerHTML'

    hx_retarget = '#dialog'
    hx_reswap = 'outerHTML'

    def get_filter_list_view(self):
        view = super().get_filter_list_view()

        class OFilterListView(view):
            def get_context_data(self, *, object_list=None, **kwargs):
                context = super().get_context_data(**kwargs)
                col_vis = ",".join(self.col_vis)
                context.update({
                    'col_vis': col_vis,
                    'hx_target': self.hx_target,
                    'hx_swap': self.hx_swap,
                    'hx_form_target': self.hx_form_target,
                    'hx_form_swap': self.hx_form_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                return context

            def get_template_names(self):
                if self.table_class is None:
                    template = 'list.html'
                    template_partial = 'list_partial.html'
                else:
                    template = 'list_table.html'
                    template_partial = 'list_table_partial.html'
                if self.request.htmx:
                    template_name = "%s/%s" % (
                        self.partial_template_name_base, template_partial
                    )
                else:
                    template_name = "%s/%s" % (
                        self.template_name_base, template
                    )

                return template_name

            def get(self, request, *args, **kwargs):
                table = self.get_table(**self.get_table_kwargs())
                table_columns = table.columns.columns
                col = request.GET.get("vis", None)
                visibility = request.GET.get("set_visibility_value", None)
                if col is not None and visibility is None and col not in self.col_vis:
                    self.col_vis.append(col)
                if col is not None and visibility == 'on' and col in self.col_vis:
                    self.col_vis.remove(col)
                self.table_class.col_vis = self.col_vis
                self.table_class.getparams = self.getparams
                RequestConfig(request).configure(table)
                export_format = request.GET.get("_export", None)
                if MyTableExport.is_valid_format(export_format):
                    footer = []
                    for column in table.columns.columns:
                        if (column not in self.col_vis) and (not table.base_columns[column].exclude_from_export):
                            footer.append(table_columns[column].footer)
                    exporter = MyTableExport(
                        export_format,
                        table,
                        exclude_columns=self.request.GET.get('excluded_columns').split(','),
                        dataset_kwargs={'footer': footer}
                    )
                    return exporter.response(f"table.{export_format}")
                else:
                    return super().get(request=request)

        return OFilterListView

    def get_update_view(self):
        view = super().get_update_view()

        class OEditView(view):

            def get_template_names(self):
                template = 'update.html'
                template_partial = 'partial_update.html'

                if self.request.htmx:
                    template_name = "%s/%s" % (
                        self.partial_template_name_base, template_partial
                    )
                else:
                    template_name = "%s/%s" % (
                        self.template_name_base, template
                    )

                return template_name

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "user": self.request.user,
                        "post": self.request.POST,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                ctx = super(OEditView, self).get_context_data(**kwargs)
                ctx.update({
                    'modal_form_title': 'Formaulario Modal',
                    'max_width': '950px',
                    'hx_target': self.hx_target,
                    'hx-swap': self.hx_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                return ctx

            def form_invalid(self, form, **kwargs):
                """If the form is invalid, render the invalid form."""
                ctx = self.get_context_data(**kwargs)
                ctx['form'] = form
                tpl = self.get_template_names()
                response = render(self.request, tpl, ctx)
                response['HX-Retarget'] = ctx['hx_retarget']
                response['HX-Reswap'] = ctx['hx_reswap']
                return response

            def get_success_url(self):
                url = super(OEditView, self).get_success_url()
                if self.getparams:  # fixed filter edit action
                    url += '?' + self.getparams
                elif self.request.htmx:
                    url += get_current_url_abs_path(self.request.htmx)
                return url

        return OEditView

    def get_create_view(self):
        view = super().get_create_view()

        class OCreateView(view):
            hx_target = self.hx_target

            def get_template_names(self):
                template = 'create.html'
                template_partial = 'partial_create.html'

                if self.request.htmx:
                    template_name = "%s/%s" % (
                        self.partial_template_name_base, template_partial
                    )
                else:
                    template_name = "%s/%s" % (
                        self.template_name_base, template
                    )

                return template_name

            def get_form_kwargs(self):
                form_kwargs = super().get_form_kwargs()
                form_kwargs.update(
                    {
                        "user": self.request.user,
                    }
                )
                return form_kwargs

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'modal_form_title': 'Formaulario Modal',
                    'max_width': '950px',
                    'hx_target': self.hx_target,
                    'hx-swap': self.hx_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                return ctx

            def get_retarget_response(self, form, ctx):
                ctx['form'] = form
                tpl = "%s/%s" % (self.partial_template_name_base, 'partial_create.html')
                response = render(self.request, tpl, ctx)
                response['HX-Retarget'] = ctx['hx_retarget']
                response['HX-Reswap'] = ctx['hx_reswap']
                return response

            def form_valid(self, form):
                event_action = None
                if self.request.method == 'POST':
                    event_action = self.request.POST.get('event_action', None)
                elif self.request.method == 'GET':
                    event_action = self.request.GET.get('event_action', None)
                if form.is_valid():
                    rtn = super(OCreateView, self).form_valid(form)
                    return HttpResponseLocation(
                        # rtn,
                        self.get_success_url(),
                        target=self.hx_target,
                        headers={
                            'HX-Trigger': self.request.htmx.trigger,
                            'HX-Trigger-Name': self.request.htmx.trigger_name,
                            'event_action': event_action,
                        },
                        values={
                            'event_action': event_action,
                        }
                    )
                else:
                    return render(self.request, self.get_template_names(), {
                        'form': form,
                    })

            def form_invalid(self, form, **kwargs):
                """If the form is invalid, render the invalid form."""
                ctx = self.get_context_data(**kwargs)
                return self.get_retarget_response(form=form, ctx=ctx)

            def get_success_url(self):
                if ("another" in self.request.POST) and not self.modal:
                    url = self.request.path
                elif "inline" in self.request.POST:
                    namespace = self.namespace + ':'
                    self.hx_target = '#dialog'
                    url = reverse_lazy(
                        crud_url_name(self.model, 'update', namespace), args=[self.object.pk]
                    )
                else:
                    url = super(OCreateView, self).get_success_url()
                if self.getparams:  # fixed filter create action
                    url += '?' + self.getparams
                elif self.request.htmx:
                    url += get_current_url_abs_path(self.request.htmx)
                return url

        return OCreateView

    def get_detail_view(self):
        view = super().get_detail_view()

        class ODetailView(view):

            def get_template_names(self):
                template = 'detail.html'
                template_partial = 'detail_partial.html'
                if self.request.htmx:
                    template_name = "%s/%s" % (
                        self.partial_template_name_base, template_partial
                    )
                else:
                    template_name = "%s/%s" % (
                        self.template_name_base, template
                    )

                return template_name

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                if self.inlines:
                    for inline in self.inlines:
                        inline.table_class.col_vis.append('actions')
                ctx.update({
                    'max_width': '950px',
                    'hx_target': self.hx_target,
                    'hx-swap': self.hx_swap,
                    'hx_retarget': self.hx_retarget,
                    'hx_reswap': self.hx_reswap,
                })
                if 'pk' in kwargs:
                    obj = self.model.objects.get(id=self.kwargs['pk'])
                    ctx['form'] = self.form_class(instance=obj)
                    ctx['modal_form_title'] = 'Ver Detalles de ' + obj.__str__()
                elif 'object' in kwargs:
                    ctx['form'] = self.form_class(instance=kwargs['object'])
                    ctx['modal_form_title'] = 'Ver Detalles de ' + kwargs['object'].__str__()
                return ctx

        return ODetailView

    def get_delete_view(self):
        view = super().get_delete_view()

        class ODeleteView(view):

            def get_context_data(self, **kwargs):
                ctx = super().get_context_data(**kwargs)
                ctx.update({
                    'hx_target': self.hx_target,
                    'hx-swap': self.hx_swap,
                })
                return ctx

        return ODeleteView


class BaseModalFormView(FormView):
    """
    Base Modal Form View para ser heredado y utilizado por los descendientes
    """
    # Nombre de la plantilla del modal, por defecto es: 'app_index/modals/modal_form.html'
    template_name = 'app_index/modals/modal_form.html'

    # Nombre de la clase formulario, puede estar definida en forms.py mediante crispy-forms,
    # Por defecto es None por lo que debe definirse en los descendientes.
    form_class = None

    # Nombre del View padre de donde se genera la llamada y al cual se debe retornar,
    # Por defecto es None por lo que debe definirse en los descendientes.
    father_view = None

    # Es un diccionario, con el nombre del evento/acción como llave y con el nombre de la vista a la cual se retorna una vez se ejecute
    # la acción asociada a dicho evento. Debe definirse como parámetro en el botoón del formulario (mediante hx-vals).
    # ....en el template...
    # hx-vals='{"event_action": "submitted"}'
    # ....en el form.....
    # viewname = {"submitted": nombre_del_view_que_ejecuta_la_acción}
    # Por defecto es {} por lo que debe definirse en los descendientes.
    viewname = {}

    # Es un diccionario, con el nombre del evento/acción como llave y con el nombre de la función que va a ejecutar la lógica requerida
    # asociada a dicho evento. Debe definirse como parámetro en el botoón del formulario (mediante hx-vals).
    # ....en el template...
    # hx-vals='{"event_action": "submitted"}'
    # ....en el form.....
    # funcname = {"submitted": nombre_de_la_función_que_ejecuta_la_acción}
    # Por defecto es {} por lo que debe definirse en los descendientes. Las funciones asociadas a los eventos deben estar definidas
    # antes que el descendiente de BaseModalFormView
    funcname = {}

    # Si el formulario contine alguna tabla 'inline'. Utiliza un formato de lista de diccionarios con el formato siguiente:
    # [{
    #       "table": table_class, #-------> Clase que contiene la tabla
    #       "name": table_name,  #--------> Nombre de la tabla
    #       "visible": True/False, #------> Si la tabla será visible o no
    #       "title": "table_title", #-----> Título de la tabla
    #   }]
    # Se le pueden adicionar otros parámetros al diccionario en el descendiente seg�n se necesite
    #   None por defecto
    inline_tables = None

    # Si se usa htmx, el 'id' del elemento donde se va a introducir la plantilla parcial correspondiente al viewname.
    # Por defecto es '#main_content_swap' pero debe definirse de acuerdo a las nececidades propias del viewform.
    hx_target = '#main_content_swap'

    # Si se usa htmx, la estrategia de intercambio a la hora de reemplazar el elemento definido en 'hx_target'
    # con la plantilla parcial correspondiente al viewname.
    # Por defecto es 'outerHTML' pero debe definirse de acuerdo a las nececidades propias del viewform.
    hx_swap = 'outerHTML',

    # Si se usa htmx, el 'id' del elemento donde se va a introducir la plantilla parcial correspondiente al form.
    # Por defecto es '#dialog' pero debe definirse de acuerdo a las nececidades propias del viewform.
    hx_form_target = '#dialog'

    # Si se usa htmx, la estrategia de intercambio a la hora de reemplazar el elemento definido en 'hx_form_target'
    # con la plantilla parcial correspondiente al form.
    # Por defecto es 'outerHTML' pero debe definirse de acuerdo a las nececidades propias del viewform.
    hx_form_swap = 'outerHTML',

    # Si se usa htmx, el 'id' del elemento del formulario modal donde se va a volver hacer render una vez que el
    # formulario es inválido. Por defecto es '#dialog'
    hx_retarget = '#dialog',

    # Si se usa htmx, la estrategia de intercambio a la hora de reemplazar el elemento definido en 'hx_retarget'
    # cuando el formulario es declarado inválido. Por defecto es 'outerHTML'.
    hx_reswap = 'outerHTML',

    # Título del formulario modal
    modal_form_title = 'Formulario Modal'

    # Ancho máximo de la ventana modal. Debe ajustarse de acuerdo al contenido y campos del formulario.
    max_width = '500px'

    def get_fields_kwargs(self, form):
        """
        Retorna el valor de cada 'field' en el diccionario 'kw'.
        Esta función es útil a la hora de definir qué valores del formulario se retornan,
        por defecto se retornan todos, pero si se quiere devolver alguno o algunos de manera
        específica se debe heredar y rehacer la función.
        """
        kw = {}
        for field in form.fields:
            kw.update({field: form.cleaned_data[field]})
        return kw

    def form_valid(self, form):
        kw = {}
        event_action = None
        params = '?' + self.request.htmx.current_url_abs_path.split('?')[1] if self.request.htmx.current_url_abs_path.split('?').__len__() > 1 else ''
        if self.request.method == 'POST':
            event_action = self.request.POST.get('event_action', None)
        elif self.request.method == 'GET':
            event_action = self.request.GET.get('event_action', None)
        if form.is_valid():
            kw.update(self.get_fields_kwargs(form))
            if self.viewname:
                self.success_url = reverse_lazy(
                    self.viewname[event_action],
                    kwargs=kw
                )
            if self.funcname:
                func_ret = self.execute(func=self.funcname[event_action], kwargs=kw)
                if func_ret['success']:
                    if func_ret['success_title']:
                        sweetify.success(self.request, title=func_ret['success_title'], icon='success')
                else:
                    if func_ret['error_title']:
                        sweetify.error(self.request, title=func_ret['error_title'], icon='error')
                    event_action = 'not_submitted'
                self.success_url = reverse_lazy(self.father_view) + params
            return HttpResponseLocation(
                self.get_success_url(),
                target=self.hx_target,
                headers={
                    'HX-Trigger': self.request.htmx.trigger,
                    'HX-Trigger-Name': self.request.htmx.trigger_name,
                    'HX-Replace-Url': 'false',
                    'event_action': event_action,
                },
                values={
                    'event_action': event_action,
                }
            )
        else:
            return render(self.request, self.template_name, {
                'form': form,
            })

    def form_invalid(self, form, **kwargs):
        ctx = self.get_context_data(**kwargs)
        ctx['form'] = form
        response = render(self.request, self.template_name, ctx)
        response['HX-Retarget'] = self.hx_retarget
        response['HX-Reswap'] = self.hx_reswap
        return response

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx.update({
            'modal_form_title': self.modal_form_title,
            'max_width': self.max_width,
            'hx_target': self.hx_target,
            'hx_swap': self.hx_swap,
            'hx_form_target': self.hx_form_target,
            'hx_form_swap': self.hx_form_swap,
            'hx_retarget': self.hx_retarget,
            'hx_reswap': self.hx_reswap,
            'form_view': True,
            'inline_table': self.inline_tables,
            'btn_rechazar': None,
            'btn_aceptar': 'Aceptar',
        })
        return ctx

    @staticmethod
    def execute(func, *args, **kwargs):
        func_return = func(*args, **kwargs)
        return func_return

    def dispatch(self, request, *args, **kwargs):
        # Try to dispatch to the right method; if a method doesn't exist,
        # defer to the error handler. Also defer to the error handler if the
        # request method isn't on the approved list.
        if request.method.lower() in self.http_method_names:
            handler = getattr(
                self, request.method.lower(), self.http_method_not_allowed
            )
        else:
            handler = self.http_method_not_allowed
        return handler(request, *args, **kwargs)


class Noauthorized(TemplateView):
    template_name = 'app_index/cruds/403.html'
