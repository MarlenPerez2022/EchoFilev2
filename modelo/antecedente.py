from modelo.conexion import Conexion

class Antecedente:
    """Antecedentes generales asociados a un expediente."""
    def __init__(self, expediente_id, heredo_familiares,
                 personales_no_patologicos, personales_patologicos,
                 gineco_obstetricos, padecimiento_actual):
        self.expediente_id = expediente_id
        self.heredo_familiares = heredo_familiares
        self.personales_no_patologicos = personales_no_patologicos
        self.personales_patologicos = personales_patologicos
        self.gineco_obstetricos = gineco_obstetricos
        self.padecimiento_actual = padecimiento_actual

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO antecedente (expediente_id, heredo_familiares, "
               "personales_no_patologicos, personales_patologicos, "
               "gineco_obstetricos, padecimiento_actual) VALUES (%s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (self.expediente_id, self.heredo_familiares,
                             self.personales_no_patologicos, self.personales_patologicos,
                             self.gineco_obstetricos, self.padecimiento_actual))
        conn.commit()
        conn.close()