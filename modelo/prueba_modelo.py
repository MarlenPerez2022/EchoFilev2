from .usuario import Usuario
from .paciente import Paciente
from .expediente import Expediente

if __name__ == "__main__":
    # Crear y guardar un usuario de prueba
    usuario_prueba = Usuario("Dr. Prueba", "drprueba", "pass123")
    usuario_prueba.insertar()
    print("Usuarios:", Usuario.obtener_todos())

    # Crear y guardar un paciente de prueba
    paciente_prueba = Paciente(
        "Juan Pérez", 30, "M", "1995-01-01",
        "Ingeniero", "Hispano", "Calle Falsa 1",
        "555-0000", "Ana", "Madre", "555-1111"
    )
    paciente_prueba.insertar()
    print("Pacientes:", Paciente.obtener_todos())

    # Crear y guardar un expediente de prueba
    expediente_prueba = Expediente(
        "EXP0001", "Unidad A", "2025-05-12", "10:00:00",
        paciente_id=1, usuario_id=1
    )
    expediente_prueba.insertar()
    print("Expedientes:", Expediente.obtener_todos())
