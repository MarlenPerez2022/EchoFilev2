import tkinter as tk
from PIL import Image, ImageTk
import os
import sys
import subprocess

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if len(sys.argv) > 1:
    usuario_actual = sys.argv[1]
else:
    usuario_actual = "default_user"

from controlador.usuario_controlador import UsuarioControlador

class MiPerfil(tk.Tk):
    def __init__(self, usuario_actual):
        super().__init__()
        self.title("Mi perfil")
        self.geometry("1000x600")
        self.configure(bg="#70E6FF")  # menta-azulado

        # === Cargar datos desde la base ===
        uc = UsuarioControlador()
        datos = uc.buscar_por_usuario(usuario_actual)
        if datos:
            nombre_usuario = datos['nombre']
            usuario = datos['usuario']
            contrasena = datos['contrasena']
        else:
            nombre_usuario = ""
            usuario = usuario_actual
            contrasena = ""

        # === Carga de iconos PNG con rutas absolutas ===
        img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))
        img_edit = ImageTk.PhotoImage(Image.open(os.path.join(img_dir, "editar.png")))
        img_save = ImageTk.PhotoImage(Image.open(os.path.join(img_dir, "guardar-el-archivo.png")))
        img_exit = ImageTk.PhotoImage(Image.open(os.path.join(img_dir, "cerrar-sesion.png")))
        eye_closed_img = Image.open(os.path.join(img_dir, "ojo.png")).resize((22, 22))
        eye_open_img = Image.open(os.path.join(img_dir, "ojo-abierto.png")).resize((22, 22))
        self.eye_closed_tk = ImageTk.PhotoImage(eye_closed_img)
        self.eye_open_tk = ImageTk.PhotoImage(eye_open_img)

        # === Marco principal blanco con borde negro ===
        main = tk.Frame(self, bg="white", bd=2, relief="solid")
        main.place(relx=0.05, rely=0.05, relwidth=0.9, relheight=0.9)

        # === Título ===
        tk.Label(main, text="Mi perfil", bg="white",
                 font=("Arial", 18)).pack(anchor="nw", padx=20, pady=(20,10))

        # === Contenedor de campos ===
        campos = tk.Frame(main, bg="white")
        campos.pack(padx=50, pady=30, anchor="nw")

        # --- Campo: Nombre del médico
        tk.Label(campos, text="Nombre del médico:", bg="white",
                 font=("Arial", 12)).grid(row=0, column=0, sticky="e", pady=10, padx=(0,10))
        self.nombre_entry = tk.Entry(campos, font=("Arial", 12), width=30, bg="white")
        self.nombre_entry.grid(row=0, column=1, pady=10)
        self.nombre_entry.insert(0, nombre_usuario)

        # --- Campo: Usuario
        tk.Label(campos, text="Usuario:", bg="white",
                 font=("Arial", 12)).grid(row=1, column=0, sticky="e", pady=10, padx=(0,10))
        self.usuario_entry = tk.Entry(campos, font=("Arial", 12), width=30, bg="white")
        self.usuario_entry.grid(row=1, column=1, pady=10)
        self.usuario_entry.insert(0, usuario)

        # --- Campo: Contraseña con botón de ojo
        tk.Label(campos, text="Contraseña:", bg="white",
                 font=("Arial", 12)).grid(row=2, column=0, sticky="e", pady=10, padx=(0,10))
        self.contra_var = tk.StringVar(value=contrasena)
        self.contra_entry = tk.Entry(campos, font=("Arial", 12), width=30, bg="white",
                                     show="*", textvariable=self.contra_var)
        self.contra_entry.grid(row=2, column=1, pady=10, sticky="w")
        self.ojito = tk.Button(
            campos,
            image=self.eye_closed_tk,
            bd=0,
            bg="white",
            activebackground="white",
            command=self.toggle_password
        )
        self.ojito.grid(row=2, column=2, padx=(10, 0), sticky="w")

        # === Botones Editar, Guardar y Salir ===
        botones = tk.Frame(main, bg="white")
        botones.pack(anchor="se", padx=20, pady=20)

        btn_edit = tk.Button(
            botones,
            image=img_edit,
            text="Editar",
            compound="left",
            font=("Arial", 12),
            bg="lightgray",
            command=lambda: print("Editar perfil")
        )
        btn_edit.image = img_edit
        btn_edit.pack(side="top", pady=(0,10), fill="x")

        btn_save = tk.Button(
            botones,
            image=img_save,
            text="Guardar",
            compound="left",
            font=("Arial", 12),
            bg="lightgray",
            command=lambda: print("Guardar cambios")
        )
        btn_save.image = img_save
        btn_save.pack(side="top", pady=(0,10), fill="x")

        btn_exit = tk.Button(
            botones,
            image=img_exit,
            text="Salir",
            compound="left",
            font=("Arial", 12),
            bg="lightgray",
            command=self.salir_menu_principal
        )
        btn_exit.image = img_exit
        btn_exit.pack(side="top", fill="x")

    def toggle_password(self):
        if self.contra_entry.cget('show') == "":
            self.contra_entry.config(show="*")
            self.ojito.config(image=self.eye_closed_tk)
        else:
            self.contra_entry.config(show="")
            self.ojito.config(image=self.eye_open_tk)

    def salir_menu_principal(self):
        self.destroy()
        ruta = os.path.join(os.path.dirname(__file__), "MenuPrincipalV.py")
        subprocess.run([sys.executable, ruta])

if __name__ == "__main__":
    app = MiPerfil(usuario_actual)
    app.mainloop()
