"""Gestor central: mantiene listas internas y protege la aplicación de fallos."""
from entidades import Cliente
from excepciones import ErrorSoftwareFJ
from registro_logs import obtener_logger
from reservas import Reserva


class GestorFJ:
    """Administra clientes, servicios y reservas sin base de datos (solo listas)."""

    def __init__(self):
        self.clientes, self.servicios, self.reservas = [], [], []   # Listas internas
        self.log = obtener_logger()

    def _ejecutar(self, descripcion, funcion, *args, **kwargs):
        """Ejecuta una operación; si falla, registra el error (con su causa) y continúa."""
        try:
            resultado = funcion(*args, **kwargs)
        except ErrorSoftwareFJ as e:
            causa = f" | causa: {type(e.__cause__).__name__}: {e.__cause__}" if e.__cause__ else ""
            self.log.error("%s FALLÓ -> %s: %s%s", descripcion, type(e).__name__, e, causa)
            print(f"  [ERROR controlado] {descripcion}: {e}{causa}")
            return None
        except Exception as e:                                       # Cualquier error inesperado
            self.log.exception("%s ERROR INESPERADO: %s", descripcion, e)
            print(f"  [ERROR inesperado] {descripcion}: {e}")
            return None
        else:
            self.log.info("%s OK", descripcion)
            print(f"  [OK] {descripcion}")
            return resultado
        finally:
            pass  # Aquí podrían liberarse recursos; se deja para demostrar la estructura

    def registrar_cliente(self, *datos):
        cliente = self._ejecutar(f"Registro de cliente {datos[:2]}", Cliente, *datos)
        if cliente:
            self.clientes.append(cliente)
        return cliente

    def registrar_servicio(self, clase, *datos):
        servicio = self._ejecutar(f"Creación de servicio {clase.__name__} {datos[:2]}", clase, *datos)
        if servicio:
            self.servicios.append(servicio)
        return servicio

    def crear_reserva(self, identificador, cliente, servicio, horas, **extras):
        reserva = self._ejecutar(f"Creación de reserva {identificador}",
                                 Reserva, identificador, cliente, servicio, horas, **extras)
        if reserva:
            self.reservas.append(reserva)
        return reserva

    def confirmar(self, reserva):
        return self._ejecutar(f"Confirmación de {reserva.identificador}", reserva.confirmar)

    def cancelar(self, reserva):
        return self._ejecutar(f"Cancelación de {reserva.identificador}", reserva.cancelar)

    def procesar(self, reserva, descuento=0.0):
        total = self._ejecutar(f"Procesamiento de {reserva.identificador}", reserva.procesar, descuento)
        if total:
            print(f"      Total a pagar: ${total:,.2f}")
        return total
