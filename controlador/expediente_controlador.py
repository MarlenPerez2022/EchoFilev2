from modelo.expediente import Expediente

class ExpedienteControlador:
    """Orquesta operaciones relacionadas con expedientes médicos."""
    def insertar_expediente(self, folio, unidad_medica,
                             fecha_elaboracion, hora_elaboracion,
                             paciente_id, usuario_id):
        e = Expediente(folio, unidad_medica,
                      fecha_elaboracion, hora_elaboracion,
                      paciente_id, usuario_id)
        e.insertar()
        return e

    def obtener_todos(self):
        return Expediente.obtener_todos()
