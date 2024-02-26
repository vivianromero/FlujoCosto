from rest_framework import viewsets, permissions

from codificadores.models import Cuenta
from .serializers import CuentaSerializer


class CuentaViewSet(viewsets.ModelViewSet):
    queryset = Cuenta.objects.all()
    serializer_class = CuentaSerializer
    permission_classes = [permissions.IsAuthenticated]
