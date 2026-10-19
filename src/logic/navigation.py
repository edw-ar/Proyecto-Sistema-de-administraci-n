import flet as ft
from src.ui.ventanas.inventario import vista_inventario
from src.ui.ventanas.agregar import vista_agregar
from src.ui.ventanas.buscar import vista_buscar
from src.ui.ventanas.modificar import vista_modificar
from src.ui.ventanas.dashboard import vista_dashboard

def configurar_app(page: ft.Page, archivo: str):
    page.title = "Sistema de Inventario"
    page.window.width = 1170
    page.window.height = 500
    page.padding = 0
    page.bgcolor = ft.Colors.WHITE

    contenido = ft.Container(
        content=vista_inventario(archivo),
        expand=True,
        padding=20,
    )

    def cambiar_vista(e):
        index = e.control.selected_index
        vistas = {
            0: lambda: vista_inventario(archivo),
            1: lambda: vista_agregar(archivo),
            2: lambda: vista_buscar(archivo),
            3: lambda: vista_modificar(archivo),
            4: lambda: vista_dashboard(archivo),
        }
        contenido.content = vistas[index]()
        page.update()

    nav = ft.NavigationRail(
        bgcolor=ft.Colors.GREY_100,
        group_alignment=0,
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=150,
        indicator_color=ft.Colors.BLUE_200,
        on_change=cambiar_vista,
        #Tamaño del texto seleccionado
        selected_label_text_style=ft.TextStyle(size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK),
        #Tamaño del texto no seleccionado
        unselected_label_text_style=ft.TextStyle(size=14, color=ft.Colors.BLACK),
        destinations=[
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.LIST, size=35),
            label="Inventario",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.ADD, size=35),
            label="Agregar",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.SEARCH, size=35),
            label="Buscar",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.EDIT, size=35),
            label="Modificar",
        ),
        ft.NavigationRailDestination(
            icon=ft.Icon(ft.Icons.BAR_CHART, size=35),
            label="Dashboard",
        ),
        ],
    )

    page.add(
        ft.Row(
            controls=[nav, contenido],
            expand=True,
        )
    )