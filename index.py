import io
import sys
import dearpygui.dearpygui as dpg
import os
import yt_dlp
import tkinter as tk
from tkinter import filedialog
import ffmpeg

def log(msg):
    current_text = dpg.get_value("log")
    next_text = current_text + msg  + '\n'
    dpg.set_value("log", next_text) 

class LogRedirect(io.StringIO):
    def write(self, msg):
        current_text = dpg.get_value("log")
        next_text = current_text + msg
        dpg.set_value("log", next_text)

def descargar():

    URL = dpg.get_value("urls").strip().split('\n')

    PATH = dpg.get_value("path").strip()

    data_type = dpg.get_value("datatype")

    if not PATH:
        log("Por favor, seleccione una carpeta de descarga.\n")
        return
    
    ydl_opts = {
    'logtostderr' : True,
    'outtmpl': os.path.join(PATH, '%(title)s.%(ext)s'),
    'embedthumbnail': True,
    'writethumbnail': True
    
    }

    if data_type == "Audio":
        ydl_opts['format'] = 'm4a/bestaudio/best'
        ydl_opts['postprocessors'] = [{  # Extract audio using ffmpeg
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'm4a'
        },
        {
            'key': 'EmbedThumbnail'
        }
        ]
           
    for i in range(len(URL)):
        ydl = yt_dlp.YoutubeDL(ydl_opts)
        ydl.download(URL[i])
           

def examinar():
    root = tk.Tk()
    root.withdraw()  
    
    directory_path = filedialog.askdirectory(title="Selecciona una carpeta")
    if directory_path:
        dpg.set_value("path", directory_path)
    
def limpiar_urls():
    dpg.set_value("urls", "")



sys.stdout = LogRedirect()
sys.stderr = LogRedirect()

dpg.create_context()

with dpg.font_registry():
    # Se pone el path de las fuentes
    default_font = dpg.add_font("assets/OpenSans-Regular.ttf", 20)


with dpg.window(tag="Primary Window", no_resize=True, width=600, height=600):

    dpg.bind_font(default_font)

    dpg.add_text(default_value="Ingrese las URLs de YouTube aquí:")
    with dpg.group(horizontal=True):

        url = dpg.add_input_text(tag="urls", hint = "URL...", multiline=True, width=400, height= 100)   
        with dpg.group():   
            dpg.add_text("")  
            dpg.add_spacer(height=1)
            dpg.add_button(label = "Limpiar enlaces", callback=lambda: dpg.set_value("urls", ""))
        

    dpg.add_spacer(height=10)  # Separador
    # Grupo de seleccion de directorio
    dpg.add_text(default_value="Seleccione la carpeta de descarga:")
    with dpg.group(horizontal=True) as path:
        path = dpg.add_input_text(hint= "Dirección del directorio", tag= "path", width=400)
        dpg.add_button(label="Examinar", callback=examinar)
    
    dpg.add_spacer(height=10)
    with dpg.group(horizontal=True):
        dpg.add_text(default_value="Tipo de archivo:")
        dpg.add_combo(items=["Audio", "Video"], default_value="Audio", width= 100 , tag= "datatype" )

    dpg.add_spacer(height=10)
    # Texto que se actualiza para ver el estado de las descargas
    with dpg.group(horizontal=True):
        dpg.add_input_text(tag="log", multiline=True, readonly=True, width=400, height=200, enabled=False, no_horizontal_scroll=False)
        with dpg.group():
            dpg.add_text("")  
            dpg.add_text("") 
            dpg.add_spacer(height=2) 
            dpg.add_button(label = "Limpiar logs", callback=lambda: dpg.set_value("log", ""))
    #Boton de descarga de prueba
    dpg.add_button(label="Descargar", callback=descargar)


# Parametros de iniciacion de la ventana
dpg.create_viewport(title='Descargador UwU', width=600, height=600, resizable=False)
dpg.add_input_text

dpg.setup_dearpygui()

dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()

# while dpg.is_dearpygui_running():
#     # insert here any code you would like to run in the render loop
#     # you can manually stop by using stop_dearpygui()
    
#     dpg.render_dearpygui_frame()

dpg.destroy_context()

