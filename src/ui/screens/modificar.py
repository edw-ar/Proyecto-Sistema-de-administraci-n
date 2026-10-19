import flet as ft
from src.logic.databaseexcel import buscar_producto
from src.logic.functions import calcular_estado
from src.ui.componentes.table import (CABECERA, CAMPOS_READONLY, boton_accion,
                           dropdown_criterio, validar_valor)

def vista_modificar(archivo: str):

    dropdown        = dropdown_criterio()
    campo_busqueda  = ft.TextField(label="Valor a buscar", hint_text="Ej: L0001", expand=True)
    mensaje         = ft.Text("", size=13)
    resultado       = ft.Column(controls=[], spacing=10)
    estado_busqueda = {"wb": None, "fila": None, "campos_edit": []}

    def buscar(e):
        valor = campo_busqueda.value.strip()
        if not valor:
            campo_busqueda.error_text = "Ingresa un valor"
            e.page.update()
            return

        campo_busqueda.error_text = None
        wb, ws, fila, _ = buscar_producto(archivo, dropdown.value, valor)

        if fila is None:
            mensaje.value = f"⚠ No encontrado."
            mensaje.color = ft.Colors.RED_600
            resultado.controls.clear()
            e.page.update()
            return

        estado_busqueda.update({"wb": wb, "fila": fila, "campos_edit": []})
        filas_tabla = []

        for i, col in enumerate(CABECERA):
            campo_edit = ft.TextField(
                value=str(fila[i].value or ""),
                dense=True,
                read_only=col in CAMPOS_READONLY,
                border_color=ft.Colors.TRANSPARENT,
                focused_border_color=ft.Colors.BLUE_400,
                color=ft.Colors.GREY_500 if col in CAMPOS_READONLY else None,
            )
            estado_busqueda["campos_edit"].append(campo_edit)
            filas_tabla.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(col, weight=ft.FontWeight.BOLD)),
                    ft.DataCell(campo_edit),
                ])
            )

        mensaje.value = "✔ Producto encontrado. Edita los campos y guarda."
        mensaje.color = ft.Colors.GREEN_600

        resultado.controls = [
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Campo", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                    ft.DataColumn(ft.Text("Valor", weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)),
                ],
                rows=filas_tabla,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                border_radius=8,
                heading_row_color=ft.Colors.with_opacity(1, '#2E4957'),
                column_spacing=40,
            ),
            boton_accion("Guardar cambios", ft.Icons.SAVE, guardar_cambios),
        ]
        e.page.update()

    def guardar_cambios(e):
        fila   = estado_busqueda["fila"]
        wb     = estado_busqueda["wb"]
        campos = estado_busqueda["campos_edit"]
        if fila is None:
            return

        hubo_error = False
        for i, col in enumerate(CABECERA):
            if col in CAMPOS_READONLY:
                continue
            ok, valor_convertido = validar_valor(col, campos[i].value or "")
            if not ok:
                campos[i].error_text = valor_convertido
                hubo_error = True
            else:
                campos[i].error_text = None
                fila[i].value = valor_convertido

        if hubo_error:
            mensaje.value = "⚠ Corrige los campos marcados en rojo."
            mensaje.color = ft.Colors.RED_600
            e.page.update()
            return

        idx_cant   = CABECERA.index('Cantidad')
        idx_estado = CABECERA.index('Estado')
        nuevo_estado           = calcular_estado(int(fila[idx_cant].value))
        fila[idx_estado].value = nuevo_estado
        campos[idx_estado].value = nuevo_estado

        try:
            wb.save(archivo)
            mensaje.value = "✔ Producto modificado correctamente."
            mensaje.color = ft.Colors.GREEN_600
        except PermissionError:
            mensaje.value = "⚠ Cierra el archivo en Excel e intenta de nuevo."
            mensaje.color = ft.Colors.RED_600

        e.page.update()

    return ft.Column(
        controls=[
            ft.Text("✏️ Modificar producto", size=24, weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Row(
                controls=[dropdown, campo_busqueda,
                           boton_accion("Buscar", ft.Icons.SEARCH, buscar)],
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