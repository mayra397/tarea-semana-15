import tkinter as tk
from tkinter import ttk, messagebox
from servicios.restaurante_servicio import RestauranteServicio

class LoginView(tk.Toplevel):
    def __init__(self, parent, servicio: RestauranteServicio, on_login_success):
        super().__init__(parent)
        self.servicio = servicio
        self.on_login_success = on_login_success

        self.title("Restaurante App - Inicio de Sesión")
        self.geometry("380x300")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", parent.destroy)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        frame = ttk.Frame(self, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(frame, text="Iniciar Sesión", font=("Helvetica", 16, "bold")).pack(pady=10)

        ttk.Label(frame, text="Usuario:").pack(anchor=tk.W, pady=(5, 0))
        self.txt_usuario = ttk.Entry(frame, width=30)
        self.txt_usuario.pack(fill=tk.X, pady=5)
        self.txt_usuario.insert(0, "candrade")

        ttk.Label(frame, text="Contraseña:").pack(anchor=tk.W, pady=(5, 0))
        self.txt_password = ttk.Entry(frame, width=30, show="*")
        self.txt_password.pack(fill=tk.X, pady=5)
        self.txt_password.insert(0, "123")

        # Botón con command= asociado al callback de login
        btn_login = ttk.Button(frame, text="Ingresar", command=self._on_login_click)
        btn_login.pack(pady=15, fill=tk.X)

    def _on_login_click(self):
        usuario = self.txt_usuario.get().strip()
        password = self.txt_password.get().strip()

        if not usuario or not password:
            messagebox.showwarning("Atención", "Por favor ingrese usuario y contraseña.", parent=self)
            return

        if self.servicio.autenticar(usuario, password):
            self.withdraw()
            self.on_login_success()
        else:
            messagebox.showerror("Error", "Credenciales incorrectas.", parent=self)