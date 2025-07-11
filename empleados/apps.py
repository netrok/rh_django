from django.apps import AppConfig


class EmpleadosConfig(AppConfig):
    name = 'empleados'

    def ready(self):
        import empleados.signals  # noqa: F401
