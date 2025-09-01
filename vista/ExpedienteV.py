import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
import sys
import os
import subprocess
import traceback
import json
import threading
import random
import string

_image_refs = []

# Añadir directorio padre al path para que funcione import controlador
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from controlador.audio_visualizador import AudioVisualizer
from controlador.VoskC import VozControlador
from controlador.expediente_controlador import ExpedienteControlador
from tkinter import messagebox
from mysql.connector import Error as MySQLError
# ─── Mantener vivas las imágenes para que Tk no las elimine ──────────────
_image_refs = []

def btn_img(master, filename, text, cmd):
    """
    Crea un Button con icono.
    Guarda la PhotoImage en _image_refs para que no se recoja.
    """
    import os
    from PIL import Image, ImageTk

    img_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'imagenes', filename)
    )
    img = ImageTk.PhotoImage(Image.open(img_path))
    _image_refs.append(img)
    return tk.Button(master,
                     image=img,
                     text=text,
                     compound="left",
                     font=("Arial", 10),
                     command=cmd)
# ───────────────────────────────────────────────────────────────────────────


def crear_ventana(voz_controlador, usuario_id_actual,expediente_id=None):
    if tk._default_root is None:
        root = tk.Tk()
        _run_mainloop = True
    else:
        root = tk.Toplevel(tk._default_root)
        _run_mainloop = False

    root.title("Expediente Médico")
    ww, wh = 1500, 850
    sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
    x = (sw - ww) // 2
    y = (sh - wh) // 2
    root.geometry(f"{ww}x{wh}+{x}+{y}")
    root.config(bg="#f0f0f0")

    voz_controlador = VozControlador()
    controlador = ExpedienteControlador()


    img_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'imagenes'))

    # BARRA SUPERIOR
    frame_top = tk.Frame(root, bg="#d3d3d3")
    frame_top.pack(fill="x", pady=(5, 0))

    # Reloj digital a la derecha
    reloj_frame = tk.Frame(frame_top, bg="#222237")
    reloj_frame.pack(side="right", padx=(30, 100), pady=5)
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

    current_section = tk.StringVar(value=sections[0])

    def go_to(section):
        """Scroll hasta la LabelFrame de la sección indicada."""
        frame = sec_frames[section]
        inner.update_idletasks()
        # Calcula posición relativa y mueve el canvas
        y = frame.winfo_y() / inner.winfo_height()
        canvas.yview_moveto(y)
        current_section.set(section)

    # Asigna el comando a cada botón
    for name, btn in botones_tabs.items():
        btn.config(command=lambda n=name: go_to(n))



    # ÁREA CENTRAL SCROLLEABLE
    frame_middle = tk.Frame(root)
    frame_middle.pack(fill="both", expand=True, padx=10, pady=5)

    canvas = tk.Canvas(frame_middle, bg="white")
    vsb = ttk.Scrollbar(frame_middle, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=vsb.set)
    vsb.pack(side="right", fill="y")
    canvas.pack(side="left", fill="both", expand=True)

    inner = tk.Frame(canvas, bg="white")
    inner_id = canvas.create_window((0, 0), window=inner, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    inner.bind("<Configure>", on_configure)

    def resize_inner(event):
        canvas.itemconfig(inner_id, width=event.width)
    canvas.bind("<Configure>", resize_inner)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    sec_frames = {}

    # --- DATOS GENERALES ---
    f1 = tk.LabelFrame(inner, text="Datos generales", font=("Arial", 12, "bold"), padx=10, pady=10)
    f1.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Datos generales"] = f1
    f1.columnconfigure(1, weight=1)
    f1.columnconfigure(3, weight=1)

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

    # --- FICHA DE IDENTIFICACIÓN ---
    f2 = tk.LabelFrame(inner, text="Ficha de identificación", font=("Arial", 12, "bold"), padx=10, pady=10)
    f2.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Ficha de identificación"] = f2
    f2.columnconfigure(1, weight=1)
    f2.columnconfigure(3, weight=1)


    tk.Label(f2, text="Nombre del médico:").grid(row=0, column=0, sticky="w", pady=5)
    entry_nombre_medico = tk.Entry(f2, width=40)
    entry_nombre_medico.grid(row=0, column=1, sticky="we", padx=5)


    tk.Label(f2, text="Edad:").grid(row=1, column=2, sticky="e", padx=(20, 0))
    entry_edad = tk.Entry(f2, width=10)
    entry_edad.grid(row=1, column=3, sticky="we", pady=5)


    tk.Label(f2, text="Nombre del la o del paciente:").grid(row=1, column=0, sticky="w", pady=5)
    entry_nombre_paciente = tk.Entry(f2, width=40)
    entry_nombre_paciente.grid(row=1, column=1, sticky="we", padx=5)


    tk.Label(f2, text="Sexo:").grid(row=2, column=0, sticky="w", pady=5)
    sexo_var = tk.StringVar(value="")
    sexo_frame = tk.Frame(f2)
    rb1 = tk.Radiobutton(sexo_frame, text="Femenino", variable=sexo_var, value="Femenino")
    rb2 = tk.Radiobutton(sexo_frame, text="Masculino", variable=sexo_var, value="Masculino")
    rb3 = tk.Radiobutton(sexo_frame, text="Otro", variable=sexo_var, value="Otro")
    rb1.pack(side="left")
    rb2.pack(side="left")
    rb3.pack(side="left")
    sexo_frame.grid(row=2, column=1, sticky="w", padx=5)


    tk.Label(f2, text="Fecha de nacimiento:").grid(row=2, column=2, sticky="e", padx=(20, 0))
    entry_fecha_nacimiento = DateEntry(f2, date_pattern='yyyy-mm-dd')
    entry_fecha_nacimiento.grid(row=2, column=3, sticky="we", padx=5)


    tk.Label(f2, text="Ocupación del la o del paciente:").grid(row=3, column=0, sticky="w", pady=5)
    entry_ocupacion = tk.Entry(f2, width=80)
    entry_ocupacion.grid(row=3, column=1, columnspan=3, sticky="we", padx=5)


    tk.Label(f2, text="Grupo étnico:").grid(row=4, column=0, sticky="w", pady=5)
    entry_grupo_etnico = tk.Entry(f2, width=40)
    entry_grupo_etnico.grid(row=4, column=1, columnspan=3, sticky="we", padx=5)


    tk.Label(f2, text="Domicilio:").grid(row=5, column=0, sticky="w", pady=5)
    entry_domicilio = tk.Entry(f2, width=50)
    entry_domicilio.grid(row=5, column=1, columnspan=3, sticky="we", padx=5)


    tk.Label(f2, text="Teléfono:").grid(row=5, column=2, sticky="e", padx=(20, 0))
    entry_telefono = tk.Entry(f2, width=15)
    entry_telefono.grid(row=5, column=3, sticky="we", padx=5)


    tk.Label(f2, text="Nombre del Padre o Tutor").grid(row=6, column=0, sticky="w", pady=5)
    entry_padre_tutor = tk.Entry(f2, width=60)
    entry_padre_tutor.grid(row=6, column=1, columnspan=3, sticky="we", padx=5)
    tk.Label(f2, text="(caso en ser menor de edad o persona con capacidades dif.)", fg="red", font=("Arial", 9)).grid(row=7, column=1, sticky="w")


    tk.Label(f2, text="Parentesco con la o el paciente:").grid(row=8, column=0, sticky="w", pady=5)
    entry_parentesco = tk.Entry(f2, width=40)
    entry_parentesco.grid(row=8, column=1, sticky="we", padx=5)
    tk.Label(f2, text="Teléfono tutor:").grid(row=8, column=2, sticky="e", padx=(20, 0))
    entry_telefono2 = tk.Entry(f2, width=15)
    entry_telefono2.grid(row=8, column=3, sticky="we", padx=5)


    # --- ANTECEDENTES ---
    f3 = tk.LabelFrame(inner, text="Antecedentes", font=("Arial", 12, "bold"), padx=10, pady=10)
    f3.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Antecedentes"] = f3
    f3.columnconfigure(1, weight=1)


    labels_ante = [
        "Heredo Familiares:",
        "Personales No Patológicos:",
        "Personales Patológicos:",
        "Gineco-Obstétricos:",
        "Padecimiento actual:"
    ]
    entries_ante = []

    tk.Label(f3, text="Heredo Familiares:").grid(row=0, column=0, sticky="w", pady=5)
    entry_heredo_familiares = tk.Entry(f3, width=80)
    entry_heredo_familiares.grid(row=0, column=1, padx=5, pady=5, sticky="we")
    entries_ante.append(entry_heredo_familiares)


    tk.Label(f3, text="Personales No Patológicos:").grid(row=1, column=0, sticky="w", pady=5)
    entry_no_patologicos = tk.Entry(f3, width=80)
    entry_no_patologicos.grid(row=1, column=1, padx=5, pady=5, sticky="we")
    entries_ante.append(entry_no_patologicos)


    tk.Label(f3, text="Personales Patológicos:").grid(row=2, column=0, sticky="w", pady=5)
    entry_patologicos = tk.Entry(f3, width=80)
    entry_patologicos.grid(row=2, column=1, padx=5, pady=5, sticky="we")
    entries_ante.append(entry_patologicos)


    tk.Label(f3, text="Gineco-Obstétricos:").grid(row=3, column=0, sticky="w", pady=5)
    entry_gineco_obs = tk.Entry(f3, width=80)
    entry_gineco_obs.grid(row=3, column=1, padx=5, pady=5, sticky="we")
    entries_ante.append(entry_gineco_obs)


    tk.Label(f3, text="Padecimiento actual:").grid(row=4, column=0, sticky="w", pady=5)
    entry_padecimiento_actual = tk.Entry(f3, width=80)
    entry_padecimiento_actual.grid(row=4, column=1, padx=5, pady=5, sticky="we")
    entries_ante.append(entry_padecimiento_actual)


    # --- Interrogatorio por sistemas ---
    sub3 = tk.LabelFrame(inner, text="Interrogatorio por aparatos y sistemas", font=("Arial", 11), padx=10, pady=10)
    sub3.pack(fill="x", expand=True, padx=10, pady=10)
    sub3.columnconfigure(1, weight=1)
    sub3.columnconfigure(3, weight=1)


    # Fila 0
    tk.Label(sub3, text="Cardiovascular:").grid(row=0, column=0, sticky="w", pady=5)
    entry_cardiovascular = tk.Entry(sub3, width=30)
    entry_cardiovascular.grid(row=0, column=1, padx=5, pady=5, sticky="we")


    tk.Label(sub3, text="Endócrino:").grid(row=0, column=2, sticky="w", padx=(20, 0))
    entry_endocrino = tk.Entry(sub3, width=30)
    entry_endocrino.grid(row=0, column=3, padx=5, pady=5, sticky="we")

    # Fila 1
    tk.Label(sub3, text="Respiratorio:").grid(row=1, column=0, sticky="w", pady=5)
    entry_respiratorio = tk.Entry(sub3, width=30)
    entry_respiratorio.grid(row=1, column=1, padx=5, pady=5, sticky="we")


    tk.Label(sub3, text="Nervioso:").grid(row=1, column=2, sticky="w", padx=(20, 0))
    entry_nervioso = tk.Entry(sub3, width=30)
    entry_nervioso.grid(row=1, column=3, padx=5, pady=5, sticky="we")


    # Fila 2
    tk.Label(sub3, text="Gastrointestinal:").grid(row=2, column=0, sticky="w", pady=5)
    entry_gastrointestinal = tk.Entry(sub3, width=30)
    entry_gastrointestinal.grid(row=2, column=1, padx=5, pady=5, sticky="we")


    tk.Label(sub3, text="Musculoesquelético:").grid(row=2, column=2, sticky="w", padx=(20, 0))
    entry_musculoesqueletico = tk.Entry(sub3, width=30)
    entry_musculoesqueletico.grid(row=2, column=3, padx=5, pady=5, sticky="we")


    # Fila 3
    tk.Label(sub3, text="Gastrourinario:").grid(row=3, column=0, sticky="w", pady=5)
    entry_gastrourinario = tk.Entry(sub3, width=30)
    entry_gastrourinario.grid(row=3, column=1, padx=5, pady=5, sticky="we")


    tk.Label(sub3, text="Piel y Anexos:").grid(row=3, column=2, sticky="w", padx=(20, 0))
    entry_piel_anexos = tk.Entry(sub3, width=30)
    entry_piel_anexos.grid(row=3, column=3, padx=5, pady=5, sticky="we")


    # Fila 4 (solo un campo)
    tk.Label(sub3, text="Hématico/Linfático:").grid(row=4, column=0, sticky="w", pady=5)
    entry_hematico_linfatico = tk.Entry(sub3, width=30)
    entry_hematico_linfatico.grid(row=4, column=1, padx=5, pady=5, sticky="we")


    # Lista opcional por si la quieres recorrer después
    #entries_interrogatorio = [
    #entry_cardiovascular,
    #entry_endocrino,
    #entry_respiratorio,
    #entry_nervioso,
    #entry_gastrointestinal,
    #entry_musculoesqueletico,
    #entry_gastrourinario,
    #entry_piel_anexos,
    #entry_hematico_linfatico
    #]


    # --- EVALUACIÓN CLÍNICA ---
    f4 = tk.LabelFrame(inner, text="Evaluación clínica", font=("Arial", 12, "bold"), padx=10, pady=10)
    f4.pack(fill="x", expand=True, padx=10, pady=10)
    sec_frames["Evaluación clínica"] = f4
    for c in range(1, 15): f4.columnconfigure(c, weight=1)


    # Signos Vitales / Antropometría
    tk.Label(f4, text="Signos Vitales/Antropometría", font=("Arial", 11, "bold")).grid(row=0, column=0, columnspan=8, sticky="w", pady=(0,5))

    # Etiquetas y campos en una sola fila
    tk.Label(f4, text="Tensión Arterial:").grid(row=1, column=0, sticky="e", pady=5)
    entry_presion = tk.Entry(f4, width=12)
    entry_presion.grid(row=1, column=1, sticky="we", padx=5)


    tk.Label(f4, text="Temperatura:").grid(row=1, column=2, sticky="e", pady=5)
    entry_temp = tk.Entry(f4, width=12)
    entry_temp.grid(row=1, column=3, sticky="we", padx=5)


    tk.Label(f4, text="Frecuencia Cardíaca:").grid(row=1, column=4, sticky="e", pady=5)
    entry_fc = tk.Entry(f4, width=12)
    entry_fc.grid(row=1, column=5, sticky="we", padx=5)


    tk.Label(f4, text="Frecuencia Respiratoria:").grid(row=1, column=6, sticky="e", pady=5)
    entry_fr = tk.Entry(f4, width=12)
    entry_fr.grid(row=1, column=7, sticky="we", padx=5)


    tk.Label(f4, text="Peso:").grid(row=1, column=8, sticky="e", pady=5)
    entry_peso = tk.Entry(f4, width=12)
    entry_peso.grid(row=1, column=9, sticky="we", padx=5)


    tk.Label(f4, text="Talla:").grid(row=1, column=10, sticky="e", pady=5)
    entry_talla = tk.Entry(f4, width=12)
    entry_talla.grid(row=1, column=11, sticky="we", padx=5)


    # Exploración Física
    tk.Label(f4, text="Exploración Física", font=("Arial", 11, "bold")).grid(row=2, column=0, columnspan=8, sticky="w",
                                                                             pady=(12, 5))

    # Izquierda
    tk.Label(f4, text="Habitus Exterior:").grid(row=3, column=0, sticky="e", pady=5)
    entry_habitus = tk.Entry(f4, width=60)
    entry_habitus.grid(row=3, column=1, columnspan=4, sticky="we", padx=5)


    tk.Label(f4, text="Cabeza:").grid(row=4, column=0, sticky="e", pady=5)
    entry_cabeza = tk.Entry(f4, width=60)
    entry_cabeza.grid(row=4, column=1, columnspan=4, sticky="we", padx=5)


    tk.Label(f4, text="Cuello:").grid(row=5, column=0, sticky="e", pady=5)
    entry_cuello = tk.Entry(f4, width=60)
    entry_cuello.grid(row=5, column=1, columnspan=4, sticky="we", padx=5)



    tk.Label(f4, text="Tórax:").grid(row=6, column=0, sticky="e", pady=5)
    entry_torax = tk.Entry(f4, width=60)
    entry_torax.grid(row=6, column=1, columnspan=4, sticky="we", padx=5)


    # Derecha
    tk.Label(f4, text="Abdomen:").grid(row=3, column=6, sticky="e", padx=(30, 0), pady=5)
    entry_abdomen = tk.Entry(f4, width=30)
    entry_abdomen.grid(row=3, column=7, columnspan=3, sticky="we", padx=5)


    tk.Label(f4, text="Genitales:").grid(row=4, column=6, sticky="e", padx=(30, 0), pady=5)
    entry_genitales = tk.Entry(f4, width=30)
    entry_genitales.grid(row=4, column=7, columnspan=3, sticky="we", padx=5)


    tk.Label(f4, text="Extremidades:").grid(row=5, column=6, sticky="e", padx=(30, 0), pady=5)
    entry_extremidades = tk.Entry(f4, width=30)
    entry_extremidades.grid(row=5, column=7, columnspan=3, sticky="we", padx=5)


    tk.Label(f4, text="Piel:").grid(row=6, column=6, sticky="e", padx=(30, 0), pady=5)
    entry_piel = tk.Entry(f4, width=30)
    entry_piel.grid(row=6, column=7, columnspan=3, sticky="we", padx=5)


    # Resultados y Diagnósticos
    start_row = 7

    tk.Label(f4, text="Resultados Previos y Actuales de Laboratorio, Gabinete y otros:").grid(
        row=start_row, column=0, columnspan=2, sticky="w", pady=5)
    entry_resultados_lab = tk.Entry(f4, width=100)
    entry_resultados_lab.grid(row=start_row, column=2, columnspan=11, sticky="we", padx=5, pady=5)



    tk.Label(f4, text="Diagnósticos o Problemas Clínicos:").grid(
        row=start_row + 1, column=0, columnspan=2, sticky="w", pady=5)
    entry_diagnostico = tk.Entry(f4, width=100)
    entry_diagnostico.grid(row=start_row + 1, column=2, columnspan=11, sticky="we", padx=5, pady=5)


    tk.Label(f4, text="Farmacológico:").grid(
        row=start_row + 2, column=0, columnspan=2, sticky="w", pady=5)
    entry_farmacologico = tk.Entry(f4, width=100)
    entry_farmacologico.grid(row=start_row + 2, column=2, columnspan=11, sticky="we", padx=5, pady=5)


    tk.Label(f4, text="Terapéutica Empleada y Resultados (Previos):").grid(
        row=start_row + 3, column=0, columnspan=2, sticky="w", pady=5)
    entry_terapeutica_previa = tk.Entry(f4, width=100)
    entry_terapeutica_previa.grid(row=start_row + 3, column=2, columnspan=11, sticky="we", padx=5, pady=5)


    tk.Label(f4, text="Terapéutica Actual:").grid(
        row=start_row + 4, column=0, columnspan=2, sticky="w", pady=5)
    entry_terapeutica_actual = tk.Entry(f4, width=100)
    entry_terapeutica_actual.grid(row=start_row + 4, column=2, columnspan=11, sticky="we", padx=5, pady=5)


    tk.Label(f4, text="Pronóstico:").grid(
        row=start_row + 5, column=0, columnspan=2, sticky="w", pady=5)
    entry_pronostico = tk.Entry(f4, width=100)
    entry_pronostico.grid(row=start_row + 5, column=2, columnspan=11, sticky="we", padx=5, pady=5)

    if expediente_id is not None:
        datos = controlador.obtener_por_id(expediente_id)
        if not datos:
            messagebox.showerror("Error", f"Expediente {expediente_id} no existe.")
            root.destroy()
            return

        # extraer datos individuales
        unidad_medica = datos[1]
        fecha_elaboracion = datos[2]
        num_folio = datos[3]
        hora_elaboracion = datos[4]
        nombre_medico = datos[5]
        nombre_paciente = datos[6]
        edad = datos[7]
        sexo = datos[8]
        fecha_nacimiento = datos[9]
        ocupacion = datos[10]
        grupo_etnico = datos[11]
        domicilio = datos[12]
        telefono = datos[13]
        padre_tutor = datos[14]
        parentesco = datos[15]
        telefono_tutor = datos[16]
        heredo_familiares = datos[17]
        personales_no_patologicos = datos[18]
        personales_patologicos = datos[19]
        gineco_obstetricos = datos[20]
        padecimiento_actual = datos[21]
        cardiovascular = datos[22]
        endocrino = datos[23]
        respiratorio = datos[24]
        nervioso = datos[25]
        gastrointestinal = datos[26]
        musculoesqueletico = datos[27]
        gastrourinario = datos[28]
        piel_mucosa_anexos = datos[29]
        hematico_linfatico = datos[30]
        presion = datos[31]
        temperatura = datos[32]
        frecuencia_cardiaca = datos[33]
        frecuencia_respiratoria = datos[34]
        peso = datos[35]
        talla = datos[36]
        habitus_exterior = datos[37]
        abdomen = datos[38]
        cabeza = datos[39]
        genitales = datos[40]
        extremidades = datos[41]
        cuello = datos[42]
        torax = datos[43]
        piel = datos[44]
        resultados_previos_gabinete = datos[45]
        diagnosticos_clinicos = datos[46]
        farmacologico = datos[47]
        terapeutica_previos = datos[48]
        terapeutica_actual = datos[49]
        pronostico = datos[50]

        # poblar los widgets
        entry_unidad_medica.insert(0, unidad_medica)
        entry_fecha_elaboracion.set_date(fecha_elaboracion)
        entry_num_folio.insert(0, num_folio)
        entry_hora_elaboracion.insert(0, hora_elaboracion)

        entry_nombre_medico.insert(0, nombre_medico)
        entry_edad.insert(0, edad)
        entry_nombre_paciente.insert(0, nombre_paciente)
        sexo_var.set(sexo)
        entry_fecha_nacimiento.set_date(fecha_nacimiento)

        entry_ocupacion.insert(0, ocupacion)
        entry_grupo_etnico.insert(0, grupo_etnico)
        entry_domicilio.insert(0, domicilio)
        entry_telefono.insert(0, telefono)

        entry_padre_tutor.insert(0, padre_tutor)
        entry_parentesco.insert(0, parentesco)
        entry_telefono2.insert(0, telefono_tutor)

        entry_heredo_familiares.insert(0, heredo_familiares)
        entry_no_patologicos.insert(0, personales_no_patologicos)
        entry_patologicos.insert(0, personales_patologicos)
        entry_gineco_obs.insert(0, gineco_obstetricos)
        entry_padecimiento_actual.insert(0, padecimiento_actual)

        entry_cardiovascular.insert(0, cardiovascular)
        entry_endocrino.insert(0, endocrino)
        entry_respiratorio.insert(0, respiratorio)
        entry_nervioso.insert(0, nervioso)
        entry_gastrointestinal.insert(0, gastrointestinal)
        entry_musculoesqueletico.insert(0, musculoesqueletico)
        entry_gastrourinario.insert(0, gastrourinario)
        entry_piel_anexos.insert(0, piel_mucosa_anexos)
        entry_hematico_linfatico.insert(0, hematico_linfatico)

        entry_presion.insert(0, presion)
        entry_temp.insert(0, temperatura)
        entry_fc.insert(0, frecuencia_cardiaca)
        entry_fr.insert(0, frecuencia_respiratoria)
        entry_peso.insert(0, peso)
        entry_talla.insert(0, talla)

        entry_habitus.insert(0, habitus_exterior)
        entry_abdomen.insert(0, abdomen)
        entry_cabeza.insert(0, cabeza)
        entry_genitales.insert(0, genitales)
        entry_extremidades.insert(0, extremidades)
        entry_cuello.insert(0, cuello)
        entry_torax.insert(0, torax)
        entry_piel.insert(0, piel)

        entry_resultados_lab.insert(0, resultados_previos_gabinete)
        entry_diagnostico.insert(0, diagnosticos_clinicos)
        entry_farmacologico.insert(0, farmacologico)
        entry_terapeutica_previa.insert(0, terapeutica_previos)
        entry_terapeutica_actual.insert(0, terapeutica_actual)
        entry_pronostico.insert(0, pronostico)

    else:
        # inicializar variables vacías para nuevo expediente
        unidad_medica = fecha_elaboracion = num_folio = ""


    campos = [
        # DATOS GENERALES
        entry_unidad_medica,
        entry_fecha_elaboracion,
        entry_num_folio,
        entry_hora_elaboracion,

        # FICHA DE IDENTIFICACIÓN
        entry_nombre_medico,
        entry_edad,
        entry_nombre_paciente,
        sexo_var,
        entry_fecha_nacimiento,
        entry_ocupacion,
        entry_grupo_etnico,
        entry_domicilio,
        entry_telefono,
        entry_padre_tutor,
        entry_parentesco,
        entry_telefono2,

        # ANTECEDENTES
        entry_heredo_familiares,
        entry_no_patologicos,
        entry_patologicos,
        entry_gineco_obs,
        entry_padecimiento_actual,

        # INTERROGATORIO POR APARATOS Y SISTEMAS
        entry_cardiovascular,
        entry_endocrino,
        entry_respiratorio,
        entry_nervioso,
        entry_gastrointestinal,
        entry_musculoesqueletico,
        entry_gastrourinario,
        entry_piel_anexos,
        entry_hematico_linfatico,

        # EVALUACIÓN CLÍNICA - SIGNOS VITALES
        entry_presion,
        entry_temp,
        entry_fc,
        entry_fr,
        entry_peso,
        entry_talla,

        # EXPLORACIÓN FÍSICA
        entry_habitus,
        entry_abdomen,
        entry_cabeza,
        entry_genitales,
        entry_cuello,
        entry_extremidades,
        entry_torax,
        entry_piel,

        # RESULTADOS Y DIAGNÓSTICOS
        entry_resultados_lab,
        entry_diagnostico,
        entry_farmacologico,
        entry_terapeutica_previa,
        entry_terapeutica_actual,
        entry_pronostico,
    ]

    excluded = [entry_fecha_elaboracion, entry_hora_elaboracion, sexo_var]
    campos_voz = [w for w in campos if w not in excluded]
    indice_voz = 0
    is_recording = False

    numeric_fields = {
        entry_edad,
        entry_num_folio,
        entry_telefono,
        entry_telefono2,
        entry_fecha_nacimiento,  # DateEntry
        entry_hora_elaboracion,  # Entry
        entry_presion,
        entry_temp,
        entry_fc,
        entry_fr,
        entry_peso,
        entry_talla,
    }

    # ─── Funciones de navegación ───
    def focus_on_current():
        w = campos_voz[indice_voz]
        if hasattr(w, "focus_set"):
            w.focus_set()

    def move_up(event=None):
        nonlocal indice_voz
        if not is_recording: return
        indice_voz = max(indice_voz - 1, 0)
        focus_on_current()
        return "break"

    def move_down(event=None):
        nonlocal indice_voz
        if not is_recording: return
        indice_voz = min(indice_voz + 1, len(campos_voz) - 1)
        focus_on_current()
        return "break"

    def move_left(event=None):
        return move_up(event)

    def move_right(event=None):
        return move_down(event)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def configurar_navegacion_teclado():
        # Rueda y flechas para scroll
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Up>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Down>", lambda e: canvas.yview_scroll(1, "units"))
        # WSAD para navegar entre campos de voz
        canvas.bind_all("<KeyPress-w>", move_up)
        canvas.bind_all("<KeyPress-s>", move_down)
        canvas.bind_all("<KeyPress-a>", move_left)
        canvas.bind_all("<KeyPress-d>", move_right)

    # ─── Sincronización de foco con índice ───
    def on_focus_in(event):
        nonlocal indice_voz
        w = event.widget
        if w in campos_voz:
            indice_voz = campos_voz.index(w)

    for w in campos_voz:
        w.bind("<FocusIn>", on_focus_in)

    # ─── Avanzar con ENTER ───
    def on_enter(event):
        nonlocal indice_voz
        w = event.widget
        if w in campos_voz:
            indice_voz = min(campos_voz.index(w) + 1, len(campos_voz) - 1)
            focus_on_current()
        return "break"

    for w in campos_voz:
        if isinstance(w, tk.Entry):
            w.bind("<Return>", on_enter)

    # ─── Flechas arriba/abajo según foco ───
    def on_arrow(event):
        w = event.widget
        if w in campos_voz:
            if event.keysym == "Up":
                move_up()
            elif event.keysym == "Down":
                move_down()
            return "break"
        # scroll si no es campo de voz
        if event.keysym == "Up":
            canvas.yview_scroll(-1, "units")
        elif event.keysym == "Down":
            canvas.yview_scroll(1, "units")
        return "break"

    root.bind_all("<Up>", on_arrow)
    root.bind_all("<Down>", on_arrow)


    # Pon el foco en el primer campo al iniciar
    focus_on_current()
    configurar_navegacion_teclado()

    # Bindea el evento a cada campo de voz

    for w in campos_voz:
        # los Entry y DateEntry aceptan bind; si fuera StringVar, bindea al widget asociado
        w.bind("<FocusIn>", on_focus_in)
    indice_actual = 0  # apuntará al primer campo en 'campos'

    configurar_navegacion_teclado()

    # BARRA INFERIOR
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
        bar_w = max(7, int(w/(N*1.2)))
        spacing = (w - bar_w*N)//(N+1)
        for i, v in enumerate(niveles):
            bar_h = int(h*v)
            x0 = spacing + i*(bar_w+spacing)
            y0 = h - bar_h
            x1, y1 = x0+bar_w, h
            canvas_ondas.create_rectangle(x0, y0, x1, y1, fill="#2dd0ff", outline="")
        canvas_ondas.after(50, actualizar_onda)
    actualizar_onda()


    def salir_y_regresar_menu():
        from vista.MenuPrincipalV import mostrar_menu

        mostrar_menu(usuario_id_actual)

    def insertar_texto_en_campo_actual(texto):
        nonlocal campos_voz, indice_voz
        texto = texto.strip()
        if not texto or indice_voz >= len(campos_voz):
            return  # Nada que insertar o índice fuera de rango

        w = campos_voz[indice_voz]
        if isinstance(w, tk.Entry):
            existente = w.get().strip()
            if existente:
                # Añade al final del texto existente
                w.insert(tk.END, " " + texto)
            else:
                # Primer texto en el campo
                w.insert(0, texto)
        elif isinstance(w, DateEntry):
            try:
                w.set_date(texto)
            except Exception:
                pass
        elif isinstance(w, tk.StringVar):
            w.set(texto)

        def worker():
            nonlocal indice_voz, is_recording
            print("[DEBUG] worker arrancado")

            recog = voz_controlador.create_recognizer()  # método que devuelva un Recognizer Vosk
            stream = voz_controlador.open_stream()  # método que abra PyAudio stream

            while True:
                data = stream.read(4000, exception_on_overflow=False)
                if recog.AcceptWaveform(data):
                    texto_final = voz_controlador.parse_result(recog.Result())
                    insertar_texto_en_campo_actual(texto_final)
                    is_recording = False
                    break
                else:
                    texto_p = voz_controlador.parse_partial(recog.PartialResult())
                    insertar_texto_en_campo_actual(texto_p)

            # Cierra y reestablece botones
            stream.stop_stream()
            stream.close()
            btn_grab.config(state="normal")
            btn_stop.config(state="disabled")


        # Deshabilita el botón para evitar dobles pulsaciones
        btn_grab.config(state="disabled")
        btn_stop.config(state="normal")
        threading.Thread(target=worker, daemon=True).start()


    def funcion_guardar():
        # ==== 1. VALIDACIONES PREVIAS ====

        # 1.1 Campos obligatorios
        required = [
            (entry_unidad_medica, "Unidad médica"),
            (entry_num_folio, "Número de folio"),
            (entry_nombre_medico, "Nombre del médico"),
            (entry_nombre_paciente, "Nombre del paciente")
        ]
        for widget, label in required:
            if not widget.get().strip():
                messagebox.showerror("Error", f"{label} no puede estar vacío.")
                return

        # 1.2 Edad (entero positivo)
        edad_str = entry_edad.get().strip()
        try:
            edad = int(edad_str)
            if edad <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero positivo.")
            return

        # 1.3 Sexo
        sexo = sexo_var.get().strip()
        if sexo not in ("Femenino", "Masculino", "Otro"):
            messagebox.showerror("Error", "Debes seleccionar un sexo válido.")
            return

        # 1.4 Teléfonos (solo dígitos si no están vacíos)
        for widget, label in [(entry_telefono, "Teléfono"), (entry_telefono2, "Teléfono tutor")]:
            val = widget.get().strip()
            if val and not val.isdigit():
                messagebox.showerror("Error", f"{label} debe contener solo dígitos.")
                return

        # 1.5 Signos vitales / Antropometría
        checks = [
            ("Tensión arterial", entry_presion, False),  # formato “120/80”
            ("Temperatura (°C)", entry_temp, True),
            ("Frecuencia cardiaca", entry_fc, True),
            ("Frecuencia respiratoria", entry_fr, True),
            ("Peso (kg)", entry_peso, True),
            ("Talla (m)", entry_talla, True),
        ]
        for label, widget, numeric in checks:
            val = widget.get().strip()
            if val:
                if numeric:
                    if not val.replace(".", "", 1).isdigit():
                        messagebox.showerror("Error", f"{label} debe ser un número válido.")
                        return
                else:
                    if "/" not in val:
                        messagebox.showerror("Error", f"{label} debe tener formato “120/80”.")
                        return

        # ==== 2. ARMADO DEL TUPLE PLANO ====
        flat = (
            # -- expediente --
            entry_unidad_medica.get().strip(),
            entry_fecha_elaboracion.get(),
            entry_num_folio.get().strip(),
            entry_hora_elaboracion.get(),

            # -- paciente --
            entry_nombre_medico.get().strip(),
            entry_nombre_paciente.get().strip(),
            edad,
            sexo,
            entry_fecha_nacimiento.get(),
            entry_ocupacion.get().strip(),
            entry_grupo_etnico.get().strip(),
            entry_domicilio.get().strip(),
            entry_telefono.get().strip(),
            entry_padre_tutor.get().strip(),
            entry_parentesco.get().strip(),
            entry_telefono2.get().strip(),

            # -- antecedentes --
            entry_heredo_familiares.get().strip(),
            entry_no_patologicos.get().strip(),
            entry_patologicos.get().strip(),
            entry_gineco_obs.get().strip(),
            entry_padecimiento_actual.get().strip(),

            # -- interrogatorio --
            entry_cardiovascular.get().strip(),
            entry_endocrino.get().strip(),
            entry_respiratorio.get().strip(),
            entry_nervioso.get().strip(),
            entry_gastrointestinal.get().strip(),
            entry_musculoesqueletico.get().strip(),
            entry_gastrourinario.get().strip(),
            entry_piel_anexos.get().strip(),
            entry_hematico_linfatico.get().strip(),

            # -- signos vitales --
            entry_presion.get().strip(),
            entry_temp.get().strip(),
            entry_fc.get().strip(),
            entry_fr.get().strip(),
            entry_peso.get().strip(),
            entry_talla.get().strip(),

            # -- exploración física --
            entry_habitus.get().strip(),
            entry_abdomen.get().strip(),
            entry_cabeza.get().strip(),
            entry_genitales.get().strip(),
            entry_cuello.get().strip(),
            entry_extremidades.get().strip(),
            entry_torax.get().strip(),
            entry_piel.get().strip(),

            # -- evaluación clínica --
            entry_resultados_lab.get().strip(),
            entry_diagnostico.get().strip(),
            entry_farmacologico.get().strip(),
            entry_terapeutica_previa.get().strip(),
            entry_terapeutica_actual.get().strip(),
            entry_pronostico.get().strip(),

            # -- metadatos --
            usuario_id_actual,
            "abierto"
        )
        # ==== 3. LLAMADA AL CONTROLADOR ====
        try:
            if expediente_id:
                controlador.actualizar(expediente_id, flat)
                messagebox.showinfo("Éxito", "Expediente actualizado correctamente.")
            else:
                controlador.guardar(flat)
                messagebox.showinfo("Éxito", "Expediente creado correctamente.")
        except MySQLError as me:
            messagebox.showerror(
                "Error de base de datos",
                f"{me.msg}\nRevisa columnas vs placeholders"
            )
            return
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Error al guardar el expediente:\n{e}"
            )
            return

        # Navegación por tabs
        current_section = tk.StringVar(value="Datos generales")

        def go_to(section):
            frame = sec_frames[section]
            inner.update_idletasks()
            y = frame.winfo_y() / inner.winfo_height()
            canvas.yview_moveto(y)
            current_section.set(section)

        for name, btn in botones_tabs.items(): btn.config(command=lambda n=name: go_to(n))

    def iniciar_grabacion():
        nonlocal indice_voz, is_recording
        print(f"[DEBUG] iniciar_grabacion() → campo inicial {indice_voz}")
        is_recording = True
        btn_grab.config(state="disabled")
        btn_stop.config(state="normal")

        def worker():
            nonlocal indice_voz, is_recording
            print("[DEBUG] worker arrancado")

            # 1) Elegir gramática según tipo de campo
            w = campos_voz[indice_voz]
            if w in numeric_fields:
                # solo dígitos
                tokens = [str(i) for i in range(10)]
            else:
                # letras y dígitos
                tokens = [chr(c) for c in range(ord('A'), ord('Z') + 1)]
                tokens += [str(i) for i in range(10)]
            grammar = json.dumps(tokens)
            print(f"[DEBUG] grammar para campo {w}: {grammar}")

            recog = voz_controlador.create_recognizer(grammar=grammar)
            stream = voz_controlador.open_stream()
            print(f"[DEBUG] stream abierto {stream}")

            # 2) Lee audio hasta detectar texto final o que cancelen
            while is_recording:
                try:
                    data = stream.read(4000, exception_on_overflow=False)
                except OSError as oe:
                    print("[DEBUG] Stream cerrado, reabriendo", oe)
                    stream = voz_controlador.open_stream()
                    continue

                print(f"[DEBUG] Bytes leídos: {len(data)}")
                if recog.AcceptWaveform(data):
                    texto_final = voz_controlador.parse_result(recog.Result()).strip()
                    print(f"[DEBUG] texto_final: '{texto_final}'")
                    if texto_final:
                        # Inserta SOLO si hay texto
                        campos_voz[indice_voz].delete(0, tk.END)
                        campos_voz[indice_voz].insert(0, texto_final)
                    # Detén el worker para que no borre ni escriba más en este campo
                    is_recording = False
                    break
                else:
                    parcial = recog.PartialResult()
                    texto_p = voz_controlador.parse_partial(parcial).strip()
                    print(f"[DEBUG] texto_parcial: '{texto_p}'")
                    if texto_p:
                        campos_voz[indice_voz].delete(0, tk.END)
                        campos_voz[indice_voz].insert(0, texto_p)
            print("[DEBUG] worker finalizando, cerrando stream")

            voz_controlador.stop_stream()
            btn_grab.config(state="normal")
            btn_stop.config(state="disabled")
            print("[DEBUG] grabación detenida")

        threading.Thread(target=worker, daemon=True).start()

    def detener_grabacion():
            nonlocal is_recording
            is_recording = False
            btn_grab.config(state="normal")
            btn_stop.config(state="disabled")
            voz_controlador.stop_stream()

    # ----------- botones de voz (igual que antes) ------------
    btn_grab = btn_img(frame_bot, "grabar-voz.png", "Grabar", iniciar_grabacion)
    btn_stop = btn_img(frame_bot, "boton-detener.png", "Detener", detener_grabacion)
    btn_stop.config(state="disabled")

    # decide el texto del botón según modo edición o nuevo
    if expediente_id is not None:
        datos = controlador.obtener_por_id(expediente_id)
        boton_texto = "Actualizar"
    else:
        boton_texto = "Guardar"

    # crea los botones de Guardar/Actualizar y Salir
    btn_save = btn_img(frame_bot,
                       "guardar-el-archivo.png",
                       boton_texto,
                       funcion_guardar)
    btn_exit = btn_img(frame_bot,
                       "cerrar-sesion.png",
                       "Salir",
                       salir_y_regresar_menu)

    # empaqueta todos
    for w in (btn_grab, btn_stop, btn_save):
        w.pack(side="left", padx=5)
    btn_exit.pack(side="right", padx=5)



    print("Modelo cargado desde:", voz_controlador.model)

    if _run_mainloop:
        root.mainloop()

if __name__ == "__main__":
    from controlador.VoskC import VozControlador
    vc = VozControlador()
    crear_ventana(vc,
                  usuario_id_actual=self.usuario_id,
                  expediente_id=uid)