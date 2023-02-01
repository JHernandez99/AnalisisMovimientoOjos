from librarys.funciones_botones import *
from librarys.console_functionability import *
import dearpygui.dearpygui as dpg
def start():
    with dpg.window(label="Seleccion de video", width=300, height=200, pos=(0,0)):
        with dpg.group() as group0:
            dpg.add_text("Fuente:")
            dpg.add_radio_button(('Video','Camara'), callback=fuente_seleccionada, tag='rbFuente')

        with dpg.group() as group1:
            dpg.add_text("Seleccionar Video",tag='txtSelVideo')
            dpg.add_button(label="Seleccionar", tag='btnSel')
            #dpg.bind_item_theme(dpg.last_item(),dpg.mvThemeCol_Button)
            dpg.add_input_text(tag='ruta_video',label="RUTA", default_value="Ruta de video")
        with dpg.group() as group2:
            dpg.add_text('Camara',tag='txtCamara')
            dpg.add_button(label='Activar camara',tag='btnActivarCamara')

        #dpg.add_slider_float(label="float", default_value=0.273, max_value=1)

    with dpg.window(label="Parametros",width=200,height=200, pos=(300,0)):
        dpg.add_text("Hola mundo 2")
        dpg.add_text("Hola mundo 3")

    with dpg.window(label="VIDEO ANALISIS", width=500, height=360, pos=(0,200)):
        dpg.add_text(dpg.get_value('ruta_video'), pos=(200,20))



    with dpg.window(label='Console log',width=288,height=100, pos=(500,460),tag='console_log'):
        pass


    started = False
    if started == False:
        dpg.set_value('rbFuente','Video')
        fuente_seleccionada()
        started = True
        consola("Todos los componentes inicializados",0)
        consola("Seleccionar fuente",1)
