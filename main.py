# Punto de entrada principal del sistema Software FJ
# Ejecuta 12 operaciones completas (válidas e inválidas) demostrando estabilidad ante errores
from logger_sistema import LoggerSistema
from cliente import Cliente
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from reserva import SistemaSoftwareFJ
from excepciones import ErrorSistemaFJ


def ejecutar_simulacion() -> None:
    """Ejecuta paso a paso las operaciones de prueba del sistema sin interrupciones."""
    # Inicializa el sistema de logs y el controlador principal
    logger = LoggerSistema("registro_eventos_fj.log")
    sistema = SistemaSoftwareFJ(logger)

    print("=" * 75)
    print("INICIANDO SIMULACIÓN INTEGRAL - SOFTWARE FJ (SIN BASE DE DATOS)")
    print("=" * 75)

    # --- OPERACIÓN 1: Registro VÁLIDO de Cliente 1 ---
    try:
        c1 = Cliente("CLI-01", "Julián David Santos", "julian.santos@softwarefj.com", "3104567890")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 1 - Creación Cliente 1", e)
    else:
        # Bloque else: se ejecuta únicamente si no hubo excepciones en el bloque try
        sistema.registrar_cliente(c1)
        print("[OK] Op. 1: Cliente CLI-01 registrado correctamente.")

    # --- OPERACIÓN 2: Registro VÁLIDO de Cliente 2 ---
    try:
        c2 = Cliente("CLI-02", "Laura Camila Gómez", "laura.gomez@empresa.co", "3209876543")
        sistema.registrar_cliente(c2)
        print("[OK] Op. 2: Cliente CLI-02 registrado correctamente.")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 2 - Registro Cliente 2", e)

    # --- OPERACIÓN 3: Registro INVÁLIDO de Cliente (correo mal formado y nombre con números) ---
    try:
        c_invalido = Cliente("CLI-03", "Carlos123", "correo-sin-arroba.com", "123")
        sistema.registrar_cliente(c_invalido)
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 3 - Registro Cliente Inválido", e)
        print(f"[CONTROLADO] Op. 3: Error de cliente capturado sin detener el sistema -> {e}")

    # --- OPERACIÓN 4: Creación VÁLIDA de Servicio 1 (Sala de Juntas) ---
    try:
        s1 = ReservaSala("SRV-01", "Sala Innovación A", tarifa_hora=80000, capacidad=12, tiene_proyector=True)
        sistema.registrar_servicio(s1)
        print("[OK] Op. 4: Servicio SRV-01 (Sala) creado correctamente.")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 4 - Creación Sala", e)

    # --- OPERACIÓN 5: Creación VÁLIDA de Servicio 2 (Alquiler de Equipo con stock = 1) ---
    try:
        s2 = AlquilerEquipo("SRV-02", "Workstation Dell Precision", tarifa_dia=120000, stock_disponible=1, gama="Alta")
        sistema.registrar_servicio(s2)
        print("[OK] Op. 5: Servicio SRV-02 (Equipo) creado correctamente.")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 5 - Creación Equipo", e)

    # --- OPERACIÓN 6: Creación VÁLIDA de Servicio 3 (Asesoría Especializada) ---
    try:
        s3 = AsesoriaEspecializada("SRV-03", "Arquitectura Cloud y Python", tarifa_hora=150000, especialidad="Cloud Computing", nivel_senior=True)
        sistema.registrar_servicio(s3)
        print("[OK] Op. 6: Servicio SRV-03 (Asesoría) creado correctamente.")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 6 - Creación Asesoría", e)

    # --- OPERACIÓN 7: Creación INVÁLIDA de Servicio (Tarifa negativa / no numérica) ---
    try:
        s_invalido = ReservaSala("SRV-04", "Sala Fantasma", tarifa_hora=-50000, capacidad=5)
        sistema.registrar_servicio(s_invalido)
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 7 - Servicio con tarifa negativa", e)
        print(f"[CONTROLADO] Op. 7: Error en creación de servicio capturado -> {e}")

    # --- OPERACIÓN 8: Reserva EXITOSA de Sala con descuento (método sobrecargado) ---
    try:
        r1 = sistema.crear_reserva("RES-01", "CLI-01", "SRV-01", duracion=4, impuesto=0.19, descuento=0.10)
        r1.confirmar()
        r1.procesar()
        logger.registrar_evento("INFO", f"Reserva RES-01 confirmada y procesada. Total: ${r1.costo_total:,.2f}")
        print(f"[OK] Op. 8: Reserva RES-01 procesada con éxito. Total: ${r1.costo_total:,.2f}")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 8 - Reserva Sala", e)

    # --- OPERACIÓN 9: Reserva EXITOSA de Equipo (agota el único stock disponible) ---
    try:
        r2 = sistema.crear_reserva("RES-02", "CLI-02", "SRV-02", duracion=3)
        r2.confirmar()
        logger.registrar_evento("INFO", f"Reserva RES-02 confirmada. Stock restante equipo: {s2.stock_disponible}")
        print(f"[OK] Op. 9: Reserva RES-02 confirmada. Stock restante: {s2.stock_disponible}")
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 9 - Reserva Equipo", e)

    # --- OPERACIÓN 10: Reserva FALLIDA por Servicio No Disponible (stock agotado en Op. 9) ---
    try:
        r3 = sistema.crear_reserva("RES-03", "CLI-01", "SRV-02", duracion=2)
        r3.confirmar()
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 10 - Reserva sin stock disponible", e)
        print(f"[CONTROLADO] Op. 10: Intento de reserva sin stock bloqueado -> {e} (Causa: {e.__cause__})")

    # --- OPERACIÓN 11: Reserva FALLIDA por duración fuera de rango en Asesoría (máx 8 horas) ---
    try:
        r4 = sistema.crear_reserva("RES-04", "CLI-02", "SRV-03", duracion=15)
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 11 - Duración excedida en Asesoría", e)
        print(f"[CONTROLADO] Op. 11: Validación polimórfica de duración activada -> {e}")

    # --- OPERACIÓN 12: Operación NO PERMITIDA (intentar cancelar una reserva ya PROCESADA) ---
    try:
        r1.cancelar()
    except ErrorSistemaFJ as e:
        logger.registrar_error("Operación 12 - Cancelación de reserva procesada", e)
        print(f"[CONTROLADO] Op. 12: Protección de estado de reserva activada -> {e}")
    finally:
        # Bloque finally: resumen final ejecutado pase lo que pase
        print("=" * 75)
        print("SIMULACIÓN FINALIZADA SIN INTERRUPCIONES.")
        print(f"Clientes activos: {len(sistema.clientes)} | Servicios: {len(sistema.servicios)} | Reservas registradas: {len(sistema.reservas)}")
        print("Revisa el archivo 'registro_eventos_fj.log' para ver la auditoría completa.")
        print("=" * 75)


if __name__ == "__main__":
    ejecutar_simulacion()