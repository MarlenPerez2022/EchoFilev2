# modelo/expediente.py

import re
import os
import sys

from modelo.conexion import Conexion

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

    @classmethod
    def buscar_por_usuario(cls, usuario_id):
        """
        SELECT id, num_folio, nombre_paciente
        FROM expediente
        WHERE usuario_id = %s
        """
        conn = Conexion().conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, num_folio, nombre_paciente "
            "FROM expediente "
            "WHERE usuario_id = %s",
            (usuario_id,)
        )
        rows = cursor.fetchall()
        cursor.close()
        conn.close()
        return rows

    @classmethod
    def eliminar_por_id(cls, expediente_id):
        conn = Conexion().conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM expediente WHERE id = %s", (expediente_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @classmethod
    def obtener_por_id(cls, expediente_id):
        """
        Devuelve una tupla con todos los campos de expediente
        para el id dado, o None si no existe.
        """
        conn = Conexion().conectar()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM expediente WHERE id = %s",
            (expediente_id,)
        )
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        return row

    def actualizar(self, expediente_id):
        conn = Conexion().conectar()
        cursor = conn.cursor()

        sql = """
              UPDATE expediente
              SET unidad_medica               = %s,
                  fecha_elaboracion           = %s,
                  num_folio                   = %s,
                  hora_elaboracion            = %s,
                  nombre_medico               = %s,
                  nombre_paciente             = %s,
                  edad                        = %s,
                  sexo                        = %s,
                  fecha_nacimiento            = %s,
                  ocupacion                   = %s,
                  grupo_etnico                = %s,
                  domicilio                   = %s,
                  telefono                    = %s,
                  padre_tutor                 = %s,
                  parentesco                  = %s,
                  telefono_tutor              = %s,
                  heredo_familiares           = %s,
                  personales_no_patologicos   = %s,
                  personales_patologicos      = %s,
                  gineco_obstetricos          = %s,
                  padecimiento_actual         = %s,
                  cardiovascular              = %s,
                  endocrino                   = %s,
                  respiratorio                = %s,
                  nervioso                    = %s,
                  gastrointestinal            = %s,
                  musculoesqueletico          = %s,
                  gastrourinario              = %s,
                  piel_mucosa_anexos          = %s,
                  hematico_linfatico          = %s,
                  presion                     = %s,
                  temperatura                 = %s,
                  frecuencia_cardiaca         = %s,
                  frecuencia_respiratoria     = %s,
                  peso                        = %s,
                  talla                       = %s,
                  habitus_exterior            = %s,
                  abdomen                     = %s,
                  cabeza                      = %s,
                  genitales                   = %s,
                  extremidades                = %s,
                  cuello                      = %s,
                  torax                       = %s,
                  piel                        = %s,
                  resultados_previos_gabinete = %s,
                  diagnosticos_clinicos       = %s,
                  farmacologico               = %s,
                  terapeutica_previos         = %s,
                  terapeutica_actual          = %s,
                  pronostico                  = %s
              WHERE id = %s \
              """

        # self.datos fue construido con TODOS los campos + usuario_id + status
        # aquí quitamos esos dos últimos antes de añadir el id
        params = self.datos[:-2] + (expediente_id,)

        cursor.execute(sql, params)
        conn.commit()
        filas = cursor.rowcount
        cursor.close()
        conn.close()
        return filas

    def buscar(self, folio=None, nombre=None):
        conn = Conexion().conectar()
        cursor = conn.cursor()
        try:
            sql = "SELECT id, num_folio, nombre_paciente, fecha_elaboracion, estado FROM expediente WHERE 1=1"
            params = []
            if folio is not None:
                sql += " AND num_folio = %s"
                params.append(folio)
            if nombre is not None:
                sql += " AND nombre_paciente LIKE %s"
                params.append(f"%{nombre}%")
            cursor.execute(sql, tuple(params))
            return cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
