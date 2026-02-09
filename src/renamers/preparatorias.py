"""
Renombrador de documentos de preparatoria CCEE.
"""
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from ..ui.base_renamer import BaseRenamerUI
from ..utils.validators import DateValidator
from ..utils.formatters import DateFormatter


# Mapa de lugares a códigos
LUGAR_MAP = {
    "Ezeiza": "ZZ",
    "F. Varela - DOA - La Plata": "LP",
    "Glew": "GW",
    "Kilo 5": "K5",
    "Llavallol": "LLV",
    "P. Constitucion": "PC",
    "Temperley": "TY"
}


class PreparatoriaRenamerApp(BaseRenamerUI):
    """Aplicación para renombrar documentos de preparatoria CCEE."""
    
    def __init__(self, root: tk.Toplevel):
        # Path específico para preparatorias
        default_path = r"g:\Material Rodante\ESCANEOS LLAVALLOL\PREPARATORIA\2025"
        super().__init__(root, "Renombrador de Preparatorias", default_path)
    
    def setup_control_frame(self, control_frame):
        """Configura los controles específicos del renombrador de preparatorias."""
        # Campo de formación
        ttk.Label(control_frame, text="N° Formación:").grid(column=0, row=0, sticky=tk.W, padx=(0, 5))
        self.formacion_entry = ttk.Entry(control_frame, width=12)
        self.formacion_entry.grid(column=1, row=0, sticky=tk.W, padx=(0, 15))
        self.formacion_entry.bind("<Return>", self._focus_next_widget)
        
        # Campo de día (opcional)
        ttk.Label(control_frame, text="Día (DD) (Opcional):").grid(column=2, row=0, sticky=tk.W, padx=(0, 5))
        self.dia_entry = ttk.Entry(control_frame, width=12)
        self.dia_entry.grid(column=3, row=0, sticky=tk.W, padx=(0, 15))
        self.dia_entry.bind("<Return>", self._rename_on_enter)
        
        # Botones de acción
        self.rename_button = ttk.Button(control_frame, text="Renombrar", command=self.rename_file)
        self.rename_button.grid(column=4, row=0, padx=5)
        ttk.Button(control_frame, text="Limpiar", command=self.clear_fields).grid(column=5, row=0, padx=5)
        ttk.Button(control_frame, text="Volver al Menú", 
                  command=self.root.destroy).grid(column=6, row=0, padx=5)
    
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
        if not self.current_pdf:
            messagebox.showerror("Error", "Por favor, selecciona un archivo PDF.")
            return
        
        # Obtener y validar entrada
        formacion_num = self.formacion_entry.get().strip()
        dia_num = self.dia_entry.get().strip()
        
        if not formacion_num or not formacion_num.isdigit():
            messagebox.showerror("Error", "El 'N° Formación' es obligatorio y debe ser numérico.")
            return
        
        if dia_num and (not dia_num.isdigit() or not 1 <= int(dia_num) <= 31):
            messagebox.showerror("Error", "El día debe ser un número válido entre 1 y 31.")
            return
        
        # Obtener día (usar hoy si no se especificó)
        if dia_num:
            dia_final = dia_num.zfill(2)
        else:
            dia_final = datetime.now().strftime("%d")
        
        # Obtener código de lugar desde el nombre de la carpeta
        directory = os.path.dirname(self.current_pdf)
        lugar_folder_name = os.path.basename(directory)
        lugar_code = LUGAR_MAP.get(lugar_folder_name, lugar_folder_name)
        
        # Intentar obtener mes de la carpeta padre (formato: [XX] NombreMes)
        try:
            parent_dir = os.path.dirname(directory)
            mes_folder_name = os.path.basename(parent_dir)
            mes_final = mes_folder_name.split('[')[1].split(']')[0]
            
            if not mes_final.isdigit() or len(mes_final) != 2:
                raise ValueError("El formato del mes no es '[XX]'")
                
        except (ValueError, IndexError):
            messagebox.showwarning(
                "Mes no Detectado",
                "No se pudo obtener el mes de la carpeta padre (formato esperado: '[XX] NombreMes').\n"
                "Se usará el mes actual."
            )
            mes_final = datetime.now().strftime("%m")
        
        # Generar nombre: DD-MM PREP LUGAR FXX.pdf
        new_name = f"{dia_final}-{mes_final} PREP {lugar_code} F{formacion_num}.pdf"
        
        # Renombrar con manejo de conflictos
        self.rename_file_with_conflict_handling(new_name)
    
    def clear_fields(self):
        """Limpia todos los campos de entrada."""
        super().clear_fields()
        self.formacion_entry.delete(0, tk.END)
        self.dia_entry.delete(0, tk.END)
