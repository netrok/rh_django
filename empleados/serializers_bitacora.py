# empleados/serializers_bitacora.py
from rest_framework import serializers
from .models import BitacoraEmpleado


class BitacoraEmpleadoSerializer(serializers.ModelSerializer):
    empleado_nombre = serializers.CharField(source='empleado.nombres', read_only=True)
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)

    class Meta:
        model = BitacoraEmpleado
        fields = ['id', 'empleado', 'empleado_nombre', 'usuario', 'usuario_username', 'accion', 'fecha', 'detalles']
