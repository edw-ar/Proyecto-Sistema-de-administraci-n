import ssl
import certifi
ssl._create_default_https_context = ssl.create_default_context
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
import flet as ft
import os
from src.logic.databaseexcel import crear_archivo
from src.logic.navigation import configurar_app

#Crea el archivo en el escritorio de la pc, pero solo sirve si el escritorio esta en OneDrive
ARCHIVO = os.path.join(os.path.expanduser("~"), "OneDrive", "inventario_prueba.xlsx")

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT  # ← fuerza modo claro siempre
#Configuracion general de colores
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            error=ft.Colors.RED_600, 
            on_error=ft.Colors.WHITE, 
        )
    )
    if not os.path.exists(ARCHIVO):
        crear_archivo(ARCHIVO)
    configurar_app(page, ARCHIVO)

ft.run(main)