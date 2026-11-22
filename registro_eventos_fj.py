[2026-11-22 20:56:12] [INICIO] Sistema de registro de logs inicializado correctamente.
[2026-11-22 20:56:12] [INFO] Cliente registrado exitosamente: Cliente [CLI-01] - Julián David Santos | Email: julian.santos@softwarefj.com | Tel: 3104567890
[2026-11-22 20:56:12] [INFO] Cliente registrado exitosamente: Cliente [CLI-02] - Laura Camila Gómez | Email: laura.gomez@empresa.co | Tel: 3209876543
[2026-11-22 20:56:12] [ERROR] Contexto: Operación 3 - Registro Cliente Inválido | Tipo: DatoInvalidoError | Mensaje: Nombre de cliente inválido: 'Carlos123'. No debe contener números.
[2026-11-22 20:56:12] [INFO] Servicio agregado al catálogo: [SRV-01] Sala 'Sala Innovación A' (Capacidad: 12 personas, con proyector) - $80,000.00/hora
[2026-11-22 20:56:12] [INFO] Servicio agregado al catálogo: [SRV-02] Equipo 'Workstation Dell Precision' (Gama Alta, Stock: 1) - $120,000.00/día
[2026-11-22 20:56:12] [INFO] Servicio agregado al catálogo: [SRV-03] Asesoría 'Arquitectura Cloud y Python' (Cloud Computing - Consultor Senior) - $150,000.00/hora
[2026-11-22 20:56:12] [ERROR] Contexto: Operación 7 - Servicio con tarifa negativa | Tipo: DatoInvalidoError | Mensaje: La tarifa base del servicio debe ser mayor a cero.
[2026-11-22 20:56:12] [INFO] Reserva creada: Reserva [RES-01] | Estado: PENDIENTE | Cliente: Julián David Santos | Servicio: Sala Innovación A | Duración: 4 | Total: $376,992.00
[2026-11-22 20:56:12] [INFO] Reserva RES-01 confirmada y procesada. Total: $376,992.00
[2026-11-22 20:56:12] [INFO] Reserva creada: Reserva [RES-02] | Estado: PENDIENTE | Cliente: Laura Camila Gómez | Servicio: Workstation Dell Precision | Duración: 3 | Total: $446,250.00
[2026-11-22 20:56:12] [INFO] Reserva RES-02 confirmada. Stock restante equipo: 0
[2026-11-22 20:56:12] [ERROR] Contexto: Operación 10 - Reserva sin stock disponible | Tipo: ReservaInvalidaError | Mensaje: Fallo al procesar la creación de la reserva 'RES-03'. | Causa raíz: ServicioNoDisponibleError: El equipo 'Workstation Dell Precision' está agotado o inactivo.
[2026-11-22 20:56:12] [ERROR] Contexto: Operación 11 - Duración excedida en Asesoría | Tipo: ReservaInvalidaError | Mensaje: Fallo al procesar la creación de la reserva 'RES-04'. | Causa raíz: DatoInvalidoError: Las sesiones de asesoría deben durar entre 1 y 8 horas.
[2026-11-22 20:56:12] [ERROR] Contexto: Operación 12 - Cancelación de reserva procesada | Tipo: OperacionNoPermitidaError | Mensaje: No es posible cancelar una reserva que ya fue PROCESADA.
