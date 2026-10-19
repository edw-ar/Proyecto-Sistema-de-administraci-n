import flet as ft
from src.logic.databaseexcel import buscar_producto
from src.ui.componentes.table import CABECERA, construir_tabla, boton_accion, dropdown_criterio

def vista_buscar(archivo: str):

    dropdown = dropdown_criterio()
    campo_busqueda = ft.TextField(label="Valor a buscar", hint_text="Ej: L0001", expand=True)
    mensaje = ft.Text("", size=13)
    resultado = ft.Column(controls=[], spacing=10)

    def buscar(e):
        valor = campo_busqueda.value.strip()
        if not valor:
            campo_busqueda.error_text = "Ingresa un valor para buscar"
            e.page.update()
            return

        campo_busqueda.error_text = None
        wb, ws, fila, _ = buscar_producto(archivo, dropdown.value, valor)

        if fila is None:
            mensaje.value = f"⚠ No se encontró ningún producto con {dropdown.value.upper()} = '{valor}'."
            mensaje.color = ft.Colors.RED_600
            resultado.controls.clear()
        else:
            valores = [celda.value for celda in fila]
            mensaje.value = "✔ Producto encontrado."
            mensaje.color = ft.Colors.GREEN_600
            resultado.controls = [
                ft.Container(
                    content=ft.Row(
                        controls=[construir_tabla([valores])],
                        scroll=ft.ScrollMode.AUTO,
                    )
                )
            ]

        e.page.update()

    return ft.Column(
        controls=[
            ft.Text("🔍 Buscar producto", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row(
                controls=[dropdown, campo_busqueda, boton_accion("Buscar", ft.Icons.SEARCH, buscar)],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.END,
            ),
            mensaje,
            ft.Divider(),
            resultado,
        ],
        spacing=16,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )