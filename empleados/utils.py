import json
from .models import Bitacora, BitacoraEmpleado, Empleado


def registrar_bitacora(instancia, accion, usuario=None, cambios=None, instancia_anterior=None):
    """
    Registra una entrada en la bitácora general del sistema y en la bitácora de empleados (si aplica).

    Parámetros:
    - instancia: objeto afectado (ej. un Empleado)
    - accion: 'CREACIÓN', 'EDICIÓN', 'ELIMINACIÓN'
    - usuario: usuario que realizó la acción
    - cambios: cambios personalizados opcionales (dict)
    - instancia_anterior: versión anterior del objeto (solo para ediciones)
    """
    modelo_nombre = instancia.__class__.__name__
    objeto_id = instancia.pk

    # Detectar cambios si es EDICIÓN
    if accion == 'EDICIÓN' and instancia_anterior:
        cambios = {}
        for field in instancia._meta.fields:
            nombre = field.name
            antes = getattr(instancia_anterior, nombre, None)
            despues = getattr(instancia, nombre, None)
            if antes != despues:
                cambios[nombre] = {
                    "antes": str(antes),
                    "después": str(despues)
                }

    # Para CREACIÓN sin cambios personalizados
    elif accion == 'CREACIÓN' and not cambios:
        cambios = {
            field.name: str(getattr(instancia, field.name))
            for field in instancia._meta.fields
        }

    # Serializar cambios a JSON
    cambios_json = json.dumps(cambios or {}, ensure_ascii=False, indent=2)

    # Validar usuario autenticado
    usuario_valido = usuario if usuario and getattr(usuario, "is_authenticated", False) else None

    # === Bitácora general ===
    Bitacora.objects.create(
        usuario=usuario_valido,
        modelo_afectado=modelo_nombre,
        objeto_id=objeto_id,
        accion=accion,
        cambios=cambios_json
    )

    # === Bitácora específica de empleados ===
    if isinstance(instancia, Empleado):
        BitacoraEmpleado.objects.create(
            empleado=instancia,
            usuario=usuario_valido,
            accion=accion,
            detalles=f"Cambio detectado:\n{cambios_json}"
        )


def registrar_exportacion_empleados(request, tipo_exportacion):
    """
    Registra una exportación masiva de empleados (Excel o PDF).
    """
    usuario_valido = request.user if request.user and request.user.is_authenticated else None

    Bitacora.objects.create(
        usuario=usuario_valido,
        modelo_afectado='Empleado',
        objeto_id=0,
        accion=f"Exportación a {tipo_exportacion}",
        cambios=json.dumps({
            "detalle": f"Exportación masiva de empleados a {tipo_exportacion.upper()}"
        }, ensure_ascii=False, indent=2)
    )


def registrar_intento_fallido_exportacion(request, tipo_exportacion):
    """
    Registra un intento fallido de exportación por falta de permisos.
    """
    usuario_valido = request.user if request.user and request.user.is_authenticated else None

    Bitacora.objects.create(
        usuario=usuario_valido,
        modelo_afectado='Empleado',
        objeto_id=0,
        accion=f"Intento fallido de exportación a {tipo_exportacion}",
        cambios=json.dumps({
            "detalle": f"Intento NO autorizado de exportar empleados a {tipo_exportacion.upper()}"
        }, ensure_ascii=False, indent=2)
    )
