import mysql.connector
from mysql.connector import Error

class Conexion:
    """Maneja la conexión a la base de datos MySQL."""
    def __init__(self, host='localhost', user='root', password='1234', database='echofile_db'):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def conectar(self):
        """Abre la conexión y la retorna. Si falla, imprime el error y retorna None."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return self.connection
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")
        return None

    def cerrar_conexion(self):
        """Cierra la conexión si está abierta."""
        if self.connection and self.connection.is_connected():
            self.connection.close()