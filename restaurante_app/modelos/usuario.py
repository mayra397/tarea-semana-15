class Usuario:
    def __init__(self, id_usuario: int, nombre: str, rol: str, username: str, password: str = ""):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.rol = rol
        self.username = username
        self.password = password

    def to_dict(self) -> dict:
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "rol": self.rol,
            "username": self.username,
            "password": self.password
        }

    @staticmethod
    def from_dict(data: dict):
        return Usuario(
            id_usuario=data["id_usuario"],
            nombre=data["nombre"],
            rol=data["rol"],
            username=data["username"],
            password=data.get("password", "")
        )