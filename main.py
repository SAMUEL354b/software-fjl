"""Simulación de 12 operaciones del sistema Software FJ (válidas e inválidas)."""
from gestor import GestorFJ
from servicios import AlquilerEquipo, AsesoriaEspecializada, ReservaSala


def main():
    g = GestorFJ()
    print("=== SOFTWARE FJ: simulación ===\n")

    print("-- Clientes --")
    ana = g.registrar_cliente("C001", "Ana Gómez", "ana@correo.com", "3101234567")      # 1. válido
    luis = g.registrar_cliente("C002", "Luis Pérez", "luis@correo.com", "3209876543")   # 2. válido
    g.registrar_cliente("C003", "J0hn", "correo-malo", "123")                           # 3. inválido
    g.registrar_cliente("", "Sin Id", "x@y.com", "3001112233")                          # 4. ID faltante

    print("\n-- Servicios --")
    sala = g.registrar_servicio(ReservaSala, "S01", "Sala Alfa", 50000, 10)             # 5. válido
    equipo = g.registrar_servicio(AlquilerEquipo, "S02", "Proyector 4K", 20000, "Video")  # 6. válido
    asesoria = g.registrar_servicio(AsesoriaEspecializada, "S03", "Arquitectura", 90000, "Software")  # 7. válido
    g.registrar_servicio(ReservaSala, "S04", "Sala Beta", -100, 5)                      # 8. tarifa inválida

    print("\n-- Reservas --")
    r1 = g.crear_reserva("R01", ana, sala, 3, personas=8)                               # 9. exitosa
    g.crear_reserva("R02", luis, sala, 2, personas=25)                                  # 10. excede capacidad
    r3 = g.crear_reserva("R03", luis, equipo, 5, seguro=True)                           # 11. exitosa
    g.crear_reserva("R04", ana, asesoria, 2, nivel="gurú")                              # 12. nivel inválido
    g.crear_reserva("R05", ana, sala, 2)                                                # parámetro faltante
    r6 = g.crear_reserva("R06", luis, asesoria, 4, nivel="senior")                      # exitosa

    print("\n-- Ciclo de vida --")
    g.confirmar(r1); g.procesar(r1, 0.10)        # Confirmar y procesar con 10 % descuento
    g.procesar(r3)                               # Falla: no confirmada
    g.confirmar(r3); g.procesar(r3)              # Ahora sí
    g.cancelar(r1)                               # Falla: ya procesada
    g.cancelar(r6)                               # Cancelación válida
    g.confirmar(r6)                              # Falla: ya cancelada
    equipo.cambiar_disponibilidad(False)         # Servicio fuera de servicio
    g.crear_reserva("R07", ana, equipo, 1)       # Falla: no disponible
    g.procesar(r3, 1.5)                          # Falla: ya procesada (la app sigue viva)

    print("\n-- Resumen --")
    for r in g.reservas:
        print(" ", r)
    print("\nLa aplicación terminó sin interrupciones. Revise logs/software_fj.log")


if __name__ == "__main__":
    main()
