from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from empleados.models import Empleado

User = get_user_model()


class TestEmpleadoAPI(APITestCase):
    def setUp(self):
        self.super_user = User.objects.create_user(
            username='superadmin',
            password='admin123',
            is_staff=True,
            is_superuser=True  # 👈 Esto activa permisos de SuperAdmin
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.super_user)

        self.empleado = Empleado.objects.create(
            num_empleado="E001",
            nombres="Juan",
            apellido_paterno="Pérez",
            apellido_materno="Gómez",
            fecha_nacimiento="1990-01-01",
            genero="Masculino",
            estado_civil="Soltero",
            curp="PEGA900101HDFRZN09",
            rfc="PEGA900101AAA",
            nss="12345678901",
            telefono="5551234567",
            email="juan.perez@example.com",
            puesto="Desarrollador",
            departamento="TI",
            fecha_ingreso="2020-01-01",
            activo=True,
        )

    def test_listar_empleados(self):
        url = reverse('empleado-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_crear_empleado(self):
        url = reverse('empleado-list-create')
        data = {
            "num_empleado": "E002",
            "nombres": "Ana",
            "apellido_paterno": "López",
            "apellido_materno": "Hernández",
            "fecha_nacimiento": "1992-02-02",
            "genero": "Femenino",
            "estado_civil": "Casada",
            "curp": "LOHA920202MDFRZN01",
            "rfc": "LOHA920202BBB",
            "nss": "10987654321",
            "telefono": "5559876543",
            "email": "ana.lopez@example.com",
            "puesto": "Analista",
            "departamento": "RH",
            "fecha_ingreso": "2021-02-01",
            "activo": True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_actualizar_empleado(self):
        url = reverse('empleado-detail', kwargs={'pk': self.empleado.pk})
        data = {"puesto": "Líder de Proyecto"}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["puesto"], "Líder de Proyecto")

    def test_eliminar_empleado(self):
        url = reverse('empleado-detail', kwargs={'pk': self.empleado.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_exportar_excel(self):
        url = reverse('empleado-exportar-excel')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.get("Content-Type"),
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

    def test_exportar_pdf(self):
        url = reverse('empleados_export_pdf')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.get("Content-Type"), "application/pdf")

    def test_dashboard_empleados(self):
        url = reverse('empleado-dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("total_empleados", response.data)
