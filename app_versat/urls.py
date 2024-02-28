from django.urls import path

from .general import views

app_name = 'appversat'
urlpatterns = [
    path('appversat/', views.GenUnidadcontableList.as_view(), name='uc_appversat'),
]

