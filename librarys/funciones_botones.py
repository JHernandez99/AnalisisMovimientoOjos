from librarys.console_functionability import *
def fuente_seleccionada():
    consola("Fuente seleccionada: {}".format(dpg.get_value('rbFuente')),0)
    if(dpg.get_value('rbFuente') == 'Video'):
        dpg.configure_item(item='txtCamara',show=False)
        dpg.configure_item(item='btnActivarCamara', show=False)
        dpg.configure_item(item='txtSelVideo', show=True)
        dpg.configure_item(item='btnSel', show=True)
        dpg.configure_item(item='ruta_video', show=True)
    else:
        dpg.configure_item(item='txtCamara', show=True)
        dpg.configure_item(item='btnActivarCamara', show=True)
        dpg.configure_item(item='txtSelVideo', show=False)
        dpg.configure_item(item='btnSel', show=False)
        dpg.configure_item(item='ruta_video', show=False)

