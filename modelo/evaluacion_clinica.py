from modelo.conexion import Conexion

class EvaluacionClinica:
    """Diagnósticos y plan terapéutico de la consulta."""
    def __init__(self, expediente_id, resultados_previos_gabinete,
                 diagnosticos_clinicos, farmacologico,
                 terapeutica_previos, terapeutica_actual, pronostico):
        self.expediente_id = expediente_id
        self.resultados_previos_gabinete = resultados_previos_gabinete
        self.diagnosticos_clinicos = diagnosticos_clinicos
        self.farmacologico = farmacologico
        self.terapeutica_previos = terapeutica_previos
        self.terapeutica_actual = terapeutica_actual
        self.pronostico = pronostico

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO evaluacion_clinica (expediente_id, resultados_previos_gabinete, diagnosticos_clinicos, "
               "farmacologico, terapeutica_previos, terapeutica_actual, pronostico) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (
            self.expediente_id,
            self.resultados_previos_gabinete,
            self.diagnosticos_clinicos,
            self.farmacologico,
            self.terapeutica_previos,
            self.terapeutica_actual,
            self.pronostico
        ))
        conn.commit()
        conn.close()