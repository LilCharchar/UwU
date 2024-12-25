import dearpygui.dearpygui as dpg
import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog



def actualizar_texto():
    # Simulando la llegada de nuevos datos
    new_data = "Nuevo dato recibido...\n"
    # Añadir los datos al campo de texto
    current_text = dpg.get_value("text_output")
    updated_text = current_text + new_data
    dpg.set_value("text_output", updated_text)

def examinar():
    root = tk.Tk()
    root.withdraw()  
    
    directory_path = filedialog.askdirectory(title="Selecciona una carpeta")
    if directory_path:
        dpg.set_value("path", directory_path)
    

dpg.create_context()

with dpg.font_registry():
    # Se pone el path de las fuentes
    default_font = dpg.add_font("assets/OpenSans-Regular.ttf", 20)


with dpg.window(tag="Primary Window", no_resize=True, width=600, height=600):

    dpg.bind_font(default_font)

    dpg.add_text(default_value="Ingrese las URLs de YouTube aquí:")
    with dpg.group(horizontal=True):
               
        url = dpg.add_input_text(tag="urls", hint = "URL...", multiline=True, width=400, height= 100)        
        dpg.add_button(label = "Limpiar Enlaces")
        

    dpg.add_spacer(height=10)  # Separador
    # Grupo de seleccion de directorio
    dpg.add_text(default_value="Seleccione la carpeta de descarga:")
    with dpg.group(horizontal=True) as path:
        path = dpg.add_input_text(hint= "Dirección del directorio", tag= "path", width=400)
        dpg.add_button(label="examinar", callback=examinar)
    
    dpg.add_spacer(height=10)
    with dpg.group(horizontal=True):
        dpg.add_text(default_value="Tipo de archivo:")
        dpg.add_combo(items=["Audio", "Video"], default_value="Audio", width= 100 )

    dpg.add_spacer(height=10)
    # Texto que se actualiza para ver el estado de las descargas
    dpg.add_input_text(tag="text_output", multiline=True, readonly=True, width=400, height=200, enabled=False)

    #Boton de descarga de prueba
    dpg.add_button(label="Descargar", callback=actualizar_texto)


# Parametros de iniciacion de la ventana
dpg.create_viewport(title='Descargador UwU', width=600, height=600, resizable=False)

dpg.setup_dearpygui()

dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()

# while dpg.is_dearpygui_running():
#     # insert here any code you would like to run in the render loop
#     # you can manually stop by using stop_dearpygui()
    
#     dpg.render_dearpygui_frame()

dpg.destroy_context()