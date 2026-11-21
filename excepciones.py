"""Excepciones personalizadas del sistema Software FJ."""


class ErrorSoftwareFJ(Exception):
    """Excepción base: todas las demás excepciones del sistema heredan de ella."""


class DatoInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando un dato no cumple las reglas de validación."""


class ParametroFaltanteError(ErrorSoftwareFJ):
    """Se lanza cuando falta un parámetro obligatorio."""


class ClienteInvalidoError(ErrorSoftwareFJ):
    """Se lanza cuando no es posible crear o usar un cliente."""


class ServicioNoDisponibleError(ErrorSoftwareFJ):
    """Se lanza cuando el servicio solicitado no está disponible."""


class ReservaInvalidaError(ErrorSoftwareFJ):
    """Se lanza cuando una reserva es incorrecta o falla su procesamiento."""


class OperacionNoPermitidaError(ErrorSoftwareFJ):
    """Se lanza cuando se intenta una operación no válida para el estado actual."""


class CalculoInconsistenteError(ErrorSoftwareFJ):
    """Se lanza cuando un cálculo de costos produce un resultado incoherente."""
