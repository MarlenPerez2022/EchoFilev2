# controlador/usuario_controlador.py
import sys, os

# Asegura que el path al paquete 'modelo' esté presente
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from modelo.usuario import Usuario

class UsuarioControlador:
    """Orquesta operaciones relacionadas con usuarios (médicos)."""
    def insertar_usuario(self, nombre, usuario, contrasena):
        u = Usuario(nombre, usuario, contrasena)
        u.insertar()
        return u

    def obtener_todos(self):
        return Usuario.obtener_todos()

    def obtener_por_id(self, username: str):
        """
        Retorna la tupla de datos del usuario cuyo ID coincida con usuario_id.
        Si no lo encuentra, lanza ValueError.
        """
        usuarios = self.obtener_todos()
        for u in usuarios:
            # asumo que u[0] es el campo ID en la tupla devuelta
            if u[2] == username :
                return u
        raise ValueError(f"Usuario '{username}' no encontrado")

    def buscar_por_usuario(self, usuario):
        return Usuario.buscar_por_usuario(usuario)

    def obtener_por_username(self, username: str):
        """
         Retorna la tupla del usuario cuyo campo username coincide con el string dado.
        """
        usuario = self.obtener_todos()

        for u in usuario:
            if u[2] == username:  # asume u[2] es el campo 'usuario'

                return u

        raise ValueError(f"Usuario '{username}' no encontrado")

    def actualizar(self, username: str, nuevo_nombre: str, nuevo_usuario: str, nueva_pwd: str):
        """
        Actualiza en la base de datos el registro del usuario cuyo username sea 'username',
        cambiando nombre, username y contraseña a los valores indicados.
        """
        # 1) Buscamos la tupla actual
        datos = self.obtener_por_username(username)
        id_usuario = datos[0]  # asumimos que la PK está en la posición 0

        # 2) Llamamos al modelo para hacer el UPDATE
        #    El método Usuario.actualizar debe encargarse de la consulta SQL
        Usuario.actualizar(id_usuario, nuevo_nombre, nuevo_usuario, nueva_pwd)