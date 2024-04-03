from django_tables2.templatetags.django_tables2 import QuerystringNode

from cruds_adminlte3.templatetags import register


@register.simple_tag(takes_context=True)
def exclude_columns_url(context, columns=None):

    exclude_columns_trigger_param = "exclude_columns"
    if columns is None:
        columns = ''

    return QuerystringNode(updates={exclude_columns_trigger_param: columns}, removals=[]).render(
        context
    )