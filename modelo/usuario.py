from modelo.conexion import Conexion

class Usuario:
    """Clase que representa a un médico usuario del sistema."""
    def __init__(self, nombre, usuario, contrasena):
        self.nombre = nombre
        self.usuario = usuario
        self.contrasena = contrasena

    def insertar(self):
        """Inserta este usuario en la tabla `usuario`."""
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = "INSERT INTO usuario (nombre, usuario, contrasena) VALUES (%s, %s, %s)"
        cursor.execute(sql, (self.nombre, self.usuario, self.contrasena))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        """Devuelve todos los usuarios como lista de tuplas."""
        conn = Conexion().conectar()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        rows = cursor.fetchall()
        conn.close()
        return rows

    @staticmethod
    def buscar_por_usuario(usuario):
        """
        Busca un usuario por el campo 'usuario' y regresa sus datos.
        Devuelve un diccionario con los datos si lo encuentra, None si no existe.
        """
        conn = Conexion().conectar()
        cursor = conn.cursor()
        sql = "SELECT id, nombre, usuario, contrasena FROM usuario WHERE usuario = %s"
        cursor.execute(sql, (usuario,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            return {
                'id': row[0],
                'nombre': row[1],
                'usuario': row[2],
                'contrasena': row[3]
            }
        else:
            return None