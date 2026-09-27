import os
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta
from servicios.archivo_servicio import ArchivoServicio

class RestauranteServicio:
    def __init__(self, base_dir: str):
        self.ruta_usuarios = os.path.join(base_dir, "datos", "usuarios.json")
        self.ruta_productos = os.path.join(base_dir, "datos", "productos.json")
        self.ruta_ventas = os.path.join(base_dir, "datos", "ventas.json")

    def autenticar(self, username: str, password: str) -> bool:
        usuarios = self.obtener_usuarios()
        return any(u.username == username and u.password == password for u u in usuarios)

    def obtener_usuarios(self) -> list[Usuario]:
        datos = ArchivoServicio.cargar_json(self.ruta_usuarios)
        return [Usuario.from_dict(u) for u in datos]

    def obtener_productos(self) -> list[Producto]:
        datos = ArchivoServicio.cargar_json(self.ruta_productos)
        return [Producto.from_dict(p) for p in datos]

    def obtener_ventas(self) -> list[Venta]:
        datos = ArchivoServicio.cargar_json(self.ruta_ventas)
        return [Venta.from_dict(v) for v in datos]

    def registrar_venta(self, id_usuario: int, id_producto: int) -> tuple[bool, str]:
        # Validaciones de reglas de negocio
        usuarios = self.obtener_usuarios()
        productos = self.obtener_productos()

        usuario = next((u for u in usuarios if u.id_usuario == id_usuario), None)
        if not usuario:
            return False, "El usuario seleccionado no existe."

        producto = next((p for p in productos if p.id_producto == id_producto), None)
        if not producto:
            return False, "El producto seleccionado no existe."

        ventas = self.obtener_ventas()
        nuevo_id = max([v.id_venta for v in ventas], default=0) + 1

        nueva_venta = Venta(
            id_venta=nuevo_id,
            id_usuario=usuario.id_usuario,
            cliente_nombre=usuario.nombre,
            id_producto=producto.id_producto,
            producto_nombre=producto.nombre,
            precio=producto.precio
        )

        ventas.append(nueva_venta)
        datos_ventas = [v.to_dict() for v in ventas]

        if ArchivoServicio.guardar_json(self.ruta_ventas, datos_ventas):
            return True, f"Venta #{nuevo_id} registrada con éxito."
        else:
            return False, "Error al guardar la venta en la base de datos."