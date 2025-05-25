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
        exp = Expediente(datos_tuple)
        rows = exp.actualizar(expediente_id)
        if not rows:
            raise Exception(f"No existe expediente {expediente_id} o no hubo cambios.")
        return rows

    def obtener_todos(self):
        return Expediente.obtener_todos()
