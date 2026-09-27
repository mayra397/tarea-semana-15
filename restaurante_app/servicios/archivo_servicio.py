import json
import os

class ArchivoServicio:
    @staticmethod
    def cargar_json(ruta: str) -> list:
        if not os.path.exists(ruta):
            return []
        try:
            with open(ruta, "r", encoding="utf-8") as file:
                return json.load(file)
        except Exception:
            return []

    @staticmethod
    def guardar_json(ruta: str, datos: list) -> bool:
        try:
            os.makedirs(os.path.dirname(ruta), exist_ok=True)
            with open(ruta, "w", encoding="utf-8") as file:
                json.dump(datos, file, indent=4, ensure_ascii=False)
            return True
        except Exception:
            return False