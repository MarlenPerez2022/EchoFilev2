import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import subprocess

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

class MiExpediente(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mis expedientes")
        self.geometry("1000x600")
        self.configure(bg="#70E6FF")  # menta-azulado

        # === Carga de imágenes PNG con rutas absolutas ===
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))

        img = Image.open(os.path.join(img_dir, "basura.png"))
        self.img_delete = ImageTk.PhotoImage(img)
        img = Image.open(os.path.join(img_dir, "editar.png"))
        self.img_edit   = ImageTk.PhotoImage(img)
        img = Image.open(os.path.join(img_dir, "cerrar-sesion.png"))
        self.img_exit   = ImageTk.PhotoImage(img)

        # Marco principal blanco con borde negro
        main = tk.Frame(self, bg="white", bd=2, relief="solid")
        main.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Título
        tk.Label(main, text="Mis expedientes", bg="white",
                 font=("Arial", 16)).pack(anchor="nw", padx=10, pady=(10,0))

        # Barra de búsqueda
        search_bar = tk.Frame(main, bg="lightgray", height=40)
        search_bar.pack(fill="x", padx=20, pady=10)
        tk.Label(search_bar, text="Búsqueda de expediente",
                 bg="lightgray", font=("Arial",12)).pack(side="left", padx=5)
        tk.Entry(search_bar, font=("Arial",12)).pack(side="left", fill="x", expand=True, padx=5)
        tk.Button(search_bar, text="🔍", font=("Arial",12),
                  command=lambda: print("Buscar...")).pack(side="left", padx=5)

        # Encabezados de la tabla
        header = tk.Frame(main, bg="white")
        header.pack(fill="x", padx=20)
        tk.Label(header, text="Folio:", font=("Arial",12,"underline"),
                 bg="white").grid(row=0, column=0, padx=5, sticky="w")
        tk.Label(header, text="Nombre del paciente", font=("Arial",12,"underline"),
                 bg="white").grid(row=0, column=1, padx=5, sticky="w")
        tk.Label(header, text="Eliminar", font=("Arial",12,"underline"),
                 bg="white").grid(row=0, column=2, padx=5)
        tk.Label(header, text="Abrir", font=("Arial",12,"underline"),
                 bg="white").grid(row=0, column=3, padx=5)

        # Filas de ejemplo
        for i in range(1, 4):
            row = tk.Frame(main, bg="white")
            row.pack(fill="x", padx=20, pady=5)
            # Folio
            tk.Label(row, text=str(i), font=("Arial",12),
                     bg="white").grid(row=0, column=0, padx=5)
            # Nombre (vacío)
            tk.Label(row, text="", font=("Arial",12),
                     width=30, anchor="w", bg="white").grid(row=0, column=1, padx=5)
            # Botón Eliminar
            tk.Button(row, image=self.img_delete, bg="lightgray", bd=0,
                      command=lambda idx=i: print(f"Eliminar fila {idx}")).grid(row=0, column=2, padx=5)
            # Botón Editar
            tk.Button(row, image=self.img_edit, bg="lightgray", bd=0,
                      command=lambda idx=i: print(f"Abrir fila {idx}")).grid(row=0, column=3, padx=5)

        def salir_y_regresar_menu():
            # 1. Cierra la ventana actual
            self.destroy()
            # 2. Abre el menú principal (ajusta el nombre del archivo si es necesario)
            menu_path = os.path.join(os.path.dirname(__file__), "MenuPrincipalV.py")
            subprocess.run([sys.executable, menu_path])
        # Botón Salir
        tk.Button(main, text="Salir", image=self.img_exit, compound="left",
                  font=("Arial",12), bg="lightgray", command=salir_y_regresar_menu)\
          .pack(anchor="se", padx=20, pady=20)


if __name__ == "__main__":
     app = MiExpediente()
     app.mainloop()
