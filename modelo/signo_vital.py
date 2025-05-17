from modelo.conexion import Conexion

class SignoVital:
    """Signos vitales medidos en la consulta."""
    def __init__(self, expediente_id, tension_arterial, temperatura,
                 frecuencia_cardiaca, frecuencia_respiratoria,
                 peso, talla):
        self.expediente_id = expediente_id
        self.tension_arterial = tension_arterial
        self.temperatura = temperatura
        self.frecuencia_cardiaca = frecuencia_cardiaca
        self.frecuencia_respiratoria = frecuencia_respiratoria
        self.peso = peso
        self.talla = talla

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO signo_vital (expediente_id, tension_arterial, temperatura, "
               "frecuencia_cardiaca, frecuencia_respiratoria, peso, talla) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (self.expediente_id, self.tension_arterial,
                             self.temperatura, self.frecuencia_cardiaca,
                             self.frecuencia_respiratoria, self.peso,
                             self.talla))
        conn.commit()
        conn.close()