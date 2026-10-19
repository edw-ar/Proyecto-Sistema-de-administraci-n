from datetime import datetime

def es_numero(valor):
    try:
        float(valor)
        return True
    except:
        return False

def es_entero(valor):
    try:
        int(valor)
        return True
    except:
        return False

def es_fecha(valor):
    try:
        datetime.strptime(valor, "%d/%m/%Y")
        return True
    except:
        return False