class FacturaService:
    IVA = 0.15
    def __init__(self, factura_repository):
        self.factura_repository = factura_repository
        self.IVA_PERCENT = 0.15

    def generar_detalle_factura(self, monto_base:float):
        if monto_base <= 0:
            raise ValueError("El monto base debe ser mayor a cero")
        
        iva = monto_base * self.IVA
        total = monto_base + iva

        return {
            "subtotal" : round(monto_base,2),
            "I.V.A" : round(iva, 2),
            "total" : round(total,2)
        }