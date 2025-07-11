# 🧠 Sistema de Recursos Humanos - Django API

Este repositorio contiene el backend del **Sistema de Recursos Humanos** desarrollado en **Django + Django REST Framework**, con funcionalidades avanzadas como bitácora de auditoría, exportaciones, filtros, seguridad por roles y mucho más.

---

## 🚀 Tecnologías utilizadas

- Python 3.11+
- Django 4.x
- Django REST Framework
- PostgreSQL (recomendado)
- Django Filters
- WeasyPrint (PDF)
- OpenPyXL (Excel)
- JWT Authentication (con djangorestframework-simplejwt)

---

## ⚙️ Funcionalidades clave

✅ Gestión de empleados (CRUD completo)  
✅ Filtros, búsqueda y ordenamiento avanzado  
✅ Dashboard de estadísticas por edad, género, puesto y más  
✅ Exportación profesional a **Excel y PDF**  
✅ Bitácora general de cambios (creación, edición, eliminación)  
✅ Bitácora específica por empleado  
✅ Seguridad avanzada por roles (`SuperAdmin`, `Admin`, `RRHH`, etc.)  
✅ Validaciones de integridad referencial y datos únicos  
✅ Serializadores robustos con validaciones personalizadas  

---

## 🔐 Seguridad y permisos

El sistema implementa permisos por rol utilizando clases personalizadas como:

- `IsSuperAdmin`
- `IsGerenteOrAdmin`
- `IsRRHHOrAdmin`

Esto asegura que cada acción esté limitada a quien le corresponda.

---

## 📦 Instalación rápida

```bash
# Clonar el proyecto
git clone https://github.com/TU_USUARIO/rh_django.git
cd rh_django

# Crear entorno virtual
python -m venv venv
source venv/Scripts/activate

# Instalar dependencias
pip install -r requirements.txt

# Migraciones y superusuario
python manage.py migrate
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver

