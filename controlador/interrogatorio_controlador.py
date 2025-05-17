from modelo.interrogatorio import Interrogatorio

class InterrogatorioControlador:
    """Orquesta operaciones de interrogatorio por sistemas."""
    def insertar_interrogatorio(self, expediente_id, cardiovascular,
                                 endocrino, respiratorio, nervioso,
                                 gastrointestinal, musculoesqueletico,
                                 gastrourinario, piel_mucosa_anexos,
                                 hematico_linfatico):
        i = Interrogatorio(expediente_id,
                           cardiovascular, endocrino, respiratorio,
                           nervioso, gastrointestinal,
                           musculoesqueletico, gastrourinario,
                           piel_mucosa_anexos, hematico_linfatico)
        i.insertar()
        return i

    def obtener_todos(self):
        return []