# modelo/expediente.py
from modelo.conexion import Conexion
import re

class Expediente:
    def __init__(self, datos):
          self.datos = datos

    def insertar(self):
        conn = Conexion().conectar()
        cursor = conn.cursor()
        sql = """
        INSERT INTO expediente (
            unidad_medica,
            fecha_elaboracion,
            num_folio,
            hora_elaboracion,
            nombre_medico,
            nombre_paciente,
            edad,
            sexo,
            fecha_nacimiento,
            ocupacion,
            grupo_etnico,
            domicilio,
            telefono,
            padre_tutor,
            parentesco,
            telefono_tutor,
            heredo_familiares,
            personales_no_patologicos,
            personales_patologicos,
            gineco_obstetricos,
            padecimiento_actual,
            cardiovascular,
            endocrino,
            respiratorio,
            nervioso,
            gastrointestinal,
            musculoesqueletico,
            gastrourinario,
            piel_mucosa_anexos,
            hematico_linfatico,
            presion,
            temperatura,
            frecuencia_cardiaca,
            frecuencia_respiratoria,
            peso,
            talla,
            habitus_exterior,
            abdomen,
            cabeza,
            genitales,
            cuello,
            extremidades,
            torax,
            piel,
            resultados_previos_gabinete,
            diagnosticos_clinicos,
            farmacologico,
            terapeutica_previos,
            terapeutica_actual,
            pronostico,
            usuario_id,
            estado
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, %s, %s,  %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
                  %s, %s, %s, %s, %s, %s, %s,%s,%s, %s,%s, %s)
        """

        num_placeholders = len(re.findall(r"%s", sql))
        num_params = len(self.datos)
        print(f"[DEBUG] placeholders={num_placeholders}, params={num_params}")
        cursor.execute(sql, self.datos)
        conn.commit()
        cursor.close()
        conn.close()
        return cursor.lastrowid
