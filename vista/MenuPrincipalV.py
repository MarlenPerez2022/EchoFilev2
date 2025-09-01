import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys

# Para que podamos importar desde /controlador
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from controlador.usuario_controlador import UsuarioControlador
from vista.ExpedienteV import crear_ventana
from controlador.VoskC import VozControlador

# Usuario pasado por parámetro o por defecto
if len(sys.argv) > 1:
    usuario = sys.argv[1]
else:
    usuario = "default_user"

# Directorio de este archivo (Vista/)
carpeta_actual = os.path.dirname(os.path.abspath(__file__))

# Rutas a los demás .py de la vista
ruta_expediente     = os.path.join(carpeta_actual, "ExpedienteV.py")
ruta_mi_expediente  = os.path.join(carpeta_actual, "MiExpedienteV.py")
ruta_perfil         = os.path.join(carpeta_actual, "MiPerfilV.py")
ruta_inicio         = os.path.join(carpeta_actual, "InicioV.py")

def mostrar_menu(usuario):
    uc = UsuarioControlador()
    id_, nombre_completo, usr, pwd = uc.obtener_por_username(usuario)

    # ─── CALLBACK Nuevo expediente ──────────────────────────────────────────
    def abrir_nuevo_expediente():
        vc = VozControlador()               # ← se carga el modelo Vosk aquí
        crear_ventana(vc, id_)              # ← pasamos id_ como usuario_id_actual
        ventana.destroy()
        try:

            vc = VozControlador()
            # Lanza la ventana de Expediente (nuevo)
            crear_ventana(vc, id_)
            # Si no hubo excepción, cerramos el menú
            ventana.destroy()
        except Exception as e:
            # Imprime la traza completa en la terminal

            import traceback
            traceback.print_exc()
            print(f"[ERROR] al abrir Nuevo Expediente: {e}")
            # (Opcional) puedes mostrar un messagebox
          # from tkinter import messagebox
          # messagebox.showerror("Error al abrir expediente", str(e))

    # ─── CALLBACK Mis expedientes ──────────────────────────────────────────
    def abrir_mis_expedientes():
        subprocess.Popen([
            sys.executable,
            ruta_mi_expediente,
            str(id_),
            usuario
        ])
        ventana.destroy()

    # ─── CALLBACK Mi perfil ─────────────────────────────────────────────────
    def abrir_mi_perfil():
        from vista.MiperfilV import crear_perfil
        crear_perfil(ventana, usuario)
        # ventana.destroy()

    # ─── CALLBACK Cerrar sesión ─────────────────────────────────────────────
    def cerrar_sesion():
        subprocess.Popen([sys.executable, ruta_inicio])
        ventana.destroy()

    # ─── Construcción de la ventana ────────────────────────────────────────
    ventana = tk.Tk()
    ventana.title("Interfaz del Médico")
    ventana.geometry("800x600")
    ventana.config(bg="white")

    sidebar = tk.Frame(ventana, bg="#70E6FF", width=200, padx=10, pady=20)
    sidebar.pack(side="left", fill="y")

    # ─── Header con imagen de usuario y nombre ─────────────────────────────
    conectado_img = ImageTk.PhotoImage(
        Image.open(os.path.join(parent_dir, "imagenes", "conectado.png"))
    )
    # Guardamos referencia para que no se recoja
    ventana._imgs = getattr(ventana, "_imgs", []) + [conectado_img]

    header_frame = tk.Frame(sidebar, bg="#70E6FF")
    header_frame.pack(pady=20)
    tk.Label(header_frame, image=conectado_img, bg="#70E6FF").pack(side="left")
    tk.Label(
        header_frame,
        text=nombre_completo,
        font=("Arial", 18),
        bg="#70E6FF",
        fg="black"
    ).pack(side="left", padx=10)

    # ─── Botón “Nuevo expediente” ──────────────────────────────────────────
    nuevo_img = ImageTk.PhotoImage(
        Image.open(os.path.join(parent_dir, "imagenes", "archivo-nuevo.png"))
    )
    ventana._imgs.append(nuevo_img)
    btn_nuevo = tk.Button(
        sidebar,
        text="Nuevo expediente",
        image=nuevo_img,
        compound="left",
        font=("Arial", 12),
        bg="#70E6FF",
        fg="black",
        command=abrir_nuevo_expediente    # ← ahora llama a la función
    )
    btn_nuevo.pack(fill="x", pady=10)

    # ─── Botón “Mis expedientes” ───────────────────────────────────────────
    mis_img = ImageTk.PhotoImage(
        Image.open(os.path.join(parent_dir, "imagenes", "expediente.png"))
    )
    ventana._imgs.append(mis_img)
    btn_mis = tk.Button(
        sidebar,
        text="Mis expedientes",
        image=mis_img,
        compound="left",
        font=("Arial", 12),
        bg="#70E6FF",
        fg="black",
        command=abrir_mis_expedientes
    )
    btn_mis.pack(fill="x", pady=10)

    # ─── Botón “Mi perfil” ─────────────────────────────────────────────────
    perfil_img = ImageTk.PhotoImage(
        Image.open(os.path.join(parent_dir, "imagenes", "usuario.png"))
    )
    ventana._imgs.append(perfil_img)
    btn_perfil = tk.Button(
        sidebar,
        text="Mi perfil",
        image=perfil_img,
        compound="left",
        font=("Arial", 12),
        bg="#70E6FF",
        fg="black",
        command=abrir_mi_perfil
    )
    btn_perfil.pack(fill="x", pady=10)

    # ─── Botón “Cerrar sesión” ────────────────────────────────────────────
    cerrar_img = ImageTk.PhotoImage(
        Image.open(os.path.join(parent_dir, "imagenes", "cerrar-sesion.png"))
    )
    ventana._imgs.append(cerrar_img)
    btn_cerrar = tk.Button(
        sidebar,
        text="Cerrar sesión",
        image=cerrar_img,
        compound="left",
        font=("Arial", 12),
        bg="#70E6FF",
        fg="black",
        command=cerrar_sesion
    )
    btn_cerrar.pack(fill="x", pady=10)

    ventana.mainloop()


if __name__ == "__main__":
    # Permite pasar el username como argumento
    if len(sys.argv) > 1:
        usuario = sys.argv[1]
    else:
        usuario = "default_user"
    mostrar_menu(usuario)
