"""Clase abstracta Servicio y tres servicios especializados."""
from abc import abstractmethod

from entidades import EntidadBase
from excepciones import (CalculoInconsistenteError, DatoInvalidoError,
                         ParametroFaltanteError)

IVA = 0.19  # Impuesto por defecto (19 %)


class Servicio(EntidadBase):
    """Clase abstracta: define el contrato común de todos los servicios."""

    def __init__(self, identificador: str, nombre: str, tarifa_hora: float):
        super().__init__(identificador)                                  # ID de la entidad
        if not isinstance(nombre, str) or not nombre.strip():            # Valida nombre
            raise ParametroFaltanteError("El servicio requiere un nombre.")
        if not isinstance(tarifa_hora, (int, float)) or tarifa_hora <= 0:  # Valida tarifa
            raise DatoInvalidoError(f"Tarifa por hora inválida: {tarifa_hora!r}")
        self._nombre = nombre.strip()        # Nombre del servicio
        self._tarifa_hora = float(tarifa_hora)  # Tarifa por hora
        self._disponible = True              # Todo servicio nace disponible

    @property
    def nombre(self) -> str:
        return self._nombre

    @property
    def disponible(self) -> bool:
        return self._disponible

    def cambiar_disponibilidad(self, estado: bool):
        """Permite habilitar o deshabilitar el servicio."""
        self._disponible = bool(estado)

    # ---- Métodos abstractos (deben sobrescribirse) ----
    @abstractmethod
    def calcular_costo(self, horas: float, **extras) -> float:
        """Costo base del servicio sin impuestos ni descuentos."""

    @abstractmethod
    def describir(self) -> str:
        """Descripción textual del servicio."""

    @abstractmethod
    def validar_parametros(self, **extras) -> None:
        """Valida los parámetros específicos del servicio."""

    # ---- Sobrecarga emulada: costo total con distintas variantes ----
    def calcular_costo_total(self, horas: float, *args, **extras) -> float:
        """Python no tiene sobrecarga nativa; se emula según los argumentos:
        - (horas)                          -> costo + IVA por defecto
        - (horas, descuento)               -> costo con descuento + IVA
        - (horas, descuento, impuesto)     -> costo con descuento e impuesto propio
        """
        if len(args) > 2:                                                # Máximo 2 opcionales
            raise DatoInvalidoError("Demasiados argumentos para calcular_costo_total.")
        descuento = args[0] if len(args) >= 1 else 0.0                   # Variante con descuento
        impuesto = args[1] if len(args) == 2 else IVA                    # Variante con impuesto
        if not 0 <= descuento < 1:                                       # Descuento válido: [0,1)
            raise CalculoInconsistenteError(f"Descuento fuera de rango: {descuento}")
        if impuesto < 0:
            raise CalculoInconsistenteError(f"Impuesto negativo: {impuesto}")
        base = self.calcular_costo(horas, **extras)                      # Polimorfismo: depende del servicio
        total = base * (1 - descuento) * (1 + impuesto)                  # Aplica descuento e impuesto
        return round(total, 2)

    def mostrar_informacion(self) -> str:
        estado = "Disponible" if self._disponible else "No disponible"
        return f"Servicio[{self.identificador}] {self.describir()} | {estado}"


class ReservaSala(Servicio):
    """Reserva de salas con capacidad máxima."""

    def __init__(self, identificador, nombre, tarifa_hora, capacidad: int):
        super().__init__(identificador, nombre, tarifa_hora)
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError(f"Capacidad inválida: {capacidad!r}")
        self._capacidad = capacidad

    def validar_parametros(self, **extras) -> None:
        personas = extras.get("personas")                                # Parámetro obligatorio
        if personas is None:
            raise ParametroFaltanteError("Reserva de sala requiere 'personas'.")
        if not isinstance(personas, int) or not 0 < personas <= self._capacidad:
            raise DatoInvalidoError(f"Personas ({personas}) excede la capacidad {self._capacidad}.")

    def calcular_costo(self, horas: float, **extras) -> float:
        return self._tarifa_hora * horas                                 # Tarifa plana por hora

    def describir(self) -> str:
        return f"Sala '{self._nombre}' (capacidad {self._capacidad}) ${self._tarifa_hora:,.0f}/h"


class AlquilerEquipo(Servicio):
    """Alquiler de equipos con seguro opcional."""

    def __init__(self, identificador, nombre, tarifa_hora, tipo_equipo: str):
        super().__init__(identificador, nombre, tarifa_hora)
        if not tipo_equipo or not tipo_equipo.strip():
            raise ParametroFaltanteError("El equipo requiere un tipo.")
        self._tipo_equipo = tipo_equipo.strip()

    def validar_parametros(self, **extras) -> None:
        if "seguro" in extras and not isinstance(extras["seguro"], bool):  # 'seguro' es opcional pero booleano
            raise DatoInvalidoError("'seguro' debe ser True o False.")

    def calcular_costo(self, horas: float, **extras) -> float:
        costo = self._tarifa_hora * horas
        if extras.get("seguro"):                                         # El seguro suma 10 %
            costo *= 1.10
        return costo

    def describir(self) -> str:
        return f"Equipo '{self._nombre}' tipo {self._tipo_equipo} ${self._tarifa_hora:,.0f}/h"


class AsesoriaEspecializada(Servicio):
    """Asesoría con recargo según nivel del consultor."""

    _RECARGOS = {"junior": 1.0, "senior": 1.35, "experto": 1.6}          # Multiplicador por nivel

    def __init__(self, identificador, nombre, tarifa_hora, especialidad: str):
        super().__init__(identificador, nombre, tarifa_hora)
        if not especialidad or not especialidad.strip():
            raise ParametroFaltanteError("La asesoría requiere especialidad.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, **extras) -> None:
        nivel = extras.get("nivel", "junior")                            # Por defecto 'junior'
        if nivel not in self._RECARGOS:
            raise DatoInvalidoError(f"Nivel inválido: {nivel!r}. Use {list(self._RECARGOS)}")

    def calcular_costo(self, horas: float, **extras) -> float:
        return self._tarifa_hora * horas * self._RECARGOS[extras.get("nivel", "junior")]

    def describir(self) -> str:
        return f"Asesoría '{self._nombre}' en {self._especialidad} ${self._tarifa_hora:,.0f}/h"
