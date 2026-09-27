from datetime import datetime

class Venta:
    def __init__(self, id_venta: int, id_usuario: int, cliente_nombre: str, id_producto: int, producto_nombre: str, precio: float, fecha: str = None):
        self.id_venta = id_venta
        self.id_usuario = id_usuario
        self.cliente_nombre = cliente_nombre
        self.id_producto = id_producto
        self.producto_nombre = producto_nombre
        self.precio = precio
        self.fecha = fecha if fecha else datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self) -> dict:
        return {
            "id_venta": self.id_venta,
            "id_usuario": self.id_usuario,
            "cliente_nombre": self.cliente_nombre,
            "id_producto": self.id_producto,
            "producto_nombre": self.producto_nombre,
            "precio": self.precio,
            "fecha": self.fecha
        }

    @staticmethod
    def from_dict(data: dict):
        return Venta(
            id_venta=data["id_venta"],
            id_usuario=data["id_usuario"],
            cliente_nombre=data["cliente_nombre"],
            id_producto=data["id_producto"],
            producto_nombre=data["producto_nombre"],
            precio=float(data["precio"]),
            fecha=data["fecha"]
        )