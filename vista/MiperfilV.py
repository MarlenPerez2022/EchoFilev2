import os
import sys
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Asegurar importar desde la raíz del proyecto
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)
from controlador.usuario_controlador import UsuarioControlador

# Directorio de iconos
ICON_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))

def load_icon(name, size=(24, 24)):
    """Carga un icono .png y lo redimensiona a 'size'"""
    path = os.path.join(ICON_DIR, name)
    img = Image.open(path).resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


def crear_perfil(parent, usuario_id):
    """
    Crea la ventana 'Mi perfil' (Toplevel) de tamaño 900×600.

    parent: ventana principal (Tk) que actúa de padre.
    usuario_id: username (string) del usuario logeado.
    """
    # 1) Obtener datos actuales
    controlador = UsuarioControlador()
    datos = controlador.obtener_por_username(usuario_id)
    _, nombre_actual, usuario_actual, pwd_actual = datos

    # 2) Cargar iconos
    icon_ojo       = load_icon('ojo.png', (24, 24))
    icon_ojo_open  = load_icon('ojo-abierto.png', (24, 24))
    icon_editar    = load_icon('editar.png', (28, 28))
    icon_guardar   = load_icon('guardar-el-archivo.png', (28, 28))
    icon_cerrar    = load_icon('cerrar-sesion.png', (28, 28))

    # 3) Crear Toplevel
    root = tk.Toplevel(parent)
    root.title("Mi perfil")
    root.geometry("900x600")
    root.resizable(False, False)
    root.configure(bg="#70E6FF")
    root.transient(parent)
    root.grab_set()

    # Evitar recolección de iconos
    root.icon_ojo       = icon_ojo
    root.icon_ojo_open  = icon_ojo_open
    root.icon_editar    = icon_editar
    root.icon_guardar   = icon_guardar
    root.icon_cerrar    = icon_cerrar

    # 4) Contenedor blanco con borde
    container = tk.Frame(root, bg="white", bd=2, relief="solid")
    container.place(relx=0.5, rely=0.5, anchor="center", width=860, height=560)

    # 5) Título
    tk.Label(
        container,
        text="Mi perfil",
        font=("Arial", 32, "underline"),
        bg="white"
    ).place(x=20, y=20)

    # 6) Frame de campos
    frm = tk.Frame(container, bg="white")
    frm.place(relx=0.5, rely=0.25, anchor="n")

    # Fuentes
    label_font = ("Arial", 16)
    entry_font = ("Arial", 14)
    btn_font   = ("Arial", 14)

    # Etiqueta / Entry: Nombre
    tk.Label(frm, text="Nombre del médico:", font=label_font,
             anchor='e', bg="white").grid(row=0, column=0, padx=10, pady=10)
    entry_nombre = tk.Entry(frm, font=entry_font, width=35,
                             bg="#f0f0f0", disabledbackground="#f0f0f0")
    entry_nombre.grid(row=0, column=1, pady=10)
    entry_nombre.insert(0, nombre_actual)

    # Usuario
    tk.Label(frm, text="Usuario:", font=label_font,
             anchor='e', bg="white").grid(row=1, column=0, padx=10, pady=10)
    entry_usuario = tk.Entry(frm, font=entry_font, width=35,
                              bg="#f0f0f0", disabledbackground="#f0f0f0")
    entry_usuario.grid(row=1, column=1, pady=10)
    entry_usuario.insert(0, usuario_actual)

    # Contraseña
    tk.Label(frm, text="Contraseña:", font=label_font,
             anchor='e', bg="white").grid(row=2, column=0, padx=10, pady=10)
    entry_password = tk.Entry(frm, font=entry_font, width=35,
                               show='*', bg="#f0f0f0", disabledbackground="#f0f0f0")
    entry_password.grid(row=2, column=1, pady=10)
    entry_password.insert(0, pwd_actual)

    # Ojo mostrar/ocultar ambas contraseñas
    def toggle_password():
        if entry_password.cget('show') == '*':
            entry_password.config(show='')
            entry_confirm.config(show='')
            btn_ojo.config(image=icon_ojo_open)
        else:
            entry_password.config(show='*')
            entry_confirm.config(show='*')
            btn_ojo.config(image=icon_ojo)

    btn_ojo = tk.Button(
        frm, image=icon_ojo, bd=0,
        bg="white", activebackground="white",
        command=toggle_password
    )
    btn_ojo.grid(row=2, column=2, padx=10)

    # Confirmar contraseña
    tk.Label(frm, text="Confirmar Contraseña:", font=label_font,
             anchor='e', bg="white").grid(row=3, column=0, padx=10, pady=10)
    entry_confirm = tk.Entry(frm, font=entry_font, width=35,
                              show='*', bg="#f0f0f0", disabledbackground="#f0f0f0")
    entry_confirm.grid(row=3, column=1, pady=10)
    entry_confirm.insert(0, pwd_actual)

    # 7) Desactivar edición inicial
    entry_nombre.config(state='disabled')
    entry_usuario.config(state='disabled')
    entry_password.config(state='disabled')
    entry_confirm.config(state='disabled')

    # 8) Habilitar edición
    def habilitar_edicion():
        entry_nombre.config(state='normal')
        entry_usuario.config(state='normal')
        entry_password.config(state='normal')
        entry_confirm.config(state='normal')
        btn_guardar.config(state='normal')

    # 9) Guardar cambios
    def guardar_cambios():
        nombre = entry_nombre.get().strip()
        usr    = entry_usuario.get().strip()
        pwd    = entry_password.get().strip()
        conf   = entry_confirm.get().strip()
        if not nombre or not usr or not pwd:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        if pwd != conf:
            messagebox.showerror("Error", "Las contraseñas no coinciden.")
            return
        try:
            controlador.actualizar(usuario_id, nombre, usr, pwd)
            messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo actualizar:\n{e}")

    # 10) Frame de botones al pie
    btn_frame = tk.Frame(container, bg="white")
    btn_frame.place(relx=0.5, rely=0.85, anchor="n")
    btn_frame.columnconfigure(0, weight=1)
    btn_frame.columnconfigure(1, weight=1)
    btn_frame.columnconfigure(2, weight=1)

    btn_editar = tk.Button(
        btn_frame, text="Editar", image=icon_editar,
        compound='left', font=btn_font,
        bg="#f0f0f0", activebackground="#e0e0e0",
        command=habilitar_edicion
    )
    btn_editar.grid(row=0, column=0, padx=20)

    btn_guardar = tk.Button(
        btn_frame, text="Guardar", image=icon_guardar,
        compound='left', font=btn_font,
        bg="#f0f0f0", activebackground="#e0e0e0",
        state='disabled', command=guardar_cambios
    )
    btn_guardar.grid(row=0, column=1, padx=20)

    btn_salir = tk.Button(
        btn_frame, text="Salir", image=icon_cerrar,
        compound='left', font=btn_font,
        bg="#f0f0f0", activebackground="#e0e0e0",
        command=lambda: (root.destroy(), parent.deiconify(), parent.lift())
    )
    btn_salir.grid(row=0, column=2, padx=20)
