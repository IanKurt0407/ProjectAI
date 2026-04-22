# src/network/api_client.py
import time

def consultar_ia(frame_queue, result_queue):
    """Comunica con el backend inteligente de tu compañero"""
    while True:
        if not frame_queue.empty():
            frame = frame_queue.get()
            
            # TODO: Aquí irá el request real a la API de la IA.
            # Simulamos el tiempo de respuesta:
            time.sleep(0.05) 
            
            # Simulamos lo que te respondería tu compañero
            detecciones = [
                {"label": "carro", "coords": (500, 300, 700, 450)},
                {"label": "obstaculo", "coords": (200, 500, 300, 600)}
            ]
            
            if not result_queue.full():
                result_queue.put((frame, detecciones))