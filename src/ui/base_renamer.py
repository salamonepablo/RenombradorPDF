"""
Clase base para interfaces de renombrado de archivos PDF.
Contiene funcionalidad común para todos los renombradores.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Optional, Callable
from ..utils.pdf_handler import PDFPreviewGenerator
from ..config.settings import Settings


class BaseRenamerUI:
    """Clase base para interfaces de renombrado."""
    
    def __init__(self, root: tk.Toplevel, title: str, default_path: str = None):
        """
        Inicializa la interfaz base.
        
        Args:
            root: Ventana principal de Tkinter
            title: Título de la ventana
            default_path: Ruta por defecto para navegación
        """
        self.root = root
        self.root.title(title)
        self.current_pdf: Optional[str] = None
        self.current_directory: str = ""
        self.default_path = default_path or Settings.DEFAULT_PATH
        self.pdf_generator = PDFPreviewGenerator()
        
        self.setup_ui()
        self.load_default_drive()
    
    def setup_ui(self):
        """Configura la interfaz de usuario."""
        # Estilos
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        
        # Frame principal
        mainframe = ttk.Frame(self.root, padding=(10, 10, 10, 5))
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        
        # Frame de navegación
        self._setup_browser_frame(mainframe)
        
        # Frame de vista previa
        self._setup_preview_frame(mainframe)
        
        # Frame de controles (debe ser implementado por subclases)
        control_frame = ttk.LabelFrame(mainframe, text="Datos para Renombrar", padding=10)
        control_frame.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=(0, 5))
        self.setup_control_frame(control_frame)
        
        # Barra de estado
        self.status_var = tk.StringVar()
        self.status_var.set("Listo. Selecciona una carpeta y un PDF.")
        status_bar = ttk.Label(mainframe, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E))
        
        # Configuración de redimensionamiento
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=3)
        mainframe.columnconfigure(0, weight=2)
        mainframe.rowconfigure(0, weight=1)
        
        # Maximizar ventana
        self.root.state('zoomed')
    
    def _setup_browser_frame(self, parent):
        """Configura el frame de navegación de archivos."""
        browser_frame = ttk.LabelFrame(parent, text="Navegación", padding=5)
        browser_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
        
        # Selector de unidad
        ttk.Label(browser_frame, text="Unidad:").grid(column=0, row=0, sticky=tk.W)
        self.drive_var = tk.StringVar()
        self.drive_combo = ttk.Combobox(browser_frame, textvariable=self.drive_var, 
                                        width=7, state="readonly")
        self.drive_combo.grid(column=1, row=0, sticky=tk.W, padx=(0, 5))
        self.drive_combo.bind('<<ComboboxSelected>>', self.on_drive_selected)
        
        # Botón navegar
        ttk.Button(browser_frame, text="Navegar", 
                  command=self.browse_folder).grid(column=2, row=0, sticky=tk.W)
        
        # Árbol de archivos
        self.tree = ttk.Treeview(browser_frame, columns=('path', 'type'), 
                                show='tree', height=10, displaycolumns=[])
        self.tree.grid(column=0, row=1, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(browser_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(column=3, row=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_file_selected)
        
        browser_frame.rowconfigure(1, weight=1)
    
    def _setup_preview_frame(self, parent):
        """Configura el frame de vista previa."""
        preview_frame = ttk.LabelFrame(parent, text="Vista Previa", padding=5)
        preview_frame.grid(column=1, row=0, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5, pady=5)
        
        self.image_label = ttk.Label(preview_frame, background="gray")
        self.image_label.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
    
    def setup_control_frame(self, control_frame):
        """
        Configura el frame de controles.
        Debe ser implementado por las subclases.
        """
        raise NotImplementedError("Las subclases deben implementar setup_control_frame")
    
    def get_available_drives(self):
        """Obtiene las unidades de disco disponibles."""
        return [f"{chr(drive)}:\\" for drive in range(ord('A'), ord('Z') + 1) 
                if os.path.exists(f"{chr(drive)}:\\")]
    
    def load_default_drive(self):
        """Carga la unidad y ruta por defecto."""
        drives = self.get_available_drives()
        self.drive_combo['values'] = drives
        
        if Settings.path_exists(self.default_path):
            self.current_directory = self.default_path
            self.drive_var.set(self.default_path[:2])
            self.update_folder_tree(self.default_path)
            self.status_var.set(f"Mostrando contenido de {self.default_path}")
        elif drives:
            self.drive_var.set(drives[0])
            self.update_folder_tree(drives[0])
            self.status_var.set(f"Mostrando contenido de {drives[0]}")
        else:
            messagebox.showwarning("Advertencia", "No se encontraron unidades de disco disponibles")
    
    def on_drive_selected(self, event):
        """Manejador de selección de unidad."""
        drive = self.drive_var.get()
        if os.path.isdir(drive):
            self.update_folder_tree(drive)
            self.status_var.set(f"Mostrando contenido de {drive}")
    
    def browse_folder(self):
        """Abre diálogo para seleccionar carpeta."""
        initial_dir = self.current_directory if os.path.isdir(self.current_directory) else "/"
        folder = filedialog.askdirectory(initialdir=initial_dir)
        if folder:
            self.current_directory = folder
            self.update_folder_tree(folder)
            self.status_var.set(f"Mostrando contenido de {folder}")
    
    def update_folder_tree(self, path: str):
        """Actualiza el árbol de archivos con el contenido de la ruta."""
        # Limpiar árbol
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            # Agregar directorio padre
            if os.path.dirname(path) != path:
                self.tree.insert('', 'end', text="..", values=(os.path.dirname(path), 'PARENT'))
            
            items = sorted(os.listdir(path), key=lambda s: s.lower())
            
            # Agregar directorios
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    self.tree.insert('', 'end', text=item, values=(full_path, 'DIR'))
            
            # Agregar archivos PDF
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isfile(full_path) and item.lower().endswith('.pdf'):
                    self.tree.insert('', 'end', text=item, values=(full_path, 'FILE'))
            
            self.current_directory = path
            
        except PermissionError:
            messagebox.showerror("Error", f"No tienes permiso para acceder a: {path}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el directorio: {str(e)}")
    
    def on_file_selected(self, event):
        """Manejador de selección de archivo."""
        selected_item_id = self.tree.focus()
        if not selected_item_id:
            return
        
        try:
            item_path, item_type = self.tree.item(selected_item_id, 'values')
            
            if item_type in ('DIR', 'PARENT'):
                self.update_folder_tree(item_path)
            elif item_type == 'FILE':
                if os.path.isfile(item_path):
                    self.current_pdf = item_path
                    self.status_var.set("Generando vista previa...")
                    self.root.update_idletasks()
                    threading.Thread(target=self._generate_preview_thread, 
                                   args=(item_path,), daemon=True).start()
        except (ValueError, IndexError):
            pass
    
    def _generate_preview_thread(self, pdf_path: str):
        """Genera la vista previa en un hilo separado."""
        photo_img, error = self.pdf_generator.generate_preview(pdf_path)
        
        if error:
            self.root.after(0, lambda: self.status_var.set(error))
            self.root.after(0, self.update_image, None)
        else:
            self.root.after(0, self.update_image, photo_img)
            self.root.after(0, lambda: self.status_var.set("Vista previa cargada. Introduce los datos."))
    
    def update_image(self, photo_img):
        """Actualiza la imagen de vista previa."""
        self.image_label.configure(image=photo_img)
        self.image_label.image = photo_img
    
    def clear_fields(self):
        """Limpia todos los campos. Debe ser extendido por subclases."""
        self.image_label.configure(image='')
        self.image_label.image = None
        self.current_pdf = None
        self.status_var.set("Campos limpiados. Listo.")
    
    def rename_file_with_conflict_handling(self, new_name: str) -> bool:
        """
        Renombra el archivo actual manejando conflictos de nombres.
        
        Args:
            new_name: Nuevo nombre para el archivo
            
        Returns:
            True si el renombrado fue exitoso, False en caso contrario
        """
        if not self.current_pdf:
            messagebox.showerror("Error", "Por favor, selecciona un archivo PDF.")
            return False
        
        try:
            directory = os.path.dirname(self.current_pdf)
            new_path = os.path.join(directory, new_name)
            
            # Manejar conflictos de nombres
            counter = 1
            base_name, ext = os.path.splitext(new_name)
            while os.path.exists(new_path):
                new_path = os.path.join(directory, f"{base_name}_{counter}{ext}")
                counter += 1
            
            os.rename(self.current_pdf, new_path)
            messagebox.showinfo("Éxito", f"Archivo renombrado a:\n{os.path.basename(new_path)}")
            self.clear_fields()
            self.update_folder_tree(directory)
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo renombrar el archivo: {str(e)}")
            return False
