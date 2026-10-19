import flet as ft
from src.logic.databaseexcel import obtener_todos
from src.ui.componentes.apartados import calcular_estadisticas, tarjeta
from src.ui.componentes.table import CABECERA, construir_tabla

def vista_dashboard(archivo: str):

    productos = obtener_todos(archivo)
    stats = calcular_estadisticas(productos)
    resultado = ft.Column(controls=[], spacing=10)

    def mostrar_filtro(estado: str):
        filtrados = productos if estado == 'TODOS' else [
            p for p in productos if p.get('Estado') == estado
        ]
        filas = [[p.get(col, '') for col in CABECERA] for p in filtrados]

        if not filtrados:
            resultado.controls = [
                ft.Text(f"No hay productos con estado '{estado}'.",
                        color=ft.Colors.GREY_600, italic=True)
            ]
        else:
            resultado.controls = [
                ft.Text(f"{len(filtrados)} producto(s)",
                        italic=True, color=ft.Colors.GREY_600, size=12),
                ft.Container(
                    content=ft.Row(
                        controls=[construir_tabla(filas)],
                        scroll=ft.ScrollMode.AUTO,
                    )
                )
            ]
        resultado.update()

    def al_click_todos(e):
        mostrar_filtro('TODOS')

    def al_click_disponible(e):
        mostrar_filtro('DISPONIBLE')

    def al_click_stock_bajo(e):
        mostrar_filtro('STOCK BAJO')

    def al_click_agotado(e):
        mostrar_filtro('AGOTADO')

    return ft.Column(
        controls=[
            ft.Text("📊 Dashboard", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text("Presiona una tarjeta para ver los productos.",
                    size=13, color=ft.Colors.GREY_600, italic=True),
            ft.Row(
                controls=[
                    tarjeta("Total productos", stats['total'],      '#2E4957',            ft.Icons.INVENTORY_2,  al_click_todos),
                    tarjeta("Disponibles",     stats['disponible'], ft.Colors.GREEN_600,  ft.Icons.CHECK_CIRCLE, al_click_disponible),
                    tarjeta("Stock bajo",      stats['stock_bajo'], ft.Colors.ORANGE_600, ft.Icons.WARNING,      al_click_stock_bajo),
                    tarjeta("Agotados",        stats['agotados'],   ft.Colors.RED_600,    ft.Icons.CANCEL,       al_click_agotado),
                ],
                spacing=20,
                wrap=True,
            ),
            ft.Divider(),
            resultado,
        ],
        spacing=20,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )