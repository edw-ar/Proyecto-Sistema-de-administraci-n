import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

def crear_archivo(archivo):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Inventario'
    cabecera = ['Lote', 'Código', 'Precio', 'Unidad', 'Cantidad', 'Tipo', 'Fecha entrada', 'Fecha vencimiento', 'Estado']
    ws.append(cabecera)
    for celda in ws[1]:
        celda.font = Font(bold=True, color='FFFFFF')
        celda.fill = PatternFill(fill_type='solid', fgColor='2E4957')
        celda.alignment = Alignment(horizontal='center')
    wb.save(archivo)
    print("Archivo creado correctamente.\n")

def agregar_productos(archivo, datos):
    try:
        wb = openpyxl.load_workbook(archivo)
        ws = wb.active
        ws.append(datos)
        wb.save(archivo)
        return True
    except PermissionError:
        print("\n⚠ Error: El archivo está abierto en Excel. Ciérralo e intente de nuevo.\n")
        return False

#Retorna (ws, wb, fila_encontrada, cabecera) o None si no existe.
def buscar_producto(archivo, criterio, valor):
    columnas = {'lote': 1, 'codigo': 2}

    if criterio not in columnas:
        print("Criterio inválido. Use 'lote' o 'codigo'.")
        return None, None, None, None

    col = columnas[criterio]
    wb = openpyxl.load_workbook(archivo)
    ws = wb.active
    cabecera = [celda.value for celda in ws[1]]

    for fila in ws.iter_rows(min_row=2):
        if str(fila[col - 1].value).upper() == str(valor).upper():
            return wb, ws, fila, cabecera

    print(f"\n⚠ No se encontró ningún producto con {criterio.upper()} = '{valor}'.\n")
    return None, None, None, None

#Imprime los datos de un producto numerados.
def mostrar_producto(cabecera, fila):
    print("\n--- Datos del producto ---")
    for i, (campo, celda) in enumerate(zip(cabecera, fila), start=1):
        print(f"  {i}. {campo}: {celda.value}")


def modificar_producto(archivo, criterio, valor):
    wb, ws, fila, cabecera = buscar_producto(archivo, criterio, valor)  # reutiliza
    if fila is None:
        return

    mostrar_producto(cabecera, fila)  # reutiliza

    print("\n¿Qué campo desea modificar? (número, o 0 para cancelar)")
    try:
        opcion = int(input("Seleccione: ").strip())
    except ValueError:
        print("⚠ Opción inválida.")
        return

    if opcion == 0:
        print("Modificación cancelada.")
        return

    if opcion < 1 or opcion > len(cabecera):
        print("⚠ Número fuera de rango.")
        return

    campo_elegido = cabecera[opcion - 1]
    nuevo_valor = input(f"Nuevo valor para '{campo_elegido}': ").strip()

    if campo_elegido == 'Precio':
        nuevo_valor = float(nuevo_valor)
    elif campo_elegido == 'Cantidad':
        nuevo_valor = int(nuevo_valor)
        from src.logic.fuctions import calcular_estado
        fila[cabecera.index('Estado')].value = calcular_estado(nuevo_valor)
        print(f"   Estado actualizado a: {fila[cabecera.index('Estado')].value}")

    fila[opcion - 1].value = nuevo_valor

    try:
        wb.save(archivo)
        print(f"\n✔ '{campo_elegido}' actualizado correctamente.\n")
    except PermissionError:
        print("\n⚠ El archivo está abierto en Excel. Ciérralo e intente de nuevo.\n")


#Retorna todos los productos como lista de dicts para mostrar en tabla.
def obtener_todos(archivo):
    wb = openpyxl.load_workbook(archivo)
    ws = wb.active
    cabecera = [celda.value for celda in ws[1]]
    productos = []
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if any(fila):  # ignora filas vacías
            productos.append(dict(zip(cabecera, fila)))
    return productos