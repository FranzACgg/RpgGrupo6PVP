INVENTARIO_MAXIMO = 30
ITEM_KEYS = {'id_item':0,'nombre':'','tipo':'','cantidad':0,'equipado':False}

# KEYS = 5 # [id_item , nombre, tipo, cantidad, equipado] 

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
    Entrada: entero (id del item a buscar), lista (inventario)
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

def usar_item(id_item, inventario):
    '''
    Entrada: entero (id del item a buscar), lista (inventario)
    Objetivo: Manejar el uso de items
    Salida: True o error
    '''
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return print('item no se encuentra en el inventario')
    if inventario[i]['tipo'] != 'consumible':
        return print('El item no es consumible')
    if inventario[i]['cantidad'] <= 0:
        return print('No hay stock del item')
    elif inventario[i]['cantidad'] == 1:
        inventario.pop(i)
    else:
        inventario[i]['cantidad'] -= 1
    return True
    
def manejar_equipado_item(id_item, inventario): # TODO agregar casos donde el subtipo de item ya esta equipado
    '''
    Entrada: entero (id del item a buscar), lista (inventario)
    Objetivo: equipar/desquipar items
    Salida: True o error
    '''
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return print('item no se encuentra en el inventario')
    if inventario[i]['tipo'] != 'equipable':
        return print('El item no es equipable')
    if inventario[i]['cantidad'] <= 0:
        return print('No hay stock del item')
    inventario[i]['equipado'] = not inventario[i]['equipado']
    return True

def exportar_items_equipados(inventario):
    '''
    Entrada: lista (inventario)
    Objetivo: exportar una lista con los items equipados
    Salida: lista de items
    '''
    return [item for item in inventario if item['equipado']]

def descartar_item(id_item, inventario):
    '''
    Entrada: entero (id), lista (inventario)
    Objetivo: descartar un item del inventario
    Salida: True/False s/exito de la operacion
    '''
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        print('item no se encuentra en el inventario')
        return False
    if inventario[i]['tipo'] == 'clave':
        print('Error, no se puede descartar items clave')
        return False
    if inventario[i]['equipado']:
        print('Error, no se puede descartar items equipados')
        return False
    if inventario[i]['cantidad'] <= 0:
        print('Error, no hay stock del item')
        return False
    if inventario[i]['cantidad'] > 1: #TODO agregar funcionalidad para que el usuario pueda elegir cuantos items descarta
        inventario[i]['cantidad'] -= 1
        return True
    else:
        inventario.pop(i)
        return True

