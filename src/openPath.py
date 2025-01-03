import tkinter as tk
from tkinter import filedialog



def examinar(dpg):
    root = tk.Tk()
    root.withdraw()  
    
    directory_path = filedialog.askdirectory(title="Selecciona una carpeta")
    if directory_path:
        dpg.set_value("path", directory_path)