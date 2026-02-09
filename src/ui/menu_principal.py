"""
Menú principal de la aplicación RenombradorPDF.
"""
import tkinter as tk
from tkinter import ttk
from ..renamers import AlistamientosRenamerApp, PreparatoriaRenamerApp, ViajeLDRenamerApp
from ..config import Settings


class MenuPrincipal:
    """Ventana de menú principal."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"Menú Principal - {Settings.APP_NAME}")
        self.setup_ui()
    
    def setup_ui(self):
        """Configura la interfaz del menú."""
        # Centrar la ventana
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = int(screen_width/2 - Settings.WINDOW_WIDTH / 2)
        center_y = int(screen_height/2 - Settings.WINDOW_HEIGHT / 2)
        self.root.geometry(
            f'{Settings.WINDOW_WIDTH}x{Settings.WINDOW_HEIGHT}+{center_x}+{center_y}'
        )
        self.root.resizable(False, False)
        
        # Estilo
        style = ttk.Style(self.root)
        style.configure("TButton", padding=5, font=('Helvetica', 10))
        
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(expand=True, fill="both")
        
        # Título
        ttk.Label(
            main_frame,
            text="Selecciona la herramienta a utilizar:",
            font=('Helvetica', 14)
        ).pack(pady=(0, 20))
        
        # Botones de aplicaciones
        self._create_app_buttons(main_frame)
    
    def _create_app_buttons(self, parent):
        """Crea los botones para lanzar cada aplicación."""
        buttons = [
            ("Renombrador de ALs / CheckLists LOCs", AlistamientosRenamerApp),
            ("Renombrador de PREPARATORIA CCEE", PreparatoriaRenamerApp),
            ("Renombrador de Viajes LD", ViajeLDRenamerApp),
        ]
        
        for text, app_class in buttons:
            btn = ttk.Button(
                parent,
                text=text,
                command=lambda cls=app_class: self.launch_app(cls)
            )
            btn.pack(fill="x", pady=5)
    
    def launch_app(self, app_class):
        """
        Lanza una aplicación de renombrado.
        
        Args:
            app_class: Clase de la aplicación a lanzar
        """
        # Ocultar menú
        self.root.withdraw()
        
        # Crear ventana hija
        window = tk.Toplevel(self.root)
        
        # Iniciar aplicación
        app = app_class(window)
        
        # Esperar hasta que se cierre
        self.root.wait_window(window)
        
        # Mostrar menú nuevamente
        self.root.deiconify()
    
    def run(self):
        """Inicia el loop principal de la aplicación."""
        self.root.mainloop()
