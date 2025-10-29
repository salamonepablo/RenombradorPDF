import os
import sys
import subprocess
import shutil
from datetime import datetime
from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import tempfile
import threading
import queue

# Configuración inicial
GHOSTSCRIPT_EXE = "gswin32c.exe"
TEMP_IMAGE_FILE = "temp_page_image.jpg"
DPI_CONVERSION = 200
APP_TITLE = "Renombrador de PDF's"
DEFAULT_PATH = r"g:/Material Rodante/.ISO 9001- 2 - Coordinación General Técnica/08 - Programación/05 - Archivo/2025/"

class PDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.current_pdf = None
        self.temp_image_path = os.path.join(tempfile.gettempdir(), TEMP_IMAGE_FILE)
        self.current_directory = ""
        self.preview_queue = queue.Queue()
        self.preview_thread = None
        self.stop_preview_thread = False
        
        # Configurar interfaz
        self.setup_ui()
        
        # Cargar unidad por defecto
        self.load_default_drive()
        
        # Verificar actualizaciones de vista previa
        self.root.after(100, self.check_preview_queue)

    def setup_ui(self):
        # ... (el resto del setup_ui permanece igual hasta los botones)
        
        # Configurar evento de cierre para limpiar
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        """Detener hilos y limpiar al cerrar"""
        self.stop_preview_thread = True
        if self.preview_thread and self.preview_thread.is_alive():
            self.preview_thread.join(timeout=1)
        if os.path.exists(self.temp_image_path):
            try:
                os.remove(self.temp_image_path)
            except:
                pass
        self.root.quit()

    def check_preview_queue(self):
        """Verificar si hay actualizaciones de vista previa"""
        try:
            while True:
                message = self.preview_queue.get_nowait()
                if message == "START":
                    self.status_var.set("Generando vista previa...")
                    self.image_label.configure(image='')
                    self.root.update()
                elif message.startswith("ERROR:"):
                    self.status_var.set(message[6:])
                elif isinstance(message, ImageTk.PhotoImage):
                    self.image_label.configure(image=message)
                    self.image_label.image = message
                    self.status_var.set("Vista previa cargada. Introduce los datos.")
        except queue.Empty:
            pass
        self.root.after(100, self.check_preview_queue)

    def on_file_selected(self, event):
        selected_item = self.tree.focus()
        if not selected_item:
            return
            
        item_values = self.tree.item(selected_item, 'values')
        item_text = self.tree.item(selected_item, 'text')
        
        if item_values and item_values[0] == 'DIR':
            # ... (código para navegar carpetas permanece igual)
            pass
        elif item_values and item_values[0] == 'FILE':
            full_path = os.path.join(self.current_directory, item_text)
            if os.path.isfile(full_path) and full_path.lower().endswith('.pdf'):
                self.current_pdf = full_path
                
                # Detener hilo anterior si está activo
                if self.preview_thread and self.preview_thread.is_alive():
                    self.stop_preview_thread = True
                    self.preview_thread.join(timeout=0.5)
                
                # Iniciar nuevo hilo para vista previa
                self.stop_preview_thread = False
                self.preview_thread = threading.Thread(
                    target=self.generate_preview, 
                    args=(full_path,),
                    daemon=True
                )
                self.preview_thread.start()

    def generate_preview(self, pdf_path):
        """Genera vista previa en un hilo separado"""
        try:
            self.preview_queue.put("START")
            
            ghostscript_path = os.path.join(os.path.dirname(sys.executable), "Ghostscript", GHOSTSCRIPT_EXE)
            if not os.path.exists(ghostscript_path):
                ghostscript_path = os.path.join(os.path.dirname(__file__), "Ghostscript", GHOSTSCRIPT_EXE)
                if not os.path.exists(ghostscript_path):
                    self.preview_queue.put("ERROR: Ghostscript no encontrado")
                    return

            # Limpiar imagen temporal anterior
            if os.path.exists(self.temp_image_path):
                try:
                    os.remove(self.temp_image_path)
                except:
                    pass

            # Comando para recortar 1/3 superior del PDF
            command = [
                ghostscript_path,
                "-dNOPAUSE", "-dBATCH", "-dNOPROMPT",
                "-sDEVICE=jpeg",
                f"-r{DPI_CONVERSION}",
                "-dFirstPage=1", "-dLastPage=1",
                "-dDEVICEWIDTHPOINTS=595",
                "-dDEVICEHEIGHTPOINTS=280",
                "-dFIXEDMEDIA",
                "-dPDFFitPage",
                "-c", "0 562 translate",
                "-f",
                f"-sOutputFile={self.temp_image_path}",
                pdf_path
            ]
            
            # Ejecutar Ghostscript
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            process = subprocess.Popen(command, startupinfo=startupinfo, 
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Esperar con timeout
            for _ in range(30):  # 30 intentos de 0.1 segundos = 3 segundos máximo
                if self.stop_preview_thread:
                    process.terminate()
                    return
                if process.poll() is not None:
                    break
                threading.Event().wait(0.1)
            else:
                process.terminate()
                self.preview_queue.put("ERROR: Tiempo de espera agotado")
                return

            if not os.path.exists(self.temp_image_path):
                self.preview_queue.put("ERROR: No se generó la vista previa")
                return

            # Cargar y redimensionar imagen
            image = Image.open(self.temp_image_path)
            width, height = image.size
            new_width = 600
            new_height = int((new_width / width) * height)
            image = image.resize((new_width, new_height), Image.LANCZOS)
            
            # Convertir para Tkinter
            photo_img = ImageTk.PhotoImage(image)
            self.preview_queue.put(photo_img)

        except Exception as e:
            self.preview_queue.put(f"ERROR: {str(e)}")

    # ... (el resto de los métodos permanece igual)

if __name__ == "__main__":
    root = Tk()
    app = PDFRenamerApp(root)
    root.mainloop()