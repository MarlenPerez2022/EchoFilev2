import os
import sys
import tkinter as tk
from tkinter import messagebox

# Asegura importar desde la raíz del proyecto
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from controlador.usuario_controlador import UsuarioControlador


def crear_perfil(parent, usuario_id):
    """
    Ventana para que el médico edite su perfil: nombre, usuario y contraseña.
    """
    controlador = UsuarioControlador()
    # Obtener datos actuales

    usuario = controlador.obtener_por_username(usuario_id)
    # usuario[2] = username, usuario[1] = nombre, usuario[3] = password

    root = tk.Tk()
    root = tk.Toplevel(parent)
    root.title("Mi Perfil")
    root.geometry("400x300")
    root.transient(parent)
    root.grab_set()

    tk.Label(root, text="Nombre Completo:").pack(pady=(20,0))
    entry_nombre = tk.Entry(root, width=40)
    entry_nombre.pack()
    entry_nombre.insert(0, usuario[1])

    tk.Label(root, text="Usuario:").pack(pady=(10,0))
    entry_usuario = tk.Entry(root, width=40)
    entry_usuario.pack()
    entry_usuario.insert(0, usuario[2])

    tk.Label(root, text="Contraseña:").pack(pady=(10,0))
    entry_password = tk.Entry(root, width=40, show="*")
    entry_password.pack()
    entry_password.insert(0, usuario[3])

    tk.Label(root, text="Confirmar Contraseña:").pack(pady=(10,0))
    entry_confirm = tk.Entry(root, width=40, show="*")
    entry_confirm.pack()
    entry_confirm.insert(0, usuario[3])

    # ————— INICIO: desactivar campos hasta pulsar "Editar" —————
    entry_nombre.config(state="disabled")
    entry_usuario.config(state="disabled")
    entry_password.config(state="disabled")
    entry_confirm.config(state="disabled")

    def habilitar_edicion():
        # Habilita los campos de texto y el botón Guardar
        entry_nombre.config(state="normal")
        entry_usuario.config(state="normal")
        entry_password.config(state="normal")
        entry_confirm.config(state="normal")
        btn_guardar.config(state="normal")


    # ————— FIN: desactivar campos ————————————————————————
    def guardar_cambios():
        nombre = entry_nombre.get().strip()
        usr = entry_usuario.get().strip()
        pwd = entry_password.get().strip()
        conf = entry_confirm.get().strip()
        # Validaciones básicas
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

        # Botón "Editar" (activa los campos de texto)

    btn_editar = tk.Button(root, text="Editar", command=habilitar_edicion)
    btn_editar.pack(side="right", padx=10, pady=20)

    # Botón "Guardar" (inicialmente deshabilitado)
    btn_guardar = tk.Button(root, text="Guardar", command=guardar_cambios, state="disabled")
    btn_guardar.pack(side="right", padx=10, pady=20)
    root.mainloop()
