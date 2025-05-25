import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import os
import sys


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

if len(sys.argv) > 1:
    usuario = sys.argv[1]
else:
    usuario = "default_user"

# Ruta absoluta del directorio actual (Vista/)
carpeta_actual = os.path.dirname(os.path.abspath(__file__))

# Construye rutas completas a los archivos .py
ruta_expediente = os.path.join(carpeta_actual, "ExpedienteV.py")
ruta_mi_expediente = os.path.join(carpeta_actual, "MiExpedienteV.py")
ruta_perfil = os.path.join(carpeta_actual, "MiPerfilV.py")
ruta_inicio = os.path.join(carpeta_actual, "InicioV.py")
def mostrar_menu(usuario):
    # Función para abrir la interfaz de Nuevo Expediente
    def abrir_nuevo_expediente():

        expediente_path = os.path.join(os.path.dirname(__file__), "ExpedienteV.py")
        subprocess.Popen([sys.executable, expediente_path])
        ventana.destroy()

    # Función para abrir la interfaz de Mis Expedientes
    def abrir_mis_expedientes():

            subprocess.Popen(["python",ruta_mi_expediente])
            ventana.destroy()

    # Función para abrir la interfaz de Mi Perfil
    def abrir_mi_perfil():

            from vista.MiperfilV import crear_perfil
            crear_perfil(ventana, usuario)
            ventana.destroy()

# Función para cerrar sesión
    def cerrar_sesion():

        ruta_inicio = os.path.join(os.path.dirname(__file__), "InicioV.py")
        subprocess.Popen([sys.executable, ruta_inicio])
        ventana.destroy()


# Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Interfaz del Médico")
    ventana.geometry("800x600")
    ventana.config(bg="white")

# Crear el sidebar con el color #70E6FF
    sidebar = tk.Frame(ventana, bg="#70E6FF", width=200, height=600, padx=10, pady=20)
    sidebar.pack(side="left", fill="y")

# Cargar la imagen de usuario (conectado.png)
    _img = Image.open(r"C:\Users\Len\Documents\EchoFilev2\imagenes\conectado.png")
    img_usuario = ImageTk.PhotoImage(_img)

# Agrupar imagen y texto en un frame horizontal
    header_frame = tk.Frame(sidebar, bg="#70E6FF")
    header_frame.pack(pady=20)

    usuario_label = tk.Label(header_frame, image=img_usuario, bg="#70E6FF")
    usuario_label.pack(side="left")

    titulo_label = tk.Label(header_frame,
                                text="Médico",
                                font=("Arial", 18),
                                bg="#70E6FF",
                                fg="black")
    titulo_label.pack(side="left", padx=10)

    # Botón "Nuevo expediente"
    _img = Image.open(r"C:\Users\Len\Documents\EchoFilev2\imagenes\archivo-nuevo.png")
    img_nuevo_expediente = ImageTk.PhotoImage(_img)
    btn_nuevo = tk.Button(sidebar,
                              text="Nuevo expediente",
                              image=img_nuevo_expediente,
                              compound="left",
                              font=("Arial", 12),
                              bg="#70E6FF",
                              fg="black",
                              command=abrir_nuevo_expediente)
    btn_nuevo.pack(fill="x", pady=10)

    # Botón "Mis expedientes"
    _img = Image.open(r"C:\Users\Len\Documents\EchoFilev2\imagenes\expediente.png")
    img_mis_expedientes = ImageTk.PhotoImage(_img)
    btn_mis = tk.Button(sidebar,
                        text="Mis expedientes",
                        image=img_mis_expedientes,
                        compound="left",
                        font=("Arial", 12),
                        bg="#70E6FF",
                        fg="black",
                        command=abrir_mis_expedientes)
    btn_mis.pack(fill="x", pady=10)

    # Botón "Mi perfil"
    _img = Image.open(r"C:\Users\Len\Documents\EchoFilev2\imagenes\usuario.png")
    img_mi_perfil = ImageTk.PhotoImage(_img)
    btn_perfil = tk.Button(sidebar,
                           text="Mi perfil",
                           image=img_mi_perfil,
                           compound="left",
                           font=("Arial", 12),
                           bg="#70E6FF",
                           fg="black",
                           command=abrir_mi_perfil)
    btn_perfil.pack(fill="x", pady=10)

    # Botón "Cerrar sesión"
    _img = Image.open(r"C:\Users\Len\Documents\EchoFilev2\imagenes\cerrar-sesion.png")
    img_cerrar = ImageTk.PhotoImage(_img)
    btn_cerrar = tk.Button(sidebar,
                           text="Cerrar sesión",
                           image=img_cerrar,
                           compound="left",
                           font=("Arial", 12),
                           bg="#70E6FF",
                           fg="black",
                           command=cerrar_sesion)
    btn_cerrar.pack(fill="x", pady=10)




    ventana.mainloop()

if __name__ == "__main__":
   mostrar_menu("default_user")