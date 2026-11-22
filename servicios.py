# Módulo con las tres clases derivadas de Servicio: ReservaSala, AlquilerEquipo y AsesoriaEspecializada
from modelos_base import Servicio
from excepciones import DatoInvalidoError, ServicioNoDisponibleError


class ReservaSala(Servicio):
    """Servicio especializado para el alquiler de salas de reuniones o capacitación."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, capacidad: int, tiene_proyector: bool = True, disponible: bool = True):
        # Inicializa la clase padre Servicio
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        # Valida la capacidad física de la sala
        if not isinstance(capacidad, int) or capacidad <= 0:
            raise DatoInvalidoError("La capacidad de la sala debe ser un número entero mayor a 0.")
        self._capacidad = capacidad
        self._tiene_proyector = bool(tiene_proyector)

    def validar_parametros(self, duracion: int) -> None:
        """Valida disponibilidad de la sala y que la reserva sea entre 1 y 12 horas."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La sala '{self.nombre}' no se encuentra disponible.")
        if not isinstance(duracion, int) or not (1 <= duracion <= 12):
            raise DatoInvalidoError("La reserva de sala debe ser un entero entre 1 y 12 horas.")

    def _calcular_subtotal_especifico(self, duracion: int) -> float:
        """Calcula el subtotal aplicando recargo del 10% si incluye proyector multimedia."""
        subtotal = self.tarifa_base * duracion
        if self._tiene_proyector:
            subtotal *= 1.10  # Recargo fijo por equipamiento audiovisual
        return subtotal

    def describir_servicio(self) -> str:
        """Retorna la ficha técnica de la sala."""
        equipo_av = "con proyector" if self._tiene_proyector else "sin proyector"
        return f"Sala '{self.nombre}' (Capacidad: {self._capacidad} personas, {equipo_av}) - ${self.tarifa_base:,.2f}/hora"

    def obtener_resumen(self) -> str:
        """Sobrescribe el resumen general heredado de EntidadBase."""
        return f"[{self.id_entidad}] {self.describir_servicio()}"


class AlquilerEquipo(Servicio):
    """Servicio especializado para el préstamo de hardware y estaciones de trabajo."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_dia: float, stock_disponible: int, gama: str = "Profesional", disponible: bool = True):
        # Inicializa la clase padre Servicio
        super().__init__(id_servicio, nombre, tarifa_dia, disponible)
        if not isinstance(stock_disponible, int) or stock_disponible < 0:
            raise DatoInvalidoError("El stock de equipos no puede ser negativo.")
        self._stock_disponible = stock_disponible
        self._gama = gama

    @property
    def stock_disponible(self) -> int:
        """Retorna la cantidad de unidades físicas en inventario."""
        return self._stock_disponible

    def descontar_unidad(self) -> None:
        """Reduce en 1 el inventario al confirmarse una reserva."""
        if self._stock_disponible <= 0:
            raise ServicioNoDisponibleError(f"No quedan unidades disponibles de '{self.nombre}'.")
        self._stock_disponible -= 1
        # Si el stock llega a cero, marca automáticamente el servicio como no disponible
        if self._stock_disponible == 0:
            self.disponible = False

    def restaurar_unidad(self) -> None:
        """Devuelve 1 unidad al inventario si se cancela una reserva."""
        self._stock_disponible += 1
        self.disponible = True

    def validar_parametros(self, duracion: int) -> None:
        """Valida existencia en inventario y que el alquiler sea entre 1 y 30 días."""
        if not self.disponible or self._stock_disponible <= 0:
            raise ServicioNoDisponibleError(f"El equipo '{self.nombre}' está agotado o inactivo.")
        if not isinstance(duracion, int) or not (1 <= duracion <= 30):
            raise DatoInvalidoError("El alquiler de equipos debe ser entre 1 y 30 días.")

    def _calcular_subtotal_especifico(self, duracion: int) -> float:
        """Calcula el subtotal aplicando un seguro obligatorio de $15.000 por alquiler."""
        seguro_equipo = 15000.0
        return (self.tarifa_base * duracion) + seguro_equipo

    def describir_servicio(self) -> str:
        """Retorna la ficha técnica del equipo."""
        return f"Equipo '{self.nombre}' (Gama {self._gama}, Stock: {self._stock_disponible}) - ${self.tarifa_base:,.2f}/día"

    def obtener_resumen(self) -> str:
        """Sobrescribe el resumen general heredado de EntidadBase."""
        return f"[{self.id_entidad}] {self.describir_servicio()}"


class AsesoriaEspecializada(Servicio):
    """Servicio especializado de consultoría técnica en ingeniería de software."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_hora: float, especialidad: str, nivel_senior: bool = True, disponible: bool = True):
        # Inicializa la clase padre Servicio
        super().__init__(id_servicio, nombre, tarifa_hora, disponible)
        if not especialidad or not isinstance(especialidad, str):
            raise DatoInvalidoError("Debe especificarse el área de especialidad de la asesoría.")
        self._especialidad = especialidad.strip()
        self._nivel_senior = bool(nivel_senior)

    def validar_parametros(self, duracion: int) -> None:
        """Valida disponibilidad del consultor y bloques de 1 a 8 horas."""
        if not self.disponible:
            raise ServicioNoDisponibleError(f"La asesoría '{self.nombre}' no tiene consultores disponibles.")
        if not isinstance(duracion, int) or not (1 <= duracion <= 8):
            raise DatoInvalidoError("Las sesiones de asesoría deben durar entre 1 y 8 horas.")

    def _calcular_subtotal_especifico(self, duracion: int) -> float:
        """Si el consultor es Senior, aplica un multiplicador de tarifa de 1.25x."""
        factor = 1.25 if self._nivel_senior else 1.0
        return (self.tarifa_base * duracion) * factor

    def describir_servicio(self) -> str:
        """Retorna la ficha técnica de la asesoría."""
        nivel = "Consultor Senior" if self._nivel_senior else "Consultor Semi-Senior"
        return f"Asesoría '{self.nombre}' ({self._especialidad} - {nivel}) - ${self.tarifa_base:,.2f}/hora"

    def obtener_resumen(self) -> str:
        """Sobrescribe el resumen general heredado de EntidadBase."""
        return f"[{self.id_entidad}] {self.describir_servicio()}"