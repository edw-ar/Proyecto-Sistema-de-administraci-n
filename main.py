import os
from pathlib import Path
from src.logic.databaseexcel import crear_archivo, agregar_productos, buscar_producto, mostrar_producto, modificar_producto
from src.logic.fuctions import ingresar_producto, menu_busqueda

ARCHIVO = os.path.join(os.path.expanduser("~"), 'OneDrive', "Desktop", "inventario_prueba.xlsx")

if not os.path.exists(ARCHIVO):
    crear_archivo(ARCHIVO)
else:
    print('Archivo existente cargado correctamente.\n')

while True:
    print("\n========= MENÚ PRINCIPAL =========")
    print("  1. Agregar producto")
    print("  2. Buscar producto")
    print("  3. Modificar producto")
    print("  4. Salir")
    opcion = input("Seleccione una opción: ").strip()

    if opcion == '1':
        datos = ingresar_producto()
        guardado = agregar_productos(ARCHIVO, datos)
        if guardado:
            print('✔ Producto guardado correctamente.')

    elif opcion == '2':
        criterio, valor = menu_busqueda()
        if criterio:
            wb, ws, fila, cabecera = buscar_producto(ARCHIVO, criterio, valor)
            if fila:
                mostrar_producto(cabecera, fila)

    elif opcion == '3':
        criterio, valor = menu_busqueda()
        if criterio:
            modificar_producto(ARCHIVO, criterio, valor)

    elif opcion == '4':
        print('Programa finalizado.')
        break

    else:
        print("⚠ Opción inválida. Intente de nuevo.")