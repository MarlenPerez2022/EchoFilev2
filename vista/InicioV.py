#!/usr/bin/env python
import sys
import os
import tkinter as tk
from PIL import Image, ImageTk
from PIL.Image import Resampling
import subprocess

def crear_inicio():
    usuario_obtenido = None
    # ——— Hack para importar el controlador ———
    parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    if parent_dir not in sys.path:
        sys.path.insert(0, parent_dir)
    from controlador.usuario_controlador import UsuarioControlador

    # ——— Preparar ventana ———
    ventanaInicio = tk.Tk()
    ventanaInicio.title("Login")
    ventanaInicio.resizable(False, False)

    WIN_W, WIN_H = 900, 600
    sw, sh = ventanaInicio.winfo_screenwidth(), ventanaInicio.winfo_screenheight()
    x = (sw - WIN_W)//2
    y = (sh - WIN_H)//2
    ventanaInicio.geometry(f"{WIN_W}x{WIN_H}+{x}+{y}")

    # Canvas de fondo
    canvas = tk.Canvas(ventanaInicio, width=WIN_W, height=WIN_H, highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))

    # Fondo
    bg = Image.open(os.path.join(img_dir, 'Fondo2.png')).resize((WIN_W, WIN_H), resample=Resampling.LANCZOS)
    bg_tk = ImageTk.PhotoImage(bg)
    canvas.create_image(0, 0, image=bg_tk, anchor="nw")

    # ——— Coordenadas base para centrar el bloque principal a la derecha
    center_x = 400  # Puedes ajustar para mover más a la derecha o izquierda
    center_y = 455
    top_y = 110

    # Logo avatar
    logo = Image.open(os.path.join(img_dir, 'Loginc.png')).resize((180, 180), resample=Resampling.LANCZOS)
    logo_tk = ImageTk.PhotoImage(logo)
    canvas.create_image(center_y, top_y+60, image=logo_tk, anchor="center")

    # Icono inferior
    med = Image.open(os.path.join(img_dir, 'medicon.png')).resize((200, 200), resample=Resampling.LANCZOS)
    med_tk = ImageTk.PhotoImage(med)
    canvas.create_image(40, WIN_H-20, image=med_tk, anchor="sw")

    # Label y Entry Usuario
    usuario_label = tk.Label(ventanaInicio, text="Usuario:", font=("Arial", 16), fg="navy", bg="#eaf6fa")
    canvas.create_window(center_x-60, top_y+170, window=usuario_label, anchor="e")
    usuario_entry = tk.Entry(ventanaInicio, font=("Arial", 14), width=22)
    canvas.create_window(center_x-55, top_y+170, window=usuario_entry, anchor="w")

    # Label y Entry Contraseña
    pass_label = tk.Label(ventanaInicio, text="Contraseña:", font=("Arial", 16), fg="navy", bg="#eaf6fa")
    canvas.create_window(center_x-60, top_y+220, window=pass_label, anchor="e")
    contrasena_entry = tk.Entry(ventanaInicio, font=("Arial", 14), width=22, show="*")
    canvas.create_window(center_x-55, top_y+220, window=contrasena_entry, anchor="w")

    # Botón ojo para mostrar/ocultar contraseña
    eye_closed_img = Image.open(os.path.join(img_dir, 'ojo.png')).resize((24, 24), resample=Resampling.LANCZOS)
    eye_open_img   = Image.open(os.path.join(img_dir, 'ojo-abierto.png')).resize((24, 24), resample=Resampling.LANCZOS)
    eye_closed_tk  = ImageTk.PhotoImage(eye_closed_img)
    eye_open_tk    = ImageTk.PhotoImage(eye_open_img)

    def toggle_password():
        if contrasena_entry.cget('show') == "":
            contrasena_entry.config(show="*")
            eye_btn.config(image=eye_closed_tk)
        else:
            contrasena_entry.config(show="")
            eye_btn.config(image=eye_open_tk)

    eye_btn = tk.Button(
        ventanaInicio, image=eye_closed_tk, bd=0, highlightthickness=0,
        activebackground="#eaf6fa", bg="#eaf6fa", command=toggle_password
    )
    canvas.create_window(center_x+190, top_y+220, window=eye_btn, anchor="w")
    ventanaInicio.eye_closed_tk = eye_closed_tk
    ventanaInicio.eye_open_tk   = eye_open_tk

    # Label de error (invisible hasta que haya error)
    error_label = tk.Label(
        ventanaInicio,
        text="",
        font=("Arial", 12),
        fg="red",
        bg="#eaf6fa"  # mismo color del fondo canvas, así parece transparente
    )
    canvas.create_window(center_y, top_y+260, window=error_label, anchor="center")

    # Label "¿Olvidaste contraseña?" sin fondo blanco
    olvido_label = tk.Label(
        ventanaInicio,
        text="¿Olvidaste contraseña?",
        font=("Arial", 11, "italic"),
        fg="black",
        bg="#eaf6fa"
    )
    canvas.create_window(center_y, top_y+295, window=olvido_label, anchor="center")

    # Lógica de inicio de sesión
    def iniciar_sesion():
        nonlocal usuario_obtenido
        u = usuario_entry.get().strip()
        p = contrasena_entry.get().strip()
        if not u or not p:
            error_label.config(text="Ingrese usuario y contraseña")
            return
        uc = UsuarioControlador()
        usuarios = uc.obtener_todos()
        encontrados = [x for x in usuarios if x[2] == u]
        if not encontrados:
            error_label.config(text="El usuario no existe")
            return
        user = encontrados[0]
        if user[3] != p:
            error_label.config(text="Usuario o contraseña incorrectos")
            return
        error_label.config(text="")  # limpia el mensaje de error al entrar

        # --- SOLO si el login es correcto, ejecuta esto ---

        usuario_obtenido = u
        ventanaInicio.destroy()

    # Botón INICIO DE SESIÓN
    login_btn = tk.Button(
        ventanaInicio, text="INICIO DE SESIÓN",
        font=("Arial", 13, "bold"),
        bg="#2979FF", fg="white", width=22,
        command=iniciar_sesion
    )
    canvas.create_window(center_y, top_y+340, window=login_btn, anchor="center")

    # Mantener referencias para imágenes
    ventanaInicio.bg_tk   = bg_tk
    ventanaInicio.logo_tk = logo_tk
    ventanaInicio.med_tk  = med_tk


    ventanaInicio.mainloop()
    return usuario_obtenido

if __name__ == "__main__":
    usuario = crear_inicio()
    print("Login exitoso:", usuario)
