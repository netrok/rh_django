from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    EmpleadoListCreateAPIView,
    EmpleadoRetrieveUpdateDestroyAPIView,
    EmpleadoDashboardAPIView,
    EmpleadoExportExcelAPIView,
    EmpleadoExportPdfAPIView,
    BitacoraListView,
    BitacoraEmpleadoAPIView,
)

from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

# ✅ Vista personalizada que devuelve el rol en el token
class CustomTokenView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

urlpatterns = [
    # ✅ Autenticación
    path('token/', CustomTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # ✅ Empleados
    path('empleados/', EmpleadoListCreateAPIView.as_view(), name='empleado-list-create'),
    path('empleados/<int:pk>/', EmpleadoRetrieveUpdateDestroyAPIView.as_view(), name='empleado-detail'),
    path('empleados/dashboard/', EmpleadoDashboardAPIView.as_view(), name='empleado-dashboard'),
    path('empleados/exportar-excel/', EmpleadoExportExcelAPIView.as_view(), name='empleado-exportar-excel'),
    path('empleados/export/pdf/', EmpleadoExportPdfAPIView.as_view(), name='empleados-export-pdf'),

    # ✅ Bitácora
    path('bitacora/', BitacoraListView.as_view(), name='bitacora-list'),
    path('bitacora/empleado/<int:empleado_id>/', BitacoraEmpleadoAPIView.as_view(), name='bitacora-empleado'),
]