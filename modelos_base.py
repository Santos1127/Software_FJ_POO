# Módulo que define las clases abstractas fundamentales de la arquitectura POO
from abc import ABC, abstractmethod  # Importa herramientas para definir clases y métodos abstractos
from excepciones import DatoInvalidoError, ParametroFaltanteError, CalculoInconsistenteError


class EntidadBase(ABC):
    """Clase abstracta raíz que representa cualquier entidad identificable del sistema."""

    def __init__(self, id_entidad: str):
        # Valida que el identificador no sea nulo ni una cadena vacía
        if not id_entidad or not isinstance(id_entidad, str) or not id_entidad.strip():
            raise ParametroFaltanteError("El identificador de la entidad es obligatorio y debe ser texto.")
        # Encapsula el atributo privado _id_entidad
        self._id_entidad = id_entidad.strip()

    @property
    def id_entidad(self) -> str:
        """Getter de solo lectura para el identificador único de la entidad."""
        return self._id_entidad

    @abstractmethod
    def obtener_resumen(self) -> str:
        """Método abstracto que obliga a las subclases a devolver su descripción textual."""
        pass


class Servicio(EntidadBase, ABC):
    """Clase abstracta que modela un servicio ofrecido por la empresa Software FJ."""

    def __init__(self, id_servicio: str, nombre: str, tarifa_base: float, disponible: bool = True):
        # Llama al constructor de EntidadBase para validar y asignar el ID
        super().__init__(id_servicio)
        # Asigna los atributos mediante propiedades encapsuladas con validación
        self.nombre = nombre
        self.tarifa_base = tarifa_base
        self.disponible = disponible

    @property
    def nombre(self) -> str:
        """Retorna el nombre comercial del servicio."""
        return self._nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        """Valida y asigna el nombre del servicio."""
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise DatoInvalidoError("El nombre del servicio debe tener al menos 3 caracteres válidos.")
        self._nombre = valor.strip()

    @property
    def tarifa_base(self) -> float:
        """Retorna la tarifa base por unidad de tiempo (hora/día)."""
        return self._tarifa_base

    @tarifa_base.setter
    def tarifa_base(self, valor: float) -> None:
        """Valida que la tarifa base sea numérica y estrictamente positiva."""
        try:
            # Intenta convertir el valor recibido a flotante
            tarifa_num = float(valor)
        except (TypeError, ValueError) as exc:
            # Encadena la excepción nativa dentro de una excepción de dominio
            raise DatoInvalidoError(f"La tarifa '{valor}' no es un valor numérico válido.") from exc

        if tarifa_num <= 0:
            raise DatoInvalidoError("La tarifa base del servicio debe ser mayor a cero.")
        self._tarifa_base = tarifa_num

    @property
    def disponible(self) -> bool:
        """Indica si el servicio se encuentra habilitado para ser reservado."""
        return self._disponible

    @disponible.setter
    def disponible(self, estado: bool) -> None:
        """Valida que el estado de disponibilidad sea booleano."""
        if not isinstance(estado, bool):
            raise DatoInvalidoError("El estado de disponibilidad debe ser True o False.")
        self._disponible = estado

    def calcular_costo(self, duracion: int, impuesto: float = 0.19, descuento: float = 0.0) -> float:
        """
        Método con parámetros opcionales (sobrecarga funcional en Python) para calcular
        el costo total aplicando impuestos y descuentos opcionales.
        """
        # Valida los parámetros de entrada antes de ejecutar la operación matemática
        self.validar_parametros(duracion)

        # Verifica rangos válidos para impuesto y descuento
        if not (0.0 <= impuesto <= 1.0):
            raise CalculoInconsistenteError(f"Porcentaje de impuesto inválido: {impuesto}")
        if not (0.0 <= descuento < 1.0):
            raise CalculoInconsistenteError(f"Porcentaje de descuento inválido: {descuento}")

        # Calcula el subtotal polimórfico implementado por cada subclase
        subtotal = self._calcular_subtotal_especifico(duracion)
        # Aplica descuento sobre el subtotal
        subtotal_con_descuento = subtotal * (1 - descuento)
        # Calcula el monto final sumando el impuesto
        total = round(subtotal_con_descuento * (1 + impuesto), 2)

        # Verificación final de integridad del cálculo
        if total <= 0:
            raise CalculoInconsistenteError("El cálculo final del servicio arrojó un valor menor o igual a cero.")
        return total

    @abstractmethod
    def _calcular_subtotal_especifico(self, duracion: int) -> float:
        """Método abstracto interno para que cada subclase aplique su propia regla tarifaria."""
        pass

    @abstractmethod
    def validar_parametros(self, duracion: int) -> None:
        """Método abstracto para validar reglas de negocio propias de cada tipo de servicio."""
        pass

    @abstractmethod
    def describir_servicio(self) -> str:
        """Método abstracto para describir las características técnicas del servicio."""
        pass