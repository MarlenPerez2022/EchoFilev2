import os
os.environ["VOSK_LOG_LEVEL"] = "0"

import pyaudio
from vosk import Model, KaldiRecognizer

class VozControlador:
    def __init__(self, modelo_path=None):
        """
        Inicializa el controlador de voz con un modelo Vosk.
        Si no se pasa una ruta, se asume la carpeta 'vosk-model-es-0.42' en la raíz del proyecto.
        """
        # Calcula la ruta a la carpeta raíz del proyecto (un nivel arriba de 'controlador')
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

        # Si no se especifica ruta, usar la carpeta predeterminada
        if modelo_path is None:
            modelo_path = os.path.join(base_dir, "vosk-model-es-0.42")

        # Verifica que la carpeta exista
        if not os.path.isdir(modelo_path):
            raise FileNotFoundError(f"Carpeta de modelo no encontrada: {modelo_path}")

        # Carga el modelo Vosk (lazy load si deseas)
        self.model = Model(modelo_path)
        print("La librería de vosk ejecutada exitosamente en:", modelo_path)

        # Inicializa el reconocedor para 16kHz
        self.rec = KaldiRecognizer(self.model, 16000)
        # Prepara PyAudio para capturar audio
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None

    def iniciar_stream(self):
        """
        Abre el stream del micrófono con PyAudio.
        """
        self.stream = self.pyaudio_instance.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=8000
        )
        self.stream.start_stream()

    def detener_stream(self):
        """
        Detiene y cierra el stream del micrófono.
        """
        if self.stream is not None:
            self.stream.stop_stream()
            self.stream.close()
            self.stream = None
        self.pyaudio_instance.terminate()

    def escuchar(self, segundos=5):
        """
        Escucha durante un tiempo dado (en segundos) y devuelve el texto reconocido.
        """
        import time, json

        self.iniciar_stream()
        texto_final = ""
        start = time.time()
        while time.time() - start < segundos:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                resultado = self.rec.Result()
                texto = json.loads(resultado).get("text", "")
                texto_final += texto + " "
        self.detener_stream()
        return texto_final.strip()

    def escuchar_continuo(self, detener_flag):
        """
        Escucha de forma continua hasta que detener_flag() devuelva True.
        """
        import json

        self.iniciar_stream()
        texto_final = ""
        while not detener_flag():
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.rec.AcceptWaveform(data):
                resultado = self.rec.Result()
                texto = json.loads(resultado).get("text", "")
                texto_final += texto + " "
        self.detener_stream()
        return texto_final.strip()

    def grabar_y_reconocer(self, segundos=5):
        """
        Graba una porción de audio de "segundos" segundos, devuelve texto y nivel de voz (RMS).
        """
        import time, math

        self.iniciar_stream()
        frames = []
        start = time.time()
        # Leer datos y calcular RMS
        while time.time() - start < segundos:
            data = self.stream.read(4000, exception_on_overflow=False)
            frames.append(data)
        # Reconocer texto de todos los frames
        texto_final = ""
        for chunk in frames:
            if self.rec.AcceptWaveform(chunk):
                resultado = self.rec.Result()
                texto_final += json.loads(resultado).get("text", "") + " "
        # Calcular nivel de voz aproximado (RMS)
        # Convertir bytes a enteros
        import struct
        sum_squares = 0.0
        count = 0
        for chunk in frames:
            shorts = struct.unpack(f"{len(chunk)//2}h", chunk)
            for s in shorts:
                sum_squares += s*s
                count += 1
        nivel_voz = math.sqrt(sum_squares/count) if count else 0.0
        self.detener_stream()
        return texto_final.strip(), nivel_voz
