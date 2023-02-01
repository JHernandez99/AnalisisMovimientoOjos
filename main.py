#INSTALACION Y LIBRERIAS EMPLEADAS
# CONDA CREATE ENVIRONMENT --name eyes pyhon=3.9
# conda activate eyes
# pip install dearpygui

from librarys.crearComponentesVentanaPrincipal import *
import dearpygui.dearpygui as dpg


dpg.create_context()
dpg.create_viewport(title='Analisis de movimiento de ojos', width=800, height=600)
start()


#dpg.show_documentation()
#dpg.show_debug()
#dpg.show_imgui_demo()
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()