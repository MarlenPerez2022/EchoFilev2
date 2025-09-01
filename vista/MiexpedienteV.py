import os
import sys
import subprocess
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# Asegura importar módulos desde la raíz del proyecto
def _insert_parent_dir():
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
_insert_parent_dir()

from controlador.expediente_controlador import ExpedienteControlador
from controlador.VoskC import VozControlador
from vista.ExpedienteV import crear_ventana
from functools import partial


class MiExpediente(tk.Tk):
    def __init__(self, usuario_id,username):
        super().__init__()
        self.usuario_id = usuario_id
        self.username = username
        self.title("Mis expedientes")
        self.geometry("1000x600")
        self.configure(bg="#70E6FF")

        # Cargar imágenes con resampling LANCZOS
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))
        self.img_delete = ImageTk.PhotoImage(
            Image.open(os.path.join(img_dir, "basura.png")).resize((24,24), Image.Resampling.LANCZOS)
        )
        self.img_edit = ImageTk.PhotoImage(
            Image.open(os.path.join(img_dir, "editar.png")).resize((24,24), Image.Resampling.LANCZOS)
        )
        self.img_exit = ImageTk.PhotoImage(
            Image.open(os.path.join(img_dir, "cerrar-sesion.png")).resize((24,24), Image.Resampling.LANCZOS)
        )

        # Contenedor principal blanco con borde
        self.main = tk.Frame(self, bg="white")
        self.main.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # Contenedor para la “tabla” con grid
        self.table = tk.Frame(self.main, bg="white")
        self.table.place(relx=0.02, rely=0.25, relwidth=0.96, relheight=0.65)

        self.table.grid_columnconfigure(0, weight=0)  # Folio fijo
        self.table.grid_columnconfigure(1, weight=1)  # Paciente se expande
        self.table.grid_columnconfigure(2, weight=0)  # Botón Eliminar
        self.table.grid_columnconfigure(3, weight=0)  # Botón Editar

        # Encabezados
        headers = ["No.Folio", "Nombre del paciente", "Eliminar", "Editar"]
        for col, text in enumerate(headers):
            lbl = tk.Label(self.table,
                           text=text,
                           font=("Arial", 14, "underline"),
                           bg="white")
            lbl.grid(row=0, column=col, padx=10, pady=(0, 5), sticky="w")
        # Espacio extra tras encabezados
        spacer = tk.Frame(self.table, height=10, bg="white")
        spacer.grid(row=1, column=0, columnspan=4)
        # Título
        tk.Label(self.main, text="Mis expedientes", bg="white",
                 font=("Arial", 16)).pack(anchor="nw", padx=10, pady=(10,0))

        # ─── Barra de búsqueda por folio y paciente ─────────────────────────
        self.search_bar = tk.Frame(self.main, bg="lightgray", height=40)
        self.search_bar.pack(fill="x", padx=20, pady=10)

        tk.Label(self.search_bar, text="No. Folio:", bg="lightgray", font=("Arial", 12)) \
            .pack(side="left", padx=(5, 0))
        self.entry_search_folio = tk.Entry(self.search_bar, font=("Arial", 12), width=10)
        self.entry_search_folio.pack(side="left", padx=(0, 10))

        tk.Label(self.search_bar, text="Nombre Paciente:", bg="lightgray", font=("Arial", 12)) \
            .pack(side="left", padx=(0, 5))
        self.entry_search_nombre = tk.Entry(self.search_bar, font=("Arial", 12), width=20)
        self.entry_search_nombre.pack(side="left", padx=(0, 10))

        tk.Button(self.search_bar, text="🔍", font=("Arial", 12),
                  command=self.buscar_expedientes) \
            .pack(side="left", padx=5)
        # ─────────────────────────────────────────────────────────────────────

        # Encabezados de la tabla
        self.header = tk.Frame(self.main, bg="white")
        self.header.pack(fill="x", padx=20)


        # Botón salir
        tk.Button(self.main, text="Salir",
                  image=self.img_exit,
                  compound="left",
                  font=("Arial",12),
                  bg="lightgray",
                  activebackground="white",
                  command=self._salir_y_regresar) \
            .place(relx=0.98, rely=0.90, anchor="se")
        # Lista de filas para reload
        self.rows = []

        # Carga inicial de expedientes
        self.cargar_expedientes()

    def buscar_expedientes(self):
        folio = self.entry_search_folio.get().strip() or None
        nombre = self.entry_search_nombre.get().strip() or None
        try:
            resultados = self.controlador.buscar(folio, nombre)
            # limpia la tabla
            for iid in self.tree.get_children():
                self.tree.delete(iid)
            # repuebla solo con los resultados
            for fila in resultados:
                self.tree.insert("", "end", values=fila)
        except Exception as e:
            print(f"Error al buscar expedientes: {e}")


    def cargar_expedientes(self):
        """Recarga la “tabla” de expedientes usando grid."""
        # 1) Limpia filas anteriores
        for widget in self.table.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()

        # 2) Trae sólo folio y paciente
        expedientes = ExpedienteControlador().buscar_por_usuario(self.usuario_id)

        # 3) Dibuja filas
        for i, (exp_id, num_folio, nombre_paciente) in enumerate(expedientes, start=2):
            # Folio
            tk.Label(self.table,
                     text=num_folio,
                     font=("Arial", 12),
                     bg="white") \
                .grid(row=i, column=0, padx=10, sticky="w")
            # Paciente
            tk.Label(self.table,
                     text=nombre_paciente,
                     font=("Arial", 12),
                     bg="white") \
                .grid(row=i, column=1, padx=10, sticky="w")

            # Eliminar
            def cb_del(uid=exp_id, folio=num_folio):
                if messagebox.askyesno("Confirmar", f"¿Eliminar expediente {folio}?"):
                    ExpedienteControlador().eliminar(uid)
                    messagebox.showinfo("Éxito", f"Expediente {folio} borrado exitosamente.")
                    self.cargar_expedientes()

            tk.Button(self.table,
                      image=self.img_delete,
                      bd=0,
                      bg="white",
                      activebackground="white",
                      command=cb_del) \
                .grid(row=i, column=2, padx=10, sticky="w")

            # Editar
            def cb_edit(uid=exp_id):
                from controlador.VoskC import VozControlador
                vc = VozControlador()
                crear_ventana(vc, self.usuario_id, expediente_id=uid)

            tk.Button(self.table,
                      image=self.img_edit,
                      bd=0,
                      bg="white",
                      activebackground="white",
                      command=cb_edit) \
                .grid(row=i, column=3, padx=10, sticky="w")



    def _salir_y_regresar(self):
        # 1) destruye esta ventana

        menu_path = os.path.join(os.path.dirname(__file__), "MenuPrincipalV.py")
        subprocess.Popen([sys.executable, menu_path, self.username])
        self.destroy()

if __name__ == "__main__":
    import sys

    usuario_id = int(sys.argv[1])
    username = sys.argv[2]
    app = MiExpediente(usuario_id, username)
    app.mainloop()
