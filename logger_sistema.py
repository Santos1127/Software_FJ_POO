# Módulo encargado de persistir eventos y errores en un archivo de texto plano (.log)
import datetime  # Importa el módulo estándar para obtener marcas de tiempo exactas


class LoggerSistema:
    """Gestiona la escritura segura de eventos e incidentes en el archivo de logs."""

    def __init__(self, ruta_archivo: str = "registro_eventos_fj.log"):
        # Define la ruta del archivo donde se almacenarán los registros
        self.ruta_archivo = ruta_archivo
        # Registra el inicio de sesión del sistema al instanciar el logger
        self.registrar_evento("INICIO", "Sistema de registro de logs inicializado correctamente.")

    def registrar_evento(self, nivel: str, mensaje: str) -> None:
        """Escribe una línea formateada con fecha y hora en el archivo de logs."""
        # Obtiene la fecha y hora actual en formato legible
        marca_tiempo = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # Construye la cadena de texto estructurada para el log
        linea = f"[{marca_tiempo}] [{nivel.upper()}] {mensaje}\n"

        # Uso de bloque try/except/finally para garantizar el manejo seguro del archivo
        archivo = None  # Inicializa la referencia del archivo en None
        try:
            # Abre el archivo en modo 'a' (append) con codificación UTF-8
            archivo = open(self.ruta_archivo, mode="a", encoding="utf-8")
            # Escribe la línea en el archivo de registro
            archivo.write(linea)
        except OSError as error_io:
            # Si falla el disco o permisos, informa en consola sin detener la aplicación
            print(f"[ALERTA CRÍTICA DE LOG] No se pudo escribir en el archivo: {error_io}")
        finally:
            # Asegura que el recurso del archivo siempre se cierre si fue abierto
            if archivo is not None and not archivo.closed:
                archivo.close()

    def registrar_error(self, contexto: str, excepcion: Exception) -> None:
        """Registra un error detallado incluyendo su causa encadenada si existe."""
        # Extrae el nombre de la clase de la excepción capturada
        tipo_error = type(excepcion).__name__
        # Construye el mensaje principal del error
        detalle = f"Contexto: {contexto} | Tipo: {tipo_error} | Mensaje: {excepcion}"
        # Verifica si existe una excepción original encadenada (__cause__)
        if excepcion.__cause__ is not None:
            # Añade la información de la causa raíz al registro
            detalle += f" | Causa raíz: {type(excepcion.__cause__).__name__}: {excepcion.__cause__}"
        # Delega la escritura al método registrar_evento con nivel ERROR
        self.registrar_evento("ERROR", detalle)