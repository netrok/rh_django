from django.urls import path
from .views import (
    EmpleadoListCreateAPIView,
    EmpleadoRetrieveUpdateDestroyAPIView,
    EmpleadoDashboardAPIView,
    EmpleadoExportExcelAPIView,
    EmpleadoExportPdfAPIView,
    BitacoraListView,
    BitacoraEmpleadoAPIView  # ✅ IMPORTACIÓN QUE FALTABA
)

urlpatterns = [
    path('empleados/', EmpleadoListCreateAPIView.as_view(), name='empleado-list-create'),
    path('empleados/<int:pk>/', EmpleadoRetrieveUpdateDestroyAPIView.as_view(), name='empleado-detail'),
    path('empleados/dashboard/', EmpleadoDashboardAPIView.as_view(), name='empleado-dashboard'),
    path('empleados/exportar-excel/', EmpleadoExportExcelAPIView.as_view(), name='empleado-exportar-excel'),
    path('empleados/export/pdf/', EmpleadoExportPdfAPIView.as_view(), name='empleados-export-pdf'),

    # ✅ Bitácora general y por empleado
    path('bitacora/', BitacoraListView.as_view(), name='bitacora-list'),
    path('bitacora/empleado/<int:empleado_id>/', BitacoraEmpleadoAPIView.as_view(), name='bitacora-empleado'),
]
