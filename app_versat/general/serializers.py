from rest_framework import serializers

from app_versat.general.general import GenUnidadcontable, GenMedida


class GenUnidadcontableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenUnidadcontable
        fields = ['codigo', 'nombre', 'activo']

class GenUnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenMedida
        fields = ['clave', 'descripcion']