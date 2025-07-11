from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Empleado
from .utils import registrar_bitacora


@receiver(post_save, sender=Empleado)
def auditar_guardado_empleado(sender, instance, created, **kwargs):
    accion = 'creado' if created else 'actualizado'
    registrar_bitacora(instancia=instance, accion=accion)


@receiver(post_delete, sender=Empleado)
def auditar_eliminacion_empleado(sender, instance, **kwargs):
    registrar_bitacora(instancia=instance, accion='eliminado')
