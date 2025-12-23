from datetime import datetime

class ReservaService:
    def __init__(self, reserva_repository, habitacion_repository):
        self.reserva_repository = reserva_repository
        self.habitacion_repository = habitacion_repository

    def _validar_fechas(self, fecha_inicio, fecha_fin, precio_noche):
        formato = "%Y-%m-%d"
        inicio = datetime.strptime(fecha_inicio, formato)
        fin = datetime.strptime(fecha_fin, formato)

        if fin <= inicio:
            raise ValueError("La fecha de salida debe ser mayor a la de entrada")
        return (fin-inicio).days
    
    def _validar_disponibilidad(self, habitacion):
            if habitacion.get("estado") != "Disponible":
                raise ValueError("La habitación no está disponible")

    # ---------------- LOGICA DE NEGOCIO ---------------- #

    def crear_reserva(self, datos_reserva: dict):
        if not datos_reserva.get("habitacion_id"):
            raise ValueError("La habitación es obligatoria")

        if not datos_reserva.get("huesped_id"):
            raise ValueError("El huésped es obligatorio")

        habitacion = self.habitacion_repository.obtener_por_id(
            datos_reserva["habitacion_id"]
        )

        if not habitacion:
            raise ValueError("La habitación no existe")

        self._validar_disponibilidad(habitacion)

        dias = self._validar_fechas(
            datos_reserva["fecha_entrada"],
            datos_reserva["fecha_salida"]
        )

        datos_reserva["total"] = dias * habitacion["precio"]

        return self.reserva_repository.save(datos_reserva)