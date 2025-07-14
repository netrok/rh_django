from django.db import models
from django.conf import settings  # ✅ para usar AUTH_USER_MODEL


# === MODELO EMPLEADO ===
class Empleado(models.Model):
    num_empleado = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=10)
    estado_civil = models.CharField(max_length=15)
    curp = models.CharField(max_length=18, unique=True)
    rfc = models.CharField(max_length=13, unique=True)
    nss = models.CharField(max_length=15, unique=True)
    telefono = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    puesto = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100)
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)
    foto = models.ImageField(upload_to='empleados/fotos/', null=True, blank=True)

    def __str__(self):
        return f"{self.num_empleado} - {self.nombres} {self.apellido_paterno}"


# === BITÁCORA DE EMPLEADO (DETALLADA) ===
class BitacoraEmpleado(models.Model):
    ACCIONES = [
        ('CREACIÓN', 'Creación'),
        ('EDICIÓN', 'Edición'),
        ('ELIMINACIÓN', 'Eliminación'),
    ]

    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    accion = models.CharField(max_length=20, choices=ACCIONES)
    fecha = models.DateTimeField(auto_now_add=True)
    detalles = models.TextField(blank=True)

    def __str__(self):
        return f'{self.accion} - {self.empleado} - {self.fecha.strftime("%Y-%m-%d %H:%M")}'


# === BITÁCORA GENERAL DEL SISTEMA ===
class Bitacora(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    modelo_afectado = models.CharField(max_length=100)
    objeto_id = models.PositiveIntegerField()
    accion = models.CharField(max_length=50)  # Ej: creado, actualizado, eliminado
    cambios = models.TextField(blank=True, null=True)  # JSON de diferencias o descripción
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.fecha} - {self.usuario} - {self.accion} {self.modelo_afectado} ({self.objeto_id})"