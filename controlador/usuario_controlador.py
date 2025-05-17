from modelo.usuario import Usuario

class UsuarioControlador:
    """Orquesta operaciones relacionadas con usuarios (médicos)."""
    def insertar_usuario(self, nombre, usuario, contrasena):
        u = Usuario(nombre, usuario, contrasena)
        u.insertar()
        return u

    def obtener_todos(self):
        return Usuario.obtener_todos()

    def buscar_por_usuario(self, usuario):
        return Usuario.buscar_por_usuario(usuario)