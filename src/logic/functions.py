#Calcular el estado dependiendo de la cantidad del producto
def calcular_estado(cantidad):
    if cantidad == 0:
        return 'AGOTADO'
    elif cantidad <= 4:
        return 'STOCK BAJO'
    else:
        return 'DISPONIBLE'

#Entrada datos del producto
def ingresar_producto():
    from src.logic.functions import calcular_estado  # evita importar todo el módulo
    print('\n--- Ingrese los datos del producto --- \n')
    lote      = input('Escriba el Lote del producto: ')
    codigo    = input('Escriba el Código del producto: ')
    precio    = float(input('Escriba el Precio del producto: '))
    unidad    = input('Escriba la Unidad del producto: ')
    cantidad  = int(input('Escriba la Cantidad del producto: '))
    tipo      = input('Escriba el Tipo del producto: ')
    fech_entr = input('Escriba la fecha de entrada: ')
    fech_venc = input('Escriba la fecha de vencimiento: ')
    estado    = calcular_estado(cantidad)

    return [lote, codigo, precio, unidad, cantidad, tipo, fech_entr, fech_venc, estado]

#
def menu_busqueda():
    print("\n¿Cómo desea buscar el producto?")
    print("  1. Por Lote")
    print("  2. Por Código")
    opcion = input("Seleccione (1/2): ").strip()

    if opcion == '1':
        valor = input("Ingrese el Lote: ").strip()
        return 'lote', valor
    elif opcion == '2':
        valor = input("Ingrese el Código: ").strip()
        return 'codigo', valor
    else:
        print("Opción inválida.")
        return None, None