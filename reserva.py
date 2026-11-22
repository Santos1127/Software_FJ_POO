# Módulo que integra Cliente, Servicio y Duración en la clase Reserva y gestiona las listas internas
from modelos_base import EntidadBase, Servicio
from cliente import Cliente
from servicios import AlquilerEquipo
from logger_sistema import LoggerSistema
from excepciones import (
    DatoInvalidoError,
    OperacionNoPermitidaError,
    ReservaInvalidaError,
    ErrorSistemaFJ,
)


class Reserva(EntidadBase):
    """Integra un Cliente, un Servicio y una duración con ciclo de vida controlado."""

    # Estados válidos permitidos dentro del ciclo de vida de una reserva
    ESTADOS_VALIDOS = ("PENDIENTE", "CONFIRMADA", "PROCESADA", "CANCELADA")

    def __init__(self, id_reserva: str, cliente: Cliente, servicio: Servicio, duracion: int, impuesto: float = 0.19, descuento: float = 0.0):
        # Inicializa el identificador de la reserva
        super().__init__(id_reserva)
        # Verifica que el cliente recibido sea una instancia válida de Cliente
        if not isinstance(cliente, Cliente):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Cliente.")
        # Verifica que el servicio recibido herede de la clase abstracta Servicio
        if not isinstance(servicio, Servicio):
            raise DatoInvalidoError("La reserva requiere una instancia válida de Servicio.")

        # Ejecuta las validaciones polimórficas propias del servicio elegido
        servicio.validar_parametros(duracion)

        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._impuesto = impuesto
        self._descuento = descuento
        self._estado = "PENDIENTE"
        # Calcula el costo inicial utilizando el método sobrecargado de Servicio
        self._costo_total = self._servicio.calcular_costo(duracion, impuesto, descuento)

    @property
    def estado(self) -> str:
        """Retorna el estado actual de la reserva."""
        return self._estado

    @property
    def costo_total(self) -> float:
        """Retorna el valor monetario calculado de la reserva."""
        return self._costo_total

    def confirmar(self) -> None:
        """Cambia el estado de PENDIENTE a CONFIRMADA y actualiza inventario si aplica."""
        if self._estado != "PENDIENTE":
            raise OperacionNoPermitidaError(f"No se puede confirmar una reserva en estado '{self._estado}'.")
        # Revalida que el servicio siga disponible al momento de confirmar
        self._servicio.validar_parametros(self._duracion)
        # Si es un alquiler de equipo, descuenta una unidad física del inventario
        if isinstance(self._servicio, AlquilerEquipo):
            self._servicio.descontar_unidad()
        self._estado = "CONFIRMADA"

    def procesar(self) -> None:
        """Finaliza la ejecución del servicio pasando de CONFIRMADA a PROCESADA."""
        if self._estado != "CONFIRMADA":
            raise OperacionNoPermitidaError(f"Solo se pueden procesar reservas CONFIRMADAS (estado actual: '{self._estado}').")
        self._estado = "PROCESADA"

    def cancelar(self) -> None:
        """Cancela la reserva si no ha sido procesada y restaura recursos si corresponde."""
        if self._estado == "PROCESADA":
            raise OperacionNoPermitidaError("No es posible cancelar una reserva que ya fue PROCESADA.")
        if self._estado == "CANCELADA":
            raise OperacionNoPermitidaError("La reserva ya se encuentra CANCELADA.")

        # Si estaba confirmada y era un equipo, devuelve la unidad al inventario
        if self._estado == "CONFIRMADA" and isinstance(self._servicio, AlquilerEquipo):
            self._servicio.restaurar_unidad()

        self._estado = "CANCELADA"

    def obtener_resumen(self) -> str:
        """Retorna el detalle completo de la reserva."""
        return (
            f"Reserva [{self.id_entidad}] | Estado: {self._estado} | "
            f"Cliente: {self._cliente.nombre_completo} | Servicio: {self._servicio.nombre} | "
            f"Duración: {self._duracion} | Total: ${self._costo_total:,.2f}"
        )


class SistemaSoftwareFJ:
    """Controlador principal que administra clientes, servicios y reservas en listas en memoria."""

    def __init__(self, logger: LoggerSistema):
        # Inyecta la instancia del logger para trazabilidad completa
        self.logger = logger
        # Listas internas en memoria (sin base de datos)
        self.clientes: list[Cliente] = []
        self.servicios: list[Servicio] = []
        self.reservas: list[Reserva] = []

    def registrar_cliente(self, cliente: Cliente) -> None:
        """Agrega un cliente a la lista verificando que no exista ID duplicado."""
        if any(c.id_entidad == cliente.id_entidad for c in self.clientes):
            raise DatoInvalidoError(f"Ya existe un cliente registrado con el ID '{cliente.id_entidad}'.")
        self.clientes.append(cliente)
        self.logger.registrar_evento("INFO", f"Cliente registrado exitosamente: {cliente.obtener_resumen()}")

    def registrar_servicio(self, servicio: Servicio) -> None:
        """Agrega un servicio al catálogo en memoria verificando ID único."""
        if any(s.id_entidad == servicio.id_entidad for s in self.servicios):
            raise DatoInvalidoError(f"Ya existe un servicio registrado con el ID '{servicio.id_entidad}'.")
        self.servicios.append(servicio)
        self.logger.registrar_evento("INFO", f"Servicio agregado al catálogo: {servicio.obtener_resumen()}")

    def crear_reserva(self, id_reserva: str, id_cliente: str, id_servicio: str, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> Reserva:
        """Busca las entidades en memoria, crea la reserva y maneja encadenamiento de errores."""
        try:
            # Busca el cliente por su identificador en la lista interna
            cliente = next((c for c in self.clientes if c.id_entidad == id_cliente), None)
            if cliente is None:
                raise DatoInvalidoError(f"No se encontró ningún cliente con ID '{id_cliente}'.")

            # Busca el servicio por su identificador en la lista interna
            servicio = next((s for s in self.servicios if s.id_entidad == id_servicio), None)
            if servicio is None:
                raise DatoInvalidoError(f"No se encontró ningún servicio con ID '{id_servicio}'.")

            # Verifica que el ID de reserva no esté repetido
            if any(r.id_entidad == id_reserva for r in self.reservas):
                raise ReservaInvalidaError(f"El código de reserva '{id_reserva}' ya existe.")

            # Instancia la nueva reserva
            nueva_reserva = Reserva(id_reserva, cliente, servicio, duracion, impuesto, descuento)
            self.reservas.append(nueva_reserva)
            self.logger.registrar_evento("INFO", f"Reserva creada: {nueva_reserva.obtener_resumen()}")
            return nueva_reserva

        except ErrorSistemaFJ as err:
            # Encadena cualquier error de dominio dentro de ReservaInvalidaError para trazabilidad
            raise ReservaInvalidaError(f"Fallo al procesar la creación de la reserva '{id_reserva}'.") from err