from django.urls import path

from . import views

app_name = 'apiversat'
urlpatterns = [
    path('uc_apiversat/', views.UC_Versat, name='uc_apiversat'),
    path('cc_apiversat/', views.CC_Versat, name='cc_apiversat'),
]