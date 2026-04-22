# src/main.py
import threading
import queue

# Importamos las funciones de tus otros archivos
from capture.grabber import capturar_pantalla
from network.api_client import consultar_ia
from overlay.drawer import dibujar_interfaz

def iniciar_app():
    # 1. Creamos las colas que conectan los módulos
    frame_queue = queue.Queue(maxsize=2)
    result_queue = queue.Queue(maxsize=2)

    # 2. Iniciamos la captura y la IA como procesos de fondo (daemons)
    hilo_captura = threading.Thread(target=capturar_pantalla, args=(frame_queue,), daemon=True)
    hilo_ia = threading.Thread(target=consultar_ia, args=(frame_queue, result_queue), daemon=True)

    hilo_captura.start()
    hilo_ia.start()

    # 3. Arrancamos el dibujo en el hilo principal
    dibujar_interfaz(result_queue)

if __name__ == "__main__":
    iniciar_app()