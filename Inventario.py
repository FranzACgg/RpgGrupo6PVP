import os
import msvcrt

INVENTARIO_MAXIMO = 30
ITEM_KEYS = {'id_item':0,'nombre':'','tipo':'','cantidad':0,'equipado':False}

# Tamaño del UI del inventario
ANCHO_UI = 45

# Bordes del Inventario
BORDE_HORIZONTAL_SIMPLE = '─' * ANCHO_UI
BORDE_HORIZONTAL_DOBLE = '═' * ANCHO_UI

# cuantos items mostrar por pagina
ITEMS_POR_PAGINA = 8


# KEYS = 5 # [id_item , nombre, tipo, cantidad, equipado] 

# tipos de items tentativos: consumible, equipable, intercambiable, clave, usable


# Logica del Inventario

def crear_inventario():
    '''
    Objetivo: crear inventario.
    Salida: lista vacia
    '''
    return []

def agregar_item(item,inventario):
    '''
    Entrada: Diccionario , Lista
    Params: 
        item: Diccionario con el item a agregar al inventario
        inventario: Lista con todos los items en el inventario
    Objetivo: Agregar item al inventario
    Salida: none. Modifica el inventario original que toma la funcion
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
    Entrada: Entero, Lista
    Params:
        id_item: Id del item a buscar
        inventario: Lista con todos los items en el inventario
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
    Entrada: Entero, Lista
    Params:
        id_item: Id del item a usar
        inventario: Lista con todos los items en el inventario
    Objetivo: Manejar el uso de items
    Salida: Diccionario del item que se uso o none si hubo un error. Modifica el inventario original que toma la funcion
    '''
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return print('item no se encuentra en el inventario')
    item = inventario[i]
    if item['tipo'] != 'consumible':
        return print('El item no es consumible')
    if item['cantidad'] <= 0:
        return print('No hay stock del item')
    elif item['cantidad'] == 1:
        inventario.pop(i)
    else:
        item['cantidad'] -= 1
    return item
    
def manejar_equipado_item(id_item, inventario): # TODO agregar casos donde el subtipo de item ya esta equipado
    '''
    Entrada: Entero, Lista
    Params: 
        id_item: Id del item a equipar/desequipar
        inventario: Lista con todos los items en el inventario
    Objetivo: equipar/desquipar items
    Salida: Diccionario con el item que se equipo / desquipo o none si hubo un error. Modifica el inventario original que toma la funcion
    '''
    i = busqueda_item_por_id(id_item, inventario)
    if i == -1:
        return print('item no se encuentra en el inventario')
    item = inventario[i]
    if item['tipo'] != 'equipable':
        return print('El item no es equipable')
    if item['cantidad'] <= 0:
        return print('No hay stock del item')
    item['equipado'] = not item['equipado']
    return item

def exportar_items_equipados(inventario):
    '''
    Entrada: lista (inventario)
    Params:
        inventario: Lista con todos los items en el inventario
    Objetivo: exportar una lista con los items equipados
    Salida: lista de diccionarios con los items equipados
    '''
    return [item for item in inventario if item['equipado']]

def descartar_item(id_item, inventario):
    '''
    Entrada: entero, lista
    Params: 
        id_item: Id del item a descartar
        inventario: Lista con todos los items en el inventario
    Objetivo: descartar un item del inventario
    Salida: True/False s/exito de la operacion. Modifica el inventario original que toma la funcion
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
    
# UI del Inventario

def limpiar_consola():
    '''
    Objetivo: limpiar consola según el sistema operativo
    nt = Windows, cls es el comando para limpiar la consola en Windows
    clear es el comando para limpiar la consola en Unix/Linux/Mac
    Salida: none
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_tecla():
    '''
    Objetivo: obtener una tecla sin necesidad de presionar enter (solo Windows) usando msvcrt
    msvcrt.getch() pausa el programa haste que el usuario presione usa tecla, luego devuelve un byte, este se decodifica a string en formato utf-8 y se convierte a minuscula para facilitar la comparación
    Salida: string (la tecla que se presionó)
    '''
    return msvcrt.getch().decode('utf-8').lower()

def centrar_texto(cadena):
    '''
    Entrada: string
    Params:
        cadena: texto a centrar
    Objetivo: centrar texto en el ancho del UI
    Salida: string
    '''
    return cadena.center(ANCHO_UI)

def mostrar_inventario(inventario,cursor,desvio_cursor):
    '''
    Entrada: lista, entero, entero
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
        desvio_cursor: Desde que posicion de la lista empezar a dibujar la pantalla.
    Objetivo: mostrar a el usuario el panel del inventario con todos los items
    Salida: none
    '''
    print(BORDE_HORIZONTAL_DOBLE)
    print(centrar_texto(f'INVENTARIO ({len(inventario)}/{INVENTARIO_MAXIMO})'))
    print(BORDE_HORIZONTAL_DOBLE)

    if len(inventario) == 0:
        print(' ' * ANCHO_UI)
        print(BORDE_HORIZONTAL_SIMPLE)
        return

    if desvio_cursor + ITEMS_POR_PAGINA < len(inventario):
        rango = desvio_cursor + ITEMS_POR_PAGINA
    else:
        rango = len(inventario)
    for i in range(desvio_cursor, rango):
        puntero = ' ' 
        if i == cursor: 
            puntero = '> '
        cadena = puntero + inventario[i]['nombre'] + ' ' + str(inventario[i]['cantidad'])
        if inventario[i]['equipado']:
            cadena += ' [E]'
        print(cadena)
    
    print(BORDE_HORIZONTAL_SIMPLE)

def mostrar_panel_detalle(inventario, cursor):
    '''
    Entrada: lista, entero
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
    Objetivo: mostrar a el panel de detalle
    Salida: none
    '''
    if len(inventario) == 0:
        print(' ' * ANCHO_UI)
        print(BORDE_HORIZONTAL_SIMPLE)
        return
    print(f'{inventario[cursor]["nombre"]}')
    print(f'{inventario[cursor]["tipo"]} | X{inventario[cursor]["cantidad"]}')
    print(BORDE_HORIZONTAL_SIMPLE)

def mostrar_controles(inventario, cursor):
    '''
    Entrada: lista, entero
    Params:
        inventario: Lista con todos los items en el inventario
        cursor: Posición del item seleccionado actualmente en la lista
    Objetivo: Mostrar el panel de controles disponibles para el item seleccionado
    Salida: none
    '''
    if len(inventario) == 0:
        print(' ' * ANCHO_UI)
        print(BORDE_HORIZONTAL_DOBLE)
        return
    item = inventario[cursor]
    cadena = ''
    if item['tipo'] == 'consumible':
        cadena += '[U] Usar '
    if item['tipo'] == 'equipable':
        if item['equipado']:
            cadena += '[E] Desequipar '
        else:
            cadena += '[E] Equipar '
    if item['tipo'] != 'clave' and not item['equipado']:
        cadena += '[T] Tirar '
    print(cadena)
    print('[W/S] Navegar | [Q] Cerrar')
    print(BORDE_HORIZONTAL_DOBLE)
    
def manejar_inventario(inventario):
    '''
    Entrada: lista
    Params:
        inventario: Lista con todos los items en el inventario
    Objetivo: Maneja y coordina todas las operaciones del inventario
    Salida: none
    '''
    tecla = ''
    cursor = 0
    desvio_cursor = 0
    while tecla != 'q':
        largo_original = len(inventario)
        limpiar_consola()
        mostrar_inventario(inventario,cursor,desvio_cursor)
        mostrar_panel_detalle(inventario, cursor)
        mostrar_controles(inventario, cursor)
        tecla = obtener_tecla()
        if len(inventario) > 0:
            id_item = inventario[cursor]['id_item']
            if tecla == 'w':
                if cursor != 0:
                    cursor -= 1
            elif tecla == 's':
                if cursor != len(inventario) -1:
                    cursor += 1
            elif tecla == 'u':
                usar_item(id_item, inventario)
                if len(inventario) < largo_original and cursor != 0:
                    cursor -= 1
            elif tecla == 'e':
                manejar_equipado_item(id_item, inventario)
            elif tecla == 't':
                print(f'Descartar {inventario[cursor]["nombre"]}? [S/N]')
                confirmacion = ''
                while confirmacion not in ['s','n']:
                    confirmacion = obtener_tecla()
                if confirmacion == 's':
                    descartar_item(id_item,inventario)
                if len(inventario) < largo_original and cursor != 0:
                    cursor -= 1
        if cursor < desvio_cursor:
            desvio_cursor = cursor
        elif cursor >= desvio_cursor + ITEMS_POR_PAGINA:
            desvio_cursor += 1

