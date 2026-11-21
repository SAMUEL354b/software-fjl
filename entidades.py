"""Clase abstracta EntidadBase y clase Cliente."""
import re                      # Expresiones regulares para validar email/teléfono
from abc import ABC, abstractmethod  # Herramientas para clases abstractas

from excepciones import DatoInvalidoError, ParametroFaltanteError


class EntidadBase(ABC):
    """Clase abstracta que representa cualquier entidad general del sistema."""

    def __init__(self, identificador: str):
        if not identificador or not str(identificador).strip():   # Un ID vacío no es válido
            raise ParametroFaltanteError("La entidad requiere un identificador.")
        self._identificador = str(identificador).strip()          # Atributo protegido (encapsulación)

    @property
    def identificador(self) -> str:
        """Solo lectura: el ID no se puede modificar desde fuera."""
        return self._identificador

    @abstractmethod
    def mostrar_informacion(self) -> str:
        """Cada entidad concreta debe describirse a sí misma."""

    def __str__(self) -> str:
        return self.mostrar_informacion()   # Al imprimir el objeto se usa su descripción


class Cliente(EntidadBase):
    """Cliente con datos personales encapsulados y validados."""

    _PATRON_EMAIL = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")   # Formato básico de correo
    _PATRON_TEL = re.compile(r"^\d{7,10}$")                     # 7 a 10 dígitos

    def __init__(self, identificador: str, nombre: str, email: str, telefono: str):
        super().__init__(identificador)    # Inicializa la parte abstracta (ID)
        self.nombre = nombre               # Usa el setter con validación
        self.email = email                 # Usa el setter con validación
        self.telefono = telefono           # Usa el setter con validación

    @property
    def nombre(self) -> str:
        return self.__nombre               # Atributo privado (name mangling)

    @nombre.setter
    def nombre(self, valor: str):
        if not isinstance(valor, str) or len(valor.strip()) < 3:     # Mínimo 3 caracteres
            raise DatoInvalidoError(f"Nombre inválido: {valor!r}")
        if any(c.isdigit() for c in valor):                          # No se aceptan números
            raise DatoInvalidoError(f"El nombre no puede contener números: {valor!r}")
        self.__nombre = valor.strip().title()                        # Normaliza el formato

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, valor: str):
        if not isinstance(valor, str) or not self._PATRON_EMAIL.match(valor.strip()):
            raise DatoInvalidoError(f"Correo inválido: {valor!r}")
        self.__email = valor.strip().lower()

    @property
    def telefono(self) -> str:
        return self.__telefono

    @telefono.setter
    def telefono(self, valor: str):
        if not self._PATRON_TEL.match(str(valor).strip()):
            raise DatoInvalidoError(f"Teléfono inválido: {valor!r}")
        self.__telefono = str(valor).strip()

    def mostrar_informacion(self) -> str:
        """Implementación del método abstracto."""
        return f"Cliente[{self.identificador}] {self.nombre} | {self.email} | Tel: {self.telefono}"
