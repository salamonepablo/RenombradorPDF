"""
Renombrador de viajes de larga distancia.
"""
import tkinter as tk
from tkinter import ttk, messagebox
from ..ui.base_renamer import BaseRenamerUI
from ..utils.validators import DateValidator, TrainValidator
from ..utils.formatters import DateFormatter, FilenameFormatter


class ViajeLDRenamerApp(BaseRenamerUI):
    """Aplicación para renombrar documentos de viajes LD."""
    
    def __init__(self, root: tk.Toplevel):
        super().__init__(root, "Renombrador de Viajes LD")
    
    def setup_control_frame(self, control_frame):
        """Configura los controles específicos del renombrador de viajes LD."""
        # Campo de fecha
        ttk.Label(control_frame, text="Fecha (DDMM):").grid(column=0, row=0, sticky=tk.W, padx=(0, 5))
        self.date_entry = ttk.Entry(control_frame, width=12)
        self.date_entry.grid(column=1, row=0, sticky=tk.W, padx=(0, 15))
        self.date_entry.bind("<FocusOut>", self._format_date_entry)
        self.date_entry.bind("<Return>", self._focus_next_widget)
        
        # Campo de número de tren
        ttk.Label(control_frame, text="Nro. Tren:").grid(column=2, row=0, sticky=tk.W, padx=(0, 5))
        self.train_entry = ttk.Entry(control_frame, width=12)
        self.train_entry.grid(column=3, row=0, sticky=tk.W, padx=(0, 15))
        self.train_entry.bind("<Return>", self._rename_on_enter)
        
        # Botones de acción
        self.rename_button = ttk.Button(control_frame, text="Renombrar", command=self.rename_file)
        self.rename_button.grid(column=4, row=0, padx=5)
        ttk.Button(control_frame, text="Limpiar", command=self.clear_fields).grid(column=5, row=0, padx=5)
        ttk.Button(control_frame, text="Volver al Menú", 
                  command=self.root.destroy).grid(column=6, row=0, padx=5)
    
    def _format_date_entry(self, event):
        """Formatea automáticamente la entrada de fecha."""
        content = self.date_entry.get()
        formatted = DateFormatter.format_date_input(content)
        if formatted != content:
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, formatted)
    
    def _focus_next_widget(self, event):
        """Mueve el foco al siguiente widget."""
        event.widget.tk_focusNext().focus()
        return "break"
    
    def _rename_on_enter(self, event):
        """Renombra cuando se presiona Enter."""
        self.rename_file()
        return "break"
    
    def rename_file(self):
        """Realiza el renombrado del archivo."""
        # Obtener y validar entrada
        date_str = self.date_entry.get()
        train_input = self.train_entry.get().strip()
        
        if not train_input:
            messagebox.showerror("Error", "Por favor, introduce el Número de Tren.")
            return
        
        if not TrainValidator.validate_train_number(train_input):
            messagebox.showerror("Error", 
                               "Formato de Nro. Tren incorrecto.\nDebe ser un número entre 301 y 310.")
            return
        
        if date_str and not DateValidator.validate_date(date_str):
            messagebox.showerror("Error", 
                               "Formato de fecha incorrecto. Debe ser DD-MM y una fecha válida.")
            return
        
        # Obtener fecha (usar hoy si no se especificó)
        final_date = date_str if date_str else DateFormatter.get_today_formatted()
        
        # Generar nombre
        new_name = FilenameFormatter.format_viaje_ld(final_date, train_input)
        
        # Renombrar con manejo de conflictos
        self.rename_file_with_conflict_handling(new_name)
    
    def clear_fields(self):
        """Limpia todos los campos de entrada."""
        super().clear_fields()
        self.date_entry.delete(0, tk.END)
        self.train_entry.delete(0, tk.END)
