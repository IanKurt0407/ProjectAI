# src/overlay/drawer.py
import cv2
from config import COLORS # Importamos tu paleta de colores

def dibujar_interfaz(result_queue):
    """Dibuja los cuadros y muestra la ventana"""
    print("Iniciando Asistencia Visual. Presiona 'Q' en la ventana para salir.")
    
    while True:
        if not result_queue.empty():
            frame, detecciones = result_queue.get()
            
            for obj in detecciones:
                x1, y1, x2, y2 = obj["coords"]
                color = COLORS.get(obj["label"], (255, 255, 255))
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), color, 6)
                cv2.putText(frame, obj["label"].upper(), (x1, y1 - 15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 4)

            cv2.imshow("Accesibilidad Forza", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cv2.destroyAllWindows()