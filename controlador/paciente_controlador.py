from modelo.paciente import Paciente

class PacienteControlador:
    """Orquesta operaciones relacionadas con pacientes."""
    def insertar_paciente(self, nombre, edad, sexo, fecha_nacimiento,
                          ocupacion, grupo_etnico, domicilio,
                          telefono, tutor, parentesco, telefono_tutor):
        p = Paciente(nombre, edad, sexo, fecha_nacimiento,
                     ocupacion, grupo_etnico, domicilio,
                     telefono, tutor, parentesco, telefono_tutor)
        p.insertar()
        return p

    def obtener_todos(self):
        return Paciente.obtener_todos()