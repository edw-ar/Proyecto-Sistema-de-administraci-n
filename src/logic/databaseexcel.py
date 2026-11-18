import openpyxl
import hashlib
import secrets
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
        return False

#Retorna (ws, wb, fila_encontrada, cabecera) o None si no existe.
def buscar_producto(archivo, criterio, valor):
    columnas = {'lote': 1, 'codigo': 2}

    if criterio not in columnas:
        return None, None, None, None

    col = columnas[criterio]
    wb = openpyxl.load_workbook(archivo)
    ws = wb.active
    cabecera = [celda.value for celda in ws[1]]

    for fila in ws.iter_rows(min_row=2):
        if str(fila[col - 1].value).upper() == str(valor).upper():
            return wb, ws, fila, cabecera

    return None, None, None, None

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
# ---------- USUARIOS ----------

def hashear_clave(clave, sal):
    return hashlib.sha256((sal + clave).encode('utf-8')).hexdigest()

def asegurar_hoja_usuarios(archivo):
    # Crea la hoja Usuarios vacía si no existe.
    wb = openpyxl.load_workbook(archivo)
    if 'Usuarios' in wb.sheetnames:
        return
    ws = wb.create_sheet('Usuarios')
    ws.append(['Usuario', 'Sal', 'Contraseña (hash)'])
    for celda in ws[1]:
        celda.font = Font(bold=True, color='FFFFFF')
        celda.fill = PatternFill(fill_type='solid', fgColor='2E4957')
        celda.alignment = Alignment(horizontal='center')
    wb.save(archivo)

def agregar_usuario(archivo, usuario, clave):
    # Devuelve True si lo agregó y False si el usuario ya existe.
    # Si el Excel está abierto, deja pasar el PermissionError para que la pantalla avise.
    wb = openpyxl.load_workbook(archivo)
    ws = wb['Usuarios']
    for fila in ws.iter_rows(min_row=2, values_only=True):
        if fila[0] and str(fila[0]).lower() == usuario.lower():
            return False
    sal = secrets.token_hex(8)
    ws.append([usuario, sal, hashear_clave(clave, sal)])
    wb.save(archivo)
    return True

def verificar_usuario(archivo, usuario, clave):
    # Devuelve el nombre del ususario si los datos son correctos, o None si no lo son.
    wb = openpyxl.load_workbook(archivo, read_only=True)
    try:
        ws = wb['Usuarios']
        for fila in ws.iter_rows(min_row=2, values_only=True):
            if fila[0] and str(fila[0]).lower() == usuario.lower():
                if hashear_clave(clave, fila[1]) == fila[2]:
                    return str(fila[0])
                return None
        return None
    finally:
        wb.close()