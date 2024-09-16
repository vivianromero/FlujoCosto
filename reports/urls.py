from django.urls import path, include
from reports.reports import ver_pdf

app_name = 'reportes'
urlpatterns = [
    path('reporte/pdf/', ver_pdf, name='ver_pdf'),
]
