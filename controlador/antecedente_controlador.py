from modelo.antecedente import Antecedente

class AntecedenteControlador:
    """Orquesta operaciones de antecedentes generales."""
    def insertar_antecedente(self, expediente_id, heredo_familiares,
                              personales_no_patologicos, personales_patologicos,
                              gineco_obstetricos, padecimiento_actual):
        a = Antecedente(expediente_id,
                       heredo_familiares,
                       personales_no_patologicos,
                       personales_patologicos,
                       gineco_obstetricos,
                       padecimiento_actual)
        a.insertar()
        return a

    def obtener_todos(self):
        # En caso de necesitar listar antecedentes
        return []  # Implementar si es necesario