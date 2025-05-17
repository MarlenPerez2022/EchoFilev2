import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
import sys
import os
import subprocess

# Añadir directorio padre al path para que funcione import controlador
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from controlador.audio_visualizador import AudioVisualizer
from controlador.VoskC import VozControlador


def crear_ventana():
    root = tk.Tk()
    root.title("Expediente Médico")
    ww, wh = 1500, 850
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x = (sw - ww) // 2
    y = (sh - wh) // 2
    root.geometry(f"{ww}x{wh}+{x}+{y}")
    root.config(bg="#f0f0f0")

    voz_controlador = VozControlador()

    img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))

    # BARRA SUPERIOR
    frame_top = tk.Frame(root, bg="#d3d3d3")
    frame_top.pack(fill="x", pady=(5,0))

    # Reloj digital a la derecha
    reloj_frame = tk.Frame(frame_top, bg="#222237")
    reloj_frame.pack(side="right", padx=(30,100), pady=5)
    lbl_reloj = tk.Label(reloj_frame, font=("DS-Digital", 22), fg="#2dd0ff", bg="#222237")
    lbl_reloj.pack()
    lbl_fecha = tk.Label(reloj_frame, font=("Arial", 11), fg="#d3d3d3", bg="#222237")
    lbl_fecha.pack()
    def actualizar_reloj():
        ahora = datetime.now()
        lbl_reloj.config(text=ahora.strftime("%H:%M:%S"))
        lbl_fecha.config(text=ahora.strftime("%Y-%m-%d"))
        lbl_reloj.after(1000, actualizar_reloj)
    actualizar_reloj()

    # Botones de secciones
    sections = ["Datos generales", "Ficha de identificación", "Antecedentes", "Evaluación clínica"]
    botones_tabs = {}
    for name in sections:
        btn = tk.Button(frame_top, text=name, bg="lightgray", font=("Arial", 11, "bold"))
        btn.pack(side="left", padx=5, pady=5)
        botones_tabs[name] = btn

    # ÁREA CENTRAL SCROLLEABLE (canvas + inner)
    frame_middle = tk.Frame(root)
    frame_middle.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(frame_middle, bg="white")
    vsb = ttk.Scrollbar(frame_middle, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    # Frame interno
    inner = tk.Frame(canvas, bg="white")
    inner_id = canvas.create_window((0,0), window=inner, anchor="nw", tags="inner_window")
    def on_configure(_event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner.bind("<Configure>", on_configure)
    def resize_inner(event):
        canvas.itemconfig(inner_id, width=event.width)
    canvas.bind("<Configure>", resize_inner)
    # Scroll soporte
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    canvas.bind_all("<Up>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind_all("<Down>", lambda e: canvas.yview_scroll(1, "units"))

    sec_frames = {}

    # ==============================
    # --- DATOS GENERALES ---
    # ==============================
    f1 = tk.LabelFrame(inner, text="Datos generales", font=("Arial", 12, "bold"), padx=10, pady=10)
    f1.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Datos generales"] = f1
    f1.columnconfigure(1, weight=1)
    f1.columnconfigure(3, weight=1)

    # Entrys declarados y asociados
    tk.Label(f1, text="Unidad médica:").grid(row=0, column=0, sticky="w", pady=5)
    entry_unidad_medica = tk.Entry(f1, width=30)
    entry_unidad_medica.grid(row=0, column=1, sticky="we", pady=5, padx=5)

    tk.Label(f1, text="Fecha de elaboración:").grid(row=0, column=2, sticky="w", pady=5, padx=(20, 0))
    entry_fecha_elaboracion = DateEntry(f1, date_pattern='yyyy-mm-dd')
    entry_fecha_elaboracion.grid(row=0, column=3, sticky="we", padx=5, pady=5)

    tk.Label(f1, text="No. de Folio:").grid(row=1, column=0, sticky="w", pady=5)
    entry_num_folio = tk.Entry(f1, width=30)
    entry_num_folio.grid(row=1, column=1, sticky="we", pady=5, padx=5)

    tk.Label(f1, text="Hora de elaboración:").grid(row=1, column=2, sticky="w", pady=5, padx=(20, 0))
    entry_hora_elaboracion = tk.Entry(f1, width=30)
    entry_hora_elaboracion.grid(row=1, column=3, sticky="we", pady=5, padx=5)
    def actualizar_hora():
        ahora = datetime.now().strftime("%H:%M:%S")
        entry_hora_elaboracion.delete(0, tk.END)
        entry_hora_elaboracion.insert(0, ahora)
        entry_hora_elaboracion.after(1000, actualizar_hora)
    actualizar_hora()

    # ==============================
    # --- FICHA DE IDENTIFICACIÓN ---
    # ==============================
    f2 = tk.LabelFrame(inner, text="Ficha de identificación", font=("Arial", 12, "bold"), padx=10, pady=10)
    f2.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Ficha de identificación"] = f2
    f2.columnconfigure(1, weight=1)
    f2.columnconfigure(3, weight=1)

    tk.Label(f2, text="Nombre del médico:").grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre_medico = tk.Entry(f2, width=40)
    entry_nombre_medico.grid(row=0, column=1, sticky="we", padx=5)

    tk.Label(f2, text="Edad:").grid(row=0, column=2, sticky="e", padx=(20, 0))
    entry_edad = tk.Entry(f2, width=10)
    entry_edad.grid(row=0, column=3, pady=5, sticky="we")

    tk.Label(f2, text="Nombre de la o del expediente:").grid(row=1, column=0, sticky="w", pady=5)
    entry_nombre_expediente = tk.Entry(f2, width=40)
    entry_nombre_expediente.grid(row=1, column=1, sticky="we", padx=5)

    # Fila sexo + fecha de nacimiento
    tk.Label(f2, text="Sexo:").grid(row=2, column=0, sticky="w", pady=5)
    sexo_var = tk.StringVar(value="ninguno")
    sexo_frame = tk.Frame(f2, bg="#f3f3f3")
    rb1 = tk.Radiobutton(sexo_frame, text="Femenino", variable=sexo_var, value="Femenino")
    rb2 = tk.Radiobutton(sexo_frame, text="Masculino", variable=sexo_var, value="Masculino")
    rb3 = tk.Radiobutton(sexo_frame, text="Otro", variable=sexo_var, value="Otro")
    rb1.pack(side="left")
    rb2.pack(side="left")
    rb3.pack(side="left")
    sexo_frame.grid(row=2, column=1, sticky="w", padx=5)
    tk.Label(f2, text="Fecha de nacimiento:").grid(row=2, column=2, sticky="e", padx=(40, 0))
    entry_fecha_nacimiento = DateEntry(f2, date_pattern='yyyy-mm-dd')
    entry_fecha_nacimiento.grid(row=2, column=3, sticky="we", padx=5)

    tk.Label(f2, text="Ocupación del la o del paciente:").grid(row=3, column=0, sticky="w", pady=5)
    entry_ocupacion = tk.Entry(f2, width=80)
    entry_ocupacion.grid(row=3, column=1, columnspan=5, sticky="we", padx=5)

    tk.Label(f2, text="Grupo étnico:").grid(row=4, column=0, sticky="w", pady=5)
    entry_grupo_etnico = tk.Entry(f2, width=40)
    entry_grupo_etnico.grid(row=4, column=1, columnspan=5, sticky="we", padx=5)

    tk.Label(f2, text="Domicilio:").grid(row=5, column=0, sticky="w", pady=5)
    entry_domicilio = tk.Entry(f2, width=50)
    entry_domicilio.grid(row=5, column=1, columnspan=5, sticky="we", padx=5)
    tk.Label(f2, text="Teléfono:").grid(row=5, column=2, sticky="e", padx=(20, 0))
    entry_telefono = tk.Entry(f2, width=15)
    entry_telefono.grid(row=5, column=3, columnspan=3, sticky="we")

    tk.Label(f2, text="Nombre del Padre/Tutor (si aplica):").grid(row=6, column=0, sticky="w", pady=5)
    entry_padre_tutor = tk.Entry(f2, width=60)
    entry_padre_tutor.grid(row=6, column=1, columnspan=5, sticky="we", padx=5)
    tk.Label(f2, text="(caso en ser menor de edad o persona con capacidades dif.)", fg="red", font=("Arial", 9)).grid(
        row=7, column=1, columnspan=5, sticky="w", padx=5, pady=(0, 7))

    tk.Label(f2, text="Parentesco:").grid(row=8, column=0, sticky="w", pady=5)
    entry_parentesco = tk.Entry(f2, width=40)
    entry_parentesco.grid(row=8, column=1, columnspan=3, sticky="we", padx=5)
    tk.Label(f2, text="Teléfono:").grid(row=8, column=2, sticky="e", padx=(20, 0))
    entry_telefono2 = tk.Entry(f2, width=15)
    entry_telefono2.grid(row=8, column=3, columnspan=3, sticky="we")

    # ==============================
    # --- ANTECEDENTES ---
    # ==============================
    f3 = tk.LabelFrame(inner, text="Antecedentes", font=("Arial", 12, "bold"), padx=10, pady=10)
    f3.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Antecedentes"] = f3
    f3.columnconfigure(1, weight=1)
    tk.Label(f3, text="Heredo Familiares:").grid(row=0, column=0, sticky="w", pady=5)
    entry_heredo_familiares = tk.Entry(f3, width=80)
    entry_heredo_familiares.grid(row=0, column=1, padx=5, pady=5, sticky="we")
    tk.Label(f3, text="Personales No Patológicos:").grid(row=1, column=0, sticky="w", pady=5)
    entry_no_patologicos = tk.Entry(f3, width=80)
    entry_no_patologicos.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    tk.Label(f3, text="Personales Patológicos:").grid(row=2, column=0, sticky="w", pady=5)
    entry_patologicos = tk.Entry(f3, width=80)
    entry_patologicos.grid(row=2, column=1, padx=5, pady=5, sticky="we")
    tk.Label(f3, text="Gineco-Obstétricos:").grid(row=3, column=0, sticky="w", pady=5)
    entry_gineco_obs = tk.Entry(f3, width=80)
    entry_gineco_obs.grid(row=3, column=1, padx=5, pady=5, sticky="we")
    tk.Label(f3, text="Padecimiento actual:").grid(row=4, column=0, sticky="w", pady=5)
    entry_padecimiento_actual = tk.Entry(f3, width=80)
    entry_padecimiento_actual.grid(row=4, column=1, padx=5, pady=5, sticky="we")

    # ==============================
    # ...EL RESTO DE SECCIONES IGUAL QUE YA LLEVABAS...
    # ==============================

    # LISTA DE TODOS LOS CAMPOS EN ORDEN
    campos = [
        entry_unidad_medica,
        entry_fecha_elaboracion,    # <-- Calendar widget
        entry_num_folio,
        entry_hora_elaboracion,
        entry_nombre_medico,
        entry_edad,
        entry_nombre_expediente,
        sexo_var,                   # <-- Guarda el valor seleccionado, no Entry
        entry_fecha_nacimiento,     # <-- Calendar widget
        entry_ocupacion,
        entry_grupo_etnico,
        entry_domicilio,
        entry_telefono,
        entry_padre_tutor,
        entry_parentesco,
        entry_telefono2,
        entry_heredo_familiares,
        entry_no_patologicos,
        entry_patologicos,
        entry_gineco_obs,
        entry_padecimiento_actual,
    ]

    # ========== BARRA INFERIOR (ONDAS TIPO BARRA VERTICAL) ==========
    frame_bot = tk.Frame(root, bg="#70E6FF", height=120)
    frame_bot.pack(fill="x", side="bottom", padx=10, pady=5)
    visual = AudioVisualizer()
    canvas_ondas = tk.Canvas(frame_bot, width=800, height=120, bg="#070920", highlightthickness=0)
    canvas_ondas.pack(side="left", fill="x", expand=True)
    def actualizar_onda():
        niveles = visual.read_levels()
        canvas_ondas.delete("all")
        w = canvas_ondas.winfo_width()
        h = canvas_ondas.winfo_height()
        N = len(niveles)
        bar_width = max(4, int(w / (N * 1.2)))
        spacing = (w - bar_width * N) // (N + 1)
        for i, v in enumerate(niveles):
            bar_h = int(h * v)
            x0 = spacing + i * (bar_width + spacing)
            y0 = h - bar_h
            x1 = x0 + bar_width
            y1 = h
            color = "#2dd0ff"
            canvas_ondas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color, width=0)
        canvas_ondas.after(50, actualizar_onda)
    actualizar_onda()

    # Botón auxiliar con imagen+texto
    def btn_img(master, filename, text, cmd):
        path = os.path.join(img_dir, filename)
        img = ImageTk.PhotoImage(Image.open(path))
        b = tk.Button(master, image=img, text=text,
                      compound="left", font=("Arial",10),
                      command=cmd)
        b.image = img
        return b

    def salir_y_regresar_menu():
        root.destroy()
        menu_path = os.path.join(os.path.dirname(__file__), "MenuPrincipalV.py")
        subprocess.run([sys.executable, menu_path])

    # Funciones de grabación (sólo de ejemplo, modifícalas según tu flujo)
    indice_actual = 0
    def insertar_texto_en_campo_actual(texto):
        nonlocal indice_actual
        if indice_actual < len(campos):
            # Si es DateEntry o StringVar, manejalo diferente si lo necesitas
            widget = campos[indice_actual]
            if isinstance(widget, tk.Entry):
                widget.delete(0, tk.END)
                widget.insert(0, texto)
            elif isinstance(widget, DateEntry):
                widget.set_date(texto)
            elif isinstance(widget, tk.StringVar):
                widget.set(texto)
            indice_actual += 1

    def iniciar_grabacion():
        texto = voz_controlador.grabar_y_reconocer()
        insertar_texto_en_campo_actual(texto)

    btn_grab = btn_img(frame_bot, "grabar-voz.png", "Grabar", iniciar_grabacion)
    btn_stop = btn_img(frame_bot, "boton-detener.png", "Detener", lambda: print("Detener"))
    btn_save = btn_img(frame_bot, "guardar-el-archivo.png", "Guardar", lambda: print("Guardar"))
    btn_exit = btn_img(frame_bot, "cerrar-sesion.png", "Salir", salir_y_regresar_menu)

    for w in (btn_grab, btn_stop, btn_save):
        w.pack(side="left", padx=5)
    btn_exit.pack(side="right", padx=5)

    # Navegación por tabs
    current_section = tk.StringVar(value="Datos generales")
    def go_to(section):
        frame = sec_frames[section]
        inner.update_idletasks()
        y = frame.winfo_y() / inner.winfo_height()
        canvas.yview_moveto(y)
        current_section.set(section)
    for name, btn in botones_tabs.items():
        btn.config(command=lambda n=name: go_to(n))

    print("Modelo cargado desde:", voz_controlador.model)


    root.mainloop()

if __name__ == "__main__":
    crear_ventana()
