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

def buscar_primer_slot_vacio():
    '''
    Objetivo: Encontrar primer lugar vacio en la matriz
    Salida: numero entero (el indice). devuelve -1 si no hay slots vacios
    '''
    for i in range(SLOTS_INVENTARIO):
        if matriz_inventario[i][0] == 0:
            return i
    return -1

def agregar_item(item):
    '''
    Entrada: lista
    Objetivo: Agregar item al inventario
    Salida: none
    '''
    if len(item) != COLUMNAS:
        return
    copia = item.copy()
    indice = buscar_primer_slot_vacio()
    if indice == -1:
        return 'Inventario LLeno'
    matriz_inventario[indice] = copia

