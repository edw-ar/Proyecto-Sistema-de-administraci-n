import flet as ft
from datetime import datetime

CABECERA = ['Lote', 'Código', 'Precio', 'Unidad', 'Cantidad', 'Tipo',
            'Fecha entrada', 'Fecha vencimiento', 'Estado']

CAMPOS_NUMERICOS = {'Precio': float, 'Cantidad': int}
CAMPOS_FECHA     = ['Fecha entrada', 'Fecha vencimiento']
CAMPOS_READONLY  = ['Estado']

#Colores dependiendo del estado
def color_estado(estado):
    if estado == 'AGOTADO':
        return ft.Colors.RED_100
    elif estado == 'STOCK BAJO':
        return ft.Colors.ORANGE_100
    return ft.Colors.GREEN_100

#Construye una tabla visible con los datos dados
def construir_tabla(filas):
    return ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text(col, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE))
            for col in CABECERA
        ],
        rows=[
            ft.DataRow(
                cells=[ft.DataCell(ft.Text(str(v))) for v in fila],
                color=color_estado(fila[CABECERA.index('Estado')])
            )
            for fila in filas
        ],
        border=ft.Border.all(1, ft.Colors.GREY_300),
        border_radius=8,
        heading_row_color=ft.Colors.with_opacity(1, '#2E4957'),
        column_spacing=20,
    )

#Validaciones para la tabla
def validar_fecha(campo):
    try:
        datetime.strptime(campo.value.strip(), "%d/%m/%Y")
        campo.error_text = None
        return True
    except ValueError:
        campo.error_text = "Formato inválido (DD/MM/AAAA)"
        return False

def validar_valor(col, valor):
    if col in CAMPOS_NUMERICOS:
        try:
            return True, CAMPOS_NUMERICOS[col](valor)
        except ValueError:
            msg = "Número (Ej: 34.50)" if col == 'Precio' else "Entero (Ej: 36)"
            return False, f"Debe ser un {msg}"
    if col in CAMPOS_FECHA:
        try:
            datetime.strptime(valor.strip(), "%d/%m/%Y")
            return True, valor.strip()
        except ValueError:
            return False, "Formato inválido (DD/MM/AAAA)"
    return True, valor.strip()

#Widgets reutilizables
"""Funcion para botones"""
def boton_accion(texto, icono, on_click):
    return ft.Button(
        content=ft.Row(
            controls=[
                ft.Icon(icono, color=ft.Colors.WHITE),
                ft.Text(texto, color=ft.Colors.WHITE),
            ],
            tight=True,
            spacing=8,
        ),
        style=ft.ButtonStyle(bgcolor='#2E4957'),
        on_click=on_click,
    )

"""Función para buscar un producto por lote o código"""
def dropdown_criterio():
    return ft.Dropdown(
        label="Buscar por",
        width=180,
        value="lote",
        options=[
            ft.dropdown.Option(key="lote",   text="Lote"),
            ft.dropdown.Option(key="codigo", text="Código"),
        ],
    )


def fila_dos_columnas(izq, der):
    return ft.Row(
        controls=[
            ft.Container(content=izq, expand=True),
            ft.Container(content=der, expand=True),
        ],
        spacing=20,
    )