from modelo.signo_vital import SignoVital

class SignoVitalControlador:
    """Orquesta operaciones de signos vitales."""
    def insertar_signo_vital(self, expediente_id, tension_arterial,
                              temperatura, frecuencia_cardiaca,
                              frecuencia_respiratoria, peso, talla):
        sv = SignoVital(expediente_id,
                        tension_arterial, temperatura,
                        frecuencia_cardiaca, frecuencia_respiratoria,
                        peso, talla)
        sv.insertar()
        return sv

    def obtener_todos(self):
        return []