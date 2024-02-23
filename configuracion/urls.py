from django.urls import path, include
from . import views

# ueb_crud = views.UebCRUD()
user_ueb_crud = views.UserUebCRUD()

app_name = 'configuracion'

urlpatterns = [
    # path("", include(ueb_crud.get_urls())),
    path("", include(user_ueb_crud.get_urls())),
]
