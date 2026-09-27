import os
import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio

class MainView(tk.Tk):
    def __init__(self, servicio: RestauranteServicio, base_dir: str):
        super().__init__()
        self.servicio = servicio
        self.base_dir = base_dir

        self.title("Restaurante App - Sistema de Gestión")
        self.geometry("850x550")
        self.resizable(False, False)

        self._cargar_recursos_assets()
        self._configurar_interfaz()
        self._cargar_datos_ventas()

    def _cargar_recursos_assets(self):
        assets_dir = os.path.join(self.base_dir, "assets")
        self.iconos = {}

        # Cargar logo de la ventana si existe
        logo_path = os.path.join(assets_dir, "logo.png")
        if os.path.exists(logo_path):
            try:
                self.iconos["logo"] = tk.PhotoImage(file=logo_path)
                self.iconphoto(True, self.iconos["logo"])
            except Exception:
                pass

    def _configurar_interfaz(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Pestañas existentes
        self.tab_usuarios = ttk.Frame(notebook)
        self.tab_productos = ttk.Frame(notebook)
        self.tab_ventas = ttk.Frame(notebook)

        notebook.add(self.tab_usuarios, text="Usuarios")
        notebook.add(self.tab_productos, text="Productos")
        notebook.add(self.tab_ventas, text="Ventas")

        self._construir_pestana_usuarios()
        self._construir_pestana_productos()
        self._construir_pestana_ventas()

    def _construir_pestana_usuarios(self):
        lbl = ttk.Label(self.tab_usuarios, text="Módulo de Consulta de Usuarios", font=("Helvetica", 14, "bold"))
        lbl.pack(pady=10)

        tree = ttk.Treeview(self.tab_usuarios, columns=("ID", "Nombre", "Rol"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Rol", text="Rol")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for u in self.servicio.obtener_usuarios():
            tree.insert("", tk.END, values=(u.id_usuario, u.nombre, u.rol))

    def _construir_pestana_productos(self):
        lbl = ttk.Label(self.tab_productos, text="Módulo de Gestión de Productos", font=("Helvetica", 14, "bold"))
        lbl.pack(pady=10)

        tree = ttk.Treeview(self.tab_productos, columns=("ID", "Nombre", "Categoría", "Precio"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Nombre", text="Nombre")
        tree.heading("Categoría", text="Categoría")
        tree.heading("Precio", text="Precio ($)")
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        for p in self.servicio.obtener_productos():
            tree.insert("", tk.END, values=(p.id_producto, p.nombre, p.categoria, f"${p.precio:.2f}"))

    def _construir_pestana_ventas(self):
        # Frame superior para el formulario de registro
        frame_form = ttk.LabelFrame(self.tab_ventas, text=" Registrar Nueva Venta ", padding=15)
        frame_form.pack(fill=tk.X, padx=10, pady=10)

        # Seleccionar Usuario
        ttk.Label(frame_form, text="Usuario/Cliente:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.cbo_usuarios = ttk.Combobox(frame_form, state="readonly", width=35)
        self.cbo_usuarios.grid(row=0, column=1, padx=5, pady=5)

        # Seleccionar Producto
        ttk.Label(frame_form, text="Producto:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.cbo_productos = ttk.Combobox(frame_form, state="readonly", width=35)
        self.cbo_productos.grid(row=0, column=3, padx=5, pady=5)

        self._actualizar_comboboxes()

        # Botón de registro con command= que apunta al callback
        btn_registrar = ttk.Button(
            frame_form, 
            text="Registrar Venta", 
            command=self._callback_registrar_venta
        )
        btn_registrar.grid(row=0, column=4, padx=15, pady=5)

        # Frame inferior para la tabla de ventas registradas
        frame_tabla = ttk.LabelFrame(self.tab_ventas, text=" Historial de Ventas ", padding=10)
        frame_tabla.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))

        self.tree_ventas = ttk.Treeview(
            frame_tabla, 
            columns=("ID", "Cliente", "Producto", "Precio", "Fecha"), 
            show="headings"
        )
        self.tree_ventas.heading("ID", text="ID Venta")
        self.tree_ventas.heading("Cliente", text="Cliente / Usuario")
        self.tree_ventas.heading("Producto", text="Producto")
        self.tree_ventas.heading("Precio", text="Total ($)")
        self.tree_ventas.heading("Fecha", text="Fecha y Hora")

        self.tree_ventas.column("ID", width=70, anchor=tk.CENTER)
        self.tree_ventas.column("Cliente", width=180)
        self.tree_ventas.column("Producto", width=220)
        self.tree_ventas.column("Precio", width=90, anchor=tk.E)
        self.tree_ventas.column("Fecha", width=160, anchor=tk.CENTER)

        self.tree_ventas.pack(fill=tk.BOTH, expand=True)

    def _actualizar_comboboxes(self):
        self.dict_usuarios = {f"{u.nombre} (ID: {u.id_usuario})": u.id_usuario for u in self.servicio.obtener_usuarios()}
        self.dict_productos = {f"{p.nombre} - ${p.precio:.2f} (ID: {p.id_producto})": p.id_producto for p in self.servicio.obtener_productos()}

        self.cbo_usuarios["values"] = list(self.dict_usuarios.keys())
        self.cbo_productos["values"] = list(self.dict_productos.keys())

        if self.cbo_usuarios["values"]:
            self.cbo_usuarios.current(0)
        if self.cbo_productos["values"]:
            self.cbo_productos.current(0)

    def _callback_registrar_venta(self):
        """
        CALLBACK DE EVENTO:
        Flujo: Acción del usuario -> command= -> Callback -> Servicio -> Persistencia -> UI
        """
        sel_usuario = self.cbo_usuarios.get()
        sel_producto = self.cbo_productos.get()

        if not sel_usuario or not sel_producto:
            messagebox.showwarning("Atención", "Debe seleccionar un usuario y un producto.", parent=self)
            return

        id_usuario = self.dict_usuarios.get(sel_usuario)
        id_producto = self.dict_productos.get(sel_producto)

        # Delegación completa al Servicio
        exito, mensaje = self.servicio.registrar_venta(id_usuario, id_producto)

        if exito:
            messagebox.showinfo("Éxito", mensaje, parent=self)
            self._cargar_datos_ventas() # Actualización de la vista
        else:
            messagebox.showerror("Error", mensaje, parent=self)

    def _cargar_datos_ventas(self):
        # Limpiar filas existentes en la tabla
        for item in self.tree_ventas.get_children():
            self.tree_ventas.delete(item)

        # Cargar ventas actualizadas desde la capa de servicio
        ventas = self.servicio.obtener_ventas()
        for v in ventas:
            self.tree_ventas.insert(
                "", 
                tk.END, 
                values=(v.id_venta, v.cliente_nombre, v.producto_nombre, f"${v.precio:.2f}", v.fecha)
            )