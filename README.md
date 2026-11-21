# Software FJ – Sistema integral de clientes, servicios y reservas
Proyecto POO en Python 3 (sin bases de datos). Curso Programación 213023 – UNAD.

## Ejecución
    python main.py
El registro de eventos y errores queda en `logs/software_fj.log`.

## Estructura
- `excepciones.py`: jerarquía de excepciones personalizadas.
- `registro_logs.py`: configuración del archivo de logs.
- `entidades.py`: clase abstracta `EntidadBase` y `Cliente`.
- `servicios.py`: clase abstracta `Servicio` + `ReservaSala`, `AlquilerEquipo`, `AsesoriaEspecializada`.
- `reservas.py`: clase `Reserva` (confirmar, cancelar, procesar).
- `gestor.py`: listas internas y ejecución protegida de operaciones.
- `main.py`: simulación de 12+ operaciones válidas e inválidas.
