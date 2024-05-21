from django.db.models import F

from .models import *


def ids_documentos_versat_procesados(fecha_inicio, fecha_fin, departamento, ueb):

    # id de los documentos que se han introducido al sistema durante el mes que se está procesando, ya que en el cierre
    # mensual no se permite dejar doc del versat sin procesar
    query_doc_acept = DocumentoOrigenVersat.objects.filter(fecha_documentoversat__gte=fecha_inicio,
                                                           fecha_documentoversat__lte=fecha_fin,
                                                           documento__departamento=departamento,
                                                           documento__ueb=ueb, ).values(
        iddocversat=F('documentoversat')).all()

    # id de los documentos que se han rechazado en el mes que se está procesando, ya que en el cierre
    # mensual no se permite dejar doc del versat sin procesar
    query_doc_rechaz = DocumentoVersatRechazado.objects.filter(
        fecha_documentoversat__gte=fecha_inicio,
        fecha_documentoversat__lte=fecha_fin,
        ueb=ueb).values(iddocversat=F('documentoversat')).all()

    docs = query_doc_acept.union(query_doc_rechaz)
    ids = [i['iddocversat'] for i in docs]
    return ids