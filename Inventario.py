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
    
# UI del Inventario

def limpiar_consola():
    '''
    Objetivo: limpiar consola según el sistema operativo
    nt = Windows, cls es el comando para limpiar la consola en Windows
    clear es el comando para limpiar la consola en Unix/Linux/Mac
    '''
    os.system('cls' if os.name == 'nt' else 'clear')

# funcion para obtener una tecla sin necesidad de presionar enter, usando msvcrt (solo funciona en Windows)
def obtener_tecla():
    '''
    Objetivo: obtener una tecla sin necesidad de presionar enter (solo Windows)
    msvcrt.getch() pausa el programa haste que el usuario presione usa tecla, luego devuelve un byte, este se decodifica a string en formato utf-8 y se convierte a minuscula para facilitar la comparación
    Salida: string (la tecla que se presionó)
    '''
    return msvcrt.getch().decode('utf-8').lower()

def centrar_texto(cadena):
    '''
    Entrada: string 
    Objetivo: centrar texto en el ancho del UI
    Salida: string
    '''
    return cadena.center(ANCHO_UI)

def mostrar_inventario(inventario,cursor,desvio_cursor):
    '''
    Entrada: inventario: lista(inventario), cursor: entero (donde esta parado el cursor), desvio_cursor: entero (donde arranca a mostrarse el menu)
    Objetivo: mostrar el inventario
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
        cadena = ''
        if i == cursor:
            cadena += '> ' + inventario[i]['nombre'] + ' ' + str(inventario[i]['cantidad'])
        else:
            cadena += ' ' + inventario[i]['nombre'] + ' ' + str(inventario[i]['cantidad'])
        if inventario[i]['equipado']:
            cadena += ' [E]'
        print(cadena)
    
    print(BORDE_HORIZONTAL_SIMPLE)

def mostrar_panel_detalle(inventario, cursor):
    '''
    Entrada: inventario: lista(inventario), cursor: entero (donde esta parado el cursor)
    Objetivo: Mostrar panel detalle
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
    Entrada: inventario: lista(inventario), cursor: entero (donde esta parado el cursor)
    Objetivo: Mostrar controles
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
    print(cadena + '[T] tirar ')
    print('[W/S] Navegar | [Q] Cerrar')
    print(BORDE_HORIZONTAL_DOBLE)
    
def manejar_inventario(inventario):
    '''
    Entrada: lista
    Objetivo: Maneja y coordina todas las operaciones del inventario
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
                descartar_item(id_item,inventario)
                if len(inventario) < largo_original and cursor != 0:
                    cursor -= 1
        if cursor < desvio_cursor:
            desvio_cursor = cursor
        elif cursor >= desvio_cursor + ITEMS_POR_PAGINA:
            desvio_cursor += 1

    


