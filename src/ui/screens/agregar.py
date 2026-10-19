import flet as ft
from src.ui.componentes.formulario import Formulario
from src.logic.databaseexcel import agregar_productos
from src.logic.functions import calcular_estado

def vista_agregar(archivo: str):
    def procesar(datos, form):
        cant = int(datos['cantidad'])
        estado = calcular_estado(cant)
        lista = [datos['lote'], datos['codigo'], float(datos['precio']), 
                 datos['unidad'].upper(), cant, datos['tipo'].upper(), 
                 datos['fech_entr'], datos['fech_venc'], estado]
        
        if agregar_productos(archivo, lista):
            form.mensaje.value = "✔ Producto guardado con éxito."
            form.mensaje.color = ft.Colors.GREEN_600
            form.limpiar()
        else:
            form.mensaje.value = "⚠ Error: ¿El archivo está abierto?"
            form.mensaje.color = ft.Colors.RED_600
        form.update()

    return Formulario(on_guardar_callback=procesar)