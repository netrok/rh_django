from rest_framework.permissions import BasePermission


class IsInGroupOrAdmin(BasePermission):
    """
    Permiso base que permite acceso si el usuario es admin (is_staff)
    o pertenece a uno de los grupos permitidos.
    """
    allowed_groups = []

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        # Acceso total si es admin (staff)
        if user.is_staff:
            return True

        # Acceso si pertenece a uno de los grupos permitidos
        return user.groups.filter(name__in=self.allowed_groups).exists()


class IsRRHHOrAdmin(IsInGroupOrAdmin):
    allowed_groups = ['RRHH']


class IsGerenteOrAdmin(IsInGroupOrAdmin):
    allowed_groups = ['Gerente']


class IsSupervisorOrAdmin(IsInGroupOrAdmin):
    allowed_groups = ['Supervisor']


class IsUsuarioOrAdmin(IsInGroupOrAdmin):
    allowed_groups = ['Usuario']


class IsExportadorAutorizado(IsInGroupOrAdmin):
    """
    Permite exportar empleados a usuarios en RRHH, Gerente,
    o cualquier usuario con privilegios de admin (staff/superuser).
    """
    allowed_groups = ['RRHH', 'Gerente']


class IsSuperAdmin(BasePermission):
    """
    Permiso exclusivo para superusuarios (is_superuser).
    """

    def has_permission(self, request, view):
        user = request.user
        return user and user.is_authenticated and user.is_superuser
