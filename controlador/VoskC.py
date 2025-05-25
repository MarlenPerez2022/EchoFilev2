import os
os.environ["VOSK_LOG_LEVEL"] = "0"
import json
import pyaudio
from vosk import Model, KaldiRecognizer

class VozControlador:
    _shared_model = None
    """
    Controlador de voz basado en Vosk para captura y reconocimiento en tiempo real.
    """
    def __init__(self, modelo_path=None):
        # Calcula ruta base (un nivel arriba de este archivo)
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        if modelo_path is None:
            modelo_path = os.path.join(base_dir, "vosk-model-es-0.42")
        if not os.path.isdir(modelo_path):
            raise FileNotFoundError(f"Carpeta de modelo no encontrada: {modelo_path}")

        # ── Carga el modelo solo una vez ──
        if VozControlador._shared_model is None:
                VozControlador._shared_model = Model(modelo_path)
                print("Vosk model cargado desde:", modelo_path)
        self.model = VozControlador._shared_model

        # Inicializa PyAudio
        self.pyaudio_instance = pyaudio.PyAudio()
        self.stream = None
        # ---------------------------------------------------

    def open_stream(self):
        from pyaudio import paInt16

        # Si ya existe un stream...
        if self.stream is not None:
            try:
                # ...y sigue activo, lo reutilizamos
                if self.stream.is_active():
                    return self.stream
            except Exception:
                # Si comprobar _is_active_ falla, descartamos el stream viejo
                print("[VozControlador] stream previo inválido, reiniciando")
                try:
                    self.stream.stop_stream()
                    self.stream.close()
                except:
                    pass
                self.stream = None

        # Abrimos uno nuevo con buffer más pequeño
        try:
            self.stream = self.pyaudio_instance.open(
                format=paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=800
            )
            print("[VozControlador] stream abierto:", self.stream)
            return self.stream
        except Exception as e:
            raise RuntimeError(f"No se pudo abrir el stream de audio: {e}")
#---------------------------------------------------
    def create_recognizer(self, grammar=None,
                          max_alternatives: int = 0,
                          words: bool = True,
                          partial_words: bool = True):
        """
        Crea un KaldiRecognizer para 16 kHz.
        Si se pasa 'grammar' (JSON con lista de tokens), lo usa para filtrar el vocabulario.
        """
        if grammar:
            print(f"[DEBUG] create_recognizer: usando grammar={grammar}")
            rec = KaldiRecognizer(self.model, 16000, grammar)
        else:
            print("[DEBUG] create_recognizer: sin grammar")
            rec = KaldiRecognizer(self.model, 16000)

        # Opciones para afinar precisión
        rec.SetMaxAlternatives(max_alternatives)
        rec.SetWords(words)
        rec.SetPartialWords(partial_words)
        return rec

    def open_stream(self):
        """
        Abre (o reutiliza) el stream del micrófono con PyAudio.
        Si ya existe un stream activo, lo reutiliza; si no, crea uno nuevo.
        """
        from pyaudio import paInt16

        # Reutilizar si está activo
        if self.stream is not None and not self.stream.is_stopped():
            return self.stream

        # Cerrar previamente si existe
        if self.stream is not None:
            self.stop_stream()

        try:
            # Abre un nuevo stream con menor latencia
            self.stream = self.pyaudio_instance.open(
                format=paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=4096
            )
            return self.stream
        except Exception as e:
            raise RuntimeError(f"No se pudo abrir el stream de audio: {e}")

    def stop_stream(self):
        """
        Detiene y cierra el stream del micrófono si existe.
        """
        if self.stream is not None:
            try:
                self.stream.stop_stream()
                self.stream.close()
            finally:
                self.stream = None

    def parse_partial(self, partial_json):
        """
        Extrae el texto parcial de un JSON de PartialResult.
        """
        try:
            j = json.loads(partial_json)
            return j.get("partial", "")
        except json.JSONDecodeError:
            return ""

    def parse_result(self, result_json):
        """
        Extrae el texto final de un JSON de Result.
        """
        try:
            j = json.loads(result_json)
            return j.get("text", "")
        except json.JSONDecodeError:
            return ""

    def iniciar_grabacion_temporal(self, segundos=5):
        """
        Escucha durante `segundos` segundos y devuelve el texto reconocido.
        """
        recognizer = self.create_recognizer()
        stream = self.open_stream()
        import time
        texto = []
        end_time = time.time() + segundos
        while time.time() < end_time:
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                texto.append(self.parse_result(recognizer.Result()))
        self.stop_stream()
        return " ".join(texto).strip()

    def grabar_y_reconocer(self, segundos=5):
        """
        Graba durante `segundos` segundos y devuelve (texto_final, nivel_voz).
        El nivel de voz se aproxima con RMS de los frames capturados.
        """
        recognizer = self.create_recognizer()
        stream = self.open_stream()
        import time, math, struct

        frames = []
        end_time = time.time() + segundos
        while time.time() < end_time:
            data = stream.read(4000, exception_on_overflow=False)
            frames.append(data)
            recognizer.AcceptWaveform(data)

        # Obtener texto final y nivel RMS
        texto_final = self.parse_result(recognizer.FinalResult())
        sum_sq, count = 0.0, 0
        for chunk in frames:
            shorts = struct.unpack(f"{len(chunk)//2}h", chunk)
            for s in shorts:
                sum_sq += s*s
                count += 1
        nivel = math.sqrt(sum_sq/count) if count else 0.0
        self.stop_stream()
        return texto_final.strip(), nivel

    def escuchar_continuo(self, detener_flag):
        """
        Escucha continuamente hasta que `detener_flag()` sea True y devuelve el texto final.
        Útil para comandos en bucle.
        """
        recognizer = self.create_recognizer()
        stream = self.open_stream()
        texto = []
        while not detener_flag():
            data = stream.read(4000, exception_on_overflow=False)
            if recognizer.AcceptWaveform(data):
                texto.append(self.parse_result(recognizer.Result()))
        self.stop_stream()
        return " ".join(texto).strip()
