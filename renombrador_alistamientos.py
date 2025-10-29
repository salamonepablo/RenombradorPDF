import os
import sys
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
import threading
import fitz

APP_TITLE = "Renombrador de Alistamientos"
DEFAULT_PATH = r"g:/Material Rodante/.ISO 9001- 2 - Coordinación General Técnica/08 - Programación/05 - Archivo/2025/"

class PDFRenamerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(APP_TITLE)
        self.current_pdf = None
        self.current_directory = ""
        self.setup_ui()
        self.load_default_drive()

    def setup_ui(self):
        style = tk.ttk.Style()
        style.configure('TFrame', background='#f0f0f0')
        style.configure('TLabel', background='#f0f0f0')
        mainframe = tk.ttk.Frame(self.root, padding=(10, 10, 10, 5))
        mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        browser_frame = tk.ttk.LabelFrame(mainframe, text="Navegación", padding=5)
        browser_frame.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S), padx=5, pady=5)
        tk.ttk.Label(browser_frame, text="Unidad:").grid(column=0, row=0, sticky=tk.W)
        self.drive_var = tk.StringVar()
        self.drive_combo = tk.ttk.Combobox(browser_frame, textvariable=self.drive_var, width=7, state="readonly")
        self.drive_combo.grid(column=1, row=0, sticky=tk.W, padx=(0, 5))
        self.drive_combo.bind('<<ComboboxSelected>>', self.on_drive_selected)
        tk.ttk.Button(browser_frame, text="Navegar", command=self.browse_folder).grid(column=2, row=0, sticky=tk.W)
        self.tree = tk.ttk.Treeview(browser_frame, columns=('path', 'type'), show='tree', height=10, displaycolumns=[])
        self.tree.grid(column=0, row=1, columnspan=3, sticky=(tk.N, tk.S, tk.W, tk.E))
        scrollbar = tk.ttk.Scrollbar(browser_frame, orient="vertical", command=self.tree.yview)
        scrollbar.grid(column=3, row=1, sticky=(tk.N, tk.S))
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.bind('<<TreeviewSelect>>', self.on_file_selected)
        preview_frame = tk.ttk.LabelFrame(mainframe, text="Vista Previa", padding=5)
        preview_frame.grid(column=1, row=0, sticky=(tk.N, tk.E, tk.S, tk.W), padx=5, pady=5)
        self.image_label = tk.ttk.Label(preview_frame, background="gray")
        self.image_label.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
        control_frame = tk.ttk.LabelFrame(mainframe, text="Datos para Renombrar", padding=10)
        control_frame.grid(column=0, row=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=(0, 5))
        tk.ttk.Label(control_frame, text="Fecha (DDMM):").grid(column=0, row=0, sticky=tk.W, padx=(0, 5))
        self.date_entry = tk.ttk.Entry(control_frame, width=12)
        self.date_entry.grid(column=1, row=0, sticky=tk.W, padx=(0, 15))
        self.date_entry.bind("<FocusOut>", self._format_date_entry)
        self.date_entry.bind("<Return>", self._focus_next_widget)
        tk.ttk.Label(control_frame, text="N° Locomotora:").grid(column=2, row=0, sticky=tk.W, padx=(0, 5))
        self.train_entry = tk.ttk.Entry(control_frame, width=12)
        self.train_entry.grid(column=3, row=0, sticky=tk.W, padx=(0, 15))
        self.train_entry.bind("<FocusOut>", self._format_train_entry)
        self.train_entry.bind("<Return>", self._rename_on_enter)
        self.rename_button = tk.ttk.Button(control_frame, text="Renombrar", command=self.rename_file)
        self.rename_button.grid(column=4, row=0, padx=5)
        tk.ttk.Button(control_frame, text="Limpiar", command=self.clear_fields).grid(column=5, row=0, padx=5)
        tk.ttk.Button(control_frame, text="Volver al Menú", command=self.root.destroy).grid(column=6, row=0, padx=5)
        self.status_var = tk.StringVar()
        self.status_var.set("Listo. Selecciona una carpeta y un PDF.")
        status_bar = tk.ttk.Label(mainframe, textvariable=self.status_var, relief=tk.SUNKEN)
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

    def _format_date_entry(self, event):
        content = self.date_entry.get()
        if len(content) == 4 and content.isdigit():
            self.date_entry.delete(0, tk.END)
            self.date_entry.insert(0, f"{content[:2]}-{content[2:]}")

    def _format_train_entry(self, event):
        content = self.train_entry.get().strip()
        if content.isdigit():
            formatted_content = self.format_train_number(content)
            self.train_entry.delete(0, tk.END)
            self.train_entry.insert(0, formatted_content)

    def _focus_next_widget(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def _rename_on_enter(self, event):
        self.rename_file()
        return "break"

    def rename_file(self):
        if not self.current_pdf:
            tk.messagebox.showerror("Error", "Por favor, selecciona un archivo PDF.")
            return
        date_str = self.date_entry.get()
        train_input = self.train_entry.get()
        if not train_input:
            tk.messagebox.showerror("Error", "Por favor, introduce el Número de Locomotora.")
            return
        if not self.validate_train_number(train_input):
            tk.messagebox.showerror("Error", "Formato de N° Locomotora incorrecto.\nDebe ser un número de 2 o 3 dígitos.")
            return
        if date_str and not self.validate_date(date_str):
            tk.messagebox.showerror("Error", "Formato de fecha incorrecto. Debe ser DD-MM y una fecha válida.")
            return
        formatted_train = self.format_train_number(train_input)
        if date_str:
            new_name = f"{date_str} AL {formatted_train}.pdf"
        else:
            today = datetime.now().strftime("%d-%m")
            new_name = f"{today} AL {formatted_train}.pdf"
        try:
            directory = os.path.dirname(self.current_pdf)
            new_path = os.path.join(directory, new_name)
            counter = 1
            base_name, ext = os.path.splitext(new_name)
            while os.path.exists(new_path):
                new_path = os.path.join(directory, f"{base_name}_{counter}{ext}")
                counter += 1
            os.rename(self.current_pdf, new_path)
            tk.messagebox.showinfo("Éxito", f"Archivo renombrado a:\n{os.path.basename(new_path)}")
            self.clear_fields()
            self.update_folder_tree(directory)
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo renombrar el archivo: {str(e)}")

    def validate_date(self, date_str):
        try:
            datetime.strptime(date_str, "%d-%m")
            return True
        except ValueError:
            return False

    def validate_train_number(self, train_str):
        clean_str = train_str.strip().upper()
        if clean_str.startswith("G-0"):
            return clean_str[3:].isdigit() and len(clean_str[3:]) == 2
        if clean_str.startswith("A"):
            return clean_str[1:].isdigit() and len(clean_str[1:]) == 3
        if clean_str.isdigit():
            return len(clean_str) in (2, 3)
        return False

    def format_train_number(self, train_str):
        clean_str = train_str.strip().upper()
        if clean_str.startswith(("G-0", "A")):
            return clean_str
        if clean_str.isdigit():
            if len(clean_str) == 2:
                return f"G-0{clean_str}"
            elif len(clean_str) == 3:
                return f"A{clean_str}"
        return train_str

    def generate_preview(self, pdf_path):
        try:
            doc = fitz.open(pdf_path)
            page = doc.load_page(0)
            rect = page.rect
            clip_rect = fitz.Rect(rect.x0, rect.y0, rect.x1, rect.height / 3)
            pix = page.get_pixmap(clip=clip_rect, dpi=200)
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
            tk.messagebox.showwarning("Advertencia", "No se encontraron unidades de disco disponibles")

    def on_drive_selected(self, event):
        drive = self.drive_var.get()
        if os.path.isdir(drive):
            self.update_folder_tree(drive)
            self.status_var.set(f"Mostrando contenido de {drive}")

    def browse_folder(self):
        folder = tk.filedialog.askdirectory(initialdir=self.current_directory if os.path.isdir(self.current_directory) else "/")
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
            tk.messagebox.showerror("Error", f"No tienes permiso para acceder a: {path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"No se pudo cargar el directorio: {str(e)}")

    def on_file_selected(self, event):
        selected_item_id = self.tree.focus()
        if not selected_item_id: return
        try:
            item_path, item_type = self.tree.item(selected_item_id, 'values')
            if item_type in ('DIR', 'PARENT'):
                self.update_folder_tree(item_path)
            elif item_type == 'FILE':
                if os.path.isfile(item_path):
                    self.current_pdf = item_path
                    self.status_var.set("Generando vista previa...")
                    self.root.update_idletasks()
                    threading.Thread(target=self.generate_preview, args=(item_path,), daemon=True).start()
        except (ValueError, IndexError):
            pass
            
    def update_image(self, photo_img):
        self.image_label.configure(image=photo_img)
        self.image_label.image = photo_img

    def clear_fields(self):
        self.image_label.configure(image='')
        self.image_label.image = None
        self.date_entry.delete(0, tk.END)
        self.train_entry.delete(0, tk.END)
        self.current_pdf = None
        self.status_var.set("Campos limpiados. Listo.")

# Ya no se necesita la función main() aquí, el menú llama a la clase directamente
if __name__ == "__main__":
    # Esto es solo para pruebas, crea una ventana raíz si se ejecuta directamente
    root = tk.Tk()
    app = PDFRenamerApp(root)
    root.mainloop()