import uuid

from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Now
from django.utils.translation import gettext_lazy as _

from codificadores.models import ObjectsManagerAbstract, ProductoFlujo, FichaCostoFilas, Medida


# Fichas de costo
class FichaCostoProducto(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fecha_creacion = models.DateTimeField(db_default=Now(), verbose_name=_("Crate at"))
    fecha = models.DateField(verbose_name=_("Date"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='productoflujo_ficha',
                                 verbose_name=_("Product"))
    um = models.ForeignKey(Medida, on_delete=models.PROTECT, related_name='ficha_medida',
                           verbose_name=_("U.M"))
    cantidad = models.IntegerField(default=0, validators=[MinValueValidator(0, message=_(
        'The value must be greater than 0'))])
    tasa = models.DecimalField(max_digits=10, decimal_places=6, db_comment='Tasa',
                               verbose_name=_("Tasa"),
                               validators=[MinValueValidator(0.000000, message=_(
                                   'The value must be greater than 0'))])
    activa = models.BooleanField(default=False, verbose_name=_("Active"))
    confirmada = models.BooleanField(default=False, verbose_name=_("Confirmada"))

    class Meta:
        db_table = 'cos_fichacostoproducto'
        ordering = ['fecha', 'producto', 'confirmada', '-activa']

        indexes = [
            models.Index(
                fields=[
                    'producto',
                    'activa',
                ]
            ),
        ]

    def __str__(self):
        return "%s %s | %s" % (
            self.fecha,
            self.producto.codigo,
            self.producto.descripcion
        )


class FichaCostoProductoFilas(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fichacostoproducto = models.ForeignKey(FichaCostoProducto, on_delete=models.CASCADE,
                                           related_name='fichacostoproducto_ficha',
                                           verbose_name=_("Ficha de Costo"))
    fila = models.ForeignKey(FichaCostoFilas, on_delete=models.PROTECT,
                             related_name='fichacostoproducto_fila')
    costo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00,
                                verbose_name=_("Costo"))

    class Meta:
        db_table = 'cos_fichacostoproductofila'
        ordering = ['fila']
        unique_together = (('fila', 'fichacostoproducto'),)


class FichaCostoProductoFilaDesgloseMPMat(ObjectsManagerAbstract):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    fila = models.ForeignKey(FichaCostoProductoFilas, on_delete=models.CASCADE,
                             related_name='desglosempmat_fila',
                             verbose_name=_("Fila"))
    producto = models.ForeignKey(ProductoFlujo, on_delete=models.PROTECT, related_name='filadesglose_producto',
                                 verbose_name=_("Product"))
    costo_base_norma = models.DecimalField(max_digits=10, decimal_places=4,
                                           db_default=0.00,
                                           verbose_name=_("Norma Costo Base"))
    costo_base_precio = models.DecimalField(max_digits=10, decimal_places=6,
                                            db_default=0.00,
                                            verbose_name=_("Precio Costo Base"))
    costo_base_importe = models.DecimalField(max_digits=10, decimal_places=2,
                                             db_default=0.00,
                                             verbose_name=_("Importe Costo Base"))

    costo_propuesto_norma = models.DecimalField(max_digits=10, decimal_places=4,
                                                db_default=0.00,
                                                verbose_name=_("Norma Costo Base"))
    costo_propuesto_precio = models.DecimalField(max_digits=10, decimal_places=6,
                                                 db_default=0.00,
                                                 verbose_name=_("Precio Costo Base"))
    costo_propuesto_importe = models.DecimalField(max_digits=10, decimal_places=2,
                                                  db_default=0.00,
                                                  verbose_name=_("Importe Costo Propuesto"))

    class Meta:
        db_table = 'cos_fichacostoproductofiladesglosempmat'
        ordering = ['fila', 'producto']
        unique_together = (('fila', 'producto'),)
