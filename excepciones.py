# Módulo que define la jerarquía de excepciones personalizadas para Software FJ

class ErrorSistemaFJ(Exception):
    """Excepción base para todos los errores controlados del sistema Software FJ."""
    pass


class DatoInvalidoError(ErrorSistemaFJ):
    """Se lanza cuando un dato de entrada no cumple con el formato, tipo o rango esperado."""
    pass


class ParametroFaltanteError(ErrorSistemaFJ):
    """Se lanza cuando se omite un parámetro obligatorio o llega vacío/nulo."""
    pass


class ServicioNoDisponibleError(ErrorSistemaFJ):
    """Se lanza cuando se intenta reservar un servicio inactivo o sin cupo/stock."""
    pass


class ReservaInvalidaError(ErrorSistemaFJ):
    """Se lanza ante conflictos de estado, duración inválida o inconsistencias en una reserva."""
    pass


class CalculoInconsistenteError(ErrorSistemaFJ):
    """Se lanza si el cálculo de costos produce valores negativos, nulos o fuera de regla."""
    pass


class OperacionNoPermitidaError(ErrorSistemaFJ):
    """Se lanza cuando se intenta ejecutar una acción prohibida según el estado de la entidad."""
    pass