matriz_inventario = []
SLOTS_INVENTARIO = 30
COLUMNAS = 5 # [id_item , nombre, tipo, cantidad, equipado] 
ITEM_VACIO = [0,"","",0,False] # [entero, string, string, entero, booleano]


# tipos de items tentativos: consumible, equipable, intercambiable, clave, usable
# id_item == 0 equivale a decir que el slot esta vacio

def crear_inventario():
    '''
    Objetivo: llenar matriz inventario vacia con slots fijos.
    Salida: none
    '''
    matriz_inventario.clear()
    for i in range(SLOTS_INVENTARIO):
        item = ITEM_VACIO.copy()
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
        return f'ERROR, el largo del item a agregar ({len(item)}) no coincide con la cantidad de columnas esperadas {COLUMNAS} '
    copia = item.copy()
    indice = buscar_primer_slot_vacio()
    if indice == -1:
        return 'Inventario LLeno'
    matriz_inventario[indice] = copia

def vaciar_slot(indice):
    '''
    Entrada: Numero entero (indice a vaciar) 
    Objetivo: Vaciar slot en la mattriz
    '''
    matriz_inventario[indice] = ITEM_VACIO.copy()

def busqueda_item_por_id(item_id):
    '''
    Entrada: entero (id del item a buscar)
    Objetivo: Buscar items secuencialmente segun ID
    Salida: Numero entero (indice del slot donde esta el item buscado o -1 si el item no esta presente)
    '''
    i = 0
    while i < SLOTS_INVENTARIO and matriz_inventario[i][0] != item_id:
        i+=1
    if i < SLOTS_INVENTARIO:
        return i
    else:
        return -1

