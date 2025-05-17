from vosk import Model, KaldiRecognizer
import pyaudio
import json

class VozModel:
    """Modelo de reconocimiento de voz usando Vosk."""
    def __init__(self, model_path="vosk-model-es-0.42"):
        self.model = Model(model_path)
        self.recognizer = KaldiRecognizer(self.model, 16000)
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(format=pyaudio.paInt16,
                                      channels=1,
                                      rate=16000,
                                      input=True,
                                      frames_per_buffer=4000)
        self.stream.start_stream()

    def escuchar(self):
        """Escucha hasta obtener una frase reconocida y devuelve el texto."""
        while True:
            data = self.stream.read(4000, exception_on_overflow=False)
            if self.recognizer.AcceptWaveform(data):
                result = self.recognizer.Result()
                texto = json.loads(result).get("text", "")
                return texto

    def cerrar(self):
        self.stream.stop_stream()
        self.stream.close()
        self.audio.terminate()