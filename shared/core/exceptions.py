class FrameworkError(Exception):
    """Excepción base del framework."""


class BrowserLaunchError(FrameworkError):
    """El navegador no pudo lanzarse o configurarse."""


class ElementNotFoundError(FrameworkError):
    """Un elemento esperado no apareció en el DOM/UI."""


class WorkflowError(FrameworkError):
    """Un workflow de negocio falló (ej. login, compra)."""


class ConfigError(FrameworkError):
    """Configuración inválida o faltante."""
