import os
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView
from ui.main_view import MainView

def main():
    # Obtener el directorio raíz del proyecto
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Inicializar la capa de servicios
    servicio = RestauranteServicio(base_dir=base_dir)

    # Iniciar la ventana principal (oculta hasta completar login)
    app = MainView(servicio=servicio, base_dir=base_dir)
    app.withdraw()

    # Callback para mostrar la ventana principal tras un inicio exitoso
    def abrir_menu_principal():
        app.deiconify()

    # Mostrar la vista de login
    login = LoginView(parent=app, servicio=servicio, on_login_success=abrir_menu_principal)
    login.grab_set()

    app.mainloop()

if __name__ == "__main__":
    main()