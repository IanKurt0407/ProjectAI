# src/capture/grabber.py
import cv2
import numpy as np
from mss import mss
from config import MONITOR # Importamos las medidas

def capturar_pantalla(frame_queue):
    """Toma capturas y las envía a la cola"""
    sct = mss()
    while True:
        screenshot = np.array(sct.grab(MONITOR))
        frame = cv2.cvtColor(screenshot, cv2.COLOR_BGRA2BGR)
        
        # Si la cola no está llena, metemos la imagen nueva
        if not frame_queue.full():
            frame_queue.put(frame)