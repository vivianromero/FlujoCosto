from rest_framework import serializers

from app_versat.general.general import GenUnidadcontable


class GenUnidadcontableSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenUnidadcontable
        fields = ['codigo', 'nombre', 'activo']