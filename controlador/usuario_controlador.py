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
        usuarios = self.obtener_todos()

        for u in usuarios:
            if u[2] == username:  # asume u[2] es el campo 'usuario'

                return u

        raise ValueError(f"Usuario '{username}' no encontrado")