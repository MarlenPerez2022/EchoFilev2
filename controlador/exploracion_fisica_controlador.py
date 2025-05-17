from modelo.exploracion_fisica import ExploracionFisica

class ExploracionFisicaControlador:
    """Orquesta operaciones de exploración física."""
    def insertar_exploracion(self, expediente_id, habitus_exterior,
                              abdomen, cabeza, genitales, cuello,
                              extremidades, torax, piel):
        ef = ExploracionFisica(expediente_id,
                               habitus_exterior, abdomen, cabeza,
                               genitales, cuello, extremidades,
                               torax, piel)
        ef.insertar()
        return ef

    def obtener_todos(self):
        return []