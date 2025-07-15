import re
from datetime import date
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Empleado, Bitacora, BitacoraEmpleado

# === SERIALIZER DE EMPLEADO ===


class EmpleadoSerializer(serializers.ModelSerializer):
    foto = serializers.ImageField(required=False, allow_null=True)  # ✅ Corrección aquí

    class Meta:
        model = Empleado
        fields = '__all__'

    def to_internal_value(self, data):
        data = data.copy()

        if 'activo' in data and isinstance(data['activo'], str):
            data['activo'] = data['activo'].lower() in ['true', '1', 'yes']

        return super().to_internal_value(data)

    def validate_fecha_ingreso(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de ingreso no puede ser futura.")
        return value

    def validate_fecha_nacimiento(self, value):
        if value > date.today():
            raise serializers.ValidationError("La fecha de nacimiento no puede ser futura.")
        return value

    def validate_curp(self, value):
        curp_regex = r'^[A-Z][AEIOU][A-Z]{2}\d{2}(0[1-9]|1[0-2])' \
                     r'(0[1-9]|[12]\d|3[01])[HM]' \
                     r'(AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|' \
                     r'PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS)' \
                     r'[B-DF-HJ-NP-TV-Z]{3}[0-9A-Z]\d$'
        if not re.match(curp_regex, value.upper()):
            raise serializers.ValidationError("CURP inválido.")
        qs = Empleado.objects.filter(curp=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un empleado con este CURP.")
        return value.upper()

    def validate_rfc(self, value):
        rfc_regex = r'^[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}$'
        if not re.match(rfc_regex, value.upper()):
            raise serializers.ValidationError("RFC inválido.")
        qs = Empleado.objects.filter(rfc=value)
        if self.instance:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise serializers.ValidationError("Ya existe un empleado con este RFC.")
        return value.upper()

    def validate_nss(self, value):
        if not re.match(r'^\d{11}$', value):
            raise serializers.ValidationError("NSS inválido. Deben ser 11 dígitos.")
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

    def validate_telefono(self, value):
        if not re.fullmatch(r'^\d{10}$', value):
            raise serializers.ValidationError("El número de teléfono debe tener exactamente 10 dígitos.")
        return value


# === SERIALIZER DE BITÁCORA GENERAL ===
class BitacoraSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = Bitacora
        fields = ['id', 'usuario', 'modelo_afectado', 'objeto_id', 'accion', 'cambios', 'fecha']


# === SERIALIZER DE BITÁCORA DE EMPLEADO ===
class BitacoraEmpleadoSerializer(serializers.ModelSerializer):
    usuario = serializers.StringRelatedField()

    class Meta:
        model = BitacoraEmpleado
        fields = ['id', 'accion', 'fecha', 'usuario', 'detalles']


# === TOKEN JWT PERSONALIZADO CON ROL ===
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role  # o user.get_role_display() si usas choices
        return token
