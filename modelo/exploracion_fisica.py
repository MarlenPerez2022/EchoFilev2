from modelo.conexion import Conexion

class ExploracionFisica:
    """Resultados del examen físico."""
    def __init__(self, expediente_id, habitus_exterior, abdomen,
                 cabeza, genitales, cuello, extremidades, torax, piel):
        self.expediente_id = expediente_id
        self.habitus_exterior = habitus_exterior
        self.abdomen = abdomen
        self.cabeza = cabeza
        self.genitales = genitales
        self.cuello = cuello
        self.extremidades = extremidades
        self.torax = torax
        self.piel = piel

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO exploracion_fisica (expediente_id, habitus_exterior, abdomen, "
               "cabeza, genitales, cuello, extremidades, torax, piel) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (self.expediente_id, self.habitus_exterior,
                             self.abdomen, self.cabeza, self.genitales,
                             self.cuello, self.extremidades, self.torax,
                             self.piel))
        conn.commit()
        conn.close()