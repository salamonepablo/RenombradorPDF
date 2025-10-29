import tkinter as tk
from tkinter import ttk
import renombrador_alistamientos
import renombrador_preparatorias

def main():
    root = tk.Tk()
    root.title("Menú Principal - Renombradores")

    def launch_app(app_class):
        # 1. Ocultar la ventana del menú
        root.withdraw()
        
        # 2. Crear una nueva ventana hija (Toplevel)
        window = tk.Toplevel(root)
        
        # 3. Iniciar la aplicación en esa nueva ventana
        app = app_class(window)
        
        # 4. Esperar hasta que la ventana hija se cierre
        root.wait_window(window)
        
        # 5. Cuando se cierra, volver a mostrar el menú
        root.deiconify()

    # Centrar la ventana
    window_width = 400
    window_height = 200
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width / 2)
    center_y = int(screen_height/2 - window_height / 2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
    root.resizable(False, False)

    # Estilo con botones de tamaño normal
    style = ttk.Style(root)
    style.configure("TButton", padding=5, font=('Helvetica', 10)) # Padding reducido

    main_frame = ttk.Frame(root, padding="20")
    main_frame.pack(expand=True, fill="both")

    ttk.Label(main_frame, text="Selecciona la herramienta a utilizar:", font=('Helvetica', 14)).pack(pady=(0, 20))

    # Los botones ahora llaman directamente a la clase de la aplicación
    btn_alistamientos = ttk.Button(
        main_frame, 
        text="Renombrador de ALISTAMIENTOS", 
        command=lambda: launch_app(renombrador_alistamientos.PDFRenamerApp)
    )
    btn_alistamientos.pack(fill="x", pady=5)

    btn_preparatoria = ttk.Button(
        main_frame, 
        text="Renombrador de PREPARATORIA", 
        command=lambda: launch_app(renombrador_preparatorias.PreparatoriaRenamerApp)
    )
    btn_preparatoria.pack(fill="x", pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()