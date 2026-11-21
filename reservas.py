"""Clase Reserva: integra cliente, servicio, duración y estado."""
from entidades import Cliente, EntidadBase
from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         ErrorSoftwareFJ, OperacionNoPermitidaError,
                         ReservaInvalidaError, ServicioNoDisponibleError)
from registro_logs import obtener_logger
from servicios import Servicio

PENDIENTE, CONFIRMADA, CANCELADA, PROCESADA = "PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"


class Reserva(EntidadBase):
    """Reserva con ciclo de vida: PENDIENTE -> CONFIRMADA -> PROCESADA (o CANCELADA)."""

    def __init__(self, identificador, cliente, servicio, horas, **extras):
        super().__init__(identificador)
        try:
            if not isinstance(cliente, Cliente):                        # Cliente debe ser válido
                raise DatoInvalidoError("La reserva requiere un Cliente válido.")
            if not isinstance(servicio, Servicio):                      # Servicio debe ser válido
                raise DatoInvalidoError("La reserva requiere un Servicio válido.")
            if not isinstance(horas, (int, float)) or not 0 < horas <= 12:  # Duración 0-12 h
                raise DatoInvalidoError(f"Duración inválida: {horas!r} (máx. 12 h).")
            if not servicio.disponible:
                raise ServicioNoDisponibleError(f"'{servicio.nombre}' no está disponible.")
            servicio.validar_parametros(**extras)                       # Validación específica (polimorfismo)
        except ErrorSoftwareFJ as causa:
            # Encadenamiento de excepciones: se conserva la causa original con 'from'
            raise ReservaInvalidaError(f"No se pudo crear la reserva {identificador}") from causa
        self._cliente, self._servicio = cliente, servicio
        self._horas, self._extras = float(horas), extras
        self._estado = PENDIENTE                                        # Estado inicial
        self._costo = None                                              # Se calcula al procesar

    @property
    def estado(self): return self._estado

    @property
    def costo(self): return self._costo

    def confirmar(self):
        """Solo una reserva PENDIENTE puede confirmarse."""
        if self._estado != PENDIENTE:
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva {self._estado}.")
        self._estado = CONFIRMADA

    def cancelar(self):
        """No se puede cancelar una reserva ya procesada o cancelada."""
        if self._estado in (PROCESADA, CANCELADA):
            raise OperacionNoPermitidaError(f"No se puede cancelar una reserva {self._estado}.")
        self._estado = CANCELADA

    def procesar(self, descuento: float = 0.0):
        """Calcula el costo final. Demuestra try/except/else/finally."""
        log = obtener_logger()
        try:
            if self._estado != CONFIRMADA:
                raise OperacionNoPermitidaError("Solo se procesan reservas CONFIRMADAS.")
            total = self._servicio.calcular_costo_total(self._horas, descuento, **self._extras)
            if total <= 0:
                raise CalculoInconsistenteError(f"Costo no positivo: {total}")
        except (OperacionNoPermitidaError, CalculoInconsistenteError) as causa:
            raise ReservaInvalidaError(f"Fallo al procesar {self.identificador}") from causa  # Encadena
        else:
            self._costo, self._estado = total, PROCESADA               # Solo si no hubo error
            return total
        finally:
            log.info("Intento de procesamiento de %s (estado: %s)", self.identificador, self._estado)

    def mostrar_informacion(self) -> str:
        costo = f"${self._costo:,.2f}" if self._costo is not None else "sin calcular"
        return (f"Reserva[{self.identificador}] {self._cliente.nombre} -> {self._servicio.nombre} "
                f"| {self._horas}h | {self._estado} | {costo}")
