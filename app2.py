import tkinter as tk
from tkinter import ttk
import keyboard
import os
import psutil
import win32gui
import win32con
from win32process import GetWindowThreadProcessId
from time import sleep

# --- CONFIGURACIÓN DE DATOS PARA EL BACKEND ---
backend_data = {
    "button_1_state": False,
    "button_2_state": False,
    "button_3_state": False,
    "slider_1_val": 50.0,
    "slider_2_val": 50.0,
    "slider_3_val": 50.0,
    "is_interactive": False
}

GAME_HWND = None

def set_interactivity(interactive):
    """Cambia si la ventana recibe clics o no."""
    hwnd = root.winfo_id()
    # Obtener estilos actuales
    styles = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    
    if interactive:
        # Quitar transparencia de clics (WS_EX_TRANSPARENT)
        new_styles = styles & ~win32con.WS_EX_TRANSPARENT
        root.attributes("-alpha", 0.9) # Hacerse un poco opaco para saber que es clicable
        print("Modo Interactivo: ON")
    else:
        # Poner transparencia de clics
        new_styles = styles | win32con.WS_EX_TRANSPARENT
        root.attributes("-alpha", 1.0) # Totalmente invisible (solo se ve lo que no es negro)
        print("Modo Interactivo: OFF (Click-through)")

    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, new_styles)
    backend_data["is_interactive"] = interactive

def toggle_interactivity():
    # Check if the frame is currently visible
    if blocker_frame.winfo_viewable():
        print("Modo Interactivo: ON")
        blocker_frame.pack_forget()
    else:
        print("Modo Interactivo: ON")
        # You can specify where it reappears using pack options
        blocker_frame.pack(fill="x", pady=10)

# --- FUNCIONES DE LOS BOTONES ---
def on_button_click(id):
    backend_data[f"button_{id}_state"] = not backend_data[f"button_{id}_state"]
    print(f"Backend Update - Botón {id}: {backend_data[f'button_{id}_state']}")

def on_slider_change(id, val):
    backend_data[f"slider_{id}_val"] = float(val)
    # Aquí es donde el backend leería los datos

# --- LÓGICA DE VENTANA ---
def get_hwnd_from_exe(exe_name):
    target_pid = None
    for proc in psutil.process_iter(['name', 'pid']):
        if proc.info['name'] and proc.info['name'].lower() == exe_name.lower():
            target_pid = proc.info['pid']
            break
    if not target_pid: return None

    def callback(hwnd, hwnds):
        if win32gui.IsWindowVisible(hwnd):
            _, window_pid = GetWindowThreadProcessId(hwnd)
            if window_pid == target_pid:
                hwnds.append(hwnd)
        return True
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def track_game_window(target_exe):
    global GAME_HWND
    if GAME_HWND is None or not win32gui.IsWindow(GAME_HWND):
        GAME_HWND = get_hwnd_from_exe(target_exe)
    
    if GAME_HWND:
        try:
            left, top, right, bottom = win32gui.GetWindowRect(GAME_HWND)
            root.geometry(f'{right-left}x{bottom-top}+{left}+{top}')
        except:
            GAME_HWND = None 
    root.after(50, lambda: track_game_window(target_exe))

def exit_program():
    os._exit(0)

# --- UI SETUP ---
root = tk.Tk()
root.overrideredirect(True)
root.config(bg='#000000') # El negro será transparente
root.attributes("-transparentcolor", "#000000", "-topmost", 1)

# Contenedor para los controles (un panel lateral)
panel = tk.Frame(root, bg="#000000", padx=10, pady=10)
panel.pack(side="left")

tk.Label(panel, text="OVERLAY CONTROL", bg="#1a1a1a", fg="cyan", font=("Arial", 10, "bold")).pack(pady=5)
tk.Label(panel, text="CTRL+V: Toggle Clicks\nCTRL+X: Exit", bg="#1a1a1a", fg="white", font=("Arial", 8)).pack(pady=5)

# Crear 3 Botones
for i in range(1, 4):
    btn = tk.Button(panel, text=f"Acción {i}", command=lambda i=i: on_button_click(i), 
                    bg="#333", fg="white", activebackground="cyan")
    btn.pack(fill="x", pady=2)

# Crear 3 Sliders
for i in range(1, 4):
    tk.Label(panel, text=f"Ajuste {i}", bg="#1a1a1a", fg="white", font=("Arial", 8)).pack(pady=(10, 0))
    scl = tk.Scale(panel, from_=0, to=100, orient="horizontal", bg="#1a1a1a", fg="white", 
                   highlightthickness=0, command=lambda val, i=i: on_slider_change(i, val))
    scl.set(50)
    scl.pack(fill="x")

#blocker_frame = tk.Frame(panel, bg="#00F000")
#blocker_frame.place(x=0, y=0, relwidth=1, relheight=1)

# --- REGISTRO DE HOTKEYS ---
keyboard.add_hotkey('ctrl+v', toggle_interactivity)
keyboard.add_hotkey('ctrl+x', exit_program)

# Iniciar en modo click-through por defecto
root.after(100, lambda: set_interactivity(False))

TARGET_EXE_NAME = "xenia_canary.exe" 
track_game_window(TARGET_EXE_NAME)

root.mainloop()