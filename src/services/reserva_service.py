from datetime import datetime

class ReservaService:
    def __init__(self, reserva_repository, habitacion_repository):
        self.reserva_repository = reserva_repository
        self.habitacion_repository = habitacion_repository

    def calcular_total(self, fecha_inicio, fecha_fin, precio_noche):
        formato = "%Y-%m-%d"
        inicio = datetime.strptime(fecha_inicio, formato)
        fin = datetime.strptime(fecha_fin, formato)
        dias = (fin - inicio).days

        if dias <= 0:
            raise ValueError("La fecha de salida debe ser mayor a la de entrada")
        return dias * precio_noche
    
    def crear_reserva(self, datos_reserva):
        if not datos_reserva.get("habitacion_id") or not datos_reserva.get("huesped_id"):
            raise ValueError("La habitacion y el huesped son obligatorios")
        habitacion = self.habitacion_repository.obtener_por_id(datos_reserva["habitacion_id"])
        if not habitacion:
            raise ValueError("La habitacion seleccionada no existe")
        
        total = self.calcular_total(datos_reserva["fecha_entrada"], 
                                    datos_reserva["fecha_salida"],
                                    habitacion["precio"])
        datos_reserva["total"] = total
        return self.reserva_repository.save(datos_reserva)
    
    def validar_disponibilidad(self, habitacion_id):
        habitacion = self.habitacion_repository.obtener_por_id(habitacion_id)
        if habitacion.get("estado") != "Disponible":
            raise ValueError(f"La habitacion {habitacion_id} no esta disponible actualmente")
        return True