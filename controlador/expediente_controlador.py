import mysql.connector

from modelo.expediente import Expediente

class ExpedienteControlador:
    def guardar(self, datos_tuple):
        exp = Expediente(datos_tuple)
        eid = exp.insertar()
        if not eid:
            raise Exception("Error al insertar expediente")
        return eid

    def guardar_todo(self, datos_dict):
        flat = ()
        flat += datos_dict["expediente"]
        flat += datos_dict["paciente"]
        flat += datos_dict["antecedente"]
        flat += datos_dict["interrogatorio"]
        flat += datos_dict["signo_vital"]
        flat += datos_dict["exploracion_fisica"]
        flat += datos_dict["evaluacion_clinica"]
        flat += (datos_dict["usuario_id"], "abierto")
        exp = Expediente(flat)
        eid = exp.insertar()
        if not eid:
            raise Exception("Error al insertar expediente completo")
        return eid

    def actualizar(self, expediente_id, datos_tuple):
        """
        Actualiza un expediente dado su ID y la tupla completa de datos.
        Lanza:
          - ValueError si no existe o no hubo cambios
          - mysql.connector.ProgrammingError si falla la consulta SQL
        """
        try:
            exp = Expediente(datos_tuple)
            filas_afectadas = exp.actualizar(expediente_id)
            if filas_afectadas == 0:
                raise ValueError(f"No existe expediente {expediente_id} o no hubo cambios.")
            return filas_afectadas

        except mysql.connector.ProgrammingError as pe:
            # Atrapa errores de número de placeholders o columnas mal alineadas
            raise RuntimeError(f"Error SQL al actualizar expediente: {pe}")

        except Exception:
            # Re-lanza cualquier otro error para ser mostrado
            raise

    def obtener_todos(self):
        return Expediente.obtener_todos()

    def buscar_por_usuario(self, usuario_id):
        """
        Llama al modelo para obtener sólo id, folio y paciente
        de los expedientes de este usuario.
        """
        return Expediente.buscar_por_usuario(usuario_id)

    def eliminar(self, expediente_id):
        """
        Borra de la tabla expediente la fila con id = expediente_id.
        """
        from modelo.expediente import Expediente
        # Este método delega en el método de clase del modelo
        Expediente.eliminar_por_id(expediente_id)

    def obtener_por_id(self, expediente_id):
        return Expediente.obtener_por_id(expediente_id)

    def buscar(self, num_folio=None, nombre_paciente=None):
        try:
            # delega en el modelo
            return self.modelo.buscar(num_folio=num_folio, nombre_paciente=nombre_paciente)
        except Exception as e:
            print(f"[ERROR controlador.buscar] {e}")
            raise

    def buscar(self, folio=None, nombre=None):
        # simplemente lo delegamos al modelo
        return self.modelo.buscar(folio, nombre)
