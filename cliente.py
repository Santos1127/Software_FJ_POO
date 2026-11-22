# Módulo que implementa la entidad Cliente con encapsulación estricta
import re  # Importa expresiones regulares para validar correos y teléfonos
from modelos_base import EntidadBase
from excepciones import DatoInvalidoError, ParametroFaltanteError


class Cliente(EntidadBase):
    """Representa un cliente registrado en Software FJ con sus datos encapsulados."""

    def __init__(self, id_cliente: str, nombre_completo: str, correo: str, telefono: str):
        # Inicializa el identificador heredado de EntidadBase
        super().__init__(id_cliente)
        # Asigna los datos personales invocando los setters con validación
        self.nombre_completo = nombre_completo
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre_completo(self) -> str:
        """Retorna el nombre completo del cliente."""
        return self._nombre_completo

    @nombre_completo.setter
    def nombre_completo(self, valor: str) -> None:
        """Valida que el nombre contenga solo letras/espacios y tenga longitud mínima."""
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El nombre del cliente es obligatorio.")
        nombre_limpio = valor.strip()
        if len(nombre_limpio) < 4 or any(char.isdigit() for char in nombre_limpio):
            raise DatoInvalidoError(f"Nombre de cliente inválido: '{valor}'. No debe contener números.")
        self._nombre_completo = nombre_limpio

    @property
    def correo(self) -> str:
        """Retorna el correo electrónico validado del cliente."""
        return self._correo

    @correo.setter
    def correo(self, valor: str) -> None:
        """Valida el formato estándar de correo electrónico."""
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El correo electrónico es obligatorio.")
        patron_correo = r"^[\w\.-]+@[\w\.-]+\.\w{2,}$"
        if not re.match(patron_correo, valor.strip()):
            raise DatoInvalidoError(f"Formato de correo electrónico inválido: '{valor}'.")
        self._correo = valor.strip().lower()

    @property
    def telefono(self) -> str:
        """Retorna el número telefónico del cliente."""
        return self._telefono

    @telefono.setter
    def telefono(self, valor: str) -> None:
        """Valida que el teléfono tenga entre 7 y 15 dígitos numéricos."""
        if not valor or not isinstance(valor, str):
            raise ParametroFaltanteError("El teléfono de contacto es obligatorio.")
        solo_digitos = valor.strip().replace("+", "").replace(" ", "")
        if not solo_digitos.isdigit() or not (7 <= len(solo_digitos) <= 15):
            raise DatoInvalidoError(f"Número telefónico inválido: '{valor}'. Debe tener entre 7 y 15 dígitos.")
        self._telefono = valor.strip()

    def obtener_resumen(self) -> str:
        """Implementación polimórfica del resumen de la entidad Cliente."""
        return f"Cliente [{self.id_entidad}] - {self.nombre_completo} | Email: {self.correo} | Tel: {self.telefono}"