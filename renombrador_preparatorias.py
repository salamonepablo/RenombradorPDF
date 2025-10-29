import os
import sys
from datetime import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import threading
import fitz

APP_TITLE = "Renombrador de Preparatorias"
DEFAULT_PATH = r"g:\Material Rodante\ESCANEOS LLAVALLOL\PREPARATORIA\2025"
LUGAR_MAP = {
    "Ezeiza": "ZZ",
    "F. Varela - DOA - La Plata": "LP",
    "Glew": "GW",
    "Kilo 5": "K5",
    "Llavallol": "LLV",
    "P. Constitucion": "PC",
    "Temperley": "TY"
}

class PreparatoriaRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.current_pdf = None
        self.current_directory = ""
        self.setup_ui()
        self.load_default_drive()

    def setup_ui(self):
        style = ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        mainframe = ttk.Frame(self.root, padding=(10, 10, 10, 5))
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        browser_frame = ttk.LabelFrame(mainframe, text="Navegación", padding=5)
        browser_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
        ttk.Label(browser_frame, text="Unidad:").grid(column=0, row=0, sticky=tk.W)
        self.drive_var = tk.StringVar()
        self.drive_combo = ttk.Combobox(browser_frame, textvariable=self.drive_var, width=7, state="readonly")
        self.drive_combo.grid(column=1, row=0, sticky=tk.W, padx=(0, 5))
        self.drive_combo.bind('<<ComboboxSelected>>', self.on_drive_selected)
        ttk.Button(browser_frame, text="Navegar", command=self.browse_folder).grid(column=2, row=0, sticky=tk.W)
        self.tree = ttk.Treeview(browser_frame, columns=('path', 'type'), show='tree', height=10, displaycolumns=[])
        self.tree.grid(column=0, row=1, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        scrollbar = ttk.Scrollbar(browser_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(column=3, row=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_file_selected)
        preview_frame = ttk.LabelFrame(mainframe, text="Vista Previa", padding=5)
        preview_frame.grid(column=1, row=0, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5, pady=5)
        self.image_label = ttk.Label(preview_frame, background="gray")
        self.image_label.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        control_frame = ttk.LabelFrame(mainframe, text="Datos para Renombrar", padding=10)
        control_frame.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=(0, 5))
        ttk.Label(control_frame, text="N° Formación:").grid(column=0, row=0, sticky=tk.W, padx=(0, 5))
        self.formacion_entry = ttk.Entry(control_frame, width=12)
        self.formacion_entry.grid(column=1, row=0, sticky=tk.W, padx=(0, 15))
        self.formacion_entry.bind("<Return>", self._focus_next_widget)
        ttk.Label(control_frame, text="Día (DD) (Opcional):").grid(column=2, row=0, sticky=tk.W, padx=(0, 5))
        self.dia_entry = ttk.Entry(control_frame, width=12)
        self.dia_entry.grid(column=3, row=0, sticky=tk.W, padx=(0, 15))
        self.dia_entry.bind("<Return>", self._rename_on_enter)
        self.rename_button = ttk.Button(control_frame, text="Renombrar", command=self.rename_file)
        self.rename_button.grid(column=4, row=0, padx=5)
        ttk.Button(control_frame, text="Limpiar", command=self.clear_fields).grid(column=5, row=0, padx=5)
        ttk.Button(control_frame, text="Volver al Menú", command=self.root.destroy).grid(column=6, row=0, padx=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Listo. Selecciona una carpeta y un PDF.")
        status_bar = ttk.Label(mainframe, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.grid(column=0, row=2, columnspan=2, sticky=(tk.W, tk.E))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        mainframe.columnconfigure(1, weight=3)
        mainframe.columnconfigure(0, weight=2)
        mainframe.rowconfigure(0, weight=1)
        browser_frame.rowconfigure(1, weight=1)
        preview_frame.rowconfigure(0, weight=1)
        preview_frame.columnconfigure(0, weight=1)
        self.root.state('zoomed')

    def _focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def _rename_on_enter(self, event):
        self.rename_file()
        return "break"

    def rename_file(self):
        if not self.current_pdf:
            messagebox.showerror("Error", "Por favor, selecciona un archivo PDF.")
            return
        formacion_num = self.formacion_entry.get().strip()
        dia_num = self.dia_entry.get().strip()
        if not formacion_num or not formacion_num.isdigit():
            messagebox.showerror("Error", "El 'N° Formación' es obligatorio y debe ser numérico.")
            return
        if dia_num and (not dia_num.isdigit() or not 1 <= int(dia_num) <= 31):
             messagebox.showerror("Error", "El día debe ser un número válido entre 1 y 31.")
             return
        if dia_num:
            dia_final = dia_num.zfill(2)
        else:
            dia_final = datetime.now().strftime("%d")
        directory = os.path.dirname(self.current_pdf)
        lugar_folder_name = os.path.basename(directory)
        lugar_code = LUGAR_MAP.get(lugar_folder_name, lugar_folder_name)
        try:
            parent_dir = os.path.dirname(directory)
            mes_folder_name = os.path.basename(parent_dir)
            mes_final = mes_folder_name.split('[')[1].split(']')[0]
            if not mes_final.isdigit() or len(mes_final) != 2:
                raise ValueError("El formato del mes no es '[XX]'")
        except (ValueError, IndexError):
            messagebox.showwarning("Mes no Detectado", "No se pudo obtener el mes de la carpeta padre (formato esperado: '[XX] NombreMes').\nSe usará el mes actual.")
            mes_final = datetime.now().strftime("%m")
        new_name = f"{dia_final}-{mes_final} PREP {lugar_code} F{formacion_num}.pdf"
        try:
            new_path = os.path.join(directory, new_name)
            counter = 1
            base_name, ext = os.path.splitext(new_name)
            while os.path.exists(new_path):
                new_path = os.path.join(directory, f"{base_name}_{counter}{ext}")
                counter += 1
            os.rename(self.current_pdf, new_path)
            messagebox.showinfo("Éxito", f"Archivo renombrado a:\n{os.path.basename(new_path)}")
            self.clear_fields()
            self.update_folder_tree(directory)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo renombrar el archivo: {str(e)}")

    def generate_preview(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)
            pix = page.get_pixmap(dpi=150)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            preview_width = 800
            ratio = preview_width / img.width
            new_height = int(img.height * ratio)
            resized_img = img.resize((preview_width, new_height), Image.LANCZOS)
            photo_img = ImageTk.PhotoImage(resized_img)
            self.root.after(0, self.update_image, photo_img)
            self.status_var.set("Vista previa cargada. Introduce los datos.")
            doc.close()
        except Exception as e:
            self.status_var.set(f"Error al generar vista previa: {str(e)}")
            self.root.after(0, self.update_image, None)

    def clear_fields(self):
        self.image_label.configure(image=None)
        self.image_label.image = None
        self.dia_entry.delete(0, tk.END)
        self.formacion_entry.delete(0, tk.END)
        self.current_pdf = None
        self.status_var.set("Campos limpiados. Listo.")

    def load_default_drive(self):
        drives = self.get_available_drives()
        self.drive_combo['values'] = drives
        if os.path.exists(DEFAULT_PATH):
            self.current_directory = DEFAULT_PATH
            self.drive_var.set(DEFAULT_PATH[:2])
            self.update_folder_tree(DEFAULT_PATH)
            self.status_var.set(f"Mostrando contenido de {DEFAULT_PATH}")
        elif drives:
            self.drive_var.set(drives[0])
            self.update_folder_tree(drives[0])
            self.status_var.set(f"Mostrando contenido de {drives[0]}")
        else:
            messagebox.showwarning("Advertencia", "No se encontraron unidades de disco disponibles")

    def on_drive_selected(self, event):
        drive = self.drive_var.get()
        if os.path.isdir(drive):
            self.update_folder_tree(drive)
            self.status_var.set(f"Mostrando contenido de {drive}")

    def browse_folder(self):
        folder = filedialog.askdirectory(initialdir=self.current_directory if os.path.isdir(self.current_directory) else "/")
        if folder:
            self.current_directory = folder
            self.update_folder_tree(folder)
            self.status_var.set(f"Mostrando contenido de {folder}")

    def get_available_drives(self):
        return [f"{chr(drive)}:\\" for drive in range(ord('A'), ord('Z') + 1) if os.path.exists(f"{chr(drive)}:\\")]

    def update_folder_tree(self, path):
        for item in self.tree.get_children():
            self.tree.delete(item)
        try:
            if os.path.dirname(path) != path:
                self.tree.insert('', 'end', text="..", values=(os.path.dirname(path), 'PARENT'))
            items = sorted(os.listdir(path), key=lambda s: s.lower())
            for item in items:
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    self.tree.insert('', 'end', text=item, values=(full_path, 'DIR'))
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
        selected_item_id = self.tree.focus()
        if not selected_item_id: return
        try:
            item_path, item_type = self.tree.item(selected_item_id, 'values')
            if item_type in ('DIR', 'PARENT'):
                self.update_folder_tree(item_path)
                self.formacion_entry.focus_set()
            elif item_type == 'FILE':
                if os.path.isfile(item_path):
                    self.current_pdf = item_path
                    self.status_var.set("Generando vista previa...")
                    self.root.update_idletasks()
                    threading.Thread(target=self.generate_preview, args=(item_path,), daemon=True).start()
                    self.formacion_entry.focus_set()
        except (ValueError, IndexError):
            pass

    def update_image(self, photo_img):
        self.image_label.configure(image=photo_img)
        self.image_label.image = photo_img

if __name__ == "__main__":
    root = tk.Tk()
    app = PreparatoriaRenamerApp(root)
    root.mainloop()