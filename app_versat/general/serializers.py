from rest_framework import serializers

from app_versat.general.general import GenUnidadcontable, GenMedida, \
    MPMarca


class GenUnidadcontableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenUnidadcontable
        fields = ['codigo', 'nombre', 'activo']

class GenUnidadMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenMedida
        fields = ['clave', 'descripcion']

class MPMarcaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MPMarca
        fields = ['codigoMarca', 'descripcion']