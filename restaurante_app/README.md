# Restaurante App - Sistema de Gestión (Semana 15)

## Descripción
Evolución modular del proyecto `restaurante_app` desarrollada para la asignatura de Programación Orientada a Objetos (Semana 15). Esta versión implementa los **conceptos fundamentales del manejo de eventos** mediante el registro de ventas que relacionan usuarios y productos del restaurante.

## Flujo Fundamental de Manejo de Eventos
El registro de ventas evidencia el flujo de responsabilidades desencadenado por una acción del usuario:
1. **Acción del usuario:** Selección de usuario y producto en la interfaz.
2. **Disparo de Evento:** Clic en el botón *Registrar venta* configurado mediante `command=self._callback_registrar_venta`.
3. **Callback:** El método de la UI extrae las selecciones y delega la operación al servicio.
4. **Servicio:** `RestauranteServicio` ejecuta las validaciones y asigna los datos de la transacción.
5. **Persistencia:** Almacenamiento seguro en `datos/ventas.json` utilizando `ArchivoServicio`.
6. **Respuesta Visual:** Actualización inmediata de la tabla `Treeview` y mensaje de confirmación al usuario.

## Arquitectura Modular del Proyecto
```text
restaurante_app/
├── assets/                  # Recursos visuales e íconos del sistema
├── datos/                   # Archivos de persistencia en formato JSON
│   ├── productos.json
│   ├── usuarios.json
│   └── ventas.json
├── modelos/                 # Clases de entidades (POO)
│   ├── producto.py
│   ├── usuario.py
│   └── venta.py
├── servicios/               # Lógica de negocio y manejo de archivos
│   ├── archivo_servicio.py
│   └── restaurante_servicio.py
├── ui/                      # Vistas e interfaz gráfica con Tkinter/ttk
│   ├── login_view.py
│   └── main_view.py
└── main.py                  # Punto de entrada principal