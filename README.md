# EchoFilev2

**Expediente Médico con reconocimiento de voz**  
Aplicación en Python/Tkinter que permite rellenar un formulario de expediente médico usando voz con Vosk.

---

## 📋 Contenido

1. [Descripción](#descripción)  
2. [Requisitos](#requisitos)  
3. [Instalación](#instalación)  
4. [Descarga del modelo de Vosk](#descarga-del-modelo-de-vosk)  
5. [Uso](#uso)  
6. [Estructura de archivos](#estructura-de-archivos)  
7. [Cómo contribuir](#cómo-contribuir)  
8. [Licencia](#licencia)

---

## Descripción

EchoFilev2 es una herramienta de escritorio que integra:

- **GUI** en Tkinter para capturar datos de un paciente.  
- **Reconocimiento de voz** con Vosk para dictar cada campo.  
- **Visualizador de audio** en tiempo real.  
- **Persistencia** en MySQL (opcional, según implementación).

---

## Requisitos

- Python 3.12  
- Git  
- Paquetes de Python:
  ```bash
  pip install vosk numpy pillow tkcalendar mysql-connector-python pyaudio
- **Instalar vosk-model-es-0.42 para usar la libreria de Vosk y integrarla dentro del proyecto
