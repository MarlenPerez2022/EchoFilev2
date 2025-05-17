from modelo.evaluacion_clinica import EvaluacionClinica

class EvaluacionClinicaControlador:
    """Orquesta operaciones de evaluación clínica."""
    def insertar_evaluacion(self, expediente_id,
                             resultados_previos_gabinete,
                             diagnosticos_clinicos,
                             farmacologico, terapeutica_previos,
                             terapeutica_actual, pronostico):
        ec = EvaluacionClinica(expediente_id,
                               resultados_previos_gabinete,
                               diagnosticos_clinicos, farmacologico,
                               terapeutica_previos,
                               terapeutica_actual, pronostico)
        ec.insertar()
        return ec

    def obtener_todos(self):
        return []