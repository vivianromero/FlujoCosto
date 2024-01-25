from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# from .routers import router
from .views import (
    Index,
    Underconstruction,
    Dashboard,
)

app_name = 'app_index'

urlpatterns = [
    # Index
    path('', login_required(Index.as_view(), login_url='login/'), name='index'),
    path('under_construction/', Underconstruction.as_view(), name='under_construction'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    # Django-select2
    path("select2/", include("django_select2.urls")),
    # JWT auth
    path('api/auth/obtain_token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh_token/', TokenRefreshView.as_view(), name='token_refresh'),
    # Apps
    path('', include('app_auth.usuarios.urls')),
    path('', include('app_auth.grupos.urls')),
    path('', include('app_auth.permisos.urls')),
    path('', include('codificadores.urls')),

    # api
    # path('api/', include(router.urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
