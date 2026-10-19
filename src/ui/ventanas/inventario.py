import flet as ft
from src.logic.databaseexcel import obtener_todos
from src.ui.componentes.table import CABECERA, construir_tabla

def vista_inventario(archivo: str):
    productos = obtener_todos(archivo)
    filas = [[p.get(col, '') for col in CABECERA] for p in productos]

    return ft.Column(
        controls=[
            ft.Text("📦 Inventario", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(f"Total productos: {len(productos)}", italic=True),
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