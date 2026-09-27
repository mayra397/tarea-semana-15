class Producto:
    def __init__(self, id_producto: int, nombre: str, categoria: str, precio: float):
        self.id_producto = id_producto
        self.nombre = nombre
        self.categoria = categoria
        self.precio = precio

    def to_dict(self) -> dict:
        return {
            "id_producto": self.id_producto,
            "nombre": self.nombre,
            "categoria": self.categoria,
            "precio": self.precio
        }

    @staticmethod
    from_dict(data: dict):
        return Producto(
            id_producto=data["id_producto"],
            nombre=data["nombre"],
            categoria=data["categoria"],
            precio=float(data["precio"])
        )