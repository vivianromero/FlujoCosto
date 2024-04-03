from django.utils.translation import gettext as _

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
}
