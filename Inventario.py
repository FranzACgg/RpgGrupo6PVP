INVENTARIO_MAXIMO = 30
ITEM_KEYS = {'id_item':0,'nombre':'','tipo':'','cantidad':0,'equipado':False}

# COLUMNAS = 5 # [id_item , nombre, tipo, cantidad, equipado] 

# tipos de items tentativos: consumible, equipable, intercambiable, clave, usable

def crear_inventario():
    '''
    Objetivo: crear inventario.
    Salida: lista vacia
    '''
    return []

def agregar_item(item,inventario):
    '''
    Entrada: diccionario
    Objetivo: Agregar item al inventario
    Salida: none
    '''
    if item.keys() != ITEM_KEYS.keys():
        return print('Error, el objeto ingresado no tiene las keys de un item') # TODO: reemplazar por manejo de errores
    i = busqueda_item_por_id(item['id_item'], inventario)

    if i != -1:
        inventario[i]['cantidad'] += 1
    else:
        if len(inventario) >= INVENTARIO_MAXIMO:
            return print('Inventario lleno') # TODO: reemplazar por manejo de errores
        inventario.append(item.copy())

    
    

def busqueda_item_por_id(id_item, inventario):
    '''
    Entrada: entero (id del item a buscar)
    Objetivo: Buscar items secuencialmente segun ID
    Salida: Numero entero (indice del slot donde esta el item buscado o -1 si el item no esta presente)
    '''
    i = 0
    while i < len(inventario) and inventario[i]['id_item'] != id_item:
        i+=1
    if i < len(inventario):
        return i
    else:
        return -1

