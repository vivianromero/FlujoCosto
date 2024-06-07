from rest_framework import serializers
from django.utils.timesince import timesince

from app_versat.general import GenUnidadcontable, GenMedida, MPMarca
from app_versat.inventario import InvDocumento, InvDocumentocta, InvDocumentogasto
import decimal

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

class InvDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvDocumento
        fields = ['fecha', 'numero', 'sumaimporte']

class InvDocumentogastoSerializer(serializers.ModelSerializer):
    iddocumento_fecha = serializers.SerializerMethodField()
    iddocumento_numero = serializers.ReadOnlyField(source='iddocumento.numero', read_only=True)
    iddocumento_sumaimporte = serializers.SerializerMethodField()

    def get_iddocumento_fecha(self, obj):
        return obj.iddocumento.fecha.date

    def get_iddocumento_sumaimporte(self, obj):
        return decimal.Decimal(obj.iddocumento.sumaimporte)

    class Meta:
        model = InvDocumentogasto
        fields = ['iddocumento', 'iddocumento_fecha', 'iddocumento_numero', 'iddocumento_sumaimporte']
