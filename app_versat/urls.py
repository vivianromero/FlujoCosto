from django.urls import path

from .general import views

app_name = 'appversat'
urlpatterns = [
    path('um_appversat/', views.GenUnidadMedidaList.as_view(), name='um_appversat'),
]


