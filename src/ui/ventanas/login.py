import flet as ft
from src.logic.databaseexcel import verificar_usuario
from src.ui.componentes.table import boton_accion

def vista_login(archivo, al_entrar_correcto, al_registrarse, aviso=''):
    campo_usuario = ft.TextField(label='Usuario', width=300, autofocus=True)
    campo_clave = ft.TextField(
        label='Contraseña',
        width=300,
        password=True,
        can_reveal_password=True,
    )
    mensaje = ft.Text(
        aviso,
        size=13,
        color=ft.Colors.GREEN_600 if aviso else ft.Colors.RED_600,
    )

    def intentar_login(e):
        usuario = campo_usuario.value.strip()
        clave = campo_clave.value
        mensaje.color = ft.Colors.RED_600

        if not usuario or not clave:
            mensaje.value = '⚠ Ingresa usuario y contraseña.'
        else:
            try:
                valido = verificar_usuario(archivo, usuario, clave)
            except PermissionError:
                mensaje.value = '⚠ Cierra el Excel e intenta de nuevo.'
                e.page.update()
                return
            if valido:
                al_entrar_correcto()
                return
            mensaje.value = '⚠ Usuario o contraseña incorrectos.'
            campo_clave.value = ''
        e.page.update()

    def ir_a_registro(e):
        al_registrarse()

    campo_clave.on_submit = intentar_login

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.LOCK, size=60, color='#2E4957'),
                ft.Text('Sistema de Inventario', size=24, weight=ft.FontWeight.BOLD),
                ft.Text('Inicia sesión para continuar', size=13, color=ft.Colors.GREY_600),
                campo_usuario,
                campo_clave,
                ft.Row(
                    controls=[
                        boton_accion('Ingresar', ft.Icons.LOGIN, intentar_login),
                        boton_accion('Crear usuario', ft.Icons.PERSON_ADD, ir_a_registro),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=10,
                ),
                mensaje,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=16,
            tight=True,
        ),
    )