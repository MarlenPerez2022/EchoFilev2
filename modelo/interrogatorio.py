from modelo.conexion import Conexion

class Interrogatorio:
    """Interrogatorio por sistemas asociado a un expediente."""
    def __init__(self, expediente_id, cardiovascular, endocrino,
                 respiratorio, nervioso, gastrointestinal,
                 musculoesqueletico, gastrourinario,
                 piel_mucosa_anexos, hematico_linfatico):
        self.expediente_id = expediente_id
        self.cardiovascular = cardiovascular
        self.endocrino = endocrino
        self.respiratorio = respiratorio
        self.nervioso = nervioso
        self.gastrointestinal = gastrointestinal
        self.musculoesqueletico = musculoesqueletico
        self.gastrourinario = gastrourinario
        self.piel_mucosa_anexos = piel_mucosa_anexos
        self.hematico_linfatico = hematico_linfatico

    def insertar(self):
        conn = Conexion().conectar()
        if not conn:
            return
        cursor = conn.cursor()
        sql = ("INSERT INTO interrogatorio (expediente_id, cardiovascular, endocrino, "
               "respiratorio, nervioso, gastrointestinal, musculoesqueletico, "
               "gastrourinario, piel_mucosa_anexos, hematico_linfatico) "
               "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)")
        cursor.execute(sql, (self.expediente_id, self.cardiovascular,
                             self.endocrino, self.respiratorio, self.nervioso,
                             self.gastrointestinal, self.musculoesqueletico,
                             self.gastrourinario, self.piel_mucosa_anexos,
                             self.hematico_linfatico))
        conn.commit()
        conn.close()