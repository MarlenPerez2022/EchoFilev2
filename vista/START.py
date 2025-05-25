import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
import sys
import subprocess

#  ————— Inserta la carpeta raíz del proyecto en sys.path —————
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)
#  —————————————————————————————————————————————————————————————
carpeta_actual = os.path.dirname(os.path.abspath(__file__))
logo_path = os.path.join(carpeta_actual, "..", "imagenes", "EchoFileOficial.png")
logo_path = os.path.abspath(logo_path)

from vista.InicioV import crear_inicio
from vista.MenuPrincipalV import mostrar_menu


# Mensajes que van apareciendo durante la carga
MENSAJES = [
    "Bienvenidos a EchoFile",
    "Cargando módulos...",
    "Inicializando componentes...",
    "Conectando a la base de datos...",
    "¡Listo para comenzar!"
]



# Al completar la carga, destruye splash y abre la app principal
def launch_main_app():
    splash.destroy()
    usuario = crear_inicio()
    mostrar_menu(usuario)

# —————— Splash Window ——————
splash = tk.Tk()
splash.overrideredirect(True)  # Sin bordes

# Color mágico para transparencia
transparent_color = "#123456"
splash.config(bg=transparent_color)
splash.wm_attributes("-transparentcolor", transparent_color)

# Centrar la ventana
ww, wh = 500, 450
sw, sh = splash.winfo_screenwidth(), splash.winfo_screenheight()
x = (sw - ww) // 2
y = (sh - wh) // 2
splash.geometry(f"{ww}x{wh}+{x}+{y}")

# — Logo —
if not os.path.isfile(logo_path):
    raise FileNotFoundError(f"No se encontró el logo en:\n{logo_path}")
logo_img = Image.open(logo_path)
logo_img = logo_img.resize((250, 250), Image.LANCZOS)
logo_tk  = ImageTk.PhotoImage(logo_img)
tk.Label(splash, image=logo_tk, bg=transparent_color).pack(pady=(20, 5))

# — Título con contorno usando Canvas —
canvas_title = tk.Canvas(
    splash,
    width=400,
    height=60,
    bg=transparent_color,
    highlightthickness=0
)
canvas_title.pack(pady=(0, 10))
text_title = "EchoFile"
font_title = ("Helvetica", 32, "bold")
# Dibujar contorno blanco
x_center, y_center = 200, 30
for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
    canvas_title.create_text(
        x_center+dx,
        y_center+dy,
        text=text_title,
        font=font_title,
        fill="white"
    )
# Dibujar texto negro encima
canvas_title.create_text(
    x_center,
    y_center,
    text=text_title,
    font=font_title,
    fill="black"
)

# — Mensaje dinámico con contorno en Canvas —
canvas_msg = tk.Canvas(
    splash,
    width=450,
    height=40,
    bg=transparent_color,
    highlightthickness=0
)
canvas_msg.pack(pady=(0, 10))
font_msg = ("Arial", 16, "bold")
msg_var = tk.StringVar(value=MENSAJES[0])
def draw_message(txt):
    canvas_msg.delete("all")
    # dibujar contorno blanco
    for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
        canvas_msg.create_text(
            225+dx,
            20+dy,
            text=txt,
            font=font_msg,
            fill="white"
        )
    # dibujar texto negro encima
    canvas_msg.create_text(
        225,
        20,
        text=txt,
        font=font_msg,
        fill="black"
    )
# inicial draw
draw_message(msg_var.get())
# actualizar cuando cambie el mensaje
msg_var.trace_add("write", lambda *args: draw_message(msg_var.get()))

# — Configurar Progressbar estilo verde y vacía blanca —
style = ttk.Style(splash)
style.theme_use('default')
style.configure(
    "Green.Horizontal.TProgressbar",
    troughcolor="white",
    background="#4CAF50",
    thickness=20
)

# — Barra de progreso —
progress_var = tk.IntVar(value=0)
progress_bar = ttk.Progressbar(
    splash,
    style="Green.Horizontal.TProgressbar",
    orient="horizontal",
    length=360,
    mode="determinate",
    maximum=100,
    variable=progress_var
)
progress_bar.pack(pady=(0, 20))

# — Animación de carga (10 s total) —
def update_progress(step=[0]):
    if step[0] >= 100:
        launch_main_app()
        return
    step[0] += 1
    progress_var.set(step[0])
    # actualizar mensaje cada 25%
    idx = min(len(MENSAJES) - 1, step[0] // 25)
    msg_var.set(MENSAJES[idx])
    splash.after(100, update_progress)

# ejecutar animación tras un breve delay
splash.after(200, update_progress)
splash.mainloop()

