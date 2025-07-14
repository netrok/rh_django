from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('superadmin', 'SuperAdmin'),
        ('admin', 'Admin'),
        ('rrhh', 'RRHH'),
        ('supervisor', 'Supervisor'),
        ('gerente', 'Gerente'),
        ('usuario', 'Usuario'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='usuario')

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"