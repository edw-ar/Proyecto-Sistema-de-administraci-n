import ssl
import certifi
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
import flet as ft
import os
from src.logic.databaseexcel import crear_archivo
from src.logic.navigation import configurar_app

#Crea una carpeta que contenga el inventario en los documentos del ususario.
CARPETA = os.path.join(os.path.expanduser("~"), "Documents", "Inventario")
ARCHIVO = os.path.join(CARPETA, "inventario.xlsx")

def main(page: ft.Page):
    page.theme_mode = ft.ThemeMode.LIGHT  # ← fuerza modo claro siempre
#Configuracion general de colores
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            error=ft.Colors.RED_600, 
            on_error=ft.Colors.WHITE, 
        )
    )
    os.makedirs(CARPETA, exist_ok=True)
    if not os.path.exists(ARCHIVO):
        crear_archivo(ARCHIVO)
    configurar_app(page, ARCHIVO)

ft.run(main)