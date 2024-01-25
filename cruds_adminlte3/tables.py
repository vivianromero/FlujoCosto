import django_tables2 as tables
from django.utils.translation import gettext as _
from cruds_adminlte3.utils import attrs_center_center

dt_version = tuple(map(int, tables.__version__.split(".")[:3]))


class ColumnShiftTable(tables.Table):
    # If button for shifting columns is visible
    shift_table_column = True

    # If button is placed above table or not. If not, must be placed in your own template somewhere
    button_above_table = True

    # If true, instead of a button, a link will be rendered with dropdown menu
    nav_link = False

    # Class container for .btn-shift-column class to get the state 'off'.
    # It must be set to another value if 'button_above_table' is set to false,
    # becouse buttons will be out of '.table-container'
    button_shift_class_container = ".table-container"

    # Which columns are visible by default
    column_default_show = None

    # List of columns to exclude from choice
    column_excluded = None

    # Shifter template for tabel inherit from django_table2/bootstrap.html
    shifter_template = "cruds/django_tables2_column_shifter/table.html"

    # Css class for dropdown button above table
    dropdown_button_css = "btn btn-default btn-xs"

    def __init__(self, *args, **kwargs):
        """Override init for set shifter template"""
        super(ColumnShiftTable, self).__init__(*args, **kwargs)
        # Override default template
        if hasattr(self, "template_name"):
            self.template_name = self.shifter_template
        else:
            self.template = self.shifter_template

    def get_column_default_show(self):
        """
        Returns the columns that are visible by default
        If self.column_default_show is None then
        # default visible columns will be return from sequence
        """
        return self.column_default_show or self.sequence

    def get_column_excluded(self):
        """
        Excluded columns are not shown on list to choice
        """
        return self.column_excluded or []

    @property
    def uniq_table_class_name(self):
        """Return unique name of table class
        using in template for container div id
        prefix in django_tables2 is always a string, can be empty or not
        """
        class_name = self.__class__.__name__
        prefix = self.prefix
        return "{pref}{cls}".format(pref=prefix, cls=class_name)

    @property
    def get_dropdown_button_css(self):
        """Return css class for dropdown button above table."""
        return self.dropdown_button_css

    def get_column_class_names(self, classes_set, bound_column):
        """
        Ovveriden method to save back compability.
        Add column names as css class to the attribute of table cells.
        This functionality was changed in django table2 >= 2.0.
        """
        cset = super(ColumnShiftTable, self).get_column_class_names(classes_set, bound_column)
        cset.add(bound_column.name)
        return cset


class ColumnShiftTableBootstrap2(ColumnShiftTable):
    """
    Table class compatible with bootstrap 2
    """
    dropdown_button_css = "btn btn-small"
    shifter_template = "cruds/django_tables2_column_shifter/bootstrap2.html"


class ColumnShiftTableBootstrap3(ColumnShiftTable):
    """
    Table class compatible with bootstrap 3
    """
    shifter_template = "cruds/django_tables2_column_shifter/bootstrap3.html"


class ColumnShiftTableBootstrap4(ColumnShiftTable):
    """
    Table class compatible with bootstrap 4
    """
    shifter_template = "cruds/django_tables2_column_shifter/bootstrap4.html"


class ColumnShiftTableBootstrap4Responsive(ColumnShiftTable):
    """
    Table class compatible with Bootstrap 4 and using "table-responsive" css class.
    """
    shifter_template = "cruds/django_tables2_column_shifter/bootstrap4-responsive.html"

    def __init__(self, *args, **kwargs):
        if dt_version < (2, 5):
            raise AssertionError(
                "ColumnShiftTableBootstrap4Responsive require django-tables2 >= 2.5 "
                "your current version is {}".format(tables.__version__)
            )
        super(ColumnShiftTableBootstrap4Responsive, self).__init__(*args, **kwargs)


class ColumnShiftTableBootstrap5(ColumnShiftTable):
    """
    Table class compatible with bootstrap 5
    """
    dropdown_button_css = "btn btn-light btn-sm"
    shifter_template = "cruds/django_tables2_column_shifter/bootstrap5.html"

    def __init__(self, *args, **kwargs):
        if dt_version < (2, 5):
            raise AssertionError(
                "ColumnShiftTableBootstrap5 require django-tables2 >= 2.5 "
                "your current version is {}".format(tables.__version__)
            )
        super(ColumnShiftTableBootstrap5, self).__init__(*args, **kwargs)


class ColumnShiftTableBootstrap5Responsive(ColumnShiftTableBootstrap5):
    """
    Table class compatible with Bootstrap 5 and using "table-responsive" css class.
    """
    shifter_template = "cruds/django_tables2_column_shifter/bootstrap5-responsive.html"

    def __init__(self, *args, **kwargs):
        if dt_version < (2, 5, 3):
            raise AssertionError(
                "ColumnShiftTableBootstrap5Responsive require django-tables2 >= 2.5.3 "
                "your current version is {}".format(tables.__version__)
            )
        super(ColumnShiftTableBootstrap5Responsive, self).__init__(*args, **kwargs)


class CommonColumnShiftTableBootstrap4ResponsiveActions(ColumnShiftTableBootstrap4Responsive):
    shifter_template = "cruds/django_tables2_column_shifter/my-hx-bootstrap4-responsive.html"

    button_above_table = False

    nav_link = True

    button_shift_class_container = "shift-container"

    col_vis = []  # lista usada para gestionar el visionado de columnas de la tabla

    getparams = None

    actions = tables.TemplateColumn(
        template_name='cruds/actions/hx_actions_template.html',
        verbose_name=_('Actions'),
        exclude_from_export=True,
        orderable=False,
        attrs=attrs_center_center
    )

    class Meta:
        attrs = {
            "class": 'table display table-sm table-bordered table-striped table-hover',
            "style": 'line-height: 1;',
            "td": {
                "class": "align-middle",
                "style": 'padding: 0px;',
            },
        }
        model = None  # Must be filled in descendant classes

        fields = None # Must be filled in descendant classes

        template_name = "django_tables2/bootstrap4.html"
        table_pagination = {
            "per_page": 10
        }

    def before_render(self, request):
        """
        Método para gestionar el visionado de columnas.
        Si la columna aparece en la lista 'col_vis' entonces se ocultará dicha columna
        """
        if request.htmx:
            for col in self.col_vis:
                self.columns.hide(col)
