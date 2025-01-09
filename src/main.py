import os
import dearpygui.dearpygui as dpg
import tkinter as tk
from tkinter import filedialog
import yt_dlp


WIDTH = 600
HEIGHT = 600

dpg.create_context()


def examinar(dpg):
    root = tk.Tk()
    root.withdraw()  
    
    directory_path = filedialog.askdirectory(title="Selecciona una carpeta")
    if directory_path:
        dpg.set_value("path", directory_path)


def setquality(dpg):

    video_qualities = ["1080p", "720p", "480p", "360p", "240p"]
    # Bitrates de audio 
    # audio_bitrates = ["320 kbps", "256 kbps", "192 kbps", "128 kbps"]
    audio_bitrates = ["128 kbps"]

    try: 
        dpg.delete_item("quality")
    except: 
        pass
    dpg.add_combo(tag="quality", width=100, items= audio_bitrates if dpg.get_value("datatype") == "Audio" else video_qualities, 
    before="extra", default_value=audio_bitrates[0] if dpg.get_value("datatype") == "Audio" else video_qualities[0])
   
def descargar():

    url = dpg.get_value("URLinput").strip().split('\n')

    path = dpg.get_value("path").strip()

    data_type = dpg.get_value("datatype")
    quality = dpg.get_value("quality").strip(" kbps") if dpg.get_value("datatype") == "Audio" else dpg.get_value("quality").strip('p')

    ydl_opts = {}

    if data_type == "Audio":
        ydl_opts = {
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'ffmpeg_location': "bin/",
        'ignoreerrors': True,
        'writethumbnail': True
        }
        ydl_opts['embedthumbnail'] = True
        ydl_opts['format'] = 'm4a/bestaudio/best'
        ydl_opts['postprocessors'] = [
            {'key': 'FFmpegExtractAudio', 'preferredcodec': 'm4a'},
            {'key': 'EmbedThumbnail'}
        ]
        ydl_opts['postprocessor_args'] = ['-b:a', quality] 
    elif data_type == "Video":
        ydl_opts = {
        'outtmpl': os.path.join(path, '%(title)s.%(ext)s'),
        'ffmpeg_location': "bin/",
        'ignoreerrors': True
        }
        max_height = quality 
        ydl_opts['format'] = f'bestvideo[ext=mp4][height<={max_height}]+bestaudio[ext=m4a]/best'
        ydl_opts['merge_output_format'] = 'mp4' 
        # ydl_opts['postprocessors'] = [{
        # 'key': 'FFmpegVideoConvertor', 
        # 'preferedformat': 'mp4',  
        # }]
        ydl_opts['ffmpeg_location'] = "bin/"  

    for i in range(len(url)):
        try: 
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            ydl.download(url[i])
            print(f"Descarga completada: {url[i]}\n")
        except Exception as e:
            print(f"Error descargando {url[i]}: {str(e)}\n")




with dpg.font_registry():
    # Se pone el path de las fuentes
    default_font = dpg.add_font("assets/OpenSans-Regular.ttf", 20)

with dpg.window(tag="Main Window", no_resize=True, width=WIDTH, height=HEIGHT, max_size=[600, 600], modal=True):

    dpg.bind_font(default_font)

    dpg.add_text(default_value="Ingrese las URLs de YouTube aquí:")
    
    with dpg.group(horizontal=True):
        
        dpg.add_input_text(tag="URLinput", hint="URLs...", multiline=True, height=100, width=400)
        dpg.add_button(label="Limpiar enlaces", callback= lambda: dpg.set_value("URLinput", ""))
    
    
    dpg.add_spacer(height=10)  # Separador
    # Grupo de seleccion de directorio
    dpg.add_text(default_value="Seleccione la carpeta de descarga:")
    with dpg.group(horizontal=True):
        dpg.add_input_text(hint= "Dirección del directorio", tag= "path", width=400)
        dpg.add_button(label="Examinar", callback= lambda: examinar(dpg))
    
    dpg.add_spacer(height=10)
    
    with dpg.group(horizontal=True):
        dpg.add_text(default_value="Tipo de archivo:")
        dpg.add_combo(items=["Audio", "Video"], callback= lambda: setquality(dpg) ,default_value="Audio", width= 100 , 
        tag= "datatype" )
        # Calidades de video
        
        dpg.add_text(default_value="Calidad:")
        setquality(dpg)
        dpg.add_spacer(tag="extra")

    
    dpg.add_button(label="Descargar", callback= lambda: descargar())
                

dpg.create_viewport(title='Descargador UwU', width=WIDTH, height=HEIGHT, resizable=False, max_height=HEIGHT, max_width=WIDTH)

dpg.set_viewport_large_icon('UwU.ico')
dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("Main Window", True)

dpg.start_dearpygui()

dpg.destroy_context()

