from django.db import transaction
from django.db.models import F
from django.db.models.query_utils import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django_htmx.http import HttpResponseClientRedirect
from rest_framework.views import APIView

from codificadores import ChoiceTiposProd, ChoiceClasesMatPrima
from codificadores.models import UnidadContable, Medida, MarcaSalida, Cuenta, ProductoFlujo, TipoProducto, \
    ClaseMateriaPrima, ProductoFlujoClase, Vitola, CategoriaVitola, TipoVitola
from flujo.models import Documento
from cruds_adminlte3.utils import crud_url_name
from utiles.utils import message_success, message_error
from .general import GenProducto, SisPaxVitola
from .inventario import InvDocumento
from .contabilidad import ConCuentanat
from .serializersdata import *
from rest_framework.response import Response
from django.core import serializers



class GenUnidadMedidaList(APIView):
    """
    Devuelve las unidades de medida
    """

    def get(self, request, format=None):
        try:
            medida = GenMedida.objects.all()
            serializer = GenUnidadMedidaSerializer(medida, many=True)
            data = serializer.data
            datos = [Medida(clave=item['clave'].strip(), descripcion=item['descripcion'].strip()) for item in data]
            Medida.objects.bulk_update_or_create(datos, ['descripcion'], match_field='clave')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(Medida, 'list', 'app_index:codificadores:'))


class GenUnidadContableList(APIView):
    """
    Devuelve las unidades contable
    """

    def get(self, request, format=None):
        try:
            medida = GenUnidadcontable.objects.all()
            serializer = GenUnidadcontableSerializer(medida, many=True)
            data = serializer.data
            datos = [UnidadContable(codigo=item['codigo'].strip(), nombre=item['nombre'].strip(), activo=item['activo']) for item in
                     data_json]
            UnidadContable.objects.bulk_update_or_create(datos, ['nombre', 'activo'], match_field='codigo')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(UnidadContable, 'list', 'app_index:codificadores:'))


class MPMarcaList(APIView):
    """
    Devuelve las MARCAS DE SALIDA desde SisGestMP
    """

    def get(self, request, format=None):
        try:
            marca = MPMarca.objects.all()
            serializer = MPMarcaSerializer(marca, many=True)
            data = serializer.data
            datos = [MarcaSalida(codigo=item['codigoMarca'].strip(), descripcion=item['descripcion'].strip()) for item in data]
            MarcaSalida.objects.bulk_update_or_create(datos, ['descripcion'], match_field='codigo')
            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(MarcaSalida, 'list', 'app_index:codificadores:'))


class ConCuentanatList(APIView):
    """
    Devuelve clasificador de cuentas
    """

    def get(self, request, format=None):
        try:
            cuentanat = ConCuentanat.objects.select_related().values(
                long_niv=F('idcuenta__idapertura__idmascara__longitud'),
                posicion=F('idcuenta__idapertura__idmascara__posicion'),
                clave_cta=F('idcuenta__clave'),
                descripcion_cta=F('descripcion'),
                naturaleza_cta=F('naturaleza'),
                clavenivel=F('cuenta'),
                activa=F('idcuenta__activa'),
            ).order_by('clave_cta', 'posicion').all()
            # Llenar las cuentas
            dicc_pk_posicion = {}
            for c in cuentanat:
                posicion = c['posicion']
                clavenivel = c['clavenivel']
                descripcion = c['descripcion_cta']
                long_niv = c['long_niv']
                parent = Cuenta.objects.get(pk=dicc_pk_posicion[posicion - 1]['pk_ant']) if posicion > 1 else None
                clave = dicc_pk_posicion[posicion - 1]['clave_ant'] + '-' + clavenivel.ljust(
                    long_niv) if posicion > 1 else c[
                    'clavenivel']
                cta = Cuenta.objects.update_or_create(clave=clave, defaults={"long_niv": long_niv, "posicion": posicion,
                                                                             "clave": clave, "clavenivel": clavenivel,
                                                                             "descripcion": descripcion,
                                                                             "parent": parent}
                                                      )
                dicc_pk_posicion[posicion] = {'pk_ant': cta[0].pk, 'clave_ant': clave}

            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(Cuenta, 'list', 'app_index:codificadores:'))


class ProductoFlujoList(APIView):
    """
    Devuelve los parametros para pedir los productos
    """

    @transaction.atomic
    def get(self, request, format=None, valor_inicial=None, clase_mat_prima=None):
        try:
            tipo = TipoProducto.objects.get(pk=ChoiceTiposProd.MATERIAPRIMA)  # materia prima
            clase = ClaseMateriaPrima.objects.get(pk=clase_mat_prima)
            data = GenProducto.objects.filter(codigo__startswith=valor_inicial).all()
            datos = []
            datos_clase = []
            cod_prod = []
            for item in data:
                codigo = item.codigo.strip()
                descripcion = item.descripcion.strip()
                clave_medida = item.idmedida.clave.strip()
                medida = Medida.objects.filter(clave=clave_medida)
                prod = ProductoFlujo(codigo=codigo, descripcion=descripcion, tipoproducto=tipo,
                                     medida=medida[0] if medida.exists() else Medida.objects.create(
                                         clave=clave_medida, descripcion=item.idmedida.descripcion.strip()))

                datos.append(prod)
                cod_prod.append(prod.codigo)
            ProductoFlujo.objects.bulk_update_or_create(datos, ['descripcion', 'tipoproducto', 'medida'],
                                                        match_field='codigo')
            datos_clase = [ProductoFlujoClase(clasemateriaprima=clase, producto=prod) for prod in
                           ProductoFlujo.objects.filter(codigo__in=cod_prod)]
            ProductoFlujoClase.objects.bulk_update_or_create(datos_clase, ['clasemateriaprima'],
                                                             match_field='producto')

            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return HttpResponseClientRedirect(reverse_lazy('app_index:codificadores:codificadores_productoflujo_list'))


class VitolaList(APIView):
    """
    Vitolas
    """

    @transaction.atomic()
    def get(self, request, format=None):
        try:
            tipoprodVit = TipoProducto.objects.get(pk=ChoiceTiposProd.VITOLA)
            tipoprodPesada = TipoProducto.objects.get(pk=ChoiceTiposProd.PESADA)
            tipoprodMP = TipoProducto.objects.get(pk=ChoiceTiposProd.MATERIAPRIMA)
            claseCapa = ClaseMateriaPrima.objects.get(pk=ChoiceClasesMatPrima.CAPACLASIFICADA)
            vitolas = SisPaxVitola.objects.select_related().all()

            datos = []
            cod_prod_capa = []
            cod_prod_pesada = []
            cod_prod_vitola = []
            datos_vitola = []
            clase_capa = []
            all_prods = ProductoFlujo.objects.filter(
                Q(tipoproducto__in=[ChoiceTiposProd.PESADA, ChoiceTiposProd.VITOLA]) |
                Q(productoflujoclase_producto__clasemateriaprima=ChoiceClasesMatPrima.CAPACLASIFICADA))
            for item in vitolas:
                # producto vitola
                codigo = item.fk_prod.codigo
                descripcion = item.fk_prod.descripcion.strip()
                clave_medida = item.fk_prod.fk_um.clave.strip()
                medida = Medida.objects.filter(clave=clave_medida)
                prod = ProductoFlujo(codigo=codigo, descripcion=descripcion, tipoproducto=tipoprodVit,
                                     medida=medida[0] if medida.exists() else Medida.objects.create(
                                         clave=clave_medida, descripcion=item.fk_prod.fk_um.descripcion.strip()))

                cod_prod_vitola.append(prod.codigo)
                datos.append(prod)

                # producto pesada
                clave_medida = item.prod_pesada.fk_um.clave.strip()
                medida = Medida.objects.filter(clave=clave_medida)
                prod_pesada = ProductoFlujo(codigo=item.prod_pesada.codigo, descripcion=item.prod_pesada.descripcion,
                                            tipoproducto=tipoprodPesada,
                                            medida=medida[0] if medida.exists() else Medida.objects.create(
                                                clave=clave_medida,
                                                descripcion=item.prod_pesada.fk_um.descripcion.strip()))

                cod_prod_pesada.append(prod_pesada.codigo)
                datos.append(prod_pesada)

                # producto capa clasificada
                clave_medida = item.prod_capa.fk_um.clave.strip()
                medida = Medida.objects.filter(clave=clave_medida)

                prod_capa = ProductoFlujo(codigo=item.prod_capa.codigo, descripcion=item.prod_capa.descripcion,
                                          tipoproducto=tipoprodMP,
                                          medida=medida[0] if medida.exists() else Medida.objects.create(
                                              clave=clave_medida, descripcion=item.prod_capa.fk_um.descripcion.strip()))

                cod_prod_capa.append(prod_capa.codigo)
                datos.append(prod_capa)

                prodCapa = all_prods.filter(codigo=prod_capa.codigo).first()

                clase_capa.append(ProductoFlujoClase(clasemateriaprima=claseCapa, producto=prod_capa if not prodCapa else prodCapa))

                categoriavitola = CategoriaVitola.objects.get(pk=item.fk_cat.id)
                tipovitola = TipoVitola.objects.get(pk=item.fk_tipo.id)

                prodVit = all_prods.filter(codigo=prod.codigo).first()
                prodPesada = all_prods.filter(codigo=prod_pesada.codigo).first()

                vit = Vitola(diametro=item.diametro, longitud=item.longitud, destino=item.destino, cepo=item.cepo,
                             categoriavitola=categoriavitola,
                             producto=prod if not prodVit else prodVit, tipovitola=tipovitola,
                             pesada=prod_pesada if not prodPesada else prodPesada,
                             capa=prod_capa if not prodCapa else prodCapa)
                datos_vitola.append(vit)

            prod_flujo = ProductoFlujo.objects.bulk_update_or_create(datos, ['descripcion', 'tipoproducto', 'medida'],
                                                                     match_field='codigo')

            prod_class = ProductoFlujoClase.objects.bulk_update_or_create(clase_capa, ['clasemateriaprima'],
                                                                          match_field='producto')

            Vitola.objects.bulk_update_or_create(datos_vitola, ['diametro', 'longitud', 'destino', 'cepo',
                                                                'categoriavitola', 'tipovitola'],
                                                 match_field='producto')

            message_success(request=request, title=_("Success"), text=_('Data importation was successful'))
        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        return redirect(crud_url_name(ProductoFlujo, 'list', 'app_index:codificadores:'))

class DocumnetosInvList(APIView):
    """
    Devuelve documentos
    """

    def get(self, request, format=None):

        try:
            # docum = InvDocumento.objects.filter(fecha__date__range=['2023-01-01', '2023-01-31'])
            docum = InvDocumento.objects.all()
            serializer = InvDocumentoSerializer(docum, many=True)

        except Exception as e:
            message_error(request=request, title=_("Couldn't update"), text=_('Data error'))
        # return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'))
        return Response(serializer.data)
        # return redirect(crud_url_name(Documento, 'list', 'app_index:flujo:'), context={'data':serializer.data})
        # return redirect(crud_url_name(Cuenta, 'list', 'app_index:codificadores:'))
        # json_data = serializers.serialize("json", docum)
        # return Response(json_data)