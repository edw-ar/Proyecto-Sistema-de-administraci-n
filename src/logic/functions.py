#Calcular el estado dependiendo de la cantidad del producto
def calcular_estado(cantidad):
    if cantidad == 0:
        return 'AGOTADO'
    elif cantidad <= 4:
        return 'STOCK BAJO'
    else:
        return 'DISPONIBLE'