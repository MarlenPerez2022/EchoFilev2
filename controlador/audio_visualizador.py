import pyaudio
import numpy as np

class AudioVisualizer:
    def __init__(self, rate=16000, chunk=1024):
        self.rate    = rate
        self.chunk   = chunk
        self.p       = pyaudio.PyAudio()
        self.stream  = self.p.open(format=pyaudio.paInt16,
                                   channels=1,
                                   rate=rate,
                                   input=True,
                                   frames_per_buffer=chunk)

    def read_levels(self):
        """Lee un trozo de audio y devuelve un array con amplitudes normalizadas."""
        data = self.stream.read(self.chunk, exception_on_overflow=False)
        samples = np.frombuffer(data, dtype=np.int16)
        # normalizar a ±1
        return samples.astype(np.float32) / 32768.0

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def actualizar_visualizador(nivel_voz):
            # Limpia y dibuja barras de acuerdo al nivel_voz (puede ser una lista)
            # Este método debe ser llamado frecuentemente para actualizar el canvas
        pass