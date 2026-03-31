matriz_inventario = []
SLOTS_INVENTARIO = 30
COLUMNAS = 5 # [id_item , nombre, tipo, cantidad, equipado]

# tipos de items tentativos: consumible, equipable, intercambiable, clave, usable

def crear_inventario():
    '''
    Objetivo: llenar matriz inventario vacia con slots fijos.
    Salida: none
    '''
    matriz_inventario.clear()
    for i in range(SLOTS_INVENTARIO):
        item = [0,"","",0,False] # [entero, string, string, entero, booleano]
        matriz_inventario.append(item)
