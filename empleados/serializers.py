from datetime import date
from rest_framework import serializers
from .models import Empleado, Bitacora, BitacoraEmpleado


class EmpleadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Empleado
        fields = '__all__'

    # ✅ Fecha de ingreso no puede ser futura
    def validate_fecha_ingreso(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de ingreso no puede ser futura.")
        return value

    # ✅ Fecha de nacimiento no puede ser futura
    def validate_fecha_nacimiento(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value

    # ✅ Validaciones únicas, ignorando el mismo registro al editar
    def validate_curp(self, value):
        qs = Empleado.objects.filter(curp=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un empleado con este CURP.")
        return value

    def validate_rfc(self, value):
        qs = Empleado.objects.filter(rfc=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un empleado con este RFC.")
        return value

    def validate_nss(self, value):
        qs = Empleado.objects.filter(nss=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un empleado con este NSS.")
        return value

    def validate_email(self, value):
        qs = Empleado.objects.filter(email=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un empleado con este email.")
        return value


class BitacoraSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Bitacora
        fields = ['id', 'usuario', 'modelo_afectado', 'objeto_id', 'accion', 'cambios', 'fecha']


class BitacoraEmpleadoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = BitacoraEmpleado
        fields = ['id', 'accion', 'fecha', 'usuario', 'detalles']
