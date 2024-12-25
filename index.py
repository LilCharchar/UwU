import dearpygui.dearpygui as dpg
import os
import yt_dlp




dpg.create_context()

with dpg.font_registry():
    # Se pone el path de las fuentes
    default_font = dpg.add_font("assets/OpenSans-Regular.ttf", 20)


with dpg.window(tag="Primary Window", no_resize=True):

    dpg.bind_font(default_font)

    dpg.add_text("Descargador UwU")

    with dpg.group(horizontal=True) as Path:
        path = dpg.add_input_text(hint= "Dirección del directorio", tag= "path")
        dpg.add_button(label="examinar", before=0)

    dpg.add_input_text(tag="text_output", multiline=True, readonly=False, width=400, height=200)

dpg.create_viewport(title='Descargador UwU', width=600, height=600, resizable=False)

dpg.setup_dearpygui()

dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)

while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    
    dpg.render_dearpygui_frame()

dpg.destroy_context()