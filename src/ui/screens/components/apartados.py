import flet as ft
from src.logic.databaseexcel import obtener_todos
from src.ui.componentes.table import CABECERA

def calcular_estadisticas(productos: list) -> dict:
    return {
        'total'     : len(productos),
        'disponible': sum(1 for p in productos if p.get('Estado') == 'DISPONIBLE'),
        'stock_bajo': sum(1 for p in productos if p.get('Estado') == 'STOCK BAJO'),
        'agotados'  : sum(1 for p in productos if p.get('Estado') == 'AGOTADO'),
    }

def tarjeta(titulo, valor, color, icono, on_click=None):
    return ft.Container(
        on_click=on_click,
        ink=True,
        content=ft.Column(
            controls=[
                ft.Icon(icono, size=36, color=color),
                ft.Text(str(valor), size=40, weight=ft.FontWeight.BOLD, color=color),
                ft.Text(titulo, size=13, color=ft.Colors.GREY_600),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=6,
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=12,
        padding=24,
        width=180,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK),
            offset=ft.Offset(0, 2),
        ),
    )