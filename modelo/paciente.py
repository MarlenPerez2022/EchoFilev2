from modelo.conexion import Conexion

class Paciente:
    """Clase que representa un paciente."""
    def __init__(self, nombre, edad, sexo, fecha_nacimiento,
                 ocupacion, grupo_etnico, domicilio,
                 telefono, tutor, parentesco, telefono_tutor):
        self.nombre = nombre
        self.edad = edad
        self.sexo = sexo
        self.fecha_nacimiento = fecha_nacimiento
        self.ocupacion = ocupacion
        self.grupo_etnico = grupo_etnico
        self.domicilio = domicilio
        self.telefono = telefono
        self.tutor = tutor
        self.parentesco = parentesco
        self.telefono_tutor = telefono_tutor

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO paciente (nombre, edad, sexo, fecha_nacimiento, ocupacion, "
               "grupo_etnico, domicilio, telefono, tutor, parentesco, telefono_tutor) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (self.nombre, self.edad, self.sexo, self.fecha_nacimiento,
                             self.ocupacion, self.grupo_etnico, self.domicilio,
                             self.telefono, self.tutor, self.parentesco,
                             self.telefono_tutor))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn = Conexion().conectar()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM paciente")
        rows = cursor.fetchall()
        conn.close()
        return rows