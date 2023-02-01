import dearpygui.dearpygui as dpg
import datetime
i = 0
def consola(text,type=1):
    global tagAnterior
    global i
    hora = datetime.datetime.now()
    tagConsole = "txt{}{}".format(text,hora)
    if i<1:
        tagAnterior=tagConsole
        i=1
    #Tipo de color y significado
    # 0 info Azul
    # 1 Alerta Amarillo
    # 2 Error Rojo
    if type == 0:
        cColor = (0, 153, 255)
    elif type == 1:
        cColor = (255, 255, 0)
    elif type == 2:
        cColor = (204,0,0)
    else:
        cColor = (255, 255, 0)
    textConsola = '[{}:{}] - {}'.format(hora.hour,hora.minute,text)
    dpg.add_text(textConsola, parent='console_log', color=cColor, tag=tagConsole, before=tagAnterior)
    tagAnterior=tagConsole
    #AGREGAR COLOR DE BACKGROUND
