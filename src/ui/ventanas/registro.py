import flet as ft
from src.logic.databaseexcel import agregar_usuario
from src.ui.componentes.table import boton_accion

# Cambia este código por el que quieras. Solo deben conocerlo los empleados.
CODIGO_EMPRESA = 'MiCodigo2026'

def vista_registro(archivo, al_volver_al_login):
    campo_usuario = ft.TextField(label='Usuario', width=300, autofocus=True)
    campo_clave = ft.TextField(label='Contraseña', width=300, password=True, can_reveal_password=True)
    campo_repetir = ft.TextField(label='Repite la contraseña', width=300, password=True, can_reveal_password=True)
    campo_codigo = ft.TextField(label='Código de la empresa', width=300, password=True, can_reveal_password=True)
    mensaje = ft.Text('', size=13, color=ft.Colors.RED_600)

    def crear(e):
        usuario = campo_usuario.value.strip()
        clave = campo_clave.value

        if not usuario or not clave or not campo_codigo.value:
            mensaje.value = '⚠ Completa todos los campos.'
        elif len(clave) < 6:
            mensaje.value = '⚠ La contraseña debe tener al menos 6 caracteres.'
        elif clave != campo_repetir.value:
            mensaje.value = '⚠ Las contraseñas no coinciden.'
        elif campo_codigo.value != CODIGO_EMPRESA:
                mensaje.value = '⚠ Código de empresa incorrecto.'
                campo_codigo.value = ''
        else:
            try:
                creado = agregar_usuario(archivo, usuario, clave)
            except PermissionError:
                mensaje.value = '⚠ Cierra el Excel e intenta de nuevo.'
                e.page.update()
                return
            if creado:
                al_volver_al_login('✔ Usuario creado. Ahora inicia sesión.')
                return
            mensaje.value = '⚠ Ese usuario ya existe.'
        e.page.update()

    def volver(e):
        al_volver_al_login()

    campo_codigo.on_submit = crear

    return ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            controls=[
                ft.Icon(ft.Icons.PERSON_ADD, size=60, color='#2E4957'),
                ft.Text('Crear usuario', size=24, weight=ft.FontWeight.BOLD),
                ft.Text('Necesitas el código de la empresa para registrarte', size=13, color=ft.Colors.GREY_600),
                campo_usuario,
                campo_clave,
                campo_repetir,
                campo_codigo,
                ft.Row(
                    controls=[
                        boton_accion('Crear usuario', ft.Icons.CHECK, crear),
                        boton_accion('Volver', ft.Icons.ARROW_BACK, volver),
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