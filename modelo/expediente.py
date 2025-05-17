from modelo.conexion import Conexion

class Expediente:
    """Clase que representa un expediente médico."""
    def __init__(self, folio, unidad_medica, fecha_elaboracion,
                 hora_elaboracion, paciente_id, usuario_id):
        self.folio = folio
        self.unidad_medica = unidad_medica
        self.fecha_elaboracion = fecha_elaboracion
        self.hora_elaboracion = hora_elaboracion
        self.paciente_id = paciente_id
        self.usuario_id = usuario_id

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO expediente (folio, unidad_medica, fecha_elaboracion, "
               "hora_elaboracion, paciente_id, usuario_id) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (self.folio, self.unidad_medica,
                             self.fecha_elaboracion, self.hora_elaboracion,
                             self.paciente_id, self.usuario_id))
        conn.commit()
        conn.close()

    @staticmethod
    def obtener_todos():
        conn = Conexion().conectar()
        if not conn:
            return []
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM expediente")
        rows = cursor.fetchall()
        conn.close()
        return rows