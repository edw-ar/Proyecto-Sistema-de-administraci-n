import os
import sys
import subprocess
import flet as ft
from src.logic.databaseexcel import obtener_todos
from src.ui.componentes.table import CABECERA, construir_tabla, boton_accion

def abrir_carpeta(ruta_archivo: str):
    carpeta = os.path.dirname(ruta_archivo)
    if sys.platform.startswith("win"):
        os.startfile(carpeta)
    elif sys.platform == "darwin":
        subprocess.Popen(["open", carpeta])
    else:
        subprocess.Popen(["xdg-open", carpeta])

def vista_inventario(archivo: str):
    productos = obtener_todos(archivo)
    filas = [[p.get(col, '') for col in CABECERA] for p in productos]

    def al_abrir_carpeta(e):
        abrir_carpeta(archivo)

    return ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Text("📦 Inventario", size=24, weight=ft.FontWeight.BOLD),
                    boton_accion("Abrir carpeta", ft.Icons.FOLDER_OPEN, al_abrir_carpeta),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Divider(),
            ft.Text(f"Total productos: {len(productos)}", italic=True),
            ft.Text(f"Archivo: {archivo}", size=12, color=ft.Colors.GREY_600),
            ft.Container(
                content=ft.Row(
                    controls=[construir_tabla(filas)],
                    scroll=ft.ScrollMode.AUTO,
                ),
                expand=True,
            )
        ],
        expand=True,
        scroll=ft.ScrollMode.AUTO,
    )